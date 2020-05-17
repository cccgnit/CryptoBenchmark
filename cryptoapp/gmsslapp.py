#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# pylint: disable = unused-variable
import base64
import binascii
import sys

from gmssl import func, sm2
from gmssl.sm4 import SM4_DECRYPT, SM4_ENCRYPT, CryptSM4


def sm2_enc(data):
    """
    Run SM2 encryption algorithm
    :param data: plaintext (bytes)
    """
    # 66 bytes
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    # 128 byets
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    # hexadecimal public and private keys
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    enc_data = sm2_crypt.encrypt(data)
    # dec_data = sm2_crypt.decrypt(enc_data)
    # random_hex_str = func.random_hex(sm2_crypt.para_len)
    # sign = sm2_crypt.sign(data, random_hex_str)
    # assert sm2_crypt.verify(sign, data)


def sm4_enc(data):
    """
    Run SM4 encryption algorithm in cbc mode
    :param data: plaintext (bytes)
    """
    # 16 bytes
    key = b'3l5butlj26hvv313'
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_ecb(data)
    # crypt_sm4.set_key(key, SM4_DECRYPT)
    # decrypt_value = crypt_sm4.crypt_ecb(encrypt_value)


def sm4_enc_ebc(data):
    """
    Run SM4 encryption algorithm in ebc mode
    :param data: plaintext (bytes)
    """
    # 16 bytes
    key = b'3l5butlj26hvv313'
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_cbc(iv, data)
    # crypt_sm4.set_key(key, SM4_DECRYPT)
    # decrypt_value = crypt_sm4.crypt_cbc(iv, encrypt_value)


if __name__ == "__main__":
    # judgment program input
    if len(sys.argv) < 2:
        print(
            "Usage:gmsslapp <algorithm_type>[-mode]")
        exit(1)
    if sys.argv[1] == 'sm2':
        # data: 64 bytes
        data = b'00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83'
        sm2_enc(data)
    elif sys.argv[1] == 'sm4' or sys.argv[1] == 'sm4-cbc':
        # read input data
        # f = open('/run/media/mmcblk0p2/data/platform.pcap', 'rb+')
        f = open('/run/media/mmcblk0p2/data/s7-200stop.pcapng', 'rb+')
        data = f.read()
        f.close()
        sm4_enc(data)
    elif sys.argv[1] == 'sm4-ebc':
        # read input data
        # f = open('/run/media/mmcblk0p2/data/platform.pcap', 'rb+')
        f = open('/run/media/mmcblk0p2/data/s7-200stop.pcapng', 'rb+')
        data = f.read()
        f.close()
        sm4_enc_ebc(data)
