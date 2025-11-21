
"""
Fechadura digital

Uma fechadura digital tem um código de 4 dígitos. 
Cada botão pressionado altera um dígito de cada vez, e cada operação tem um custo.
O objetivo é chegar ao código correto com o menor número de movimentos.

Algoritmo: A* (custo unitário por passo)
Heurística: soma das distâncias circulares por dígito (admissível)

Funcionalidade:
- SENHA fixa (SENHA = "2910")
- Usuário digita tentativa (ou passa por argumento)
- Se correta -> mostra sucesso
- Se incorreta -> roda A*, mostra caminho mínimo e desenha subgrafo

"""

from typing import List, Tuple, Dict, Optional, Set
import heapq
import sys

# visualização do grafo
import networkx as nx
import matplotlib.pyplot as plt


# Configuração

SENHA = "2910"          # senha cadastrada
QDT_DIGITOS = 4         # número de dígitos (sempre manter compatível com SENHA)

# Funções auxiliares

def gerar(codigo: str) -> List[str]: 
    """Gera vizinhos mudando cada dígito em ±1 (com wrap 0-9)."""
    codigo = codigo.zfill(QDT_DIGITOS)
    resul: List[str] = []
    for posicao, ch in enumerate(codigo):
        d = int(ch)
        for mudanca in (-1, 1):
            novo = (d + mudanca) % 10
            novo_codigo = codigo[:posicao] + str(novo) + codigo[posicao+1:]
            resul.append(novo_codigo)
    return resul

def distancia(a: str, b: str) -> int:
    """Distância circular mínima entre dois dígitos 0–9."""
    # recebe caracteres '0'..'9'
    va = int(a)
    vb = int(b)
    diff = abs(va - vb)
    return min(diff, 10 - diff)

def calcular_distancia(codigo: str, estado_final: str) -> int:
    """Soma das distâncias circulares por dígito entre codigo e estado_final."""
    codigo = codigo.zfill(QDT_DIGITOS)
    estado_final = estado_final.zfill(QDT_DIGITOS)
    return sum(distancia(c, o) for c, o in zip(codigo, estado_final))


# Implementação A* (algoritmo)

def algoritmo(estado_inicial: str, estado_final: str) -> Optional[Dict]: #Busca de custo Uniforme
    """Executa o algoritmo A* para encontrar o caminho mínimo até o código correto """

    estado_inicial = estado_inicial.zfill(QDT_DIGITOS)
    estado_final = estado_final.zfill(QDT_DIGITOS)

    """Caso base: o código inicial já é o correto"""
    if estado_inicial == estado_final:  
        return {'path': [estado_inicial], 'cost': 0, 'expansions': 0}

    """Fila de prioridade para armazenar nós."""
    pilha_a: List[Tuple[int, int, str, Optional[str]]] = []  
    inicio_h = calcular_distancia(estado_inicial, estado_final)
    heapq.heappush(pilha_a, (inicio_h, 0, estado_inicial, None))

    """- Dicionários de rastreamento e custos""" 
    origem: Dict[str, Optional[str]] = {} #gerar cada nó
    custo_g: Dict[str, int] = {estado_inicial: 0} #custo acumulado
    fechados: Set[str] = set() #conjunto de nós visitados
    qtd_expandidos = 0 #contador de nós

    """Loop principal do A*"""
    while pilha_a:
        f, g, no_atual, raiz = heapq.heappop(pilha_a) #escolhe o nó com menor custo acumulado
        if no_atual in fechados:
            continue
         
        origem[no_atual] = raiz
        qtd_expandidos += 1

        if no_atual == estado_final: # se objetivo atingido, reconstruir caminho
            caminho: List[str] = [] 
            atual = no_atual
            while atual is not None:
                caminho.append(atual)
                atual = origem.get(atual)
            caminho.reverse()
            return {'path': caminho, 'cost': g, 'expansions': qtd_expandidos}
        fechados.add(no_atual)

    
        for nb in gerar(no_atual):  #expandir vizinhos
            tentative_g = g + 1  #custo uniforme por ação
            if tentative_g < custo_g.get(nb, float('inf')):
                custo_g[nb] = tentative_g
                prioridade = tentative_g + calcular_distancia(nb, estado_final) #Busca Uniforme com heurística
                heapq.heappush(pilha_a, (prioridade, tentative_g, nb, no_atual))  #sem solução (improvável)
    return None


