FROM arm64v8/ubuntu:18.04

# Set the locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# base packages
RUN apt-get update && apt-get install -y \
  file \
  patch \
  rsync \
  util-linux \
  wget \
  bzip2 \
  && apt-get autoclean

# ctng packages
RUN apt-get install -y \
    autoconf \
    gperf  \
    bison  \
    flex  \
    texinfo  \
    help2man  \
    gcc  \
    g++   \
    patch \
	ncurses-dev  \
    python-dev  \
    bzip2  \
    git \
  && apt-get autoclean

#crosstool-ng packages
RUN apt-get install -y \
    automake \
    libtool \
    make \
    unzip \
  && apt-get autoclean


COPY ./install_conda.sh /install_conda.sh
COPY ./c4aarch64_installer-1.0.0-Linux-aarch64.sh /c4aarch64_installer-1.0.0-Linux-aarch64.sh 
RUN chmod +x /install_conda.sh
RUN chmod +x /c4aarch64_installer-1.0.0-Linux-aarch64.sh 
RUN apt-get install -y dos2unix
RUN dos2unix /install_conda.sh && dos2unix /c4aarch64_installer-1.0.0-Linux-aarch64.sh
RUN /install_conda.sh

ENV PATH="/opt/conda/bin:${PATH}"