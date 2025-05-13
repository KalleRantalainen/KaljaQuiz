#!/bin/bash

# 1) Automatically detect the primary IPv4 address from a non-loopback interface
ip=$(ip -4 -o addr show scope global | awk '{print $4}' | cut -d/ -f1 | head -n1)

# 2) If the IP address couldn't be found
if [ -z "$ip" ]; then
  echo "Could not determine IP address."
  exit 1
fi

# 3) Write it into .env (Compose will pick this up)
echo "HOST_IP=$ip" > .env

# 4) Launch Docker Compose
docker compose up --build
# Or use just: docker compose up

