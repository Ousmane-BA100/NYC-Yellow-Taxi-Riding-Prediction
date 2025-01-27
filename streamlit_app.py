import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressionModel
import folium
from streamlit_folium import st_folium

# Charger SparkSession
spark = SparkSession.builder.appName("Taxi Prediction").getOrCreate()

# Charger le modèle entraîné
model_path = "./random_forest_model"
model = RandomForestRegressionModel.load(model_path)

# Configuration de l'interface Streamlit
st.title("NYC Yellow Taxi Riding Prediction")
st.markdown("### Prédiction du nombre de passagers pour les trajets de taxi à NYC.")

# Carte interactive pour sélectionner un emplacement
st.header("Choose a Pick-Up Place")
m = folium.Map(location=[40.730610, -73.935242], zoom_start=12)  # NYC par défaut
folium.Marker([40.730610, -73.935242], popup="Pick-Up Point").add_to(m)
output = st_folium(m, width=700, height=500)

# Entrées utilisateur : caractéristiques
st.subheader("Paramètres d'entrée")
hour = st.slider("Heure (0-23)", min_value=0, max_value=23, value=12, step=1)
is_business_day = st.selectbox("Jour ouvré ?", [1, 0], help="1 pour oui, 0 pour non")
weather_index = st.selectbox("Conditions météo", [0, 1], format_func=lambda x: "Clear" if x == 0 else "Rainy")
temp_avg = st.slider("Température moyenne (°C)", min_value=-10, max_value=40, value=20)
distance_category_index = st.selectbox("Catégorie de distance", [0, 1], format_func=lambda x: "Short" if x == 0 else "Long")

# Bouton pour prédire
if st.button("Prédire le nombre de passagers"):
    # Préparer les données d'entrée
    input_data = pd.DataFrame({
        "hour": [hour],
        "is_business_day": [is_business_day],
        "weather_index": [weather_index],
        "temp_avg": [temp_avg],
        "distance_category_index": [distance_category_index]
    })

    # Convertir en DataFrame Spark
    spark_df = spark.createDataFrame(input_data)

    # Vectoriser les colonnes
    assembler = VectorAssembler(
        inputCols=["hour", "is_business_day", "weather_index", "temp_avg", "distance_category_index"],
        outputCol="features"
    )
    spark_df = assembler.transform(spark_df)

    # Faire la prédiction
    prediction = model.transform(spark_df).select("prediction").collect()[0][0]

    # Afficher les résultats
    st.success(f"Nombre prédit de passagers : {round(prediction, 2)}")
