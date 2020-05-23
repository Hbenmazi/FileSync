class FilePart:
    def __init__(self, file_path, part_num, offset, length, transfer_id):
        self.file_path = file_path
        self.part_num = part_num
        self.offset = offset
        self.length = length
        self.transfer_id = transfer_id
