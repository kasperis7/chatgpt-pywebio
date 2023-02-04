FROM python:3.10-slim AS base
# Image to Build Dependencies
FROM base AS builder

WORKDIR /app

COPY ./requirements.txt /app

# Build Dependencies

# Python Dependencies
#RUN pip install --no-cache-dir --prefix=/install gunicorn
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime Environment Image
FROM base


WORKDIR /app
COPY --from=builder /install /usr/local
COPY . /app/

EXPOSE 8000
CMD python main.py

