import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Wczytanie danych, ignorujemy pierwszy wiersz (bo zawiera nazwy kategorii)
file_path = "dane.csv"
df = pd.read_csv(file_path, sep=';', encoding='utf-8', header=[0])

# Usunięcie zbędnych spacji i formatowanie tekstu
df.columns = df.columns.str.strip()
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Pierwsza kolumna to powiaty
df.rename(columns={df.columns[0]: "Powiat"}, inplace=True)

# Przetwarzanie nagłówków: wyodrębniamy kategorie i lata
category_mapping = {}
for col in df.columns[1:]:  # Pomijamy "Powiat"
    parts = col.split(";")  # Podział: "nazwa kategorii;rok;jednostka"
    if len(parts) >= 2:
        category, year = parts[0].strip(), parts[1].strip()
        category_mapping[col] = (category, year)  # Tworzymy mapowanie

# Lista unikalnych kategorii (dla listy wyboru)
kategorie = sorted(set(cat for cat, _ in category_mapping.values()))

# Funkcja prognozująca dane dla wybranego regionu i kategorii
def predict_trends(region_name, category):
    region_data = df[df["Powiat"] == region_name]
    selected_columns = [col for col, (cat, year) in category_mapping.items() if cat == category]

    region_data = region_data[selected_columns].T
    region_data.columns = ["Value"]
    region_data["Year"] = [category_mapping[col][1] for col in selected_columns]

    region_data["Year"] = region_data["Year"].astype(float)
    region_data["Value"] = region_data["Value"].astype(str).str.replace(',', '.').astype(float)

    X = region_data[["Year"]]
    y = region_data["Value"]

    model = LinearRegression()
    model.fit(X, y)

    # Prognoza do 2028 roku
    future_years = np.array(range(int(region_data["Year"].max()) + 1, 2029)).reshape(-1, 1)
    future_df = pd.DataFrame(future_years, columns=["Year"])
    predictions = model.predict(future_df)

    plt.figure(figsize=(10, 5))

    # Punkty historyczne
    plt.scatter(X, y, color='blue', label='Dane historyczne', s=50)
    for i, txt in enumerate(y):
        plt.text(X.iloc[i, 0], y.iloc[i], f'{int(txt)}', fontsize=9, ha='right', va='bottom')

    # Prognoza
    plt.scatter(future_years, predictions, color='red', label='Prognoza', s=50, marker='x')
    for i, txt in enumerate(predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='red')

    plt.xlabel('Rok')
    plt.ylabel('Liczba przestępstw')
    plt.title(f'Prognoza dla {region_name} ({category}) do 2028 roku')
    plt.legend()
    plt.grid(True)
    plt.show()
    return dict(zip(future_years.flatten(), predictions))

# Tworzenie interfejsu użytkownika (Tkinter)
def generate_prediction():
    region_name = region_var.get()
    category = category_var.get()

    if region_name and category:
        predictions = predict_trends(region_name, category)