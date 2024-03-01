# FROM python:3.10 AS base
# LABEL author="s.salazarc@uniandes.edu.co and jf.guzmanc1@uniandes.edu.co"
# RUN apt-get update && apt-get install -y
# RUN apt-get install telnet -y
# RUN pip install --upgrade pip
# RUN pip install pipenv

# FROM base AS app
# RUN groupadd -r appentrenamientos
# RUN useradd -r -m -g appentrenamientos appentrenamientos
# WORKDIR /home/appentrenamientos/app
# COPY ["Pipfile", "Pipfile.lock", "./"]
# COPY gestor_entrenamientos/src/. /home/appentrenamientos/app

# FROM app AS release
# EXPOSE 3000

# FROM release AS dev
# ENV FLASK_ENV=development
# ENV FLASK_DEBUG=1
# RUN pipenv install  --system --deploy --dev
# USER appentrenamientos
# CMD ["python", "main.py"]

# FROM release AS prod
# RUN pipenv install --system --deploy
# USER appentrenamientos
# CMD ["python","main.py"]
# #CMD ["gunicorn"  , "-b", "0.0.0.0:  3000", "app:app"]


FROM python:3.9

EXPOSE 5000/tcp

COPY ./gestor_entrenamientos/requirements.txt ./
COPY ./gestor_entrenamientos/proyecto1-experimentos-a4f693fafcec.json ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "--app", "./gestor_entrenamientos/src/main.py", "run", "--host=0.0.0.0"]