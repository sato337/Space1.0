import pygame
import math
import random
import sys
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

# Цвета
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
BUTTON_COLOR = (70, 70, 80)
HOVER_COLOR = (100, 100, 120)
TEXT_COLOR = (220, 220, 220)
TARGET_COLOR = (0, 255, 0, 128)
ARROW_COLOR = (255, 255, 0, 128)

# Игровые константы
FPS = 80
G_CONSTANT = 0.05
SUN_MASS = 1000
PLANET_MASS = 500
ASTEROID_SPAWN_RATE = 0.009
MAX_ASTEROIDS = 15

# Настройки корабля
SHIP_ROTATION_SPEED = 3
SHIP_ACCELERATION = 0.1
SHIP_MAX_SPEED = 5
SHIP_FRICTION = 0.99

# Настройки камеры
INITIAL_SCALE = 0.5
CAMERA_SCALE = 1.5
CAMERA_SMOOTHNESS = 0.1

# Настройки миссии
MISSION_POINTS = 7
MISSION_TIME = 30
TIME_BONUS = 5
POINT_RADIUS = 15

BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)

FPS = 80
G_CONSTANT = 0.05  # Уменьшаем гравитационную постоянную
SUN_MASS = 1000  # Уменьшаем массу солнца
PLANET_MASS = 500  # Масса планет
ASTEROID_SPAWN_RATE = 0.009  # Увеличили с 0.005 до 0.02
MAX_ASTEROIDS = 15  # Увеличили максимальное количество астероидов

# Добавим новые константы
SHIP_SPEED = 5
SHIP_ROTATION_SPEED = 3
SHIP_ACCELERATION = 0.1
SHIP_MAX_SPEED = 5
SHIP_FRICTION = 0.99

# Добавим константы для масштабирования
INITIAL_SCALE = 0.5  # Начальный масштаб для обзора всей системы
CAMERA_SCALE = 1.5  # Масштаб при следовании за кораблем
CAMERA_SMOOTHNESS = 0.1

# Добавляем новые константы
MISSION_POINTS = 7  # Количество точек для миссии
MISSION_TIME = 30  # Начальное время в секундах
TIME_BONUS = 5  # Бонусное время за точку
POINT_RADIUS = 15  # Размер точки
TARGET_COLOR = (0, 255, 0, 128)  # Полупрозрачный зеленый
ARROW_COLOR = (255, 255, 0, 128)  # Полупрозрачный желтый
FONT_SIZE = 36

# Загрузка звуков
explosion_sound = pygame.mixer.Sound("explosion.wav")
spawn_sound = pygame.mixer.Sound("spawn.wav")

# Константы для планет
PLANET_SIZES = {
    'mercury': 15,
    'venus': 25,
    'earth': 25,
    'mars': 20,
    'jupiter': 60,
    'saturn': 50,
    'uranus': 35,
    'neptune': 35
}

PLANET_ORBITS = {
    'mercury': 200,
    'venus': 300,
    'earth': 400,
    'mars': 500,
    'jupiter': 700,
    'saturn': 900,
    'uranus': 1100,
    'neptune': 1300
}

PLANET_COLORS = {
    'mercury': (169, 169, 169),  # Серый
    'venus': (255, 198, 73),  # Желто-оранжевый
    'earth': (100, 149, 237),  # Голубой
    'mars': (188, 39, 50),  # Красно-коричневый
    'jupiter': (255, 223, 186),  # Бежевый
    'saturn': (238, 232, 205),  # Светло-желтый
    'uranus': (173, 216, 230),  # Светло-голубой
    'neptune': (0, 0, 128)  # Темно-синий
}

# Загрузка ресурсов
font = pygame.font.Font(None, 42)
bg_image = pygame.transform.scale(
    pygame.image.load("menubackground.jpg"),
    (WIDTH, HEIGHT)
)
explosion_sound = pygame.mixer.Sound("explosion.wav")
spawn_sound = pygame.mixer.Sound("spawn.wav")


