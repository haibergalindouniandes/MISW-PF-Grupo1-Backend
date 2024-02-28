FROM python:3.10 AS base
LABEL author="s.salazarc@uniandes.edu.co and jf.guzmanc1@uniandes.edu.co"
RUN apt-get update && apt-get install -y
RUN apt-get install telnet -y
RUN pip install --upgrade pip
RUN pip install pipenv

FROM base AS app
RUN groupadd -r appservicios
RUN useradd -r -m -g appservicios appservicios
WORKDIR /home/appservicios/app
COPY ["Pipfile", "Pipfile.lock", "./"]
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
RUN pipenv install --system --deploy
USER appservicios
CMD ["gunicorn", "--bind", ":3000", "main:app"]