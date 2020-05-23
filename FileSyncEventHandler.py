import hashlib
import math
import sys
import time
import logging

from filechunkio import FileChunkIO
from watchdog.observers import Observer
from watchdog.events import *
import boto3
import botocore.exceptions
import os
from concurrent.futures import ThreadPoolExecutor

from common.Dir import Dir
from common.FilePart import FilePart
from common.utils import *


class FileSyncEventHandler(FileSystemEventHandler):
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, local_root, remote_root, threshold=15,
                 chunk_size=5):
        self.client = boto3.client('s3',
                                   endpoint_url=endpoint_url,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.local_root = local_root
        self.remote_root = remote_root
        self.bucket_name = 'hezhiwei'
        self.threshold = threshold * MB
        self.chunk_size = chunk_size * MB

    file_modified_event = set()

    def on_moved(self, event):
        """Called when a file or a directory is moved or renamed.

        :param event:
            Event representing file/directory movement.
        :type event:
            :class:`DirMovedEvent` or :class:`FileMovedEvent`
        """

        print(event)

    def on_created(self, event):
        """Called when a file or directory is created.

        :param event:
            Event representing file/directory creation.
        :type event:
            :class:`DirCreatedEvent` or :class:`FileCreatedEvent`
        """
        if isinstance(event, FileCreatedEvent):
            return
        print(event)
        # generate key in S3
        key = event.src_path.replace(self.local_root, self.remote_root, 1)
        key = key.replace('\\', '/') + '/'

        # upload
        try:
            self.client.upload_fileobj(Dir(), self.bucket_name, key)

        except botocore.exceptions.ClientError as error:
            raise error

    def on_deleted(self, event):
        """Called when a file or directory is deleted.

        :param event:
            Event representing file/directory deletion.
        :type event:
            :class:`DirDeletedEvent` or :class:`FileDeletedEvent`
        """
        print(event)

        # generate prefix in S3
        prefix = event.src_path.replace(self.local_root, self.remote_root, 1)
        prefix = prefix.replace('\\', '/')

        try:
            response = self.client.list_objects(
                Bucket=self.bucket_name,
                Prefix=prefix,
            )
            if 'Contents' in response.keys():
                delete_objects = [{'Key': s3_object['Key']} for s3_object in response['Contents']]
                response = self.client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={
                        'Objects': delete_objects
                    }
                )
                if 'Deleted' in response.keys():
                    for deleted_object in response['Deleted']:
                        print('S3 Delete Successfully:' + deleted_object['Key'])

                if 'Errors' in response.keys():
                    for error_object in response['Errors']:
                        print('S3 Delete Error:' + error_object['Key'] + '[{}]'.format(error_object['Code']))
            else:
                print('S3 ListObject : No such objects that with ' + prefix + "as prefix.")

        except botocore.exceptions.ClientError as error:
            raise error

        # delete
        # try:
        #     response = self.client.delete_object(
        #         Bucket=self.bucket_name,
        #         Key=key,
        #     )
        #     print(response)
        #
        # except botocore.exceptions.ClientError as error:
        #     raise error

    def on_modified(self, event):
        """Called when a file or directory is modified.

        :param event:
            Event representing file/directory modification.
        :type event:
            :class:`DirModifiedEvent` or :class:`FileModifiedEvent`
        """

        # get the time when event occur
        seconds = int(time.time())

        # ignore if event is DirModifiedEvent
        if isinstance(event, DirModifiedEvent):
            return

        # ignore if the same event occur within 1 second
        if (seconds, event.src_path) in self.file_modified_event:
            return

        self.file_modified_event.add((seconds, event.src_path))
        print(event)

        # generate key in S3
        key = event.src_path.replace(self.local_root, self.remote_root, 1)
        key = key.replace('\\', '/')

        # get MD5 and file size(Byte)
        while True:
            try:
                fetag = calc_etag(event.src_path, self.threshold, self.chunk_size)
                fsize = os.path.getsize(event.src_path)
                break
            except IOError as e:
                time.sleep(0.05)

        # try to get the object header in S3
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=key,
            )

        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == '404':  # Object doesn't exist in S3
                response = {}
            else:
                raise error

        # ignore if the same object has already exist in S3
        if 'ETag' in response.keys() and response['ETag'].strip("\'\"") == fetag:
            print("S3 Head Object: {} already exists".format(key))
            return

        # upload
        try:
            time.sleep(1)
            if fsize < self.threshold:
                with open(event.src_path, 'rb') as data:
                    self.client.upload_fileobj(data, self.bucket_name, key)
            else:
                response = self.client.create_multipart_upload(Bucket=self.bucket_name,
                                                               Key=key)
                if 'UploadId' in response.keys():
                    upload_id = response['UploadId']
                else:
                    raise Exception("Fail to init multipart upload for {}".format(event.src_path))

                chunk_cnt = int(math.ceil(fsize * 1.0 / self.chunk_size))

                args = [{'client': self.client,
                         'bucket_name': self.bucket_name,
                         'key': key,
                         'file_part': FilePart(file_path=event.src_path,
                                               part_num=i + 1,
                                               offset=(self.chunk_size * i),
                                               length=min(self.chunk_size, fsize - (self.chunk_size * i)),
                                               transfer_id=upload_id)}
                        for i in range(0, chunk_cnt)]

                with ThreadPoolExecutor(max_workers=4) as pool:
                    res = pool.map(upload_part, args)

                self.client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=key,
                    MultipartUpload={
                        'Parts': list(res)
                    },
                    UploadId=upload_id,
                )
                print("S3 Multipart Upload Successfully: {}".format(key))

        except botocore.exceptions.ClientError as error:
            raise error
