FROM alpine:3.16.0

COPY . /app

WORKDIR /app

ARG BUSPASS
ARG BUSUSER
ARG BUSHOST
ARG BUSPORT

ENV BUSPASS=$BUSPASS
ENV BUSUSER=$BUSUSER
ENV BUSHOST=$BUSHOST
ENV BUSPORT=$BUSPORT

RUN apk add --update --no-cache openssh
RUN apk add --update --no-cache lftp
RUN apk add --update --no-cache sshpass

EXPOSE 5000

CMD ["sh", "ensena.sh"]
