FROM debian:bookworm-slim AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY vuln /srv/app/run

ARG flag
RUN echo "$flag" > /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=30M 
