FROM alpine:3.14
RUN apk add --update clang nodejs npm openssh gcc linux-headers musl-dev \
    && mkdir -p /build
COPY main.c /build
WORKDIR /build
RUN gcc -static -Wall -Wpedantic -Wextra main.c -o main
# give hexed empty password
RUN ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -t ed25519 -N ""
RUN adduser -s /build/main -D hexed
RUN passwd -d hexed
COPY flag.txt /secret.txt
COPY index.html /build
CMD npx http-server \
    & /usr/sbin/sshd -D -e -o PermitEmptyPasswords=yes -o PermitRootLogin=no \
        -o HostKey=/etc/ssh/ssh_host_ed25519_key -o PrintMotd=no -o PrintLastLog=no
