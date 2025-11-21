# Atividade-da-Unidade-I---Busca
Fechadura Digital — README

Descrição
Este projeto implementa uma fechadura digital com código de 4 dígitos e demonstra a busca do menor número de movimentos para chegar à senha correta usando o algoritmo A*. Cada operação consiste em alterar um dígito por vez (incremento ou decremento circular em 0–9) com custo unitário por passo. A heurística utilizada é a soma das distâncias circulares por dígito, que é admissível.
O comportamento implementado no código inclui:
•	SENHA fixa (constante SENHA = "2910");
•	Entrada de tentativa pelo usuário via prompt ou argumento de linha de comando;
•	Se a tentativa for correta: mensagem de sucesso e desenho do subgrafo com o nó objetivo;
•	Se incorreta: execução do A* para calcular o caminho mínimo até a senha e desenho do subgrafo contendo o caminho e vizinhança imediata.
________________________________________
Arquivos principais
•	fechadura.py — implementação completa apresentada (A*, geração de vizinhos, heurística, visualização e interface de linha de comando).
________________________________________
Como funciona (resumo técnico)
Espaço de estados
•	Cada estado é uma string de 4 dígitos, por exemplo "0237".
•	Operadores: para cada posição do código, pode-se aplicar +1 ou -1 com wrap-around (9 -> 0 e 0 -> 9), gerando até 8 vizinhos por estado.
•	Custo de cada ação: 1 (uniforme).
Heurística
•	calcular_distancia(estado, objetivo) soma, para cada dígito, a menor distância circular entre os dígitos (por exemplo, distância entre 9 e 1 é 2 via wrap).
•	É admissível porque nunca ultrapassa o custo real mínimo restante (cada deslocamento de 1 em um dígito custa ao menos 1 ação).
A* (função algoritmo)
•	Usa fila de prioridade (heapq) com chave f = g + h.
•	Mantém custo_g (g) e dicionário origem para reconstruir caminho.
•	Retorna um dicionário com path (lista de estados), cost (custo total em passos) e expansions (nós expandidos).
________________________________________
Requisitos
•	Python 3.8+
•	Dependências Python (instalar com pip):
o	networkx
o	matplotlib
Exemplo minimal de requirements.txt:
networkx
matplotlib
________________________________________
Como executar
1) Usando prompt interativo
python fechadura.py
•	O programa solicitará que você digite a senha (4 dígitos). Digite "" (apenas Enter) para sair.
2) Passando tentativa como argumento
python fechadura.py 1234
•	O primeiro argumento não iniciando com -- é usado como tentativa única e o programa processa essa tentativa imediatamente.
3) Salvar figura em vez de abrir a janela
•	Use a opção --save junto com os argumentos para forçar a gravação do subgrafo em disco (arquivo subgrafo.png) quando a janela gráfica não puder ser aberta:
python fechadura.py 1234 --save
________________________________________
Exemplos de execução
•	Tentativa correta:
o	Entrada: 2910 → saída: ACESSO PERMITIDO! e exibição do subgrafo contendo apenas o estado objetivo.
•	Tentativa incorreta:
o	Entrada: 0000 → algoritmo A* encontra caminho mínimo (ex.: 0000 -> 1000 -> ... -> 2910) e mostra custo total e número de expansões; exibe subgrafo com caminho destacado em vermelho.
________________________________________
Visualização
•	A função draw_subgraph(nodes, path, start, goal, save=False) constrói um subgrafo contendo os nós do caminho e seus vizinhos imediatos (opcional) e colore:
o	start = verde;
o	goal = dourado;
o	path = vermelho;
o	demais nós = azul claro.
•	Se a exibição por janela não for possível (por exemplo, em execução headless), use --save para gravar subgrafo.png.
________________________________________
Limitações e observações
•	Espaço de estados: para 4 dígitos, o espaço total tem (10^4 = 10{,}000) estados — bem tratável para A* com heurística informativa.
•	O algoritmo assume custos não-negativos (aqui, unitários). Não é adequado para grafos com arestas de custo negativo.
•	A senha está codificada como constante (SENHA). Para produção, nunca armazenar senhas em texto plano.


