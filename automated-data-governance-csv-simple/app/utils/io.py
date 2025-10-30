
import hashlib, datetime, pathlib

def file_checksum(path, algo='md5'):
    h = hashlib.new(algo)
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(8192),b''):
            h.update(chunk)
    return h.hexdigest()

def ensure_dir(p):
    pathlib.Path(p).mkdir(parents=True,exist_ok=True)

def now_iso():
    return datetime.datetime.now().isoformat()
