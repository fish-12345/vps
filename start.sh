#!/bin/bash
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
  --ssh &

sleep 3

python3 -m http.server 10000 --bind 0.0.0.0 --directory /app &

exec sleep infinity
