import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


class RSACipher():
    def __init__(self) -> None:
        self.publicKey = None
        self.privateKey = None
        pass

    def GenerateKey(self):
        rsa = RSA.generate(1024, Crypto.Random.new().read)
        # master的祕鑰對的生成
        private_pem = rsa.exportKey()
        public_pem = rsa.publickey().exportKey()

        self.publicKey = public_pem.decode()
        self.privateKey = private_pem.decode()

        return {
            "public_key": self.publicKey,
            "private_key": self.privateKey
        }

    def PublicKeyImport(self, PublicKey):
        self.publicKey = PublicKey;
        pass

    # 公鑰加密
    def rsa_encode(self, message):
        rsakey = RSA.importKey(self.publicKey)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(
            cipher.encrypt(message.encode(encoding="utf-8")))
        return cipher_text.decode()


    # 公鑰解密
    def rsa_decode(self, cipher_text):
        rsakey = RSA.importKey(self.privateKey)
        cipher = PKCS1_v1_5.new(rsakey)

        text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
        return text.decode()


if __name__ == '__main__':
    print("Case 1:")
    a = RSACipher()
    a.GenerateKey()
    encrypt = a.rsa_encode("This is the testing message form case 1")
    decrypt = a.rsa_decode(encrypt)
    print("[ENCRYPTED]{}".format(encrypt))
    print("[DECRYPTED]{}".format(decrypt))

    print("\nCase 2:")
    b = RSACipher()
    b.PublicKeyImport(a.publicKey)
    encrypt = b.rsa_encode("This is the testing message form case 2")
    decrypt = a.rsa_decode(encrypt)
    print("[ENCRYPTED]{}".format(encrypt))
    print("[DECRYPTED]{}".format(decrypt))

