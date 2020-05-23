import os
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
