#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# pylint: disable = unused-variable
import http.client
import mimetypes
import subprocess
import sys
import time
from statistics import mean

openssl_cipher_types = ('aes', 'aes128', 'aes192', 'aes256', 'bf', 'blowfish',
                        'camellia', 'cast', 'cast5', 'des', 'des3', 'desx', 'id', 'rc2', 'rc4', 'seed')

IP = "169.254.91.147"
PORT = 8000


class CipherResult:
    """
    CipherResult(encryption algorithm name and parameters: str, int, float, float, float, float, float)
    """

    def __init__(self, cipher: str, startTime: int, elapsedTime: float, throughput: float, cpuUtilPct=0, memUsed=0, memUsedPct=0):
        self.cipher = cipher
        self.startTime = startTime
        self.elapsedTime = elapsedTime
        self.throughput = throughput
        self.cpuUtilPct = cpuUtilPct
        self.memUsed = memUsed
        self.memUsedPct = memUsedPct

    def __str__(self):
        # return the descriptive information of the CipherResult
        tmp = self.cipher.split('-')
        info = '********Algorithm: ' + tmp[0] + '\n\tParameters: ['
        if len(tmp) > 1:
            for i in tmp[1:]:
                info += i + ', '
        info += ']\n\tstartTime: ' + str(self.startTime) \
            + '\n\telapsedTime: ' + str(self.elapsedTime) + ' ms' \
            + '\n\tthroughput: ' + '%0.6f' % self.throughput + ' Mbytes/s' \
            + '\n\tcpuUtilPct: ' + '%0.4f' % self.cpuUtilPct \
            + '\n\tmemUsed: ' + str(self.memUsed) + ' Kbytes' \
            + '\n\tmemUsedPct: ' + '%0.4f' % self.memUsedPct
        return info

    def generate_payload(self):
        # return the json type payload
        payload = "{\"cipher\":\"" + self.cipher \
            + "\",\"startTime\":\"" + str(self.startTime) \
            + "\",\"elapsedTime\":\"" + str(self.elapsedTime) \
            + "\",\"throughput\":\"" + '%0.6f' % self.throughput \
            + "\",\"cpuUtilPct\":\"" + '%0.4f' % self.cpuUtilPct \
            + "\",\"memUsed\":\"" + str(self.memUsed) \
            + "\",\"memUsedPct\":\"" + '%0.4f' % self.memUsedPct \
            + "\"}"
        return payload


