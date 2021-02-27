FROM python
ADD / /code/
WORKDIR code
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH "/root/.poetry/bin:${PATH}"

# add and install python requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()", "--log-level", "debug", "--access-logfile", "gunicorn-access.log", "--log-file", "gunicorn.log"]

