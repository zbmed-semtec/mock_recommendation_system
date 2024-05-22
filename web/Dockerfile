FROM python:3.9.9

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_PORT=5000
EXPOSE ${FLASK_PORT}

COPY download.sh .
RUN chmod +x download.sh
RUN ./download.sh

COPY setup.sh .
RUN chmod +x setup.sh
RUN ./setup.sh

# CMD gunicorn --bind 0.0.0.0:5000 run:app

ENTRYPOINT ["python", "run.py"]