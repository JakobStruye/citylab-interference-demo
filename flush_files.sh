#!/bin/bash

scp -o StrictHostKeyChecking=no  -r output {username}@{server}.be:~/out/$(hostname) || exit 1
rm output/*