astar = algoritmo

#Visualização (subgrafo)#

def build_subgraph_nodes(path: List[str], include_neighbors: bool = True) -> Set[str]:
    """Retorna conjunto de nós para desenhar: path + vizinhos imediatos (opcional)."""
    nodes: Set[str] = set(path)
    if include_neighbors:
        for p in list(path):
            nodes.update(gerar(p))
    return nodes

def draw_subgraph(nodes: Set[str], path: List[str], start: str, goal: str, save: bool = False):
    """Desenha subgrafo simples destacando start (verde), goal (gold) e caminho (vermelho)."""
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for n in list(nodes):
        for nb in gerar(n):
            if nb in nodes:
                G.add_edge(n, nb)

    pos = nx.spring_layout(G, seed=42)
    colors: List[str] = []
    sizes: List[int] = []
    for n in G.nodes():
        if n == start:
            colors.append('green'); sizes.append(900)
        elif n == goal:
            colors.append('gold'); sizes.append(900)
        elif n in path:
            colors.append('red'); sizes.append(700)
        else:
            colors.append('lightblue'); sizes.append(300)

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    if len(path) > 1:
        nx.draw_networkx_edges(G, pos, edgelist=list(zip(path[:-1], path[1:])), width=3.0, edge_color='red')

    plt.title(f"Subgrafo (start={start}, goal={goal}) — caminho em vermelho")
    plt.axis('off')

    try:
        plt.show()
    except Exception as e:
        if save:
            plt.savefig("subgrafo.png", dpi=200)
            print(f"Janela não pôde ser aberta ({e}). Figura salva como subgrafo.png.")
    finally:
        plt.close()

#Interface com usuário#
def prompt_and_check():

    """Pergunta tentativa e aplica busca A* caso a senha esteja incorreta."""
    print("- BEM-VINDO AO LAR - \nDigite seu acesso: \n")

    salvar = '--save' in sys.argv  
    arg_tentativa = None

    """argumento"""
    for a in sys.argv[1:]: 
        if not a.startswith('--'):
            arg_tentativa = a
            break

    while True:
        if arg_tentativa:
            tentativa = arg_tentativa.zfill(QDT_DIGITOS)
            print(f"Tentativa via argumento: {tentativa}")
            arg_tentativa = None

        else:
            tentativa = input("Sua senha: ").strip()
            if tentativa == "":
                print("Saindo.")
                return
            tentativa = tentativa.zfill(QDT_DIGITOS)
    
        if not (tentativa.isdigit() and len(tentativa) == QDT_DIGITOS):
            print("Formato inválido. Use 4 dígitos (0-9).") #validação do formato do digito
            continue

        if tentativa == SENHA: #caso acerte a senha 
            print("\n -- ACESSO PERMITIDO!\n")
            nodes = build_subgraph_nodes([tentativa])
            draw_subgraph(nodes, [tentativa], tentativa, tentativa, salvar)
            return
        else:
            print("\n SENHA INCORRETA - XX \n Err... \n") #calculando caiminho mínimo A*
            result = astar(tentativa, SENHA)
            if not result:
                print("Não foi encontrado caminho (improvável).")
            else:
                path = result['path']
                print(f"Caminho mínimo ({result['cost']} passos):\n" + " -> ".join(path))
                print(f"(Nós expandidos: {result['expansions']})\n")
                nodes = build_subgraph_nodes(path)
                draw_subgraph(nodes, path, tentativa, SENHA, salvar)

# Execução principal
if __name__ == "__main__":
    prompt_and_check()
