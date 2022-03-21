FROM python:3.10-bullseye
LABEL maintainer="Erick Duarte <erickod@gmail.com>"
WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY settings.toml settings.toml
COPY main.py main.py 
COPY template_system template_system

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN echo "PATH=/root/.poetry/bin/:$PATH" >> ~/.bashrc
RUN /bin/bash -c  "source $HOME/.poetry/env"
RUN /bin/bash -c "source ~/.bashrc"
RUN ~/.poetry/bin/poetry install --no-dev
RUN apt-get update
RUN apt-get install libreoffice-core libreoffice-writer libreoffice-calc libreoffice-draw libreoffice-java-common default-jre -y

EXPOSE 8000/tcp
ENTRYPOINT ["/root/.poetry/bin/poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8100"]