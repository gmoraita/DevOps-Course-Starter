# Base
FROM python as base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /code

ENV PATH "/code:/root:/root/.poetry/bin:${PATH}"

# add and install python requirements
COPY pyproject.toml poetry.lock /code/
RUN poetry install

# Copy the rest of the code
COPY / /code/

# Development 
FROM base as development
EXPOSE 5100
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "-p", "5100"]

# Production
FROM base as production
EXPOSE 5000
CMD poetry run gunicorn -b 0.0.0.0:$PORT 'todo_app.app:create_app()' --access-logfile gunicorn-access.log --log-file gunicorn.log

# Testing - Offline
FROM base as testing-offline
CMD ["poetry", "run", "pytest", "todo_app/tests"]


# Testing - Online
FROM base as testing-online

RUN wget -c https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz -O - |tar xz 
RUN apt-get update
RUN apt -y install firefox-esr
ENV PATH "/root:${PATH}"

CMD ["poetry", "run", "pytest", "todo_app/tests_e2e"]
