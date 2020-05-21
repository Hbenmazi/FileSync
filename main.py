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
    observer = Observer()
    event_handler = FileSyncEventHandler()

    observer.schedule(event_handler, path="local", recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
