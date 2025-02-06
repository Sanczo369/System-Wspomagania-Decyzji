import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
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

    # Model liniowy
    linear_model = LinearRegression()
    linear_model.fit(X, y)

    # Model Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Model SVR
    svr_model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
    svr_model.fit(X, y)

    # Model sieci neuronowej (MLPRegressor)
    nn_model = MLPRegressor(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
    nn_model.fit(X, y)

    # Model Gradient Boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X, y)

    # Prognoza do 2028 roku
    future_years = np.array(range(int(region_data["Year"].max()) + 1, 2029)).reshape(-1, 1)
    future_df = pd.DataFrame(future_years, columns=["Year"])
    linear_predictions = linear_model.predict(future_df)
    rf_predictions = rf_model.predict(future_df)
    svr_predictions = svr_model.predict(future_df)
    nn_predictions = nn_model.predict(future_df)
    gb_predictions = gb_model.predict(future_df)

    plt.figure(figsize=(10, 5))

    # Punkty historyczne
    plt.scatter(X, y, color='blue', label='Dane historyczne', s=50)
    for i, txt in enumerate(y):
        plt.text(X.iloc[i, 0], y.iloc[i], f'{int(txt)}', fontsize=9, ha='right', va='bottom')

    # Prognoza liniowa
    plt.scatter(future_years, linear_predictions, color='red', label='Prognoza liniowa', s=50, marker='x')
    for i, txt in enumerate(linear_predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='red')

    # Prognoza Random Forest
    plt.scatter(future_years, rf_predictions, color='green', label='Prognoza Random Forest', s=50, marker='o')
    for i, txt in enumerate(rf_predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='green')

    # Prognoza SVR
    plt.scatter(future_years, svr_predictions, color='purple', label='Prognoza SVR', s=50, marker='s')
    for i, txt in enumerate(svr_predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='purple')

    # Prognoza sieci neuronowej
    plt.scatter(future_years, nn_predictions, color='orange', label='Prognoza sieci neuronowej', s=50, marker='^')
    for i, txt in enumerate(nn_predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='orange')

    # Prognoza Gradient Boosting
    plt.scatter(future_years, gb_predictions, color='brown', label='Prognoza Gradient Boosting', s=50, marker='d')
    for i, txt in enumerate(gb_predictions):
        plt.text(future_years[i, 0], txt, f'{int(txt)}', fontsize=9, ha='left', va='bottom', color='brown')

    plt.xlabel('Rok')
    plt.ylabel('Liczba przestępstw')
    plt.title(f'Prognoza dla {region_name} ({category}) do 2028 roku')
    plt.legend()
    plt.grid(True)
    plt.show()
    return dict(zip(future_years.flatten(), gb_predictions.flatten()))

# Tworzenie interfejsu użytkownika (Tkinter)
def generate_prediction():
    region_name = region_var.get()
    category = category_var.get()

    if region_name and category:
        predictions = predict_trends(region_name, category)

# Interfejs graficzny
root = tk.Tk()
root.title("System Wsparcia Decyzji")

# Wybór regionu
tk.Label(root, text="Wybierz powiat:").pack()
region_var = tk.StringVar()
region_dropdown = ttk.Combobox(root, textvariable=region_var, width=100)
region_dropdown['values'] = df["Powiat"].unique().tolist()
region_dropdown.pack()

# Wybór kategorii
tk.Label(root, text="Wybierz kategorię:").pack()
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, width=100)
category_dropdown['values'] = kategorie
category_dropdown.pack()

# Przycisk do generowania prognozy
tk.Button(root, text="Generuj prognozę", command=generate_prediction).pack()

root.mainloop()
