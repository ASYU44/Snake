import time
import pygame
import random

# initialize pygame
pygame.init()


# Define the dimensions of screen object(width,height)


clock = pygame.time.Clock()

SCALE = 2  # int
LENGTH = 15
screen = pygame.display.set_mode((30 * SCALE * LENGTH, 30 * SCALE * LENGTH))

# assets
snake_parts = pygame.transform.scale(pygame.image.load('assets\\player\\snake_parts.png'), (30 * 7 * SCALE, 30 * SCALE))

# fruits
fruits = [pygame.transform.scale(pygame.image.load('assets\\fruits\\apple.png'),
                                 (30 * 12 * SCALE, 30 * SCALE)),
          pygame.transform.scale(pygame.image.load('assets\\fruits\\cherry.png'),
                                 (30 * 12 * SCALE, 30 * SCALE)),
          pygame.transform.scale(pygame.image.load('assets\\fruits\\hamburger.png'),
                                 (30 * 12 * SCALE, 30 * SCALE)),
          pygame.transform.scale(pygame.image.load('assets\\fruits\\bunny.png'),
                                 (30 * 12 * SCALE, 30 * SCALE)),
          pygame.transform.scale(pygame.image.load('assets\\fruits\\duck.png'),
                                 (30 * 12 * SCALE, 30 * SCALE)),
          pygame.transform.scale(pygame.image.load('assets\\fruits\\orange.png'),
                                 (30 * 12 * SCALE, 30 * SCALE))]

# obstacles
obstacles_surfaces = [pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone.png'),
                                             (30 * SCALE, 30 * SCALE)),
                      pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone 2.png'),
                                             (30 * SCALE, 30 * SCALE)),
                      pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone 3.png'),
                                             (30 * SCALE, 30 * SCALE)),
                      pygame.transform.scale(pygame.image.load('assets\\obstacles\\box.png'),
                                             (30 * SCALE, 30 * SCALE)),
                      pygame.transform.scale(pygame.image.load('assets\\obstacles\\stem.png'),
                                             (30 * SCALE, 30 * SCALE))]

# terrain
terrain_surfaces = [pygame.transform.scale(pygame.image.load('assets\\terrain\\bush.png'), (30 * SCALE, 30 * SCALE)),
                    pygame.transform.scale(pygame.image.load('assets\\terrain\\mushroom.png'),
                                           (30 * SCALE, 30 * SCALE)),
                    pygame.transform.scale(pygame.image.load('assets\\terrain\\tree.png'), (30 * SCALE, 30 * SCALE))]

# fonts
Score_font = pygame.font.Font('assets\\fonts\\Exo-Black.otf', 50)
Waiting_font = pygame.font.Font('assets\\fonts\\Exo-Black.otf', 100)


def clip(surface: pygame.Surface, x: int, y: int, x_size: int, y_size: int):  # Get a part of the image
    handle_surface = surface.copy()  # Sprite that will get process later
    clip_rect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
    handle_surface.set_clip(clip_rect)  # Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip())  # Get subsurface ace
    return image.copy()  # Return


def slicing_surface(image, num_slices_x: int, num_slices_y: int) -> list:

    if (image.get_width() % num_slices_x != 0 or image.get_height() % num_slices_y != 0
            or num_slices_y < 1 or num_slices_x < 1):
        return []

    image_width = image.get_width()
    image_height = image.get_height()
    frames = []
    for slice_x in range(num_slices_x):
        for slice_y in range(num_slices_y):
            frame = clip(image, slice_x * image_width / num_slices_x, slice_y * image_height / num_slices_y,
                         image_width / num_slices_x, image_height / num_slices_y)
            frames.append(frame)
    return frames


snake_parts = slicing_surface(snake_parts, 7, 1)
for fruit_num in range(len(fruits)):
    fruits[fruit_num] = slicing_surface(fruits[fruit_num], 12, 1)


class Fruit:
    def __init__(self, x: int, y: int, kind: int = -1):
        self.x = x
        self.y = y
        if kind <= -1 or kind >= len(fruits):
            self.kind = random.randint(0, len(fruits) - 1)

    def __str__(self):
        return (f"(X, Y) - ({self.x}, {self.y})\n"
                f"Kind: '{self.kind}'")


