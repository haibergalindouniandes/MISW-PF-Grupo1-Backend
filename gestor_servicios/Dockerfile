FROM python:3.10 AS base
RUN apt-get update && apt-get install -y
RUN apt-get install telnet -y
RUN pip install --upgrade pip
RUN pip install pipenv

FROM base AS app
RUN groupadd -r appservicios
RUN useradd -r -m -g appservicios appservicios
WORKDIR /home/appservicios/app
COPY ["Pipfile", "Pipfile.lock","proyecto1-experimentos-a4f693fafcec.json", "./"]
COPY src/. /home/appservicios/app

FROM app AS release
EXPOSE 3000

FROM release AS dev
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
RUN pipenv install --system --deploy --dev
USER appservicios
CMD ["python", "main.py"]

FROM release AS prod
ENV PYTHONBUFFERED=1
ENV FLASK_DEBUG=1
ENV GOOGLE_APPLICATION_CREDENTIALS=proyecto1-experimentos-a4f693fafcec.json
RUN pipenv install --system --deploy
USER appservicios
CMD ["gunicorn", "--bind", ":3000", "main:app"]