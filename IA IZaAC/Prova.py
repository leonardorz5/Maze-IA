import numpy as np
import random
import tkinter as tk
import time
from collections import deque

# Função para gerar um labirinto perfeito
def gerar_labirinto_perfeito(tamanho):
    labirinto = np.ones((tamanho, tamanho), dtype=int)  # Cria uma matriz de uns, representando paredes
    
    # Função recursiva para cavar passagens
    def cavar_passagens_de(cx, cy):
        direcoes = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Lista de direções possíveis
        random.shuffle(direcoes)  # Embaralha as direções para gerar um labirinto aleatório
        for (dx, dy) in direcoes:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < tamanho and 0 <= ny < tamanho and labirinto[nx, ny] == 1:
                mx, my = cx + dx // 2, cy + dy // 2
                if 0 <= mx < tamanho and 0 <= my < tamanho and labirinto[mx, my] == 1:
                    labirinto[nx, ny] = 0
                    labirinto[mx, my] = 0
                    cavar_passagens_de(nx, ny)
    
    inicio = (0, 0)
    fim = (tamanho-1, tamanho-1)
    labirinto[inicio] = 0
    cavar_passagens_de(inicio[0], inicio[1])
    
    # Verifica se o ponto final não está em uma parede
    while labirinto[fim] == 1:
        fim = (random.randint(0, tamanho-1), random.randint(0, tamanho-1))

    labirinto[inicio] = -2  # S: Início do labirinto
    labirinto[fim] = -3   # E: Final do labirinto
    return labirinto, inicio, fim

# Classe para criar a interface do labirinto usando Tkinter
class AppLabirinto:
    def __init__(self, root, labirinto, inicio, fim):
        self.root = root
        self.labirinto = labirinto
        self.inicio = inicio
        self.fim = fim
        self.tamanho = len(labirinto)
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        self.tamanho_celula = 500 // self.tamanho
        self.desenhar_labirinto()
        self.caminho = self.resolver_labirinto()
        self.animar_caminho(self.caminho, final=True)

    # Desenha o labirinto na tela
    def desenhar_labirinto(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                cor = 'white'
                if self.labirinto[i, j] == 1:
                    cor = 'black'
                elif self.labirinto[i, j] == -2:
                    cor = 'green'
                elif self.labirinto[i, j] == -3:
                    cor = 'red'
                self.canvas.create_rectangle(j*self.tamanho_celula, i*self.tamanho_celula, (j+1)*self.tamanho_celula, (i+1)*self.tamanho_celula, fill=cor)

    # Verifica se a movimentação é válida
    def movimento_valido(self, x, y):
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho and self.labirinto[x, y] in [0, -3]

    # Resolve o labirinto utilizando BFS (Busca em Largura)
    def resolver_labirinto(self):
        fila = deque([(self.inicio, [self.inicio])])
        visitados = set()
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while fila:
            (x, y), caminho = fila.popleft()
            if (x, y) == self.fim:
                return caminho

            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if self.movimento_valido(nx, ny) and (nx, ny) not in visitados:
                    fila.append(((nx, ny), caminho + [(nx, ny)]))
                    visitados.add((nx, ny))

        return None

    # Anima o caminho encontrado no labirinto
    def animar_caminho(self, caminho, final=False):
        for x, y in caminho:
            cor = 'blue' if not final else 'green'
            self.canvas.create_rectangle(y*self.tamanho_celula, x*self.tamanho_celula, (y+1)*self.tamanho_celula, (x+1)*self.tamanho_celula, fill=cor)
            self.root.update()
            if final:
                time.sleep(0.01)  # Pausa para animar o caminho final

# Código principal
if __name__ == "__main__":
    tamanho = random.randint(10, 100)  # Tamanho aleatório do labirinto
    labirinto, inicio, fim = gerar_labirinto_perfeito(tamanho)
    root = tk.Tk()  # Cria a janela principal do Tkinter
    app = AppLabirinto(root, labirinto, inicio, fim)  # Inicializa o aplicativo do labirinto
    root.mainloop()  # Inicia o loop principal do Tkinter para exibir a interface
