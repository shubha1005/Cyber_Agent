from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

# Define the Blueprint for tool1
tool1 = Blueprint('tool1', __name__)

CORS(tool1)  # To allow requests from React frontend

# AES Encryption/Decryption
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return b64encode(cipher.iv + ciphertext).decode()

def aes_decrypt(data, key):
    raw = b64decode(data)
    iv, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

# DES Encryption/Decryption
def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), DES.block_size))
    return b64encode(cipher.iv + ciphertext).decode()

def des_decrypt(data, key):
    raw = b64decode(data)
    iv, ciphertext = raw[:8], raw[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), DES.block_size).decode()

# RSA Encryption/Decryption
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(data, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return b64encode(cipher.encrypt(data.encode())).decode()

def rsa_decrypt(data, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.decrypt(b64decode(data)).decode()

# API Endpoints
@tool1.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data['text']
    key = data['key']
    method = data['method']

    try:
        if method == "AES":
            key = key[:16].encode()  # AES key must be 16 bytes
            result = aes_encrypt(text, key)
        elif method == "DES":
            key = key[:8].encode()  # DES key must be 8 bytes
            result = des_encrypt(text, key)
        elif method == "RSA":
            private_key, public_key = generate_rsa_keys()
            result = rsa_encrypt(text, public_key)
        else:
            return jsonify({"error": "Unsupported method"}), 400
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tool1.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    text = data['text']
    key = data['key']
    method = data['method']

    try:
        if method == "AES":
            key = key[:16].encode()
            result = aes_decrypt(text, key)
        elif method == "DES":
            key = key[:8].encode()
            result = des_decrypt(text, key)
        elif method == "RSA":
            result = rsa_decrypt(text, key)
        else:
            return jsonify({"error": "Unsupported method"}), 400
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Don't use `app.run` here in a blueprint; it's managed by the main app.
