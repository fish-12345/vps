FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl python3 ca-certificates && \
    curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null && \
    curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | tee /etc/apt/sources.list.d/tailscale.list && \
    apt-get update && \
    apt-get install -y tailscale && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

COPY start.sh /start.sh
COPY dashboard.html /app/index.html
RUN chmod +x /start.sh
CMD ["/start.sh"]
