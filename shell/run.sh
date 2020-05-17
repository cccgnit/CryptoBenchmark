#!/bin/bash

list=( aes-128-cbc aes-128-cfb aes-128-ctr aes-128-ecb aes-128-ofb \
       aes-192-cbc aes-192-cfb aes-192-ctr aes-192-ecb aes-192-ofb \
       aes-256-cbc aes-256-cfb aes-256-ctr aes-256-ecb aes-256-ofb \
       bf-cbc bf-cfb bf-ecb bf-ofb \
       camellia-128-cbc camellia-128-cfb camellia-128-ecb camellia-128-ofb \
       camellia-192-cbc camellia-192-cfb camellia-192-ecb camellia-192-ofb \
       camellia-256-cbc camellia-256-cfb camellia-256-ecb camellia-256-ofb \
       cast-cbc cast5-cbc cast5-cfb cast5-ecb cast5-ofb \
       des-cbc des-cfb des-ecb des-ofb \
       des-ede des-ede-cbc des-ede-cfb des-ede-ofb \
       des-ede3 des-ede3-cbc des-ede3-cfb des-ede3-ofb \
       des3 desx desx-cbc \
       rc2 rc2-40-cbc rc2-64-cbc rc2-cbc rc2-cfb rc2-ecb rc2-ofb \
       rc4 rc4-40 \
       seed-cbc seed-cfb seed-ecb seed-ofb \
       sm2 sm4 sm4-cbc sm4-ebc \
       simon-64-ecb-32 simon-64-ctr-32 simon-64-cbc-32 simon-64-pcbc-32 simon-64-cfb-32 simon-64-ofb-32 \
       simon-72-ecb-48 simon-72-ctr-48 simon-72-cbc-48 simon-72-pcbc-48 simon-72-cfb-48 simon-72-ofb-48 \
       simon-96-ecb-48 simon-96-ctr-48 simon-96-cbc-48 simon-96-pcbc-48 simon-96-cfb-48 simon-96-ofb-48 \
       simon-96-ecb-64 simon-96-ctr-64 simon-96-cbc-64 simon-96-pcbc-64 simon-96-cfb-64 simon-96-ofb-64 \
       simon-128-ecb-64 simon-128-ctr-64 simon-128-cbc-64 simon-128-pcbc-64 simon-128-cfb-64 simon-128-ofb-64 \
       simon-96-ecb-96 simon-96-ctr-96 simon-96-cbc-96 simon-96-pcbc-96 simon-96-cfb-96 simon-96-ofb-96 \
       simon-144-ecb-96 simon-144-ctr-96 simon-144-cbc-96 simon-144-pcbc-96 simon-144-cfb-96 simon-144-ofb-96 \
       simon-128-ecb-128 simon-128-ctr-128 simon-128-cbc-128 simon-128-pcbc-128 simon-128-cfb-128 simon-128-ofb-128 \
       simon-192-ecb-128 simon-192-ctr-128 simon-192-cbc-128 simon-192-pcbc-128 simon-192-cfb-128 simon-192-ofb-128 \
       simon-256-ecb-128 simon-256-ctr-128 simon-256-cbc-128 simon-256-pcbc-128 simon-256-cfb-128 simon-256-ofb-128 \
       speck-64-ecb-32 speck-64-ctr-32 speck-64-cbc-32 speck-64-pcbc-32 speck-64-cfb-32 speck-64-ofb-32 \
       speck-72-ecb-48 speck-72-ctr-48 speck-72-cbc-48 speck-72-pcbc-48 speck-72-cfb-48 speck-72-ofb-48 \
       speck-96-ecb-48 speck-96-ctr-48 speck-96-cbc-48 speck-96-pcbc-48 speck-96-cfb-48 speck-96-ofb-48 \
       speck-96-ecb-64 speck-96-ctr-64 speck-96-cbc-64 speck-96-pcbc-64 speck-96-cfb-64 speck-96-ofb-64 \
       speck-128-ecb-64 speck-128-ctr-64 speck-128-cbc-64 speck-128-pcbc-64 speck-128-cfb-64 speck-128-ofb-64 \
       speck-96-ecb-96 speck-96-ctr-96 speck-96-cbc-96 speck-96-pcbc-96 speck-96-cfb-96 speck-96-ofb-96 \
       speck-144-ecb-96 speck-144-ctr-96 speck-144-cbc-96 speck-144-pcbc-96 speck-144-cfb-96 speck-144-ofb-96 \
       speck-128-ecb-128 speck-128-ctr-128 speck-128-cbc-128 speck-128-pcbc-128 speck-128-cfb-128 speck-128-ofb-128 \
       speck-192-ecb-128 speck-192-ctr-128 speck-192-cbc-128 speck-192-pcbc-128 speck-192-cfb-128 speck-192-ofb-128 \
       speck-256-ecb-128 speck-256-ctr-128 speck-256-cbc-128 speck-256-pcbc-128 speck-256-cfb-128 speck-256-ofb-128)

python3 /run/media/mmcblk0p2/cryptoapp/monitoragent.py &
pid=$(ps x | grep monitoragent | grep -v grep | awk '{print $1}')
sleep 5s
for item in ${list[@]}
do
        for a in {1..50}
        do
                python3 /run/media/mmcblk0p2/cryptoapp/cryptoapp.py ${item}
                sleep 1s
        done
done
sleep 5s
kill $pid