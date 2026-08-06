#!/bin/bash
set -e

APP=/opt/fondazionesemplice

apt update
apt install -y git docker.io docker-compose-plugin python3 python3-pip

mkdir -p /opt
cd /opt

if [ ! -d "$APP" ]; then
 git clone https://github.com/glaucogaribaldi/fondazionesemplice "$APP"
fi

cd "$APP"

docker compose up -d

echo "Fondazione Semplice installed in PAPER mode"
