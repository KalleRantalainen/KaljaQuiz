# 1) Detect the primary IPv4 on your Wi-Fi/Ethernet
$ip = (Get-NetIPAddress -AddressFamily IPv4 `
      -InterfaceAlias "Wi-Fi","Ethernet" `
      | Where-Object { $_.PrefixOrigin -eq "Dhcp" } `
      | Select-Object -First 1 -ExpandProperty IPAddress)

if (-not $ip) {
  Write-Error "Could not determine IP address."
  exit 1
}

# 2) Write it into .env (Compose will pick this up)
"HOST_IP=$ip" | Out-File -Encoding ASCII .env

# 3) Launch
docker-compose up --build
# Voi vaihtaa komentoon docker-compose up, jos ei halua buildata vaan ajaa vaan