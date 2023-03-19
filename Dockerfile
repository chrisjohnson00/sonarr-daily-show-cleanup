FROM python:3.11.2-slim

WORKDIR /usr/src/app
EXPOSE 5000

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
