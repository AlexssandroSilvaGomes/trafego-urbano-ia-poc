import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium
import random
import pandas as pd

# Baixar o grafo de ruas de São Paulo
cidade = 'São Paulo, Brazil'
G = ox.graph_from_place(cidade, network_type='all')  # 'all' pega todas as ruas, incluindo pedestres

# Converter o grafo em um DataFrame de ruas
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

# Gerar um congestionamento aleatório para cada rua (0% a 100%)
edges['congestionamento'] = [random.randint(0, 100) for _ in range(len(edges))]

# Função para converter endereço em coordenadas
def endereco_para_coordenada(endereco):
    geolocator = Nominatim(user_agent="sistema_trafego")
    location = geolocator.geocode(endereco)
    
    # Exibir resposta de geocodificação para depuração
    print(f"Resultado da geocodificação para '{endereco}':", location)
    
    if location:
        return location.latitude, location.longitude
    else:
        print(f"Endereço '{endereco}' não encontrado.")
        return None, None

# Função para calcular a melhor rota considerando o congestionamento
def melhor_rota(G, origem, destino):
    if origem is None or destino is None:
        print("Erro: Não foi possível obter as coordenadas de origem ou destino.")
        return []
    
    # Verificar se as coordenadas são válidas antes de passar para nearest_nodes
    if not (isinstance(origem, tuple) and len(origem) == 2 and None not in origem):
        print(f"Erro: Coordenadas de origem inválidas: {origem}")
        return []
    
    if not (isinstance(destino, tuple) and len(destino) == 2 and None not in destino):
        print(f"Erro: Coordenadas de destino inválidas: {destino}")
        return []
    
    # Encontrar os nós mais próximos à origem e destino no grafo
    origem_node = ox.distance.nearest_nodes(G, X=origem[1], Y=origem[0])  # longitude, latitude
    destino_node = ox.distance.nearest_nodes(G, X=destino[1], Y=destino[0])
    
    # Verificar se conseguimos encontrar os nós
    if origem_node is None or destino_node is None:
        print("Erro: Não foi possível encontrar os nós mais próximos no grafo.")
        return []

    print(f"Nós de origem encontrados: {origem_node} com coordenadas {G.nodes[origem_node]['y']}, {G.nodes[origem_node]['x']}")
    print(f"Nós de destino encontrados: {destino_node} com coordenadas {G.nodes[destino_node]['y']}, {G.nodes[destino_node]['x']}")
    
    # Usar o algoritmo de Dijkstra para encontrar o caminho de menor congestionamento
    try:
        caminho = nx.dijkstra_path(G, source=origem_node, target=destino_node, weight='congestionamento')
    except Exception as e:
        print(f"Erro ao calcular a rota: {e}")
        return []
    
    return caminho



# Função para exibir a rota no mapa, incluindo visualização dos nós de origem e destino
def exibir_rota_no_mapa(G, caminho, origem, destino):
    if not caminho:
        print("Não há caminho válido para exibir no mapa.")
        return
    
    mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)  # Coordenadas de São Paulo
    
    # Adicionando marcadores de origem e destino
    folium.Marker([origem[0], origem[1]], popup="Origem").add_to(mapa)
    folium.Marker([destino[0], destino[1]], popup="Destino").add_to(mapa)

    # Mostrar os nós encontrados no grafo
    folium.Marker([G.nodes[caminho[0]]['y'], G.nodes[caminho[0]]['x']], popup="Primeiro nó da rota").add_to(mapa)
    folium.Marker([G.nodes[caminho[-1]]['y'], G.nodes[caminho[-1]]['x']], popup="Último nó da rota").add_to(mapa)

    # Exibir a rota no mapa
    for i in range(len(caminho)-1):
        rua1 = G.nodes[caminho[i]]
        rua2 = G.nodes[caminho[i+1]]
        folium.PolyLine([(rua1['y'], rua1['x']), (rua2['y'], rua2['x'])], color='blue', weight=2.5, opacity=1).add_to(mapa)

    # Exibir o nome das ruas no caminho
    for i in range(len(caminho)-1):
        rua1 = G.nodes[caminho[i]]
        rua2 = G.nodes[caminho[i+1]]
        nome_rua1 = G.nodes[caminho[i]].get('street', 'Desconhecida')
        nome_rua2 = G.nodes[caminho[i+1]].get('street', 'Desconhecida')
        folium.Marker([rua1['y'], rua1['x']], popup=f"Rua: {nome_rua1}").add_to(mapa)
        folium.Marker([rua2['y'], rua2['x']], popup=f"Rua: {nome_rua2}").add_to(mapa)

    mapa.save("rota_sao_paulo.html")
    print("Rota salva no arquivo 'rota_sao_paulo.html'.")



# Função principal para rodar o sistema
def sistema_trafego():
    origem_endereco = input("Digite o endereço de origem: ")
    destino_endereco = input("Digite o endereço de destino: ")
    
    # Converter os endereços em coordenadas
    origem = endereco_para_coordenada(origem_endereco)
    destino = endereco_para_coordenada(destino_endereco)
    
    if origem and destino:
        # Calcular a melhor rota
        caminho = melhor_rota(G, origem, destino)
        
        # Exibir a rota no mapa
        exibir_rota_no_mapa(G, caminho, origem, destino)  # Passando origem e destino aqui
        
        print("Rota calculada e salva no mapa.")
    else:
        print("Erro ao obter as coordenadas de um ou ambos os endereços.")

# Rodar o sistema
sistema_trafego()
