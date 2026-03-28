import numpy as np
import pygame
import random

# ================================
# CONFIGURACIÓN DEL JUEGO
# ================================
GRID_SIZE = 10   # tablero 10x10
CELL_SIZE = 40   # tamaño de cada celda en píxeles
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Estados del juego
EMPTY = 0
WALL = 1
GOAL = 2
PACMAN = 3

# ================================
# CREAR TABLERO
# ================================
def create_board():
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # Obstáculos
    for i in range(15):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) != (0, 0) and (x, y) != (GRID_SIZE-1, GRID_SIZE-1):
            board[y][x] = WALL

    # Meta
    goal_x, goal_y = GRID_SIZE-1, GRID_SIZE-1
    board[goal_y][goal_x] = GOAL

    return board, (0, 0), (goal_x, goal_y)

# ================================
# Q-LEARNING
# ================================
ACTIONS = [(0,1), (0,-1), (1,0), (-1,0)]  # abajo, arriba, derecha, izquierda
ALPHA = 0.1   # tasa de aprendizaje
GAMMA = 0.9   # factor de descuento
EPSILON = 0.2 # exploración

def train_q_learning(board, start, goal, episodes=300, max_steps=100):
    Q = np.zeros((GRID_SIZE, GRID_SIZE, len(ACTIONS)))
    for ep in range(episodes):
        state = start
        steps = 0
        while state != goal and steps < max_steps:
            steps += 1
            if random.uniform(0,1) < EPSILON:
                action_idx = random.randint(0, len(ACTIONS)-1)
            else:
                action_idx = np.argmax(Q[state[1], state[0]])

            dx, dy = ACTIONS[action_idx]
            new_state = (max(0, min(GRID_SIZE-1, state[0]+dx)),
                         max(0, min(GRID_SIZE-1, state[1]+dy)))

            reward = -1
            if board[new_state[1]][new_state[0]] == WALL:
                reward = -10
                new_state = state
            elif new_state == goal:
                reward = 100

            Q[state[1], state[0], action_idx] += ALPHA * (
                reward + GAMMA * np.max(Q[new_state[1], new_state[0]]) - Q[state[1], state[0], action_idx]
            )

            state = new_state

        if ep % 50 == 0:
            print(f"Entrenando episodio {ep}/{episodes}")

    return Q

# ================================
# JUEGO CON PYGAME
# ================================
def play_game(board, start, goal, Q):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Q-Learning")

    pacman = start
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0,0,0))

        # Dibujar tablero
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if board[y][x] == WALL:
                    pygame.draw.rect(screen, (100,100,100), rect)
                elif board[y][x] == GOAL:
                    pygame.draw.rect(screen, (0,255,0), rect)

        # Dibujar Pac-Man
        pygame.draw.circle(screen, (255,255,0),
                           (pacman[0]*CELL_SIZE+CELL_SIZE//2, pacman[1]*CELL_SIZE+CELL_SIZE//2),
                           CELL_SIZE//2)

        pygame.display.flip()
        clock.tick(5)

        # Movimiento según Q-Learning
        action_idx = np.argmax(Q[pacman[1], pacman[0]])
        dx, dy = ACTIONS[action_idx]
        new_state = (max(0, min(GRID_SIZE-1, pacman[0]+dx)),
                     max(0, min(GRID_SIZE-1, pacman[1]+dy)))

        if board[new_state[1]][new_state[0]] != WALL:
            pacman = new_state

        if pacman == goal:
            print("¡Meta alcanzada!")
            running = False

        # Eventos de salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# ================================
# MAIN
# ================================
if __name__ == "__main__":
    board, start, goal = create_board()
    Q = train_q_learning(board, start, goal, episodes=300, max_steps=100)
    play_game(board, start, goal, Q)