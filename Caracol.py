import pygame
import random
import sys

pygame.init()

print("Iniciando Delivery Rush - Versión Caracol")

# Vidas
lives = 3

# Música de fondo
pygame.mixer.init()
pygame.mixer.music.load("audio/Run-On.ogg")
pygame.mixer.music.play(-1)
muted = False

# Pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delivery Rush - Caracol")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
SNAIL_BODY = (160, 82, 45)  # marrón caracol
SNAIL_SHELL = (205, 133, 63)  # concha

# Fuentes
font = pygame.font.SysFont(None, 36)

# Caracol (antes moto)
snail_width, snail_height = 40, 30
snail_speed = 3  # más lento
snail_x = WIDTH // 2 - snail_width // 2
snail_y = HEIGHT - snail_height - 10

# Rocas (antes autos)
rock_width, rock_height = 40, 40
base_rock_speed = 4
rock_speed = base_rock_speed
rock_spawn_time = 1500  # en milisegundos
rocks = []

SPAWN_ROCK = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ROCK, rock_spawn_time)

# Puntaje y nivel
score = 0
level = 1

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Juego en marcha
running = True
game_over = False

# Función para dibujar caracol pixel art
def draw_snail(surface, x, y):
    # Cuerpo caracol
    pygame.draw.ellipse(surface, SNAIL_BODY, (x + 5, y + 10, 30, 15))  # cuerpo
    # Concha caracol (espiral simplificada)
    pygame.draw.circle(surface, SNAIL_SHELL, (x + 25, y + 10), 15)
    pygame.draw.circle(surface, BROWN, (x + 25, y + 10), 10)
    pygame.draw.circle(surface, SNAIL_SHELL, (x + 25, y + 10), 5)
    # Ojos
    pygame.draw.circle(surface, WHITE, (x + 10, y + 5), 4)
    pygame.draw.circle(surface, BLACK, (x + 10, y + 5), 2)
    pygame.draw.circle(surface, WHITE, (x + 20, y + 5), 4)
    pygame.draw.circle(surface, BLACK, (x + 20, y + 5), 2)

# Función para dibujar roca
def draw_rock(surface, rect):
    pygame.draw.rect(surface, GRAY, rect)
    # Agregar detalles para que parezca una roca
    pygame.draw.line(surface, BLACK, (rect.x + 5, rect.y + 5), (rect.x + 20, rect.y + 20), 2)
    pygame.draw.line(surface, BLACK, (rect.x + 10, rect.y + 5), (rect.x + 35, rect.y + 30), 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                muted = not muted
                pygame.mixer.music.set_volume(0.0 if muted else 1.0)
                print("🔇 Música silenciada" if muted else "🎵 Música activada")

            if event.key == pygame.K_r and game_over:
                rocks.clear()
                snail_x = WIDTH // 2 - snail_width // 2
                score = 0
                lives = 3           # Resetear vidas al reiniciar
                rock_speed = base_rock_speed  # Resetear velocidad
                level = 1                     # Resetear nivel
                game_over = False

        if event.type == SPAWN_ROCK and not game_over:
            # Generar una sola roca cada vez que ocurre el evento para evitar saturar
            rock_x = random.randint(0, WIDTH - rock_width)
            new_rock = pygame.Rect(rock_x, -rock_height, rock_width, rock_height)
            rocks.append(new_rock)

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snail_x > 0:
            snail_x -= snail_speed
        if keys[pygame.K_RIGHT] and snail_x < WIDTH - snail_width:
            snail_x += snail_speed

    # Definir rectángulo del caracol para colisiones
    snail_rect = pygame.Rect(snail_x, snail_y, snail_width, snail_height)

    # Mover rocas y chequear si pasaron sin chocar
    rocks_to_remove = []
    for rock in rocks:
        rock.y += rock_speed
        if rock.y > HEIGHT:
            score += 1  # Suma 1 punto por cada roca que pasa completo
            rocks_to_remove.append(rock)

    # Remover rocas que pasaron
    for rock in rocks_to_remove:
        rocks.remove(rock)

    # Aumentar dificultad cada 10 puntos
    new_level = score // 10 + 1
    if new_level > level:
        level = new_level
        rock_speed += 1  # Incrementa velocidad en 1 por nivel
        print(f"Nivel {level} alcanzado! Velocidad de rocas aumentada a {rock_speed}.")

    # Detectar colisión
    for rock in rocks:
        if snail_rect.colliderect(rock):
            if lives > 0:
                lives -= 1
            rocks.clear()  # limpia las rocas al chocar
            snail_x = WIDTH // 2 - snail_width // 2  # reinicia caracol al centro
            if lives <= 0:
                game_over = True
            break

    # Fondo nocturno
    screen.fill((10, 10, 30))

    # Dibujar caracol
    draw_snail(screen, snail_x, snail_y)

    # Dibujar rocas
    for rock in rocks:
        draw_rock(screen, rock)

    # Dibujar puntaje y nivel
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    level_text = font.render(f"Nivel: {level}", True, WHITE)
    screen.blit(level_text, (10, 50))

    # Dibujar vidas
    lives_text = font.render(f"Vidas: {lives}", True, GREEN)
    screen.blit(lives_text, (WIDTH - 120, 10))

    if game_over:
        over_text = font.render("¡Chocaste! Presioná R para reiniciar", True, GREEN)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
sys.exit()
