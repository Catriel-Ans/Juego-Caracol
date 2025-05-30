import pygame
import random
import sys

pygame.init()

print("Iniciando Delivery Rush...")

# Música de fondo
pygame.mixer.init()
pygame.mixer.music.load("audio/Run-On.ogg")
pygame.mixer.music.play(-1)  # -1 hace que se repita en bucle
muted = False  # Estado de música

# Pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delivery Rush")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)

# Fuentes
font = pygame.font.SysFont(None, 36)

# Moto
moto_width, moto_height = 50, 30
moto_speed = 5

# Autos
auto_width, auto_height = 50, 30
autos = []
auto_speed = 5
auto_spawn_time = 1500

SPAWN_AUTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_AUTO, auto_spawn_time)

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Moto posición inicial
moto_x = WIDTH // 2 - moto_width // 2
moto_y = HEIGHT - moto_height - 10

# Juego en marcha
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tecla M para mutear/desmutear
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if muted:
                    pygame.mixer.music.set_volume(1.0)
                    muted = False
                    print("🎵 Música activada")
                else:
                    pygame.mixer.music.set_volume(0.0)
                    muted = True
                    print("🔇 Música silenciada")

    # Movimiento con teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and moto_x > 0:
        moto_x -= moto_speed
    if keys[pygame.K_RIGHT] and moto_x < WIDTH - moto_width:
        moto_x += moto_speed

    # Fondo
    screen.fill(WHITE)

    # Moto
    pygame.draw.rect(screen, BLUE, (moto_x, moto_y, moto_width, moto_height))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
