import base64
import hashlib
import json
from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size
# 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
pad = lambda s: s + (BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE)

unpad = lambda s: s[0:-ord(s[-1:])]


class PyCryptAES(object):

    key = "0CoJUm6Qyw8W8jud"
    iv = "2021012131420000"

    def __init__(self, key=None, mode=AES.MODE_CBC, iv=None):
        self.key = key if key else PyCryptAES.key
        self.mode = mode
        self.cipherText = None
        self.iv = iv if iv else PyCryptAES.iv

    def encrypt(self, text):
        """加密"""
        text = pad(text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode("utf-8"), mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return base64.b64encode(encrypted_text).decode('utf-8')

    @property
    def get_md5_value(self):
        hashlib_obj = hashlib.md5()
        hashlib_obj.update(self.key.encode("utf-8"))
        return hashlib_obj.hexdigest()

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        """解密"""
        decode = base64.b64decode(text)
        crypto = AES.new(self.key.encode("utf-8"), self.mode, self.iv.encode('utf-8'))
        plain_text = crypto.decrypt(decode)
        return unpad(plain_text).decode()


if __name__ == '__main__':
    a = PyCryptAES(
        key="0CoJUm6Qyw8W8jud",
        iv="2021012131420000"
    )
    text = json.dumps({"customer_id": 74199, "store_hash": "fhnch"})
    print(a.encrypt(text))
    print(a.decrypt("5+K+7wtraZ6dEDBbJgm4cpmf45JJCBUHrWNdYjAg54LjlE2Bav09zIY9EDzdNdROwz6FcJTeAbEwFV3PpkAy/Q=="))
