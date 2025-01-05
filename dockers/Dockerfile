FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Vancouver

RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    python3-setuptools \
    wget \
    unzip \
    mahimahi \
    jq \
    tzdata \
    ffmpeg \
    gocr \
    imagemagick \
    iputils-ping \
    iperf3 \
    net-tools \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3.9 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.9 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip
RUN pip3 install pytest numpy requests soundfile gym protobuf==3.6.1
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu

RUN wget https://github.com/Netflix/vmaf/releases/download/v2.1.0/ubuntu-18.04-vmaf.zip
RUN unzip -o ubuntu-18.04-vmaf.zip && chmod 755 vmaf && mv vmaf /usr/bin && rm ubuntu-18.04-vmaf.zip

WORKDIR /app
COPY alphartc/target/ /app/alphartc/target/
COPY . /app/
RUN useradd -m user && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R user:user /app && chmod -R 755 /app
USER user

CMD [ "/bin/bash" ]
