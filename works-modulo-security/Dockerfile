FROM python:3.8-slim-buster
WORKDIR /python-docker
RUN pip3 install flask pycryptodome
COPY . .
ARG flag
ENV FLAG=$flag
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
