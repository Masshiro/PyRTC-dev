FROM ubuntu:20.04

ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Vancouver

# Install dependencies
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "$TZ" > /etc/timezone && \
    apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-venv \
    git \
    curl \
    iputils-ping \
    lsb-release \
    wget \
    build-essential \
    ninja-build \
    cmake \
    unzip \
    clang \
    gnupg \
    pkg-config \
    libgtk-3-dev \
    libnss3-dev \
    libgconf-2-4 \
    libasound2-dev \
    libpulse-dev \
    libxcomposite-dev \
    libxrandr-dev \
    libxi-dev \
    libxcursor-dev \
    libxtst-dev \
    libxdamage-dev \
    libpci-dev \
    libudev-dev \
    mahimahi \
    jq \
    tzdata \
    ffmpeg \
    gocr \
    imagemagick \
    iputils-ping \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git /opt/depot_tools
RUN git config --global --add safe.directory /opt/depot_tools
RUN ln -s /usr/bin/python3 /usr/bin/python
ENV PATH="/opt/depot_tools:${PATH}"
RUN pip3 install gym torch protobuf==3.6.1

# Create a user with no password and sudo privileges
RUN useradd -m user && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install libraries and tools required by evaluation module
RUN pip3 install pytest numpy requests soundfile
RUN wget https://github.com/Netflix/vmaf/releases/download/v2.1.0/ubuntu-18.04-vmaf.zip
RUN unzip -o ubuntu-18.04-vmaf.zip && chmod 774 vmaf && mv vmaf /usr/bin && rm ubuntu-18.04-vmaf.zip

# Copy the whole project into container
WORKDIR /app
COPY . /app

# # Build AlphaRTC
RUN cd alphartc && \
    gclient sync && \
    cp -r src/* . && \
    rm -rf src && \
    gn gen out/Default && \
    ninja -C out/Default peerconnection_serverless
# RUN chown -R user:user /app
# USER user
# RUN chmod +x build.sh && ./build.sh
# RUN bash -c '. ./build.sh'

USER user


CMD [ "/bin/bash" ]
