import pygame
import random
import threading


def create_particles(position, screen):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    res = []
    for _ in range(particle_count):
        res.append(Particle(screen, position, random.choice(numbers), random.choice(numbers)))
    return res


def create_particles_bad(position, screen):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    res = []
    for _ in range(particle_count):
        res.append(Particle(screen, position, random.choice(numbers), random.choice(numbers), type_p='bad'))
    return res


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера

    def __init__(self, screen, pos, dx, dy, type_p='good'):
        super().__init__()
        fire = [pygame.image.load("star.png")]
        if type_p == 'bad':
            fire = [pygame.image.load("star_bad.png")]
            fire[0].set_colorkey((100, 0, 0))
        else:
            fire[0].set_colorkey((0, 0, 0))
        for scale in (5, 10, 20):
            if type_p == 'good':
                el = pygame.transform.scale(fire[0], (scale, scale))
                el.set_colorkey((0, 0, 0))
                fire.append(el)
            else:
                el = pygame.transform.scale(fire[0], (scale, scale))
                el.set_colorkey((100, 0, 0))
                fire.append(el)
        self.image = random.choice(fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1
        self.screen = screen

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen.get_rect()):
            self.kill()
