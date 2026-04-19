#!/bin/bash
curl -fsSL https://tailscale.com/install.sh | sh

mkdir -p /var/lib/tailscale /var/run/tailscale

tailscaled \
  --state=/var/lib/tailscale/tailscaled.state \
  --socket=/var/run/tailscale/tailscaled.sock \
  --tun=userspace-networking \
  --socks5-server=localhost:1055 \
  --outbound-http-proxy-listen=localhost:1055 &

sleep 3

tailscale up \
  --authkey=${TAILSCALE_AUTHKEY} \
  --hostname=${TAILSCALE_HOSTNAME:-render-vpn} \
  --advertise-exit-node \
  --ssh

# Чтобы Render не усыпил контейнер
python3 -m http.server 8080 &

exec sleep infinity
