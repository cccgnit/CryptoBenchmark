#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
from random import randint

from simon import SimonCipher
from speck import SpeckCipher

# Valid block and key sizes in bits are:
# block size  key sizes
#     32      64
#     48      72,96
#     64      96,128
#     96      96,144
#     128     128,192,256

# Both ciphers support the most common modes of block cipher operation:
# Electronic Code Book ECB (Default mode for Speck/Simon)
# Counter CTR
# Cipher Block Chaining CBC
# Propagating Cipher Block Chaining PCBC
# Cipher Feedback CFB
# Output Feedback OFB

# key = 0x1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100
# plaintxt = 0x65736f6874206e49202e72656e6f6f70


def simon_enc(cipher_info):
    """
    Run simon lightweight encryption algorithm
    :param cipher_info: the info of simon about block and key sizes, cipher mode
    """
    block_size = int(cipher_info[3])
    key_size = int(cipher_info[1])
    mode = cipher_info[2].upper()

    # plaintxt size: 30.72 kbytes
    plaintxt_size_bit = 122880
    cnt = int(plaintxt_size_bit / block_size)
    key = randint(0, (2**key_size) - 1)
    plaintxt = randint(0, (2**block_size) - 1)
    iv = 0x123456789ABCDEF0
    counter = 0x1

    if mode == 'ECB':
        c = SimonCipher(key, key_size, block_size, mode)
    elif mode == 'CTR':
        c = SimonCipher(key, key_size, block_size, mode, init=iv, counter=counter)
    else:
        c = SimonCipher(key, key_size, block_size, mode, init=iv)
    for _ in range(cnt):
        c.encrypt(plaintxt)


def speck_enc(cipher_info):
    """
    Run speck lightweight encryption algorithm
    :param cipher_info: the info of speck about block and key sizes, cipher mode
    """
    block_size = int(cipher_info[3])
    key_size = int(cipher_info[1])
    mode = cipher_info[2].upper()

    # plaintxt size: 30.72 kbytes
    plaintxt_size_bit = 122880
    cnt = int(plaintxt_size_bit / block_size)
    key = randint(0, (2**key_size) - 1)
    plaintxt = randint(0, (2**block_size) - 1)
    iv = 0x123456789ABCDEF0
    counter = 0x1

    if mode == 'ECB':
        c = SpeckCipher(key, key_size, block_size, mode)
    elif mode == 'CTR':
        c = SpeckCipher(key, key_size, block_size, mode, init=iv, counter=counter)
    else:
        c = SpeckCipher(key, key_size, block_size, mode, init=iv)
    for _ in range(cnt):
        c.encrypt(plaintxt)


if __name__ == "__main__":
    # judgment program input
    if len(sys.argv) < 2:
        print(
            "Usage:lwsslapp <algorithm_type><-key_size><-mode[chain]><-block_size>")
        exit(1)
    cipher_info = sys.argv[1].split('-')
    if cipher_info[0] == 'simon':
        simon_enc(cipher_info)
    elif cipher_info[0] == 'speck':
        speck_enc(cipher_info)
