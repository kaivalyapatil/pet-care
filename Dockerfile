FROM python:3.10

ENV POETRY_VERSION=1.1.13
ENV AWS_REGION="ap-south-1"
ENV AWS_ACCESS_KEY_ID="AKIATN5QJDAHMAA3BUUP"
ENV AWS_SECRET_ACCESS_KEY="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"

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./ ./

# Project initialization: disable virtual env and install prod dependencies 
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 5000

# Run the app instance from 'main' file using WSGI server Gunicorn
CMD ["gunicorn"  , "--bind", "0.0.0.0:5000", "--workers","1", "--reload","main:app"]