class Obstacle:
    def __init__(self, x: int, y: int, kind: int = -1):
        self.x = x
        self.y = y
        if kind <= -1 or kind >= len(fruits):
            self.kind = random.randint(0, len(obstacles_surfaces) - 1)

    def __str__(self):
        return (f"(X, Y) - ({self.x}, {self.y})\n"
                f"Kind: '{self.kind}'")


class Terrain:
    def __init__(self, x: int, y: int, kind: int = -1):
        self.x = x
        self.y = y
        if kind <= -1 or kind >= len(terrain_surfaces):
            self.kind = random.randint(0, len(terrain_surfaces) - 1)

    def __str__(self):
        return (f"(X, Y) - ({self.x}, {self.y})\n"
                f"Kind: '{self.kind}'")


class SnakePart:
    def __init__(self, x: int, y: int, kind: str):
        self.x = x
        self.y = y
        self.kind = kind

    def __str__(self):
        return (f"(X, Y) - ({self.x}, {self.y})\n"
                f"Kind: '{self.kind}'")


class Snake:
    def __init__(self, x: int, y: int, point: str, length: int):

        if length < 3:
            print('Error length too short')
            return
        self.parts = []
        self.x = x
        self.y = y
        self.point = point
        self.LENGTH = length  # starting length

        self.parts.append(SnakePart(x - (length - 1), y, 'TAIL' + point))
        for i in range(length - 2, 0, -1):
            self.parts.append(SnakePart(x - i, y, 'BODY' + point))
        self.parts.append(SnakePart(x, y, 'HEAD' + point))

    def update_snake(self, ate: bool = False) -> bool:
        if not ate:
            self.parts.pop(0)
            self.parts[0].kind = 'TAIL' + self.parts[0].kind[-1]

        if self.point == self.parts[-1].kind[-1]:
            self.parts[-1].kind = 'BODY' + self.point
        else:
            self.parts[-1].kind = 'CORNER' + self.parts[-2].kind[-1] + self.point
        if self.point == '>':
            self.x += 1
        elif self.point == '<':
            self.x -= 1
        elif self.point == 'v':
            self.y += 1
        elif self.point == '^':
            self.y -= 1
        self.parts.append(SnakePart(self.x, self.y, 'HEAD' + self.point))

        for part in self.parts[:-1]:
            if part.x == self.x and part.y == self.y:
                return True


