FROM python:3.9

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

EXPOSE 5000

COPY todo_app todo_app

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

