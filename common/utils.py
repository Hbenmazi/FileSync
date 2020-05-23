import math
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from hashlib import md5
import botocore.exceptions
from filechunkio import FileChunkIO

from .FilePart import FilePart

MB = 1024 * 1024


def upload_part(kwargs):
    client = kwargs.get('client')
    bucket_name = kwargs.get('bucket_name')
    key = kwargs.get('key')
    file_part = kwargs.get('file_part')
    try:
        with FileChunkIO(file_part.file_path, 'r', offset=file_part.offset, bytes=file_part.length) as fp_body:
            response = client.upload_part(
                Body=fp_body,
                Bucket=bucket_name,
                ContentLength=file_part.length,
                Key=key,
                PartNumber=file_part.part_num,
                UploadId=file_part.transfer_id,
            )
        return {'ETag': response['ETag'], 'PartNumber': file_part.part_num}

    except botocore.exceptions.ClientError as error:
        raise error


def calc_etag(inputfile, threshold, partsize):
    fsize = os.path.getsize(inputfile)

    if fsize < threshold:
        with open(inputfile, 'rb') as f:
            fmd5 = md5(f.read()).hexdigest()
        return fmd5
    else:
        md5_digests = []
        with open(inputfile, 'rb') as f:
            for chunk in iter(lambda: f.read(partsize), b''):
                md5_digests.append(md5(chunk).digest())
        return md5(b''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))


def upload_object(client, bucket_name, src_path, key, threshold, chunk_size):
    # get file size(Byte)
    while True:
        try:
            fsize = os.path.getsize(src_path)
            break
        except IOError:
            time.sleep(0.05)

    try:
        if fsize < threshold:
            with open(src_path, 'rb') as data:
                client.upload_fileobj(data, bucket_name, key)
        else:
            response = client.create_multipart_upload(Bucket=bucket_name,
                                                      Key=key)
            if 'UploadId' in response.keys():
                upload_id = response['UploadId']
            else:
                raise Exception("Fail to init multipart upload for {}".format(src_path))

            chunk_cnt = int(math.ceil(fsize * 1.0 / chunk_size))

            args = [{'client': client,
                     'bucket_name': bucket_name,
                     'key': key,
                     'file_part': FilePart(file_path=src_path,
                                           part_num=i + 1,
                                           offset=(chunk_size * i),
                                           length=min(chunk_size, fsize - (chunk_size * i)),
                                           transfer_id=upload_id)}
                    for i in range(0, chunk_cnt)]

            with ThreadPoolExecutor(max_workers=4) as pool:
                res = pool.map(upload_part, args)

            client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                MultipartUpload={
                    'Parts': list(res)
                },
                UploadId=upload_id,
            )
            print("S3 Multipart Upload Successfully: {}".format(key))

    except botocore.exceptions.ClientError as error:
        raise error
