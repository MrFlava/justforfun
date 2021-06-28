import os
import hashlib

paths = ['/home/user/PycharmProjects/justforfun/test_path1']


def chunk_reader(file_obj, chunk_size: int = 1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def check_for_duplicates(paths_list: list, hash_func=hashlib.sha1):
    hashes = {}
    for path in paths_list:
        for dir_path, dir_names, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dir_path, filename)
                hash_obj = hash_func()
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hash_obj.update(chunk)
                file_id = (hash_obj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    print("Duplicate found: %s and %s" % (full_path, duplicate))
                else:
                    hashes[file_id] = full_path


if __name__ == "__main__":
    if paths:
        check_for_duplicates(paths)
    else:
        print("Please, enter paths to the check_for_duplicates function")
