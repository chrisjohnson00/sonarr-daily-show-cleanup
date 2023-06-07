FROM python:3.12.0b2-slim

WORKDIR /usr/src/app
EXPOSE 5000

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
