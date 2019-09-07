# ref. http://sanshonoki.hatenablog.com/entry/2018/10/09/231345
FROM ubuntu:18.04
RUN apt update \
    && apt install -y \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    wget \
    git \
    mecab \
    curl \
    libmecab-dev \
    mecab-ipadic-utf8\
    language-pack-ja \
    xz-utils \
    file \
    openssl \
    gawk \
    sudo \
    unzip \
    && apt clean \
    && update-locale LANG=ja_JP.UTF-8

# Set locale
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8

# Install Python3.7
WORKDIR /usr/local/src
RUN wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz \
  && tar -xf Python-3.7.3.tar.xz \
  && cd Python-3.7.3 \
  && ./configure --enable-optimization \
  && make \
  && make altinstall

# Install mecab-ipadic-NEologd
WORKDIR /opt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /opt/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y
RUN cd /opt
RUN rm -rf mecab-ipadic-neologd

# Set mecab-ipadic-NEologd as default
RUN sed -i 's/dicdir = \/var\/lib\/mecab\/dic\/debian/dicdir = \/usr\/lib\/x86_64-linux-gnu\/mecab\/dic\/mecab-ipadic-neologd/' /etc/mecabrc

# Install fonts
RUN wget -O IPAfont00303.zip https://ipafont.ipa.go.jp/old/ipafont/IPAfont00303.php \
  && unzip IPAfont00303.zip \
  && mv IPAfont00303 fonts \
  && rm IPAfont00303.zip

# Install Python packages
WORKDIR /home
RUN mkdir code
RUN mkdir output
WORKDIR /home/code
COPY code .

CMD python3.7 -V
