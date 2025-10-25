@echo off
echo Stopping container...
docker stop scraper

echo Removing container...
docker rm scraper

echo scraper stopped and removed.
