FROM neuml/txtai-cpu:6.2.0 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM neuml/txtai-cpu:6.2.0

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./logging.yml /code/logging.yml

EXPOSE 8080

LABEL org.opencontainers.image.vendor="AI RnD Lab"

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--log-config=logging.yml"]
