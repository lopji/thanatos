# Start with CUDA Theano base image
FROM nakosung/dockerfiles-1
MAINTAINER Kai Arulkumaran <design@kaixhin.com>

#update & upgrade last packets
RUN apt-get -y update 
RUN apt-get -y upgrade 
RUN apt-get install nvidia-375=375.65-0ubuntu0.16.04.1

# Install bleeding-edge Lasagne
RUN pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip

# Install sockets
RUN pip install SocketIO_client

RUN echo "[global]\ndevice=gpu\nfloatX=float32\noptimizer_including=cudnn\n[lib]\ncnmem=0.1\n[nvcc]\nfastmath=True\nopenmp=True" > /root/.theanorc

RUN echo "* * * * * root pgrep -f "client" | while read PID; do echo -17 > /proc/\$PID/oom_adj; done" > /etc/cron.d/oom_disable
RUN chmod 0644 /etc/cron.d/oom_disable

COPY client.py /tmp/client.py
CMD cron && python /tmp/client.py