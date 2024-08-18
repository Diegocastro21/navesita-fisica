import pygame

# Inicializar Pygame
pygame.init()

# Crear una ventana
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mi Primer Juego con Pygame")

# Colores
white = (255, 255, 255)
blue = (0, 0, 255)

# Variables de posición
x, y = 320, 240
dx, dy = 5, 5

# Bucle del juego
running = True
while running:
    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar posición
    x += dx
    y += dy

    # Rebotar en los bordes
    if x > 640 or x < 0:
        dx = -dx
    if y > 480 or y < 0:
        dy = -dy

    # Dibujar
    screen.fill(white)
    pygame.draw.circle(screen, blue, (x, y), 30)
    pygame.display.update()

    # Control de tiempo
    pygame.time.delay(30)

# Cerrar Pygame
pygame.quit()
