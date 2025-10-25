@echo off
echo Building Docker image...
docker build -t scraper .

echo Starting container...
docker run --name scraper --env-file .env -p 5000:5000 -p 6800:6800 -d scraper

echo scraper is now running on ports 5000 and 6800
