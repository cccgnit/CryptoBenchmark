#!/bin/bash
python3 -m ensurepip
cd /run/media/mmcblk0p2/pypi/gmssl-3.2.1
python3 setup.py install
pip3 install /run/media/mmcblk0p2/pypi/simonspeckciphers-1.0.0-py2.py3-none-any.whl
cd /run/media/mmcblk0p2