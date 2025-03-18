FROM python:3.12-slim-bookworm AS app
RUN pip install --no-cache-dir cryptography

FROM pwn.red/jail
COPY --from=app / /srv
COPY communicate.py /srv/app/run
COPY secret.py /srv/app/secret.py
COPY convo.txt /srv/app/convo.txt
RUN chmod 755 /srv/app/run

ARG user

ENV JAIL_MEM=30M JAIL_ENV_USER=$user
