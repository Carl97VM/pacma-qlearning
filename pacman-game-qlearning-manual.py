import numpy as np
import pygame
import random

# ================================
# CONFIGURACIÓN DEL JUEGO
# ================================
GRID_SIZE = 10
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 100

EMPTY = 0
WALL = 1
GOAL = 2

ACTIONS = [(0,1), (0,-1), (1,0), (-1,0)]
ALPHA, GAMMA, EPSILON = 0.1, 0.9, 0.2

# ================================
# CREAR TABLERO
# ================================
def create_board():
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for i in range(15):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) not in [(0,0), (GRID_SIZE-1, GRID_SIZE-1)]:
            board[y][x] = WALL
    board[GRID_SIZE-1][GRID_SIZE-1] = GOAL
    return board, (0,0), (GRID_SIZE-1, GRID_SIZE-1)

# ================================
# Q-LEARNING
# ================================
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
            # FORMULA DE Q-LEARNING
            Q[state[1], state[0], action_idx] += ALPHA * (
                reward + GAMMA * np.max(Q[new_state[1], new_state[0]]) - Q[state[1], state[0], action_idx]
            )
            state = new_state
    return Q

# ================================
# JUEGO CON PYGAME
# ================================
def play_game(board, start, goal, Q):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Q-Learning con botones")

    font = pygame.font.SysFont("Arial", 20)
    pacman = start
    mode = "manual"
    clock = pygame.time.Clock()
    running = True

    # Botones
    btn_step = pygame.Rect(50, HEIGHT-80, 100, 40)
    btn_auto = pygame.Rect(200, HEIGHT-80, 100, 40)
    btn_reset = pygame.Rect(350, HEIGHT-80, 100, 40)

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

        # Dibujar botones
        pygame.draw.rect(screen, (0,0,255), btn_step)
        pygame.draw.rect(screen, (0,255,0), btn_auto)
        pygame.draw.rect(screen, (255,0,0), btn_reset)
        screen.blit(font.render("Paso", True, (255,255,255)), (btn_step.x+20, btn_step.y+10))
        screen.blit(font.render("Auto", True, (255,255,255)), (btn_auto.x+20, btn_auto.y+10))
        screen.blit(font.render("Reset", True, (255,255,255)), (btn_reset.x+20, btn_reset.y+10))

        # Consola abajo
        coords_text = f"Posición actual: {pacman}"
        screen.blit(font.render(coords_text, True, (255,255,255)), (50, HEIGHT-40))

        pygame.display.flip()
        clock.tick(5)

        # Movimiento automático
        if mode == "automatic":
            action_idx = np.argmax(Q[pacman[1], pacman[0]])
            dx, dy = ACTIONS[action_idx]
            new_state = (max(0, min(GRID_SIZE-1, pacman[0]+dx)),
                         max(0, min(GRID_SIZE-1, pacman[1]+dy)))
            if board[new_state[1]][new_state[0]] != WALL:
                pacman = new_state
            if pacman == goal:
                print("¡Meta alcanzada!")
                mode = "manual"

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_step.collidepoint(event.pos):
                    # Paso manual
                    action_idx = np.argmax(Q[pacman[1], pacman[0]])
                    dx, dy = ACTIONS[action_idx]
                    new_state = (max(0, min(GRID_SIZE-1, pacman[0]+dx)),
                                 max(0, min(GRID_SIZE-1, pacman[1]+dy)))
                    if board[new_state[1]][new_state[0]] != WALL:
                        pacman = new_state
                elif btn_auto.collidepoint(event.pos):
                    mode = "automatic"
                elif btn_reset.collidepoint(event.pos):
                    board, start, goal = create_board()
                    Q = train_q_learning(board, start, goal, episodes=300)
                    pacman = start
                    mode = "manual"

    pygame.quit()

# ================================
# MAIN
# ================================
if __name__ == "__main__":
    board, start, goal = create_board()
    Q = train_q_learning(board, start, goal, episodes=300)
    play_game(board, start, goal, Q)