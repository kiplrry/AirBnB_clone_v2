#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

if ! command -v nginx > /dev/null; then
    sudo apt update
    sudo apt-get install -y nginx
fi

mkdir -p /data/web_static/shared/ /data/web_static/releases/test/
html="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo "$html" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test  /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

# replace="\tserver_name localhost;\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}"

sed -i '0,/server_name ;/s//server_name _;\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}/'  /etc/nginx/sites-enabled/default

sudo service nginx restart