def run_shell(command: str) -> tuple:
    """
    Run shell command in the petalinux of Xilinx AX7010
    :param command: shell command
    :return: shell output result, [returncode]
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    stdout = p.communicate()
    return stdout


def sh_time_all(stdout_bytes_tuple: tuple):
    """
    Get all of the performance info in the ps from the stdout of 'time -v' linux shell
    :param stdout_bytes: bytes of stdout
    :return: elapsed_time(ms), throughput(Mbytes/s), cpu_util_pct(0.xx), mem_used(Kbytes), mem_used_pct(0.xx)
    """
    stdout = str(stdout_bytes_tuple[1], encoding="utf-8").split('\n\t')
    # stdout[4]: Elapsed (wall clock) time (h:mm:ss or m:ss): 0m 0.00s
    line_info = stdout[4].split()
    elapsed_time = 1000.0 * \
        (float(line_info[-2].replace('m', '')) *
         60.0 + float(line_info[-1].replace('s', '')))
    # /run/media/mmcblk0p2/data/input.mat: 8,717,240 bytes
    throughput = float(8717240) / elapsed_time / 1000.0
    # stdout[3]: Percent of CPU this job got: xxx%
    line_info = stdout[3].split()
    cpu_util_pct = float(line_info[-1].replace('%', '')) / 100.0
    # stdout[9]: Maximum resident set size (kbytes): 2672(Kbytes)
    line_info = stdout[9].split()
    mem_used = float(line_info[-1])
    # use shell: 'free' or 'cat /proc/meminfo' to get info of memory
    # XLINIX_ZYNQ ALINX AX7010 max Memory size: 510440(Kbytes)
    mem_used_pct = mem_used / 510440.0
    # return elapsed_time, throughput, cpu_util_pct, mem_used, mem_used_pct
    return cpu_util_pct, mem_used, mem_used_pct


def sh_real_time(stdout_bytes_tuple: tuple):
    """
    Get real time result from the stdout of 'time' linux shell
    :param stdout_bytes: bytes of stdout
    :return: real time (ms)
    """
    stdout_bytes = stdout_bytes_tuple[1]
    # stdout_bytes demo: b'\nreal\t0m1.212s\nuser\t0m0.390s\nsys\t0m0.100s\n'
    output = str(stdout_bytes, encoding="utf-8").split()
    l = output[1].replace('m', ' ').replace('s', ' ').split()
    output[1] = str(float(l[0])*60*1000 + float(l[1])*1000)
    l = output[3].replace('m', ' ').replace('s', ' ').split()
    output[3] = str(float(l[0])*60*1000 + float(l[1])*1000)
    l = output[5].replace('m', ' ').replace('s', ' ').split()
    output[5] = str(float(l[0])*60*1000 + float(l[1])*1000)
    result = {}
    result[output[0]] = output[1]
    result[output[2]] = output[3]
    result[output[4]] = output[5]
    return float(result.get('real'))


def openssl_encryption(cipher: str, options=''):
    """
    Openssl encryption algorithm\n
    :param cipher: str of info about encryption algorithm\n
    :return: cipher result parameters
    """
    # cipher should not be empty
    if cipher == '':
        print('openssl need cipher types')
        exit(1)
    command = "time " + options + " openssl enc -" + cipher + \
        " -in /run/media/mmcblk0p2/data/input.mat -out /run/media/mmcblk0p2/data/out.txt -pass pass:cccgnit20161653"
    stdout_bytes_tuple = run_shell(command)
    # determine which method is used for performance testing
    if options == '-v':
        return sh_time_all(stdout_bytes_tuple)
    else:
        real_time = sh_real_time(stdout_bytes_tuple)
        # /run/media/mmcblk0p2/data/input.mat: 8,717,240 bytes
        throughput = float(8717240) / real_time / 1000.0
        return real_time, throughput


def gmssl_encryption(cipher: str, options=''):
    """
    gmssl encryption algorithm\n
    :param cipher: str of info about encryption algorithm\n
    :return: cipher result parameters
    """
    # cipher should not be empty
    if cipher == '':
        print('gmssl need cipher types')
        exit(1)
    command = "time " + options + " python3 /run/media/mmcblk0p2/cryptoapp/gmsslapp.py " + cipher
    stdout_bytes_tuple = run_shell(command)
    # determine which method is used for performance testing
    if options == '-v':
        return sh_time_all(stdout_bytes_tuple)
    else:
        real_time = sh_real_time(stdout_bytes_tuple)
        if cipher.split('-')[0] == 'sm2':
            # sm2: 64 bytes
            throughput = float(64) / real_time / 1000.0
        else:
            # sm4: /run/media/mmcblk0p2/data/s7-200stop.pcapng: 1,932 bytes
            throughput = float(1932) / real_time / 1000.0
        return real_time, throughput


def lwssl_encryption(cipher: str, options=''):
    """
    lwssl encryption algorithm\n
    :param cipher: str of info about encryption algorithm\n
    :return: cipher result parameters
    """
    # cipher should not be empty
    if cipher == '':
        print('lwssl need cipher types')
        exit(1)
    command = "time " + options + " python3 /run/media/mmcblk0p2/cryptoapp/lwsslapp.py " + cipher
    stdout_bytes_tuple = run_shell(command)
    # determine which method is used for performance testing
    if options == '-v':
        return sh_time_all(stdout_bytes_tuple)
    else:
        real_time = sh_real_time(stdout_bytes_tuple)
        # /run/media/mmcblk0p2/data/s7-200stop.pcapng: 30,720 bytes
        throughput = float(30720) / real_time / 1000.0
        return real_time, throughput


def benchmark(cipher: str):
    """
    Benchmark the crypto algorithm\n
    :param cipher: str of info about encryption algorithm\n
    :return: CipherResult
    """
    cipher_info = cipher.split('-')
    if cipher_info[0] in openssl_cipher_types:
        start_time = int(time.time())
        elapsed_time, throughput = openssl_encryption(cipher)
        # in order to give the next process enough execution space to prevent parallelism
        time.sleep(0.8)
        cpu_util_pct, mem_used, mem_used_pct = openssl_encryption(
            cipher, options='-v')
        cipher_result = CipherResult(
            cipher, start_time, elapsed_time, throughput, cpu_util_pct, mem_used, mem_used_pct)
        return cipher_result
    elif cipher_info[0] == 'sm2' or cipher_info[0] == 'sm4':
        start_time = int(time.time())
        elapsed_time, throughput = gmssl_encryption(cipher)
        time.sleep(0.8)
        cpu_util_pct, mem_used, mem_used_pct = gmssl_encryption(
            cipher, options='-v')
        cipher_result = CipherResult(
            cipher, start_time, elapsed_time, throughput, cpu_util_pct, mem_used, mem_used_pct)
        return cipher_result
    elif cipher_info[0] == 'simon' or cipher_info[0] == 'speck':
        start_time = int(time.time())
        elapsed_time, throughput = lwssl_encryption(cipher)
        time.sleep(0.8)
        cpu_util_pct, mem_used, mem_used_pct = lwssl_encryption(
            cipher, options='-v')
        cipher_result = CipherResult(
            cipher, start_time, elapsed_time, throughput, cpu_util_pct, mem_used, mem_used_pct)
        return cipher_result
    else:
        print("Error: Unknow cipher type!")


def post_django(cipher_result: CipherResult):
    """
    Request POST the cipher result to the django and mysql
    :param cipher_result: CipherResult 
    :return: the respose of django
    """
    conn = http.client.HTTPConnection(IP, PORT)
    payload = cipher_result.generate_payload()
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/result/", payload, headers)
    res = conn.getresponse().read().decode("utf-8")
    return res


if __name__ == "__main__":
    # judgment program input
    if len(sys.argv) < 2:
        print(
            "Usage:cryptoapp <algorithm_type>[-key_size][-mode][-block_size]")
        exit(1)
    # run benchmark
    cipher_result = benchmark(cipher=sys.argv[1])
    # print(cipher_result)
    # communication with the Django server
    res = post_django(cipher_result)
    print(res)
