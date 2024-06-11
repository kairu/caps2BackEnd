from .common import pathlib, hashlib, os
def hash_filename(filename):
    hash_filename = hashlib.sha256((filename + str(os.urandom(10))).encode('utf-8')).hexdigest()
    hash_filename += pathlib.Path(filename).suffix
    return hash_filename