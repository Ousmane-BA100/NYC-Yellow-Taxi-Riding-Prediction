# Base image : Python avec JDK
FROM openjdk:8-jdk-slim

# Installer Python et pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copier les fichiers de l'application dans le conteneur
COPY app.py /app/app.py
COPY streamlit_app.py /app/streamlit_app.py
COPY random_forest_model /app/random_forest_model

# Définir le répertoire de travail
WORKDIR /app

# Exposer les ports pour Flask et Streamlit
EXPOSE 5000 8501

# Commande pour démarrer Flask (par défaut)
#CMD ["python3", "app.py"]

# Si vous souhaitez exécuter Streamlit à la place, commentez la ligne ci-dessus et utilisez celle-ci :
CMD ["streamlit", "run", "/app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
