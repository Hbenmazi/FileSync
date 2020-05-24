import os
import pickle
import shelve
import ZODB, ZODB.FileStorage
import transaction
from concurrent.futures import ThreadPoolExecutor


class FilePart:
    def __init__(self, bucket_name, key, file_path, part_num, offset, length, transfer_id):
        self.bucket_name = bucket_name
        self.key = key
        self.file_path = file_path
        self.part_num = part_num
        self.offset = offset
        self.length = length
        self.transfer_id = transfer_id
        if not os.path.exists("parts/{}".format(transfer_id)):
            os.makedirs("parts/{}".format(transfer_id))
        with open("parts/{}/{}.pt".format(transfer_id, part_num), "wb") as f:
            pickle.dump(self, f)


if __name__ == "__main__":
    with open("parts/{}-{}".format(1, 'key'), "rb") as f:
        a = pickle.load(f)
        print(a)
