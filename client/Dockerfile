# Start with CUDA base image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

# Install git, wget, python-dev, pip, BLAS + LAPACK and other dependencies
RUN apt-get update && apt-get install -y \
  gfortran \
  git \
  wget \
  liblapack-dev \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin

# Install bleeding-edge Theano
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
RUN pip install --upgrade six

#update & upgrade last packets
RUN apt-get -y update 
RUN apt-get -y upgrade 

# Install bleeding-edge Lasagne
RUN pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip

# Install sockets
RUN pip install SocketIO_client

RUN echo "[global]\ndevice=gpu\nfloatX=float32\noptimizer_including=cudnn\n[lib]\ncnmem=0.1\n[nvcc]\nfastmath=True\nopenmp=True" > /root/.theanorc

RUN echo "* * * * * root pgrep -f "client" | while read PID; do echo -17 > /proc/\$PID/oom_adj; done" > /etc/cron.d/oom_disable
RUN chmod 0644 /etc/cron.d/oom_disable

COPY client.py /tmp/client.py
CMD cron && python /tmp/client.py