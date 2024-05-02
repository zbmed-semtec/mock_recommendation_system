FROM python:3.9.9

WORKDIR src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_PORT=5001
EXPOSE ${FLASK_PORT}

COPY . .


ENTRYPOINT ["python", "run.py"]

# CMD ["nginx", "-g", "daemon off;"]
