FROM debian:bookworm-slim AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY server.sh /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=30M 
