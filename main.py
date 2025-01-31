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