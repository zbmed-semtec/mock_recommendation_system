FROM python:3.9.9

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
EXPOSE 5000

COPY download.sh .
RUN chmod +x download.sh
RUN ./download.sh

COPY setup.sh .
RUN chmod +x setup.sh
RUN ./setup.sh

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]