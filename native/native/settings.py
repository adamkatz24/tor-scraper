# settings.py
import os

BOT_NAME = "native"

SPIDER_MODULES = ["native.spiders"]
NEWSPIDER_MODULE = "native.spiders"

# Enable downloader middleware
DOWNLOADER_MIDDLEWARES = {
    "native.middlewares.TorProxyMiddleware": 725,
}

ITEM_PIPELINES = {
    'native.pipelines.DebugPipeline': 100
}

# Disable robots.txt
ROBOTSTXT_OBEY = False

# Add delay between requests
DOWNLOAD_DELAY = 3

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 1

# Disable cookies
COOKIES_ENABLED = False

# Set logging level to DEBUG to see more information
LOG_LEVEL = 'INFO'

# Enable all logging for debugging
LOG_ENABLED = True

# Set Tor password
TOR_CONTROL_PASSWORD = os.getenv("TOR_CONTROL_PASSWORD", "tor_password")

# Backend scraper credentials
BACKEND_SCRAPER_USERNAME = os.getenv("SCRAPER_EMAIL", "")
BACKEND_SCRAPER_PASSWORD = os.getenv("SCRAPER_PASSWORD", "")

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