def draw_snake(snake: Snake):
    for part in snake.parts:
        if part.kind == 'TAIL<':
            screen.blit(snake_parts[3], (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'TAIL>':
            screen.blit(pygame.transform.flip(snake_parts[3], True, False), (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'TAILv':
            screen.blit(pygame.transform.flip(snake_parts[6], False, True), (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'TAIL^':
            screen.blit(snake_parts[6], (part.x * SCALE * 30, part.y * SCALE * 30))

        elif part.kind[:4] == 'BODY':
            if part.kind[-1] == 'v' or part.kind[-1] == '^':
                screen.blit(snake_parts[5], (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind[-1] == '<' or part.kind[-1] == '>':
                screen.blit(snake_parts[0], (part.x * SCALE * 30, part.y * SCALE * 30))
            else:
                print('ERROR: ' + part.kind)

        elif part.kind == 'HEAD>':
            screen.blit(snake_parts[1], (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'HEAD<':
            screen.blit(pygame.transform.flip(snake_parts[1], True, False), (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'HEADv':
            screen.blit(pygame.transform.flip(snake_parts[2], False, True), (part.x * SCALE * 30, part.y * SCALE * 30))
        elif part.kind == 'HEAD^':
            screen.blit(snake_parts[2], (part.x * SCALE * 30, part.y * SCALE * 30))

        elif part.kind[:-2] == 'CORNER':
            if part.kind[-2:] == '<^' or part.kind[-2:] == 'v>':
                screen.blit(pygame.transform.flip(snake_parts[4], True, False),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind[-2:] == '<v' or part.kind[-2:] == '^>':
                screen.blit(pygame.transform.flip(snake_parts[4], True, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind[-2:] == '>v' or part.kind[-2:] == '^<':
                screen.blit(pygame.transform.flip(snake_parts[4], False, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind[-2:] == '>^' or part.kind[-2:] == 'v<':
                screen.blit(snake_parts[4], (part.x * SCALE * 30, part.y * SCALE * 30))
            else:
                print('ERROR: ' + part.kind)
        else:
            print('ERROR: ' + part.kind)


def background(color1: tuple[int, int, int], color2: tuple[int, int, int]):
    screen.fill((0, 102, 0))
    x = y = SCALE * 30
    is_color_1 = True
    while True:
        if x >= (LENGTH - 1) * SCALE * 30:
            x = SCALE * 30
            y += 30 * SCALE
            if LENGTH % 2 == 0:
                is_color_1 = not is_color_1
            if y >= (LENGTH - 1) * SCALE * 30:
                break
        if is_color_1:
            screen.fill(color1, (x, y, SCALE * 30, SCALE * 30))
        else:
            screen.fill(color2, (x, y, SCALE * 30, SCALE * 30))
        x += 30 * SCALE
        is_color_1 = not is_color_1


def print_score(player: Snake):
    score_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (255, 255, 255))
    width, height = score_surface.get_size()

    score_outline_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (0, 0, 0))
    screen.blit(score_outline_surface, (LENGTH * 15 * SCALE - SCALE - width / 2, SCALE * 16 - height / 2))
    score_outline_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (0, 0, 0))
    screen.blit(score_outline_surface, (LENGTH * 15 * SCALE + SCALE - width / 2, SCALE * 16 - height / 2))
    score_outline_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (0, 0, 0))
    screen.blit(score_outline_surface, (LENGTH * 15 * SCALE + SCALE - width / 2, SCALE * 14 - height / 2))
    score_outline_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (0, 0, 0))
    screen.blit(score_outline_surface, (LENGTH * 15 * SCALE - SCALE - width / 2, SCALE * 14 - height / 2))

    screen.blit(score_surface, (LENGTH * 15 * SCALE - width / 2, SCALE * 15 - height / 2))


def is_snake(snake: Snake, x: int, y: int) -> bool:
    for part in snake.parts:
        if x == part.x and y == part.y:
            return True
    return False


def is_in_square(squares: list, x: int, y: int) -> bool:
    for square in squares:
        if (x, y) == (square.x, square.y):
            return True
    return False


def draw_terrain(terrains: list) -> None:
    for square in terrains:
        screen.blit(terrain_surfaces[square.kind], (square.x * SCALE * 30, square.y * SCALE * 30))


def main():
    pygame.display.set_icon(snake_parts[1])
    pygame.display.set_caption('SNAKE by ASYU')
    running = True
    player = Snake(int(LENGTH / 2) + 1, int(LENGTH / 2) + 1, '>', 4)
    ate = False
    obstacles = []
    terrains = []

    num_terrain = random.randint(1, LENGTH)
    for counter_grass in range(num_terrain):
        terrain_x = random.randint(1, LENGTH - 2)
        terrain_y = random.randint(1, LENGTH - 2)
        if not is_in_square(terrains, terrain_x, terrain_y):
            terrains.append(Terrain(terrain_x, terrain_y))
    tick = 0
    fruit_x = random.randint(1, LENGTH - 2)
    fruit_y = random.randint(1, LENGTH - 2)

    while is_snake(player, fruit_x, fruit_y) or is_in_square(obstacles, fruit_x, fruit_y):
        fruit_x = random.randint(1, LENGTH - 2)
        fruit_y = random.randint(1, LENGTH - 2)

    fruit = Fruit(fruit_x, fruit_y)
    for terrain in terrains:
        if (terrain.x, terrain.y) == (fruit_x, fruit_y):
            terrains.remove(terrain)
    try:

        for sec in range(3, 0, -1):  # waiting loop
            for event in pygame.event.get():
                # Check for QUIT event
                if event.type == pygame.QUIT:
                    running = False
            if not running:
                break
            background((0, 255, 128), (0, 204, 102))
            draw_terrain(terrains)
            draw_snake(player)
            print_score(player)
            num_surface = Waiting_font.render(f'{sec}', False, (255, 0, 0))
            width, height = num_surface.get_size()
            screen.blit(num_surface, (LENGTH * 15 * SCALE - width / 2, LENGTH * SCALE * 15 - height / 2))
            pygame.display.update()  # Updating Screen
            clock.tick(1)

        while running:  # main loop
            tick += 1
            if tick >= 100000000000000:
                tick = 0
            # clearing screen from all thing by filling screen with background

            background((0, 255, 128), (0, 204, 102))
            draw_terrain(terrains)
            for obstacle in obstacles:
                screen.blit(obstacles_surfaces[obstacle.kind], (obstacle.x * SCALE * 30, obstacle.y * SCALE * 30))

            if ate:
                fruit_x = random.randint(1, LENGTH - 2)
                fruit_y = random.randint(1, LENGTH - 2)

                while is_snake(player, fruit_x, fruit_y) or is_in_square(obstacles, fruit_x, fruit_y):
                    fruit_x = random.randint(1, LENGTH - 2)
                    fruit_y = random.randint(1, LENGTH - 2)

                fruit = Fruit(fruit_x, fruit_y)
                for terrain in terrains:
                    if (terrain.x, terrain.y) == (fruit_x, fruit_y):
                        terrains.remove(terrain)

                if (len(player.parts) - player.LENGTH) % 3 == 0:
                    stone_x = random.randint(1, LENGTH - 2)
                    stone_y = random.randint(1, LENGTH - 2)
                    try_counter = 0
                    while (abs(stone_x - player.x) <= 3 or abs(stone_y - player.y) <= 3 or
                           is_in_square(obstacles, stone_x, stone_y)
                           or stone_x == fruit_x and stone_y == fruit_y):
                        stone_x = random.randint(1, LENGTH - 2)
                        stone_y = random.randint(1, LENGTH - 2)
                        try_counter += 1
                        if try_counter >= 10:
                            break
                    if try_counter < 10:
                        if is_in_square(terrains, stone_x, stone_y):
                            for terrain in terrains:
                                if (terrain.x, terrain.y) == (stone_x, stone_y):
                                    terrains.remove(terrain)
                        obstacles.append(Obstacle(stone_x, stone_y))

            failed = player.update_snake(ate)
            failed = player.x <= 0 or player.x >= LENGTH - 1 or player.y <= 0 or player.y >= LENGTH - 1 or failed
            for obstacle in obstacles:
                failed = failed or (player.x, player.y) == (obstacle.x, obstacle.y)
                if failed:
                    break

            ate = is_snake(player, fruit_x, fruit_y)
            draw_snake(player)
            print_score(player)
            if not ate:
                screen.blit(fruits[fruit.kind][tick % 12], (fruit.x * 30 * SCALE, fruit.y * 30 * SCALE))

            if failed:
                break
            pygame.display.update()  # Updating Screen

            clock.tick(9)

            for event in pygame.event.get():
                # Check for QUIT event
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if player.point != '<':
                            player.point = '>'
                            break
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if player.point != '>':
                            player.point = '<'
                            break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if player.point != '^':
                            player.point = 'v'
                            break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if player.point != 'v':
                            player.point = '^'
                            break

        if running:
            text_surface = Score_font.render(f'YOUR SCORE IS:', False, (255, 0, 0))
            width_text, height_text = text_surface.get_size()
            screen.blit(text_surface, (LENGTH * 15 * SCALE - width_text / 2, LENGTH * SCALE * 15 - height_text / 2))
            score_surface = Score_font.render(f'{len(player.parts) - player.LENGTH}', False, (255, 0, 0))
            width_score, height_score = score_surface.get_size()
            screen.blit(score_surface,
                        (LENGTH * 15 * SCALE - width_score / 2, LENGTH * SCALE * 15 - height_score / 2 + height_text))
            pygame.display.update()  # Updating Screen
            time.sleep(2)

    except KeyboardInterrupt:
        print('Game Crashed')
    try:
        # quit pygame
        pygame.display.quit()
    except pygame.error:
        pass


if __name__ == '__main__':
    main()
