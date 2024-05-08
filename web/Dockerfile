FROM python:3.9.9

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py

COPY setup.sh .
RUN chmod +x setup.sh
RUN ./setup.sh

ENTRYPOINT ["python", "run.py"]