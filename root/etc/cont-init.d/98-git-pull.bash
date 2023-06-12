#!/usr/bin/with-contenv bash

echo "Pulling GitHub Repo"
git clone https://github.com/Makario1337/AdventureBot.git /tmp 
mv /tmp/src/* /app
echo "Finished pulling..."
exit