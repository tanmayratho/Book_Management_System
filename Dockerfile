FROM python:3.9-slim

WORKDIR /app
COPY BMS/Book_Management_system/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY BMS/Book_Management_system .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["python", "run.py"]