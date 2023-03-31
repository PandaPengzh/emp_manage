from mysite2.settings import SECRET_KEY  # 加密
import hashlib

def md5(str_pwd):
    a = hashlib.md5((str_pwd+SECRET_KEY).encode())  # 加盐 SECRET_KEY
    # a.update(SECRET_KEY.encode())
    return a.hexdigest()