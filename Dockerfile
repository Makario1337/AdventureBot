FROM ghcr.io/linuxserver/baseimage-alpine:3.17
LABEL maintainer="Makario1337"

ENV src=/app


RUN \
	echo "** Installing packages **" && \
	apk add  -U --upgrade --no-cache \
		git \
		python3 \
		py3-pip  &&\
	mkdir -p ${src} && \
	chgrp users ${src} && \
	chmod g+w ${src} && \
    pip install discord 


# Copy local files
COPY root/ /
COPY config.json /app
WORKDIR ${src}