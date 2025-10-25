#!/bin/bash

# Step 1: Check if TOR_CONTROL_PASSWORD is set
if [ -z "$TOR_CONTROL_PASSWORD" ]; then
  echo "Error: TOR_CONTROL_PASSWORD environment variable is not set."
  exit 1
fi

# Step 2: Configure Tor
cat > /etc/tor/torrc << EOL
ControlPort 9051
HashedControlPassword $(tor --quiet --hash-password "${TOR_CONTROL_PASSWORD}")
CookieAuthentication 1
DataDirectory /var/lib/tor
CircuitBuildTimeout 10
KeepalivePeriod 60
NewCircuitPeriod 15
NumEntryGuards 8
EOL

# Stop any running instances first
pkill -f tor || true
pkill -f privoxy || true
pkill -f scrapyd || true
pkill -f twistd || true

# Start Tor and Privoxy
/etc/init.d/tor start
/etc/init.d/privoxy start

echo "Tor & Privoxy configuration has been updated."

# Create a proper PID directory with permissions
mkdir -p /var/run/scrapyd
chmod 777 /var/run/scrapyd

scrapyd --pidfile=/var/run/scrapyd/scrapyd.pid &

echo "Waiting for Scrapyd to start..."
until curl -s http://localhost:6800/ > /dev/null; do
  sleep 1
done

echo "Scrapyd is up!"

# Start ScrapydWeb
echo "Starting ScrapydWeb..."
echo "DEBUG: ScrapydWeb config location:"
ls -la /app/scrapydweb_settings_v11.py
scrapydweb

tail /dev/null