import math
import os
import shutil
import time
from concurrent.futures.thread import ThreadPoolExecutor
from hashlib import md5
import botocore.exceptions
from filechunkio import FileChunkIO
from common.FilePart import FilePart
from tqdm import tqdm

MB = 1024 * 1024


def upload_part(kwargs):
    client = kwargs.get('client')
    file_part = kwargs.get('file_part')

    while True:
        try:
            with FileChunkIO(file_part.file_path, 'r', offset=file_part.offset, bytes=file_part.length) as fp_body:
                response = client.upload_part(
                    Body=fp_body,
                    Bucket=file_part.bucket_name,
                    ContentLength=file_part.length,
                    Key=file_part.key,
                    PartNumber=file_part.part_num,
                    UploadId=file_part.transfer_id,
                )
            break
        except IOError:
            time.sleep(0.05)
        except botocore.exceptions.ClientError as error:
            raise error

    path = 'parts/{}/{}.pt'.format(file_part.transfer_id, file_part.part_num)
    if os.path.exists(path):
        os.remove(path)

    return {'ETag': response['ETag'], 'PartNumber': file_part.part_num}


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
                     'file_part': FilePart(bucket_name=bucket_name,
                                           key=key,
                                           file_path=src_path,
                                           part_num=i + 1,
                                           offset=(chunk_size * i),
                                           length=min(chunk_size, fsize - (chunk_size * i)),
                                           transfer_id=upload_id)}
                    for i in range(0, chunk_cnt)]

            with ThreadPoolExecutor(max_workers=4) as pool:
                res = list(
                    tqdm(pool.map(upload_part, args), total=len(args), desc="Multi Part Uploading:{}".format(key)))

            client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                MultipartUpload={
                    'Parts': res
                },
                UploadId=upload_id,
            )

            path = 'parts/{}'.format(upload_id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
            print("S3 Multipart Upload Successfully: {}".format(key))

    except botocore.exceptions.ClientError as error:
        raise error


def list_all_file(dir_path):
    for r, d, f in os.walk(dir_path):
        return f


def list_all_subdir(path):
    gen = os.walk(path)
    for x in gen:
        return x[1]


def list_all_dir(s3, root):
    res = []
    for obj in s3.ls(root, detail=True, refresh=False):
        if obj['type'] == 'directory' and obj['Key'] != root:
            res.append(obj['Key'])
            res = res + list_all_dir(s3, obj['Key'])
    return list(set(res))


if __name__ == "__main__":
    print(list_all_file('..\\parts\\{}'.format("新建文件夹")))
