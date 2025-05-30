import pygame
import random
import sys

pygame.init()
# Música de fondo
pygame.mixer.init()
pygame.mixer.music.load("audio/Run-On.ogg")

pygame.mixer.music.play(-1)  # -1 hace que se repita en bucle
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

# Autos
auto_width, auto_height = 50, 30
autos = []
auto_speed = 5
auto_spawn_time = 1500

SPAWN_AUTO = pygame.USEREVENT + 1

# Reloj
clock = pygame.time.Clock()
FPS = 60

# Sonido (placeholder)
sound_on = True

# ---------- FUNCIONES DE INTERFAZ ----------

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont(None, size)
    text_surf = font_obj.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)
    return text_rect

def main_menu():
    global sound_on
    selected = 0
    options = ["Iniciar juego", "Volumen: On", "Salir"]

    while True:
        screen.fill(WHITE)
        draw_text("🚀 MOTOMENSAJERO FREEDOM 🚀", 40, BLACK, WIDTH//2, 80)

        for i, option in enumerate(options):
            color = GREEN if i == selected else BLACK
            label = f"{option}" if not option.startswith("Volumen") else f"Volumen: {'On' if sound_on else 'Mute'}"
            draw_text(label, 30, color, WIDTH//2, 150 + i*50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game_loop()
                    elif selected == 1:
                        sound_on = not sound_on
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()

def game_loop():
    global autos

    moto_x = WIDTH // 2 - moto_width // 2
    moto_y = HEIGHT - moto_height - 10
    score = 0
    autos = []

    pygame.time.set_timer(SPAWN_AUTO, auto_spawn_time)
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_AUTO:
                x_pos = random.randint(0, WIDTH - auto_width)
                autos.append(pygame.Rect(x_pos, -auto_height, auto_width, auto_height))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and moto_x > 0:
            moto_x -= moto_speed
        if keys[pygame.K_RIGHT] and moto_x < WIDTH - moto_width:
            moto_x += moto_speed

        for auto in autos[:]:
            auto.y += auto_speed
            if auto.y > HEIGHT:
                autos.remove(auto)
                score += 1
            if auto.colliderect(pygame.Rect(moto_x, moto_y, moto_width, moto_height)):
                print("¡Chocaste! Fin del juego.")
                running = False

        # Dibujar
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (moto_x, moto_y, moto_width, moto_height))
        for auto in autos:
            pygame.draw.rect(screen, RED, auto)

        draw_text(f"Puntaje: {score}", 28, BLACK, 10, 10, center=False)
        pygame.display.flip()

    pygame.time.set_timer(SPAWN_AUTO, 0)

# ---------- INICIAR PROGRAMA ----------
if __name__ == "__main__":
    main_menu()


