import pandas as pd
import random

# Configurações para os dados
origens = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Salvador']
destinos = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Salvador']
dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
horas = list(range(0, 24))

# Criar lista de dados
data = []
for _ in range(10000):  # Gera 1000 entradas
    origem = random.choice(origens)
    destino = random.choice(destinos)
    hora = random.choice(horas)
    dia_da_semana = random.choice(dias_da_semana)
    tempo_viagem = random.randint(30, 120)  # Tempo de viagem em minutos
    data.append([origem, destino, hora, dia_da_semana, tempo_viagem])

# Criar DataFrame e salvar como CSV
df = pd.DataFrame(data, columns=['origem', 'destino', 'hora', 'dia_da_semana', 'tempo_viagem'])
df.to_csv('dados_trafego.csv', index=False)

print("Arquivo 'dados_trafego.csv' criado com sucesso!")
