ARG python_version=3.9.17
FROM python:${python_version}-slim

RUN apt-get update \
    && apt-get install -y \
    gcc \
    python3-dev

ARG entry_workdir=/app
WORKDIR /app

COPY /app .

# After storing personal token locally, passing on to container
COPY secrets/.huggingface-token /root/.cache/huggingface/token

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR ${entry_workdir}

EXPOSE 8888