from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode

def encryptData(data):
    public_key = RSA.import_key(open("public_key.pem").read())
    rsa_encryption = PKCS1_OAEP.new(public_key)
    encryptedMessage = rsa_encryption.encrypt(data.encode())
    encodeMessage = b64encode(encryptedMessage).decode()
    return encodeMessage

questions = open("encryptedWords.txt", 'w')
questions.write(encryptData(open("words.txt", 'r').read()))