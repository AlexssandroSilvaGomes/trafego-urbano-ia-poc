import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Suponha que você tenha um DataFrame `data` com as colunas necessárias
data = pd.read_csv('dados_trafego.csv')  # Substitua pelo seu arquivo

# Dividir dados em características e rótulo
X = data[['origem', 'destino', 'hora', 'dia_da_semana']]
y = data['tempo_viagem']

# Codificação de variáveis categóricas se necessário
X = pd.get_dummies(X)

# Dividir em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Avaliar o modelo
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')
