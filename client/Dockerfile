# Start with CUDA 
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin
ENV DEBIAN_FRONTEND noninteractive

# Update & upgrade last packets
RUN apt-get -y update 
RUN apt-get -y upgrade 

# Install python
Run apt-get -y install python-pip

# Install git
Run apt-get -y install git

# Install Theano & Lasagne
RUN pip install -r https://raw.githubusercontent.com/Lasagne/Lasagne/v0.1/requirements.txt
RUN pip install lasagne

# Install sockets
RUN pip install SocketIO_client

# Config theano
RUN echo "[global]\ndevice=gpu\nfloatX=float32\noptimizer_including=cudnn\n[lib]\ncnmem=0.1\n[nvcc]\nfastmath=True\nopenmp=True" > /root/.theanorc

# Install nvidia-driver
RUN apt-get -y install nvidia-375

# Install & Config cron
RUN apt-get -y install cron
RUN echo "* * * * * root pgrep -f "client" | while read PID; do echo -17 > /proc/\$PID/oom_adj; done" > /etc/cron.d/oom_disable
RUN chmod 0644 /etc/cron.d/oom_disable

# Add the client script
COPY client.py /tmp/client.py
CMD cron && python /tmp/client.py