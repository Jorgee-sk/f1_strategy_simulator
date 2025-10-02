FROM python:3.13-slim

# Evitar que Python genere .pyc y forzar stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /f1_sim

# Copiar dependencias primero (mejora cacheo en builds)
COPY requirements.txt /f1_sim/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /f1_sim/

# Comando por defecto: correr tests
CMD ["pytest"]