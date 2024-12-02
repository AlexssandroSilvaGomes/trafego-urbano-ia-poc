import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Carregar o DataFrame
data = pd.read_csv('dados_trafego.csv')  # Substitua pelo seu arquivo

# Dividir dados em características e rótulo
X = data[['origem', 'destino', 'hora', 'dia_da_semana']]
y = data['tempo_viagem']

# Codificação de variáveis categóricas
X = pd.get_dummies(X)

# Dividir em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ajuste de hiperparâmetros usando Grid Search
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}

grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Usar o melhor modelo encontrado
best_model = grid_search.best_estimator_

# Avaliar o modelo com validação cruzada
cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='neg_mean_squared_error')
mean_cv_mse = -cv_scores.mean()  # Mudar o sinal para obter o MSE positivo

# Treinar o modelo com os melhores parâmetros
best_model.fit(X_train, y_train)

# Fazer previsões
predictions = best_model.predict(X_test)

# Calcular e exibir o MSE
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error (Test Set): {round(mse)}')
print(f'Mean Squared Error (Cross Validation): {round(mean_cv_mse)}')
