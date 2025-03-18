FROM python:3.11-slim-buster
WORKDIR /python-docker
COPY prob/requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install pycryptodome
COPY prob/ .
ARG flag
ENV FLAG=$flag
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