class MenuButton:
    def __init__(self, y, text):
        self.width = 280
        self.height = 60
        self.x = WIDTH // 2 - self.width // 2
        self.y = y
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flag = False

    def draw(self, window):
        color = HOVER_COLOR if self.flag else BUTTON_COLOR
        pygame.draw.rect(window, color, self.rect, border_radius=15)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.flag = self.rect.collidepoint(mouse_pos)
        return self.flag

def main():
    """Создает меню"""
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Космическая игра")
    clock = pygame.time.Clock()

    buttons = [
        MenuButton(150, "Новая игра"),
        MenuButton(250, "Случайная галактика"),
        MenuButton(350, "Управление"),
        MenuButton(450, "Выход")
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.flag:
                        if i == 0:
                            main_game()
                        elif i == 1:
                            random_galaxy()
                        elif i == 2:
                            show_controls()
                        elif i == 3:
                            pygame.quit()
                            sys.exit()

        window.blit(bg_image, (0, 0))

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(window)

        pygame.display.flip()
        clock.tick(60)




class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, orbital_radius):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.radius = radius
        self.orbital_radius = orbital_radius
        self.velocity = [0, 0]
        self.mass = PLANET_MASS

        self.rect.center = (int(self.x), int(self.y))

    def update(self, sun):
        dx = sun.x - self.x
        dy = sun.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return

        force = G_CONSTANT * self.mass * sun.mass / (distance ** 2)
        angle = math.atan2(dy, dx)

        self.velocity[0] += (math.cos(angle) * force) / self.mass
        self.velocity[1] += (math.sin(angle) * force) / self.mass

        # Ограничение орбитальной скорости
        speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        max_speed = math.sqrt(G_CONSTANT * sun.mass / self.orbital_radius) * 1.5

        if speed > max_speed:
            self.velocity = [v * max_speed / speed for v in self.velocity]

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect.center = (int(self.x), int(self.y))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(5, 15)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        color = random.randint(150, 200)
        pygame.draw.circle(self.image, (color, color, color),
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

        # Случайная начальная позиция и скорость
        self.orbital_radius = random.randint(300, 800)
        angle = random.uniform(0, 2 * math.pi)
        self.x = WIDTH // 2 + self.orbital_radius * math.cos(angle)
        self.y = HEIGHT // 2 + self.orbital_radius * math.sin(angle)

        base_velocity = math.sqrt(G_CONSTANT * SUN_MASS / self.orbital_radius)
        speed_multiplier = random.uniform(0.7, 1.3)

        self.velocity = [
            -base_velocity * math.sin(angle) * speed_multiplier + random.uniform(-0.5, 0.5),
            base_velocity * math.cos(angle) * speed_multiplier + random.uniform(-0.5, 0.5)
        ]

        self.rect.center = (int(self.x), int(self.y))

    def update(self, sun):
        dx = sun.x - self.x
        dy = sun.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            force = G_CONSTANT * SUN_MASS / distance ** 2
            angle = math.atan2(dy, dx)

            self.velocity[0] += math.cos(angle) * force
            self.velocity[1] += math.sin(angle) * force

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect.center = (int(self.x), int(self.y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load("ship_off.png"),
            pygame.image.load("ship_on1.png"),
            pygame.image.load("ship_on2.png"),
            pygame.image.load("ship_on3.png"),
            pygame.image.load("ship_on4.png")
        ]
        self.sprites = [pygame.transform.scale(sprite, (60, 80)) for sprite in self.sprites]

        self.current_sprite = 0
        self.animation_speed = 0.2
        self.is_engine_on = False

        self.image = self.sprites[0]
        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = [0, 0]
        self.mass = 10
        self.radius = self.rect.width // 2

        self.rect.center = (int(x), int(y))

    def rotate(self, angle_change):
        self.angle += angle_change
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self):
        self.is_engine_on = True
        angle_rad = math.radians(-self.angle)

        acceleration_x = math.cos(angle_rad) * SHIP_ACCELERATION
        acceleration_y = math.sin(angle_rad) * SHIP_ACCELERATION

        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        speed = math.sqrt(sum(v * v for v in self.velocity))
        if speed > SHIP_MAX_SPEED:
            self.velocity = [v * SHIP_MAX_SPEED / speed for v in self.velocity]

    def update(self, sun):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotate(SHIP_ROTATION_SPEED)
        if keys[pygame.K_RIGHT]:
            self.rotate(-SHIP_ROTATION_SPEED)

        self.is_engine_on = keys[pygame.K_UP]
        if self.is_engine_on:
            self.accelerate()
            self.current_sprite += self.animation_speed
            if self.current_sprite >= 4:
                self.current_sprite = 1
            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.current_sprite = 0
            self.image = self.sprites[0]

        self.original_image = self.image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Применяем трение
        self.velocity = [v * SHIP_FRICTION for v in self.velocity]

        # Гравитация
        dx = sun.x - self.x
        dy = sun.y - self.y
        distance = max(math.sqrt(dx * dx + dy * dy), 100)  # Минимальное расстояние

        force = min(G_CONSTANT * self.mass * sun.mass / distance ** 2, 2.0)
        angle = math.atan2(dy, dx)

        max_gravity_acceleration = 0.5
        acceleration_x = (math.cos(angle) * force) / self.mass
        acceleration_y = (math.sin(angle) * force) / self.mass

        acceleration_magnitude = math.sqrt(acceleration_x ** 2 + acceleration_y ** 2)
        if acceleration_magnitude > max_gravity_acceleration:
            scale = max_gravity_acceleration / acceleration_magnitude
            acceleration_x *= scale
            acceleration_y *= scale

        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Ограничение максимального расстояния от центра
        dx = self.x - WIDTH // 2
        dy = self.y - HEIGHT // 2
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 3000:
            angle = math.atan2(dy, dx)
            self.x = WIDTH // 2 + math.cos(angle) * 3000
            self.y = HEIGHT // 2 + math.sin(angle) * 3000

        self.rect.center = (int(self.x), int(self.y))

    def check_collision(self, other_sprite):
        dx = self.x - other_sprite.x
        dy = self.y - other_sprite.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (self.radius + other_sprite.radius)


class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = POINT_RADIUS
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, TARGET_COLOR, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(200, 1500)
        self.x = WIDTH // 2 + math.cos(angle) * distance
        self.y = HEIGHT // 2 + math.sin(angle) * distance
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)


