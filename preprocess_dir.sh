#!/usr/bin/env bash
for i in *.c
do
    gcc -E -I../../pycparser-master/utils/fake_libc_include $i -o ${i%.c}.i
done
