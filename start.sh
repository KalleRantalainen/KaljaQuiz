#!/bin/bash

# 1) Detect the primary IPv4 on your Wi-Fi/Ethernet
ip=$(ip -4 addr show dev wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1)

# If the IP address couldn't be found
if [ -z "$ip" ]; then
  echo "Could not determine IP address."
  exit 1
fi

# 2) Write it into .env (Compose will pick this up)
echo "HOST_IP=$ip" > .env

# 3) Launch Docker Compose
docker compose up --build
# Or if you don't want to rebuild:
# docker compose up
