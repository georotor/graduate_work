FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install --no-install-recommends -y \
     curl \
     \
     && pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt \
     \
     && apt autoremove -y \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

COPY ./ /opt/app/

RUN groupadd -r rasa && useradd -d /opt/app -r -g rasa rasa \
     && chown rasa:rasa -R /opt/app

USER rasa

ENTRYPOINT ["rasa", "run", "--enable-api", "-m", "models/nlu.tar.gz"]
