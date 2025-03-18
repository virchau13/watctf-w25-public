FROM python:3.12-slim-bookworm AS app
RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    curl git strace

RUN git clone https://codeberg.org/ngn/k
WORKDIR /k
RUN make
WORKDIR /

FROM pwn.red/jail
COPY --from=app / /srv
RUN mkdir -p /srv/app/
COPY prob/chall.k /srv/app/chall.k
COPY prob/run.py /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=30M JAIL_TMP_SIZE=16384
