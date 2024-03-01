FROM python:3.9

EXPOSE 5001/tcp

COPY ./gestor_notificaciones/requirements.txt ./
COPY ./gestor_notificaciones/proyecto1-experimentos-b53d3e709d98.json ./
COPY ./gestor_notificaciones/run_commands.sh ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python",  "./gestor_notificaciones/main.py", "run"]