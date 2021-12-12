FROM python:3.9 as base

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

EXPOSE 5000

COPY todo_app todo_app

ENV FLASK_APP=todo_app/app

FROM base as development

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as production 

ENV FLASK_ENV=production

ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()"]