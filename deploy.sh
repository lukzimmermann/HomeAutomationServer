docker build -t lukzimmermann/homeserver:latest . --push

docker run -e HUE_BRIDGE_IP=192.168.1.50 -e HUE_BRIDGE_USER=MBsQGZZD3uGFcqXTglvz81wszWNJKaPqGPnp4ndr --name HomeServer -d -p 8000:8000 lukzimmermann/homeserver:latest