FROM python:3.12-alpine

WORKDIR /code

RUN pip install poetry --no-cache-dir

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-dev --no-interaction --no-ansi --no-cache

COPY . .

RUN chmod a+x *.sh

#EXPOSE 8000
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]