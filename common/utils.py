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
    """upload single part in multipart upload

        Args:
            kwargs: A dict that store parm(for ThreadPoolExecutor) For
                    example:
                    {'client':boot3.client(),
                    'file_part':common.FilePart.FilePart}

        Returns:
            A dict that store ETag and PartNumber of current part. For
            example:

            {'ETag': string, 'PartNumber': int}
        """

    client = kwargs.get('client')
    file_part = kwargs.get('file_part')

    # while loop to get read permission of target file
    while True:
        try:
            with FileChunkIO(file_part.file_path, 'r', offset=file_part.offset, bytes=file_part.length) as fp_body:
                # upload
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

    # if upload successfully, then remove the FilePart object that remain in desk
    path = 'parts/{}/{}.pt'.format(file_part.transfer_id, file_part.part_num)
    if os.path.exists(path):
        os.remove(path)

    return {'ETag': response['ETag'], 'PartNumber': file_part.part_num}


def calc_etag(inputfile, threshold, partsize):
    """compute Etag of a file

        Args:
            inputfile: file path of file to compute ETag
            threshold: threshold that trigger multipart upload,
                       since S3 use different algorithm for multipart uploaded object
            partsize: chunk size of each part

        Returns:
            Etag(String): Etag of target file
        """

    # get size of file
    fsize = os.path.getsize(inputfile)

    if fsize < threshold:
        # return md5 of the file if its size less than threshold
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
    """compute Etag of a file

        Args:
            client: boot.cliemt('s3')
            bucket_name: dest bucket of uploading
            src_path: path of file to be uploaded
            key: dest key in S3
            threshold: threshold to trigger multipart upload
            chunk_size: chunk_size of multipart upload

        """

    # get file size(while loop tp get read permission of taget file)
    while True:
        try:
            fsize = os.path.getsize(src_path)
            break
        except IOError:
            time.sleep(0.05)

    try:
        if fsize < threshold:
            # if file size less than threshold then upload it directly
            with open(src_path, 'rb') as data:
                client.upload_fileobj(data, bucket_name, key)
                print('Upload:' + key)
        else:
            # initialize a multipart upload
            response = client.create_multipart_upload(Bucket=bucket_name,
                                                      Key=key)

            # get upload id
            if 'UploadId' in response.keys():
                upload_id = response['UploadId']
            else:
                raise Exception("Fail to init multipart upload for {}".format(src_path))

            # the num of chunk
            chunk_cnt = int(math.ceil(fsize * 1.0 / chunk_size))

            # construct the parm for each part
            args = [{'client': client,
                     'file_part': FilePart(bucket_name=bucket_name,
                                           key=key,
                                           file_path=src_path,
                                           part_num=i + 1,
                                           offset=(chunk_size * i),
                                           length=min(chunk_size, fsize - (chunk_size * i)),
                                           transfer_id=upload_id)}
                    for i in range(0, chunk_cnt)]

            # upload each part
            # res = []
            # for arg in tqdm(args, total=len(args), desc="Multi Part Upload{}".format(key)):
            #     res.append(upload_part(arg))

            with ThreadPoolExecutor(max_workers=4) as pool:
                res = list(
                    tqdm(pool.map(upload_part, args), total=len(args), desc="Multi Part Uploading:{}".format(key)))

            # complete multi part upload
            client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                MultipartUpload={
                    'Parts': res
                },
                UploadId=upload_id,
            )

            # remove FilePart object in desk
            path = 'parts/{}'.format(upload_id)
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
            print("S3 Multipart Upload Successfully: {}".format(key))

    except botocore.exceptions.ClientError as error:
        raise error


def list_all_direct_file(dir_path):
    """list all file path in a dir
    """
    for r, d, f in os.walk(dir_path):
        return f


def list_all_subdir(path):
    """list all subdir in a dir(immediate)
    """
    gen = os.walk(path)
    for x in gen:
        return x[1]


def list_all_dir(s3, root):
    """list all dir under the root in s3
    """

    res = []
    for obj in s3.ls(root, detail=True, refresh=False):
        if obj['type'] == 'directory' and obj['Key'] != root:
            res.append(obj['Key'])
            res = res + list_all_dir(s3, obj['Key'])
    return list(set(res))


def allfile(basepath):
    res = []
    for item in os.listdir(basepath):
        path = os.path.join(basepath, item)
        if os.path.isfile(path):
            res.append(path)
        else:
            res = res + allfile(path)
    return res

