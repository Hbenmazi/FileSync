import time

import boto3
from watchdog.observers import Observer
from FileSyncEventHandler import FileSyncEventHandler

endpoint_url = "http://scuts3.depts.bingosoft.net:29999"
aws_access_key_id = "8A5290742BF72419BAFF"
aws_secret_access_key = "W0FGNTc5OTU0RkJEQjQ3RTZCQTA2MjgxOEYwRUY2RkREQ0JBMzI1NTRd"

# Let's use Amazon S3
s3 = boto3.resource('s3', endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)
s3_client = boto3.client('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

if __name__ == "__main__":
    endpoint_url = "http://scuts3.depts.bingosoft.net:29999"
    aws_access_key_id = "8A5290742BF72419BAFF"
    aws_secret_access_key = "W0FGNTc5OTU0RkJEQjQ3RTZCQTA2MjgxOEYwRUY2RkREQ0JBMzI1NTRd"
    remote_root = 'remote'
    local_root = 'local'

    observer = Observer()
    event_handler = FileSyncEventHandler(endpoint_url,
                                         aws_access_key_id,
                                         aws_secret_access_key,
                                         local_root=local_root,
                                         remote_root=remote_root)

    observer.schedule(event_handler, path=local_root, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
