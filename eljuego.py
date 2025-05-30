import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delivery Rush")

# Colores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Moto (jugador)
moto_width, moto_height = 50, 30
moto_x = WIDTH // 2 - moto_width // 2
moto_y = HEIGHT - moto_height - 10
moto_speed = 5

# Autos (obstáculos)
auto_width, auto_height = 50, 30
autos = []
auto_speed = 5
auto_spawn_time = 1500  # ms

# Puntaje
score = 0
font = pygame.font.SysFont(None, 36)

# Evento para crear autos periódicamente
SPAWN_AUTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_AUTO, auto_spawn_time)

# Reloj para FPS
clock = pygame.time.Clock()
FPS = 60

# Función para dibujar todo
def draw():
    screen.fill(WHITE)
    
    # Dibujar moto
    pygame.draw.rect(screen, BLUE, (moto_x, moto_y, moto_width, moto_height))
    
    # Dibujar autos
    for auto in autos:
        pygame.draw.rect(screen, RED, auto)
        
    # Dibujar puntaje
    score_text = font.render(f"Puntaje: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# Función principal
def main():
    global moto_x, score
    
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == SPAWN_AUTO:
                # Crear un auto en posición aleatoria arriba
                x_pos = random.randint(0, WIDTH - auto_width)
                new_auto = pygame.Rect(x_pos, -auto_height, auto_width, auto_height)
                autos.append(new_auto)
        
        # Movimiento moto con teclas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and moto_x > 0:
            moto_x -= moto_speed
        if keys[pygame.K_RIGHT] and moto_x < WIDTH - moto_width:
            moto_x += moto_speed
        
        # Mover autos hacia abajo
        for auto in autos[:]:
            auto.y += auto_speed
            if auto.y > HEIGHT:
                autos.remove(auto)
                score += 1  # Sumás punto por esquivar un auto
                
            # Detectar colisión con la moto
            moto_rect = pygame.Rect(moto_x, moto_y, moto_width, moto_height)
            if auto.colliderect(moto_rect):
                print("¡Chocaste! Juego terminado.")
                run = False
        
        draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()

