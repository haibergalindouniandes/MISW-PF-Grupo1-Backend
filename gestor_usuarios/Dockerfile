FROM python:3.10 AS base
LABEL author="h.galindos@uniandes.edu.co and jm.carillo@uniandes.edu.co"
LABEL app="gestor usuarios"
RUN apt-get update && apt-get install -y
RUN apt-get install telnet -y
RUN pip install --upgrade pip
RUN pip install pipenv

FROM base AS app
RUN groupadd -r appusuarios
RUN useradd -r -m -g appusuarios appusuarios
WORKDIR /home/appusuarios/app
COPY ["Pipfile", "Pipfile.lock", "./"]
COPY src/. /home/appusuarios/app

FROM app AS release
EXPOSE 3000

FROM release AS dev
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
RUN pipenv install --system --deploy --dev
USER appusuarios
CMD ["python", "main.py"]

FROM release AS prod
ENV PYTHONBUFFERED=1
ENV FLASK_DEBUG=1
RUN pipenv install --system --deploy
USER appusuarios
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
ENV JWT_SECRET_KEY=JwBGj2B4XFAKhYmn8Pgk0vH2w7UvgYfXAJ32e5rs8vI=
RUN pipenv install --system --deploy
USER appusuarios
CMD ["gunicorn", "--bind", ":80", "main:app"]