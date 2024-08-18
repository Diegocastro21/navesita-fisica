import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efecto Honda Gravitatorio")

FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
SHIP_SIZE = 20  # Tamaño para la imagen de la nave


BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))
SHIP = pygame.transform.scale(pygame.image.load("navesita.png"), (SHIP_SIZE, SHIP_SIZE))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Variables globales que se pueden modificar
G = 5
PLANET_MASS = 100
SHIP_MASS = 5


class Planet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def move(self, planet):
        global G, PLANET_MASS, SHIP_MASS
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * SHIP_MASS * PLANET_MASS) / distance ** 2

        acceleration = force / SHIP_MASS
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        # pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)
        rotated_ship = pygame.transform.rotate(SHIP, -math.degrees(math.atan2(self.vel_y, self.vel_x)))
        rect = rotated_ship.get_rect(center=(int(self.x), int(self.y)))
        win.blit(rotated_ship, rect.topleft)


def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y)
    return obj


def draw_text(text, x, y):
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, WHITE)
    win.blit(text_surface, (x, y))


def main():
    global G, PLANET_MASS, SHIP_MASS

    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    G += 1
                elif event.key == pygame.K_f:
                    G = max(1, G - 1)
                elif event.key == pygame.K_p:
                    PLANET_MASS += 10
                elif event.key == pygame.K_o:
                    PLANET_MASS = max(10, PLANET_MASS - 10)
                elif event.key == pygame.K_s:
                    SHIP_MASS += 1
                elif event.key == pygame.K_a:
                    SHIP_MASS = max(1, SHIP_MASS - 1)

        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            win.blit(SHIP, (temp_obj_pos[0] - SHIP_SIZE // 2, temp_obj_pos[1] - SHIP_SIZE // 2))
            # pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            # off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            off_screen = obj.x < -SHIP_SIZE or obj.x > WIDTH + SHIP_SIZE or obj.y < -SHIP_SIZE or obj.y > HEIGHT + SHIP_SIZE
            collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        # Mostrar valores actuales
        draw_text(f"G: {G} (G/F)", 10, 10)
        draw_text(f"Planet Mass: {PLANET_MASS} (P/O)", 10, 40)
        draw_text(f"Ship Mass: {SHIP_MASS} (S/A)", 10, 70)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()