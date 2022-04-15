from pickle import TRUE
import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1280, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Sim")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
FONT = pygame.font.SysFont("corbel", 16)

class Planet:
    #Astronomical Unit in metres
    AU = 149.6e6 * 1000
    #Gravitational Constant
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100 pixels
    #how much time should be represented
    TIMESTEP = 3600 * 24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        #don't wanna draw the orbit if it is sun
        self.sun = False
        self.distance_to_sun = 0
        #Setting up velocity on two planes i.e., x and y
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE  + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        #Displaying da-distance
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 3)}km", 5, WHITE)
            WIN.blit(distance_text, (x + 7, y + 7))

    #force of attraction b/w two objects ..... O_o
    def attraction(self, other):
        #distance b/w 2 pbjects
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        #mAtHeMaTiCs & PhYsIcS ..... probably.....
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        # F = MASS * ACC. ; ACC. = F / MASS
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        #Getting displacement/distance from velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    #Creating an infinite loop
    run = TRUE
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.3 * 10 ** 23)
    mercury.y_vel = 47.4 * 1000
    venus = Planet(-0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        #regulating FPS
        clock.tick(60)
        WIN.fill((0, 0, 0))
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main()