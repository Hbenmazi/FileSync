import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import *
import boto3
import botocore.exceptions


class Dir:
    def read(self, amount=1):
        return bytes(0)


class FileSyncEventHandler(FileSystemEventHandler):
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, local_root, remote_root):
        self.client = boto3.client('s3',
                                   endpoint_url=endpoint_url,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.local_root = local_root
        self.remote_root = remote_root
        self.bucket_name = 'hezhiwei'

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
        if isinstance(event, DirModifiedEvent) or (seconds, event.src_path) in self.file_modified_event:
            return
        self.file_modified_event.add((seconds, event.src_path))

        print(event)

        # generate key in S3
        key = event.src_path.replace(self.local_root, self.remote_root, 1)
        key = key.replace('\\', '/')

        # upload
        try:
            time.sleep(1)
            with open(event.src_path, 'rb') as data:
                self.client.upload_fileobj(data, self.bucket_name, key)

        except botocore.exceptions.ClientError as error:
            raise error
