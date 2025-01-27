# NYC Yellow Taxi Prediction - Flask & Streamlit Application

## **Description**
Ce projet permet de prédire le nombre de passagers pour les trajets des taxis jaunes à New York City. Il combine **PySpark** pour la gestion des données et la modélisation, **Flask** pour fournir une API REST, et **Streamlit** pour une interface utilisateur interactive.

## **Étapes principales**

### **1. Préparation des données**
- Les données météo et les trajets de taxi ont été récupérés via l'API NOAA et le dataset NYC Taxi.
- Les colonnes importantes (heure, jour ouvré, météo, température moyenne, catégorie de distance) ont été extraites et utilisées pour entraîner un modèle de régression.

### **2. Entraînement du modèle**
- Un modèle **Random Forest Regression** a été entraîné à l'aide de **PySpark**.
- Le modèle prédit le nombre de passagers en fonction des caractéristiques des trajets.

### **3. Sauvegarde du modèle**
- Le modèle a été sauvegardé au format MLlib avec la commande :
  ```python
  model.save("random_forest_model")

### **4. Création de l'API avec Flask**
Une API REST a été développée pour exposer le modèle entraîné. L'endpoint `/predict` accepte une requête POST avec les caractéristiques d'un trajet et retourne une prédiction.

### **5. Développement de l'interface utilisateur avec Streamlit**
Une interface Streamlit interactive permet à l'utilisateur de :
- Sélectionner un point de prise en charge sur une carte.
- Configurer les caractéristiques du trajet (heure, météo, etc.).
- Obtenir une prédiction du nombre de passagers.

### **6. Conteneurisation avec Docker**
Le projet a été conteneurisé pour garantir une compatibilité et une portabilité maximales.
- Flask et Streamlit peuvent être exécutés à partir du conteneur selon les besoins.

### **7. Arborescence du projet**
```bash
project/
├── random_forest_model/       # Modèle entraîné au format MLlib
├── app.py                     # API Flask
├── streamlit_app.py           # Application Streamlit
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Configuration Docker
└── README.md                  # Documentation du projet
```
### **8. Exécuter avec Docker**

#### **Construire l'image Docker :**

```bash
docker build -t nyc-taxi-app .
```

#### **Exécuter Flask :**

```bash
docker run -p 5000:5000 nyc-taxi-app
```

### **Tester l'API avec Postman**

Testez l'API en utilisant Postman ou un outil similaire, en définissant la méthode comme **POST**.

#### **Exemple de requête POST avec Postman :**

- **Méthode** : POST  
- **URL** : `http://localhost:5000/predict`  
- **Corps de la requête (JSON)** :  
  ```json
  {
      "features": {
          "hour": 10,
          "is_business_day": 1,
          "weather_index": 2,
          "temp_avg": 15.5,
          "distance_category_index": 3
      }
  }
```

#### **Exécuter Streamlit :**

```bash
docker run -p 8501:8501 nyc-taxi-app streamlit run /app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
