import pygame
import random
import sys

pygame.init()

print("Iniciando Delivery Rush...")

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
moto_x = WIDTH // 2 - moto_width // 2
moto_y = HEIGHT - moto_height - 10

# Autos
auto_width, auto_height = 50, 30
base_auto_speed = 5
auto_speed = base_auto_speed
auto_spawn_time = 1500
autos = []

SPAWN_AUTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_AUTO, auto_spawn_time)

# Puntaje y nivel
score = 0
level = 1

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Juego en marcha
running = True
game_over = False

# Función para dibujar moto pixel art
def draw_moto(surface, x, y):
    # Base de la moto (cuerpo)
    pygame.draw.rect(surface, (50, 50, 50), (x + 5, y + 10, 40, 15))  # carrocería gris oscuro
    pygame.draw.rect(surface, (100, 100, 100), (x + 10, y + 15, 30, 10))  # cuerpo gris claro

    # Ruedas
    pygame.draw.circle(surface, (20, 20, 20), (x + 15, y + 30), 7)  # rueda trasera negra
    pygame.draw.circle(surface, (20, 20, 20), (x + 40, y + 30), 7)  # rueda delantera negra

    pygame.draw.circle(surface, (150, 150, 150), (x + 15, y + 30), 4)  # centro rueda trasera
    pygame.draw.circle(surface, (150, 150, 150), (x + 40, y + 30), 4)  # centro rueda delantera

    # Manillar
    pygame.draw.rect(surface, (80, 80, 80), (x + 35, y + 5, 10, 5))

    # Asiento
    pygame.draw.rect(surface, (70, 70, 70), (x + 20, y + 5, 15, 10))

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
                autos.clear()
                moto_x = WIDTH // 2 - moto_width // 2
                score = 0
                lives = 3           # Resetear vidas al reiniciar
                auto_speed = base_auto_speed  # Resetear velocidad
                level = 1                     # Resetear nivel
                game_over = False

        if event.type == SPAWN_AUTO and not game_over:
            auto_x = random.randint(0, WIDTH - auto_width)
            autos.append(pygame.Rect(auto_x, -auto_height, auto_width, auto_height))
            
            
        if not game_over:
           keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and moto_x > 0:
          moto_x -= moto_speed
        if keys[pygame.K_RIGHT] and moto_x < WIDTH - moto_width:
          moto_x += moto_speed

    # Definir rectángulo de la moto para colisiones
    moto_rect = pygame.Rect(moto_x, moto_y, moto_width, moto_height)

    # Mover autos y chequear si pasaron sin chocar
    autos_to_remove = []
    for auto in autos:
        auto.y += auto_speed
        if auto.y > HEIGHT:
            score += 1  # Suma 1 punto por cada auto que pasa completo
            autos_to_remove.append(auto)

    # Remover autos que pasaron
    for auto in autos_to_remove:
        autos.remove(auto)

    # Aumentar dificultad cada 10 puntos
    new_level = score // 10 + 1
    if new_level > level:
        level = new_level
        auto_speed += 1  # Incrementa velocidad en 1 por nivel
        print(f"Nivel {level} alcanzado! Velocidad de autos aumentada a {auto_speed}.")

    # Detectar colisión
    for auto in autos:
        if moto_rect.colliderect(auto):
            if lives > 0:
                lives -= 1
            autos.clear()  # limpia los autos al chocar
            moto_x = WIDTH // 2 - moto_width // 2  # reinicia moto al centro
            if lives <= 0:
                game_over = True
            break
 

    # Fondo nocturno
    screen.fill((10, 10, 30))

    # Dibujar con función pixel art
    draw_moto(screen, moto_x, moto_y)

    # Dibujar autos
    for auto in autos:
        pygame.draw.rect(screen, RED, auto)

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
