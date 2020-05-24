import pickle
import botocore.exceptions
from common.utils import *
import time
import boto3
from watchdog.observers import Observer
from FileSyncEventHandler import FileSyncEventHandler
import threading


class FileSyncLauncher(threading.Thread):
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, local_root, remote_root, bucket_name,
                 threshold=15, chunk_size=5):
        super().__init__()
        self.client = boto3.client('s3',
                                   endpoint_url=endpoint_url,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.local_root = local_root
        self.remote_root = remote_root
        self.bucket_name = bucket_name
        self.threshold = threshold * MB
        self.chunk_size = chunk_size * MB
        self.event_handler = FileSyncEventHandler(client=self.client,
                                                  local_root=self.local_root,
                                                  remote_root=self.remote_root,
                                                  bucket_name=bucket_name)
        self.stop = False

    def run(self):
        self.resume_upload()
        observer = Observer()
        observer.schedule(self.event_handler, path=self.local_root, recursive=True)
        observer.start()

        while not self.stop:
            time.sleep(1)

        observer.stop()
        observer.join()

    def resume_upload(self):

        try:
            # get all in-progress multipart=upload
            response = self.client.list_multipart_uploads(
                Bucket=self.bucket_name
            )

            if 'Uploads' not in response.keys():
                # if there is no in-progress multipart-upload then return
                return
            else:
                # get all unfinished multipart-upload in local
                all_uploads_id = list_all_subdir('parts')

                for multi_part_upload in response['Uploads']:
                    # for each in-progress multipart-upload, get the upload_id and key
                    upload_id = multi_part_upload['UploadId']
                    key = multi_part_upload['Key']

                    # if there are local unfinished multipart-upload that correspond to the remote one then resume
                    # upload
                    if upload_id in all_uploads_id:
                        print('Resume Uploading...: ' + key)

                        # get all local FilePart objects
                        part_names = list_all_file('parts/{}'.format(upload_id))
                        file_parts = []
                        for pname in part_names:
                            with open('parts/{}/{}'.format(upload_id, pname), 'rb') as f:
                                fpart = pickle.load(f)
                            file_parts.append(fpart)

                        # get parts that have been uploaded for current multipart-upload
                        response = self.client.list_parts(
                            Bucket=self.bucket_name,
                            Key=key,
                            UploadId=upload_id
                        )

                        if 'Parts' in response.keys():
                            Parts = [{'ETag': part['ETag'], 'PartNumber': part['PartNumber']}
                                     for part in response['Parts']]
                        else:
                            Parts = []

                        # construct args for ThreadPool
                        args = [{'client': self.client,
                                 'file_part': fpart}
                                for fpart in file_parts]

                        # multi-part upload
                        with ThreadPoolExecutor(max_workers=4) as pool:
                            res = list(tqdm(pool.map(upload_part, args),
                                            total=len(args) + len(Parts),
                                            initial=len(Parts),
                                            desc="Multi Part Uploading:{}".format(key)))

                        Parts = Parts + list(res)

                        # complete multi-part upload
                        self.client.complete_multipart_upload(
                            Bucket=self.bucket_name,
                            Key=key,
                            MultipartUpload={
                                'Parts': Parts
                            },
                            UploadId=upload_id,
                        )
                        path = 'parts/{}'.format(upload_id)
                        if os.path.exists(path):
                            shutil.rmtree(path, ignore_errors=True)
                        print('Resume Upload Successfully: ' + key)

                    else:
                        # local part lost, abort the multipart_upload
                        self.client.abort_multipart_upload(
                            Bucket=self.bucket_name,
                            Key=key,
                            UploadId=upload_id
                        )

        except botocore.exceptions.ClientError as e:
            raise e
