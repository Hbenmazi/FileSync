import os
import pickle

class FilePart:
    """ FilePart store the meta data of parts when using multipart upload

    Attributes:
        bucket_name: Bucket name that the origin file to be uploaded to
        key: Dest key of the upload
        file_path: Local path of the whole file
        part_num: PartNum of current part
        offset: The start position of current part(bytes)
        length: Size of current prat(bytes)
        transfer_id: upload id
    """

    def __init__(self, bucket_name, key, file_path, part_num, offset, length, transfer_id):
        self.bucket_name = bucket_name
        self.key = key
        self.file_path = file_path
        self.part_num = part_num
        self.offset = offset
        self.length = length
        self.transfer_id = transfer_id

        # store itself to desk for breakpoint resuming
        if not os.path.exists("parts/{}".format(transfer_id)):
            os.makedirs("parts/{}".format(transfer_id))
        with open("parts/{}/{}.pt".format(transfer_id, part_num), "wb") as f:
            pickle.dump(self, f)


if __name__ == "__main__":
    with open("parts/{}-{}".format(1, 'key'), "rb") as f:
        a = pickle.load(f)
        print(a)
