FROM debian:bookworm-slim AS app
RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    curl

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN mkdir -p /tmp
COPY prob/ /tmp/build/
WORKDIR /tmp/build
RUN PATH="$HOME/.cargo/bin:$PATH" $HOME/.cargo/bin/cargo build --release
RUN cp ./target/release/precise-equality /
WORKDIR /

FROM pwn.red/jail
COPY --from=app / /srv
RUN mkdir -p /srv/app/
RUN mv /srv/precise-equality /srv/app/precise-equality
COPY run.sh /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=30M
