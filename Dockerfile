# Base
FROM python as base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH "/root/.poetry/bin:${PATH}"

ADD / /code/
WORKDIR code

# add and install python requirements
RUN poetry install

# Development 
FROM base as development
EXPOSE 5100
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "-p", "5100"]

# Production
FROM base as production
EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()", "--access-logfile", "gunicorn-access.log", "--log-file", "gunicorn.log"]

