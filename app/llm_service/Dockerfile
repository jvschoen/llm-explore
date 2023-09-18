FROM python:3.9.17-slim
WORKDIR /app
# Separated to avoid copying big model every time
COPY model/ /model

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/. .

# installs lamma package for inference
RUN pip install -e /model

CMD ["torchrun", "--nproc_per_node", "1", "llm_service.py"]