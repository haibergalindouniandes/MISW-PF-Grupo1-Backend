FROM python:3.10 AS base
RUN apt-get update && apt-get install -y
RUN apt-get install telnet -y
RUN pip install --upgrade pip
RUN pip install pipenv

FROM base AS app
RUN groupadd -r appentrenamientos
RUN useradd -r -m -g appentrenamientos appentrenamientos
WORKDIR /home/appentrenamientos/app
COPY ["Pipfile", "Pipfile.lock","proyecto1-experimentos-a4f693fafcec.json", "./"]
COPY src/. /home/appentrenamientos/app

FROM app AS release
EXPOSE 3000

FROM release AS dev
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
RUN pipenv install  --system --deploy --dev
USER appentrenamientos
CMD ["python", "main.py"]

FROM release AS prod
ENV GOOGLE_APPLICATION_CREDENTIALS=proyecto1-experimentos-a4f693fafcec.json
RUN pipenv install --system --deploy
USER appentrenamientos
CMD ["gunicorn", "--bind", ":3000", "main:app"]

FROM app AS cloudrelease
EXPOSE 80

FROM cloudrelease AS cloudprod
ENV PYTHONBUFFERED=1
ENV FLASK_DEBUG=1
ENV DB_HOST=34.136.51.44
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=postgres
ENV DB_PORT=5432
ENV GOOGLE_APPLICATION_CREDENTIALS=proyecto1-experimentos-a4f693fafcec.json
ENV ROL_PERMITIDO=USUARIO
ENV GESTORUSUARIOS_ADDRESS=https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/me
RUN pipenv install --system --deploy
USER appentrenamientos
CMD ["gunicorn", "--bind", ":80", "main:app"]