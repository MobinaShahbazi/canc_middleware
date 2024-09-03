FROM --platform=linux/amd64 pdr.hexatech.ir/python:3.10-slim

WORKDIR /middleware

COPY ./requirements.txt /middleware/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /middleware/requirements.txt

COPY ./app /middleware/app
COPY ./envs /middleware/envs

EXPOSE 42420

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "42420"]
