# Atividade-da-Unidade-I---Busca
Fechadura Digital — README
Descrição
Este projeto implementa uma fechadura digital com código de 4 dígitos e demonstra a busca do menor número de movimentos para chegar à senha correta usando o algoritmo A*. Cada operação consiste em alterar um dígito por vez (incremento ou decremento circular em 0–9) com custo unitário por passo. A heurística utilizada é a soma das distâncias circulares por dígito, que é admissível.
O comportamento implementado no código inclui:
•	SENHA fixa (constante SENHA = "2910");
•	Entrada de tentativa pelo usuário via prompt ou argumento de linha de comando;
•	Se a tentativa for correta: mensagem de sucesso e desenho do subgrafo com o nó objetivo;
•	Se incorreta: execução do A* para calcular o caminho mínimo até a senha e desenho do subgrafo contendo o caminho e vizinhança imediata.

