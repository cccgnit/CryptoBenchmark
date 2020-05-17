#!/bin/bash
starttime = $(date + %s)
echo -n "123132132121231321315665454132123" | openssl des-cbc  -iv 31313131312D2D2D -K 31313131312D2D2D -nosalt
endtime = $(date + %s)
cost = $((endtime - starttime))
echo $cost
# ps -ef| grep myprocess

time openssl enc -aes-128-cfb -in /run/media/mmcblk0p2/data/input.mat -out /run/media/mmcblk0p2/data/out.txt -pass pass:cccgnit20161653
time -v openssl enc -aes-128-cfb -in /run/media/mmcblk0p2/data/input.mat -out /run/media/mmcblk0p2/data/out.txt -pass pass:cccgnit20161653