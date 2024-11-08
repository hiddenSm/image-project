FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY requirements.txt /app/
# RUN echo "nameserver 10.202.10.202" > /etc/resolv.conf
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "imageproject.wsgi:application"]