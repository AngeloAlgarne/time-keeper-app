FROM  python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY . /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "/backend/entrypoint.sh" ]