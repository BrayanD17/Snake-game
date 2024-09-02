import tkinter as tk
import random
from queue import PriorityQueue

class SnakeGame:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Juego Snake')
        tam_celda = 479 // 20
        self.ancho_canvas = tam_celda * 20
        self.alto_canvas = tam_celda * 18
        self.ventana.geometry(
            f'{self.ancho_canvas + 6}x{self.alto_canvas + 31}')
        self.ventana.resizable(0, 0)
        self.frame_1 = tk.Frame(self.ventana, width=self.ancho_canvas + 6, height=25, bg='black')
        self.frame_1.grid(column=0, row=0, sticky='ew')
        self.frame_2 = tk.Frame(self.ventana, width=self.ancho_canvas + 6, height=self.alto_canvas, bg='black')
        self.frame_2.grid(column=0, row=1)
        self.canvas = tk.Canvas(self.frame_2, bg='black', width=self.ancho_canvas, height=self.alto_canvas)
        self.canvas.pack()
        # Botones e información de cantidad
        self.button_iniciar = tk.Button(self.frame_1, text='Iniciar', bg='aqua', command=self.iniciar_juego,
                                        highlightbackground='black')
        self.button_iniciar.pack(side='left', padx=20)
        self.button_salir = tk.Button(self.frame_1, text='Salir', bg='orange', command=self.salir,
                                      highlightbackground='black')
        self.button_salir.pack(side='left', padx=20)
        self.label_cantidad = tk.Label(self.frame_1, text='Cantidad 🍎 : 0', bg='black', fg='red',
                                       font=('Arial', 12, 'bold'))
        self.label_cantidad.pack(side='right', padx=20)
        # Crear la cuadrícula, serpiente y manzana
        self.crear_cuadricula(tam_celda)
        self.segmentos = [(0, 0), (0, 1), (0, 2)]
        self.dibujar_serpiente()
        self.manzana_x, self.manzana_y = None, None
        self.obstaculos = [(4, 5), (7, 9), (11, 14), (15, 6), (18, 12)]
        self.dibujar_manzana()
        self.agregar_obstaculos_iniciales()

    def crear_cuadricula(self, tam_celda):
        for i in range(0, 20):
            for j in range(0, 18):
                x1 = i * tam_celda
                y1 = j * tam_celda
                x2 = x1 + tam_celda
                y2 = y1 + tam_celda
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray10', outline='gray20')

    def dibujar_serpiente(self):
        tam_celda = 479 // 20
        self.canvas.delete('snake')
        for segmento in self.segmentos:
            x, y = segmento
            x1 = x * tam_celda
            y1 = y * tam_celda
            x2 = x1 + tam_celda
            y2 = y1 + tam_celda
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='gray20', tag='snake')

    def dibujar_manzana(self):
        tam_celda = 479 // 20
        self.canvas.delete('apple')
        while True:
            self.manzana_x = random.randint(0, 19)
            self.manzana_y = random.randint(0, 17)
            if (self.manzana_x, self.manzana_y) not in self.obstaculos:
                break

        x1 = self.manzana_x * tam_celda
        y1 = self.manzana_y * tam_celda
        x2 = x1 + tam_celda
        y2 = y1 + tam_celda
        print(
            f"Coordenadas de la manzana - X: {self.manzana_x}, Y: {self.manzana_y}")
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2 - tam_celda // 8, text='🍎', fill='red',
                                font=('Arial', tam_celda - 2), tag='apple')

    def agregar_obstaculos_iniciales(self):
        obstaculos = [(4, 5), (7, 9), (11, 14), (15, 6), (18, 12)]
        tam_celda = 479 // 20
        for obstaculo in obstaculos:
            x, y = obstaculo
            x1 = x * tam_celda
            y1 = y * tam_celda
            x2 = x1 + tam_celda
            y2 = y1 + tam_celda
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text='🪨', fill='gray40', font=('Arial', tam_celda - 2), tag='obstaculo')

    '''La función get_neighbors proporciona las posiciones vecinas válidas necesarias 
        para la exploración del algoritmo A* en la función buscar_manzana, ayudando así a 
        determinar la ruta óptima para que la serpiente alcance la manzana.'''
    def buscar_manzana(self):
        # Implementación del algoritmo A*
        frontier = PriorityQueue()
        start = self.segmentos[0]
        goal = (self.manzana_x, self.manzana_y)
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.get_neighbors(current):
                if next in self.obstaculos:
                    continue

                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        self.move_snake_along_path(path)
    '''Esta función genera y devuelve una lista de las 
        posiciones vecinas válidas para una posición dada (x, y) 
        en un área de juego rectangular de 20x18 '''
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 20 and 0 <= ny < 18:
                neighbors.append((nx, ny))
        return neighbors
    ''' Se encarga de hacer una estimación del costo restante desde 
        una posición a hasta una posición b basada en la distancia de Manhattan, 
        que es una heurística útil para problemas de búsqueda en cuadrículas'''
    def heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)
    '''Se encarga de mover la serpiente a lo largo de la ruta encontrada
        por el algoritmo A* para llegar a la manzana'''
    def move_snake_along_path(self, path):
        speed = 200  # Velocidad inicial ajustada para una transición más suave
        if len(path) > 1:
            next_pos = path[1]
            self.segmentos.pop()  # Eliminar el último segmento de la serpiente
            self.segmentos.insert(0, next_pos)  # Insertar el nuevo segmento en la posición 0
            if next_pos == (self.manzana_x, self.manzana_y):
                self.label_cantidad.config(
                    text=f'Cantidad 🍎 : {int(self.label_cantidad.cget("text").split(":")[1]) + 1}')
                self.dibujar_manzana()
                self.buscar_manzana()
            self.dibujar_serpiente()  # Redibujar la serpiente con las nuevas posiciones de los segmentos
            # Reducir gradualmente la velocidad para una transición más suave
            speed = max(50, speed - 5)
            # Llamar recursivamente a la función con la nueva posición
            self.ventana.after(speed, self.move_snake_along_path, path[1:])
    def iniciar_juego(self):
        self.buscar_manzana()
    def salir(self):
        self.ventana.quit()
if __name__ == "__main__":
    ventana = tk.Tk()
    juego = SnakeGame(ventana)
    ventana.mainloop()