def draw_arrow(screen, ship_pos, target_pos, scale, camera_pos):
    dx = target_pos[0] - ship_pos[0]
    dy = target_pos[1] - ship_pos[1]
    angle = math.atan2(dy, dx)

    arrow_length = 30 * scale
    arrow_width = 15 * scale
    arrow_distance = 50 * scale

    screen_ship_x = (ship_pos[0] - camera_pos[0]) * scale + WIDTH * (1 - scale) / 2
    screen_ship_y = (ship_pos[1] - camera_pos[1]) * scale + HEIGHT * (1 - scale) / 2

    base_x = screen_ship_x + math.cos(angle) * arrow_distance
    base_y = screen_ship_y + math.sin(angle) * arrow_distance

    points = [
        (base_x + math.cos(angle) * arrow_length,
         base_y + math.sin(angle) * arrow_length),
        (base_x + math.cos(angle + 2.6) * arrow_width,
         base_y + math.sin(angle + 2.6) * arrow_width),
        (base_x + math.cos(angle - 2.6) * arrow_width,
         base_y + math.sin(angle - 2.6) * arrow_width)
    ]

    pygame.draw.polygon(screen, ARROW_COLOR, points)



def create_solar_system(all_sprites, planet_sprites):
    """Создает солнечную систему с планетами"""
    sun = Planet(WIDTH // 2, HEIGHT // 2, 80, YELLOW, 1)
    sun.mass = SUN_MASS
    sun.velocity = [0, 0]
    all_sprites.add(sun)

    for name, data in PLANET_ORBITS.items():
        angle = random.uniform(0, 2 * math.pi)
        x = WIDTH // 2 + data * math.cos(angle)
        y = HEIGHT // 2 + data * math.sin(angle)

        planet = Planet(x, y, PLANET_SIZES[name], PLANET_COLORS[name], data)
        orbital_velocity = math.sqrt(G_CONSTANT * SUN_MASS / data)

        planet.velocity = [
            -orbital_velocity * math.sin(angle),
            orbital_velocity * math.cos(angle)
        ]

        all_sprites.add(planet)
        planet_sprites.add(planet)

    return sun


def handle_collisions(ship, sun, planet_sprites, asteroid_sprites, target, mission_active, screen):
    """Обрабатывает все столкновения в игре"""
    if ship.check_collision(sun):
        return handle_crash(ship, target, mission_active, screen)

    for planet in planet_sprites:
        if ship.check_collision(planet):
            return handle_crash(ship, target, mission_active, screen)

    for asteroid in asteroid_sprites:
        if ship.check_collision(asteroid):
            asteroid.kill()
            return handle_crash(ship, target, mission_active, screen)

    return True, ship, target, mission_active


def handle_crash(ship, target, mission_active, screen):
    """Обрабатывает столкновение корабля"""
    explosion_sound.play()
    if mission_active:
        show_mission_failed(screen, "Столкновение! Миссия провалена!")
        if target:
            target.kill()
    ship.kill()
    return False, None, None, False


def show_mission_failed(screen, text):
    """Показывает сообщение о провале миссии"""
    defeat_text = font.render(text, True, (255, 0, 0))
    screen.blit(defeat_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def update_camera(ship, camera_x, camera_y):
    """Обновляет позицию камеры"""
    if ship:
        target_x = ship.x - WIDTH // 2
        target_y = ship.y - HEIGHT // 2
        camera_x += (target_x - camera_x) * CAMERA_SMOOTHNESS
        camera_y += (target_y - camera_y) * CAMERA_SMOOTHNESS
    return camera_x, camera_y


def draw_game(screen, all_sprites, camera_x, camera_y, scale, ship, target, mission_active, points_collected,
              time_left):
    """Отрисовывает все элементы игры"""
    screen.fill(BACKGROUND_COLOR)

    for sprite in all_sprites:
        draw_sprite(screen, sprite, camera_x, camera_y, scale)

    if mission_active and ship and target:
        draw_arrow(screen, (ship.x, ship.y), (target.x, target.y), scale, (camera_x, camera_y))
        draw_mission_info(screen, points_collected, time_left)


def draw_sprite(screen, sprite, camera_x, camera_y, scale):
    """Отрисовывает отдельный спрайт с учетом камеры и масштаба"""
    original_pos = sprite.rect.center
    screen_x = (sprite.x - camera_x) * scale + WIDTH * (1 - scale) / 2
    screen_y = (sprite.y - camera_y) * scale + HEIGHT * (1 - scale) / 2

    scaled_image = pygame.transform.scale(
        sprite.image,
        (int(sprite.image.get_width() * scale),
         int(sprite.image.get_height() * scale))
    )

    sprite.rect.centerx = int(screen_x)
    sprite.rect.centery = int(screen_y)
    screen.blit(scaled_image, sprite.rect)
    sprite.rect.center = original_pos


def draw_mission_info(screen, points_collected, time_left):
    """Отрисовывает информацию о миссии"""
    points_text = font.render(f"Точки: {points_collected}/{MISSION_POINTS}", True, WHITE)
    time_text = font.render(f"Время: {time_left}", True, WHITE)
    screen.blit(points_text, (10, 10))
    screen.blit(time_text, (10, 50))


def main_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Инициализация игровых объектов
    all_sprites = pygame.sprite.Group()
    planet_sprites = pygame.sprite.Group()
    asteroid_sprites = pygame.sprite.Group()

    sun = create_solar_system(all_sprites, planet_sprites)

    # Инициализация игровых переменных
    camera_x = camera_y = 0
    current_scale = INITIAL_SCALE
    ship = None

    # Переменные миссии
    mission_active = False
    target = None
    points_collected = 0
    time_left = 0
    mission_start_time = 0

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and not ship:
                    ship = spawn_ship(pygame.mouse.get_pos(), current_scale, camera_x, camera_y)
                    all_sprites.add(ship)
                    current_scale = CAMERA_SCALE
                    spawn_sound.play()

                elif event.key == pygame.K_x and ship:
                    if mission_active and target:
                        target.kill()
                        mission_active = False
                    ship.kill()
                    ship = None
                    camera_x = camera_y = 0
                    current_scale = INITIAL_SCALE

                elif event.key == pygame.K_m and ship and not mission_active:
                    mission_active, target, points_collected, time_left, mission_start_time = start_mission(all_sprites)

        # Спавн астероидов
        if len(asteroid_sprites) < MAX_ASTEROIDS and random.random() < ASTEROID_SPAWN_RATE:
            new_asteroid = Asteroid()
            all_sprites.add(new_asteroid)
            asteroid_sprites.add(new_asteroid)

        # Обновление состояния игры
        all_sprites.update(sun)

        if ship:
            # Проверка столкновений
            ship_alive, ship, target, mission_active = handle_collisions(
                ship, sun, planet_sprites, asteroid_sprites, target, mission_active, screen
            )
            if not ship_alive:
                camera_x = camera_y = 0
                current_scale = INITIAL_SCALE
                continue

            # Обновление камеры
            camera_x, camera_y = update_camera(ship, camera_x, camera_y)

        # Обновление миссии
        if mission_active:
            mission_active, target, points_collected, time_left = update_mission(
                mission_active, target, points_collected, time_left,
                mission_start_time, ship, screen, all_sprites
            )

        # Отрисовка
        draw_game(screen, all_sprites, camera_x, camera_y, current_scale,
                  ship, target, mission_active, points_collected, time_left)

        pygame.display.flip()
        clock.tick(FPS)


def spawn_ship(mouse_pos, scale, camera_x, camera_y):
    """Создает корабль в указанной позиции с учетом масштаба и камеры"""
    mouse_x, mouse_y = mouse_pos
    real_x = (mouse_x - WIDTH * (1 - scale) / 2) / scale + camera_x
    real_y = (mouse_y - HEIGHT * (1 - scale) / 2) / scale + camera_y
    return Spaceship(real_x, real_y)


def start_mission(all_sprites):
    """Инициализирует новую миссию"""
    target = Target()
    all_sprites.add(target)
    return True, target, 0, MISSION_TIME, pygame.time.get_ticks()


def update_mission(mission_active, target, points_collected, time_left, mission_start_time, ship, screen, all_sprites):
    """Обновляет состояние миссии"""
    global MISSION_TIME

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - mission_start_time) // 1000
    time_left = MISSION_TIME - elapsed_time

    if time_left <= 0:
        show_mission_failed(screen, "Время вышло! Миссия провалена!")
        if target:
            target.kill()
        return False, None, points_collected, 0

    if ship and target and ship.check_collision(target):
        points_collected += 1
        target.kill()

        if points_collected >= MISSION_POINTS:
            total_time = (pygame.time.get_ticks() - mission_start_time) // 1000
            victory_text = font.render("Миссия выполнена!", True, (0, 255, 0))
            time_text = font.render(f"Время прохождения: {total_time} сек", True, (0, 255, 0))
            screen.blit(victory_text, (WIDTH // 2 - 100, HEIGHT // 2))
            screen.blit(time_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False, None, points_collected, time_left
        else:
            target = Target()
            all_sprites.add(target)
            MISSION_TIME += TIME_BONUS
            return True, target, points_collected, time_left

    return mission_active, target, points_collected, time_left


def random_galaxy():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Инициализация групп спрайтов
    all_sprites = pygame.sprite.Group()
    planet_sprites = pygame.sprite.Group()
    asteroid_sprites = pygame.sprite.Group()

    # Создание случайной звезды
    star_size = random.randint(60, 100)
    star_color = (random.randint(200, 255), random.randint(150, 255), 0)
    sun = Planet(WIDTH // 2, HEIGHT // 2, star_size, star_color, 1)
    sun.mass = SUN_MASS
    all_sprites.add(sun)

    # Генерация случайных планет
    create_random_planets(all_sprites, planet_sprites)

    # Инициализация игровых переменных
    camera_x = camera_y = 0
    current_scale = INITIAL_SCALE
    ship = None

    # Переменные миссии
    mission_active = False
    target = None
    points_collected = 0
    time_left = 0
    mission_start_time = 0

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and not ship:
                    ship = spawn_ship(pygame.mouse.get_pos(), current_scale, camera_x, camera_y)
                    all_sprites.add(ship)
                    current_scale = CAMERA_SCALE
                    spawn_sound.play()

                elif event.key == pygame.K_x and ship:
                    if mission_active and target:
                        target.kill()
                        mission_active = False
                    ship.kill()
                    ship = None
                    camera_x = camera_y = 0
                    current_scale = INITIAL_SCALE

                elif event.key == pygame.K_m and ship and not mission_active:
                    mission_active, target, points_collected, time_left, mission_start_time = start_mission(all_sprites)

        # Спавн астероидов
        spawn_asteroids(all_sprites, asteroid_sprites)

        # Обновление состояния игры
        all_sprites.update(sun)

        if ship:
            # Проверка столкновений
            ship_alive, ship, target, mission_active = handle_collisions(
                ship, sun, planet_sprites, asteroid_sprites, target, mission_active, screen
            )
            if not ship_alive:
                camera_x = camera_y = 0
                current_scale = INITIAL_SCALE
                continue

            # Обновление камеры
            camera_x, camera_y = update_camera(ship, camera_x, camera_y)

        # Обновление миссии
        if mission_active:
            mission_active, target, points_collected, time_left = update_mission(
                mission_active, target, points_collected, time_left,
                mission_start_time, ship, screen, all_sprites
            )

        # Отрисовка
        draw_game(screen, all_sprites, camera_x, camera_y, current_scale,
                  ship, target, mission_active, points_collected, time_left)

        pygame.display.flip()
        clock.tick(FPS)


def create_random_planets(all_sprites, planet_sprites):
    """Создает случайные планеты для другой галактики"""
    num_planets = random.randint(4, 10)
    min_orbit = 200
    max_orbit = 1500
    orbit_step = (max_orbit - min_orbit) / num_planets

    for i in range(num_planets):
        # Генерация параметров планеты
        orbit_radius = min_orbit + (orbit_step * i) + random.randint(-50, 50)
        size = random.randint(15, 40)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

        # Создание планеты
        angle = random.uniform(0, 2 * math.pi)
        x = WIDTH // 2 + orbit_radius * math.cos(angle)
        y = HEIGHT // 2 + orbit_radius * math.sin(angle)

        planet = Planet(x, y, size, color, orbit_radius)

        # Установка орбитальной скорости
        orbital_velocity = math.sqrt(G_CONSTANT * SUN_MASS / orbit_radius)
        speed_multiplier = random.uniform(0.9, 1.1)

        planet.velocity = [
            -orbital_velocity * math.sin(angle) * speed_multiplier,
            orbital_velocity * math.cos(angle) * speed_multiplier
        ]

        planet.mass = (size / 20) * PLANET_MASS

        all_sprites.add(planet)
        planet_sprites.add(planet)


def spawn_asteroids(all_sprites, asteroid_sprites):
    """Создает новые астероиды если их недостаточно"""
    if len(asteroid_sprites) < MAX_ASTEROIDS and random.random() < ASTEROID_SPAWN_RATE:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroid_sprites.add(asteroid)


def show_controls():
    """Показывает окно с информацией об управлении"""
    try:
        with open("rules_and_control.txt", "r", encoding='utf-8') as file:
            rules_text = file.readlines()
    except FileNotFoundError:
        rules_text = ["Файл rules.txt не найден!"]

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Создаем кнопку "Назад"
    back_button = MenuButton(HEIGHT - 100, "Назад")

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.flag:
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        window.blit(bg_image, (0, 0))

        # Отрисовка текста правил
        y_offset = 50
        for line in rules_text:
            if line.strip():  # Пропускаем пустые строки
                text_surface = font.render(line.strip(), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
                window.blit(text_surface, text_rect)
                y_offset += 40

        # Отрисовка кнопки "Назад"
        back_button.check_hover(mouse_pos)
        back_button.draw(window)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
