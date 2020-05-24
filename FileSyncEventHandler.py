import math
import time

from s3fs import S3FileSystem
from watchdog.events import *
import boto3
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
from common.Dir import Dir
from common.utils import *


class FileSyncEventHandler(FileSystemEventHandler):
    def __init__(self, client, local_root, remote_root, threshold=15,
                 chunk_size=5):
        self.client = client
        self.local_root = local_root
        self.remote_root = remote_root
        self.bucket_name = 'hezhiwei'
        self.threshold = threshold * MB
        self.chunk_size = chunk_size * MB

    file_updated_event = set()

    def on_moved(self, event):
        """Called when a file or a directory is moved or renamed.

        :param event:
            Event representing file/directory movement.
        :type event:
            :class:`DirMovedEvent` or :class:`FileMovedEvent`
        """
        print(event)
        src_prefix = event.src_path.replace(self.local_root, self.remote_root, 1).replace('\\', '/')
        dest_prefix = event.dest_path.replace(self.local_root, self.remote_root, 1).replace('\\', '/')
        response = self.client.list_objects(
            Bucket=self.bucket_name,
            Prefix=src_prefix,
        )

        if 'Contents' in response.keys():
            # Todo:parallel
            for s3_object in response['Contents']:
                src_key = s3_object['Key']
                dest_key = s3_object['Key'].replace(src_prefix, dest_prefix, 1)
                copy_source = {
                    'Bucket': self.bucket_name,
                    'Key': src_key
                }
                self.client.copy(CopySource=copy_source,
                                 Bucket=self.bucket_name,
                                 Key=dest_key)

            delete_objects = [{'Key': s3_object['Key']} for s3_object in response['Contents']]
            self.client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': delete_objects
                }
            )

        else:
            pass

    def on_created(self, event):
        """Called when a file or directory is created.

        :param event:
            Event representing file/directory creation.
        :type event:
            :class:`DirCreatedEvent` or :class:`FileCreatedEvent`
        """

        # get the time when event occur
        seconds = int(time.time())

        if not event.is_directory:

            # ignore if the same event occur within 1 second
            if (seconds, event.src_path) in self.file_updated_event:
                return

            self.file_updated_event.add((seconds, event.src_path))

        print(event)

        # generate key in S3
        key = event.src_path.replace(self.local_root, self.remote_root, 1)
        key = key.replace('\\', '/')

        # upload

        if event.is_directory:
            try:
                self.client.upload_fileobj(Dir(), self.bucket_name, key + '/')

            except botocore.exceptions.ClientError as error:
                raise error
        else:
            try:
                self.client.head_object(
                    Bucket=self.bucket_name,
                    Key=key,
                )

            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == '404':  # Object doesn't exist in S3
                    upload_object(self.client, self.bucket_name, event.src_path, key, self.threshold, self.chunk_size)
                else:
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
        if (seconds, event.src_path) in self.file_updated_event:
            return

        self.file_updated_event.add((seconds, event.src_path))
        print(event)

        # generate key in S3
        key = event.src_path.replace(self.local_root, self.remote_root, 1)
        key = key.replace('\\', '/')

        # get ETag
        while True:
            try:
                fetag = calc_etag(event.src_path, self.threshold, self.chunk_size)
                break
            except IOError:
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

        upload_object(self.client, self.bucket_name, event.src_path, key, self.threshold, self.chunk_size)
