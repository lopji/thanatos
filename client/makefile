hostname = default
main: build run
build: Dockerfile
	sudo docker build -t thanatos .
run:
	sudo docker run --privileged -h $(hostname) -ti thanatos 
gpu:
	sudo docker run --privileged -h $(hostname) -ti --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidia1:/dev/nvidia1 --device /dev/nvidia2:/dev/nvidia2 --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm thanatos /bin/bash
clean:
	./clean.sh
