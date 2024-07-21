# ASYU made this Game

# imports
import pygame
import random
import clip_and_slice

# initialize pygame
pygame.init()

# define pygame Clock
clock = pygame.time.Clock()

# stats
SCALE = 2  # int (may work with float or double but more likely to crash) (30 / LENGTH is recommended)
LENGTH = 15  # LENGTH of screen (30 / SCALE is recommended)
BORDERS = False  # change for setting BORDERS to True
IMMORTAL = False  # change for immortality
TICKS_PER_SEC = 10  # 7 to 10 are recommended (choose a number between 1 and 20 otherwise it will do an instant kill).
TERRAIN_PER_TICKS = 20  # greater than 1 (20 is recommended)
NUM_FRUITS = 5  # Num of fruits in game
SAFE_RADIUS = 2  # should not spawn any obstacles in this radius (snake head is the middle)  (2 is recommended)
STARTING_LENGTH = 4  # starting in Length of that value between 3 and LENGTH - 2 (4 is recommended)
DIFFICULTY = 5  # between 1 and 10 (6 and 5 are recommended)
SNAKE_KIND = -1  # kind of snake for random put negative number or a very large number

# setting STATS to appropriate values
SCALE = int(SCALE)  # preventing it from not being int
LENGTH = int(LENGTH)  # preventing it from not being int
TERRAIN_PER_TICKS = max(TERRAIN_PER_TICKS, 1)  # preventing the TERRAIN_PER_TICKS to be less than 1

if TICKS_PER_SEC == 0:  # preventing from TICKS_IN_SEC to be less than 1
    TICKS_PER_SEC += 1
TICKS_IN_SEC = abs(TICKS_PER_SEC)

# using BORDERS as int in some cases so this line should prevent BORDERS to be something else then 1 or 0
BORDERS = bool(BORDERS)

STARTING_LENGTH = max(3, min(LENGTH - 2 - BORDERS * 2, STARTING_LENGTH))  # preventing from being a bad length

DIFFICULTY = 11 - max(1, min(10, DIFFICULTY))  # setting difficulty to its purpose in code

# Define the dimensions of screen object(width,height)
screen = pygame.display.set_mode((30 * SCALE * LENGTH, 30 * SCALE * LENGTH))

# snake assets
snakes_parts = [pygame.transform.scale(pygame.image.load('assets\\player\\Blue_snake.png'),
                                       (30 * 7 * SCALE, 30 * SCALE)),
                pygame.transform.scale(pygame.image.load('assets\\player\\Invisible_snake.png'),
                                       (30 * 7 * SCALE, 30 * SCALE)),
                pygame.transform.scale(pygame.image.load('assets\\player\\Cyan_Green_snake.png'),
                                       (30 * 7 * SCALE, 30 * SCALE)),
                pygame.transform.scale(pygame.image.load('assets\\player\\Human_snake.png'),
                                       (30 * 7 * SCALE, 30 * SCALE))]

fruits_surfaces = {'apple': pygame.transform.scale(pygame.image.load('assets\\fruits\\apple.png'),
                                                   (30 * 12 * SCALE, 30 * SCALE)),
                   'cherry': pygame.transform.scale(pygame.image.load('assets\\fruits\\cherry.png'),
                                                    (30 * 12 * SCALE, 30 * SCALE)),
                   'hamburger': pygame.transform.scale(pygame.image.load('assets\\fruits\\hamburger.png'),
                                                       (30 * 12 * SCALE, 30 * SCALE)),
                   'bunny': pygame.transform.scale(pygame.image.load('assets\\fruits\\bunny.png'),
                                                   (30 * 12 * SCALE, 30 * SCALE)),
                   'duck': pygame.transform.scale(pygame.image.load('assets\\fruits\\duck.png'),
                                                  (30 * 12 * SCALE, 30 * SCALE)),
                   'chicken': pygame.transform.scale(pygame.image.load('assets\\fruits\\chicken.png'),
                                                     (30 * 8 * SCALE, 30 * SCALE)),
                   'orange': pygame.transform.scale(pygame.image.load('assets\\fruits\\orange.png'),
                                                    (30 * 12 * SCALE, 30 * SCALE))}

# obstacles assets
obstacles_surfaces = {'stone': pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone.png'),
                                                      (30 * SCALE, 30 * SCALE)),
                      'stone 2': pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone 2.png'),
                                                        (30 * SCALE, 30 * SCALE)),
                      'stone 3': pygame.transform.scale(pygame.image.load('assets\\obstacles\\stone 3.png'),
                                                        (30 * SCALE, 30 * SCALE)),
                      'box': pygame.transform.scale(pygame.image.load('assets\\obstacles\\box.png'),
                                                    (30 * SCALE, 30 * SCALE)),
                      'stem': pygame.transform.scale(pygame.image.load('assets\\obstacles\\stem.png'),
                                                     (30 * SCALE, 30 * SCALE))}

# terrain assets
terrain_surfaces = {'bush': pygame.transform.scale(pygame.image.load('assets\\terrain\\bush.png'),
                                                   (30 * SCALE, 30 * SCALE)),
                    'mushroom': pygame.transform.scale(pygame.image.load('assets\\terrain\\mushroom.png'),
                                                       (30 * SCALE, 30 * SCALE)),
                    'tree': pygame.transform.scale(pygame.image.load('assets\\terrain\\tree.png'),
                                                   (30 * SCALE, 30 * SCALE))}

# fonts
Score_font = pygame.font.Font('assets\\fonts\\Exo-Black.otf', 25 * SCALE)
Waiting_font = pygame.font.Font('assets\\fonts\\Exo-Black.otf', 50 * SCALE)

# sounds assets
eating_sound = pygame.mixer.Sound('assets\\Sounds\\Eating_voice.mp3')
background_sound = pygame.mixer.Sound('assets\\Sounds\\background_voice.mp3')
background_sound.set_volume(0.3)
losing_sound = pygame.mixer.Sound('assets\\Sounds\\losing_voice.mp3')

for snake_parts in range(len(snakes_parts)):
    snakes_parts[snake_parts] = clip_and_slice.slicing_surface(snakes_parts[snake_parts],
                                                               int(snakes_parts[snake_parts].get_width() / (
                                                                       30 * SCALE)),
                                                               int(snakes_parts[snake_parts].get_height() / (
                                                                       30 * SCALE)))
for fruit_key in fruits_surfaces:
    fruits_surfaces[fruit_key] = clip_and_slice.slicing_surface(fruits_surfaces[fruit_key],
                                                                int(fruits_surfaces[fruit_key].get_width() / (
                                                                        30 * SCALE)),
                                                                int(fruits_surfaces[fruit_key].get_height() / (
                                                                        30 * SCALE)))


class Square:
    def __init__(self, x: int, y: int, kind: str) -> None:
        self.x = x
        self.y = y
        self.kind = kind

    def __str__(self) -> str:
        type_ = str(type(self))[:-2]
        type_ = type_[17:]
        return (f"{type_}\n(X, Y) - ({self.x}, {self.y})\n"
                f"Kind: '{self.kind}'")


class SnakePart(Square):
    def __init__(self, x: int, y: int, kind: str) -> None:
        super().__init__(x, y, kind)


class Snake:
    def __init__(self, x: int, y: int, kind: int = -1, point: str = '^', length: int = 3) -> None:

        self.parts = []
        self.x = x
        self.y = y
        if 0 <= kind < len(snakes_parts):  # Snake kind cannot be greater than the last index of snake_parts
            self.kind = kind
        else:
            self.kind = random.randint(0, len(snakes_parts) - 1)

        if point not in '<>^v':
            print('ERROR: ' + point)
            self.point = '>'
        else:
            self.point = point

        self.LENGTH = max(3, length)  # starting length can't be below 3

        if self.point == '<':
            self.parts.append(SnakePart(x + (self.LENGTH - 1), y, 'TAIL' + point))
            for i in range(self.LENGTH - 2, 0, -1):
                self.parts.append(SnakePart(x + i, y, 'BODY' + point))
        elif self.point == '>':
            self.parts.append(SnakePart(x - (self.LENGTH - 1), y, 'TAIL' + point))
            for i in range(self.LENGTH - 2, 0, -1):
                self.parts.append(SnakePart(x - i, y, 'BODY' + point))
        elif self.point == 'v':
            self.parts.append(SnakePart(x, y - (self.LENGTH - 1), 'TAIL' + point))
            for i in range(self.LENGTH - 2, 0, -1):
                self.parts.append(SnakePart(x, y - i, 'BODY' + point))
        elif self.point == '^':
            self.parts.append(SnakePart(x, y + (self.LENGTH - 1), 'TAIL' + point))
            for i in range(self.LENGTH - 2, 0, -1):
                self.parts.append(SnakePart(x, y + i, 'BODY' + point))

        self.parts.append(SnakePart(x, y, 'HEAD' + point))

    def __str__(self) -> str:
        str_parts = list([str(part) for part in self.parts])
        return '\n------------------\n' + '\n\n'.join(str_parts) + '\n------------------\n'

    def update_snake(self, game_length: int, ate: bool = False) -> bool:
        """
        update the snake on board
        returns if snake touched himself
        """
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

        if self.x < 0:
            self.x += game_length
        elif self.x >= game_length:
            self.x -= game_length
        if self.y < 0:
            self.y += game_length
        else:
            self.y = self.y % game_length

        failed = self.is_snake(self.x, self.y)  # checking about anything but the Head because we haven't added it yet
        self.parts.append(SnakePart(self.x, self.y, 'HEAD' + self.point))  # adding the new head
        return failed

    def is_snake(self, x: int, y: int) -> bool:
        for part in self.parts:
            if (x, y) == (part.x, part.y):
                return True
        return False

    def draw_snake(self) -> None:
        for part in self.parts:
            if part.kind == 'TAIL<':
                screen.blit(snakes_parts[self.kind][3], (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'TAIL>':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][3], True, False),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'TAILv':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][6], False, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'TAIL^':
                screen.blit(snakes_parts[self.kind][6], (part.x * SCALE * 30, part.y * SCALE * 30))

            elif part.kind == 'BODYv' or part.kind == 'BODY^':
                screen.blit(snakes_parts[self.kind][5], (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'BODY>' or part.kind == 'BODY<':
                screen.blit(snakes_parts[self.kind][0], (part.x * SCALE * 30, part.y * SCALE * 30))

            elif part.kind == 'HEAD>':
                screen.blit(snakes_parts[self.kind][1], (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'HEAD<':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][1], True, False),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'HEADv':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][2], False, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'HEAD^':
                screen.blit(snakes_parts[self.kind][2], (part.x * SCALE * 30, part.y * SCALE * 30))

            elif part.kind == 'CORNER<^' or part.kind == 'CORNERv>':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][4], True, False),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'CORNER<v' or part.kind == 'CORNER^>':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][4], True, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'CORNER>v' or part.kind == 'CORNER^<':
                screen.blit(pygame.transform.flip(snakes_parts[self.kind][4], False, True),
                            (part.x * SCALE * 30, part.y * SCALE * 30))
            elif part.kind == 'CORNER>^' or part.kind == 'CORNERv<':
                screen.blit(snakes_parts[self.kind][4], (part.x * SCALE * 30, part.y * SCALE * 30))

            else:
                print(f'ERROR: {part.kind} is not a kind of part')


class Fruit(Square):
    def __init__(self, x: int, y: int, kind: str = '') -> None:
        if kind in fruits_surfaces:
            super().__init__(x, y, kind)
        else:
            super().__init__(x, y, list(fruits_surfaces.keys())[random.randint(0, len(fruits_surfaces) - 1)])


class Obstacle(Square):
    def __init__(self, x: int, y: int, kind: str = '') -> None:
        if kind in obstacles_surfaces:
            super().__init__(x, y, kind)
        else:
            super().__init__(x, y, list(obstacles_surfaces.keys())[random.randint(0, len(obstacles_surfaces) - 1)])


class Terrain(Square):
    def __init__(self, x: int, y: int, kind: str = '') -> None:
        if kind in terrain_surfaces:
            super().__init__(x, y, kind)
        else:
            super().__init__(x, y, list(terrain_surfaces.keys())[random.randint(0, len(terrain_surfaces) - 1)])


class Board:
    def __init__(self, length: int, borders: bool = False, snake: Snake = None) -> None:
        self.length = length
        self.borders = borders
        if snake is None:
            self.snake = Snake(int((self.length + STARTING_LENGTH) / 2) - 1, int(self.length / 2) + 1, -1,
                               '>', STARTING_LENGTH)
        else:
            self.snake = snake
        self.fruits = []
        self.terrains = []
        self.obstacles = []

    def background(self, color1: tuple[int, int, int], color2: tuple[int, int, int],
                   color3: tuple[int, int, int] = (0, 102, 0)) -> None:
        if self.borders:  # drawing Borders
            screen.fill(color3, (SCALE * 30, 0, SCALE * 30 * (self.length - 2), SCALE * 30))  # Up
            screen.fill(color3, (0, 0, SCALE * 30, SCALE * 30 * (self.length - 1)))  # Left
            screen.fill(color3, (SCALE * 30 * (self.length - 1), 0, SCALE * 30, SCALE * 30 * self.length))  # Right
            screen.fill(color3, (0, SCALE * 30 * (self.length - 1), SCALE * 30 * (self.length - 1), SCALE * 30))  # Down

        x = y = SCALE * 30 * self.borders
        is_color_1 = True
        while True:
            if x >= (self.length - self.borders) * SCALE * 30:
                x = SCALE * 30 * self.borders
                y += 30 * SCALE

                if self.length % 2 == 0:
                    is_color_1 = not is_color_1

            if y >= (self.length - self.borders) * SCALE * 30:
                break

            if is_color_1:
                screen.fill(color1, (x, y, SCALE * 30, SCALE * 30))
            else:
                screen.fill(color2, (x, y, SCALE * 30, SCALE * 30))
            x += 30 * SCALE
            is_color_1 = not is_color_1

    def generate_terrain(self) -> None:
        """
        Generating new Terrain Object and adding it to "Board.terrains"
        """
        # adding terrain
        for try_counter in range(25):  # gives 25 tries to generate a fruit
            terrain_x = random.randint(self.borders, self.length - 1 - self.borders)
            terrain_y = random.randint(self.borders, self.length - 1 - self.borders)
            if not (self.is_terrain(terrain_x, terrain_y) or
                    self.is_obstacle(terrain_x, terrain_y) or
                    self.is_fruit(terrain_x, terrain_y) or self.snake.is_snake(terrain_x, terrain_y)):
                self.terrains.append(Terrain(terrain_x, terrain_y))
                break

    def generate_fruit(self) -> None:
        # generating place for first fruit
        fruit_x = random.randint(BORDERS, LENGTH - 1 - BORDERS)
        fruit_y = random.randint(BORDERS, LENGTH - 1 - BORDERS)

        while (self.snake.is_snake(fruit_x, fruit_y) or
               self.is_obstacle(fruit_x, fruit_y) or
               self.is_fruit(fruit_x, fruit_y)):
            fruit_x = random.randint(BORDERS, LENGTH - 1 - BORDERS)
            fruit_y = random.randint(BORDERS, LENGTH - 1 - BORDERS)

        fruit = Fruit(fruit_x, fruit_y)
        self.fruits.append(fruit)

        # removing terrain that is on the same square as the fruit
        for terrain in self.terrains:
            if (terrain.x, terrain.y) == (fruit.x, fruit.y):
                self.terrains.remove(terrain)

    def generate_obstacle(self) -> None:
        stone_x = random.randint(BORDERS, self.length - 1 - BORDERS)  # generating random x
        stone_y = random.randint(BORDERS, self.length - 1 - BORDERS)  # generating random y
        try_counter = 0
        while ((self.is_obstacle(stone_x, stone_y) or self.is_fruit(stone_x, stone_y) or
                self.snake.is_snake(stone_x, stone_y) or
                (self.length - SAFE_RADIUS <= abs(self.snake.x - stone_x) <= self.length - 1 or
                 self.snake.x - SAFE_RADIUS <= stone_x <= self.snake.x + SAFE_RADIUS)
                and (self.length - SAFE_RADIUS <= abs(self.snake.y - stone_y) <= self.length - 1) or
                self.snake.y - SAFE_RADIUS <= stone_y <= self.snake.y + SAFE_RADIUS)):
            stone_x = random.randint(BORDERS, self.length - 1 - BORDERS)
            stone_y = random.randint(BORDERS, self.length - 1 - BORDERS)
            try_counter += 1
            if try_counter >= 10:
                break
        if try_counter < 10:
            for terrain in self.terrains:
                if (terrain.x, terrain.y) == (stone_x, stone_y):
                    self.terrains.remove(terrain)
            self.obstacles.append(Obstacle(stone_x, stone_y))

    def draw_terrain(self) -> None:
        for square in self.terrains:
            screen.blit(terrain_surfaces[square.kind], (square.x * SCALE * 30, square.y * SCALE * 30))

    def draw_obstacles(self) -> None:
        for obstacle in self.obstacles:
            screen.blit(obstacles_surfaces[obstacle.kind], (obstacle.x * SCALE * 30, obstacle.y * SCALE * 30))

    def draw_fruits(self, tick: int = 0) -> None:
        for fruit in self.fruits:  # drawing fruits
            try:
                screen.blit(fruits_surfaces[fruit.kind][tick % len(fruits_surfaces[fruit.kind])],  # drawing fruits
                            (fruit.x * 30 * SCALE, fruit.y * 30 * SCALE))
            except ZeroDivisionError:
                print(f'{fruit} Error fruits_surfaces[{fruit.kind}] is Empty')

    def print_score(self) -> None:

        score_surface = clip_and_slice.create_text_with_outline(Score_font,
                                                                f'{len(self.snake.parts) - self.snake.LENGTH}',
                                                                (255, 255, 255), (0, 0, 0), SCALE * 2)
        width, height = score_surface.get_size()

        screen.blit(score_surface, (self.length * 15 * SCALE - width / 2,
                                    SCALE * 15 - height / 2))

    def is_obstacle(self, x: int, y: int) -> bool:
        for square in self.obstacles:
            if (x, y) == (square.x, square.y):
                return True
        return False

    def is_terrain(self, x: int, y: int) -> bool:
        for square in self.terrains:
            if (x, y) == (square.x, square.y):
                return True
        return False

    def is_fruit(self, x: int, y: int) -> bool:
        for square in self.fruits:
            if (x, y) == (square.x, square.y):
                return True
        return False


def main() -> bool:
    pygame.display.set_icon(snakes_parts[0][1])  # setting icon
    pygame.display.set_caption('SNAKE by ASYU')  # setting name

    if background_sound.get_num_channels() == 0:  # checking if music is playing
        background_sound.play()  # playing music

    board = Board(LENGTH, BORDERS)
    running = True
    ate = False
    # generating player

    tick = 0  # tick

    # generating random terrain
    num_terrain = random.randint(board.length * 2, board.length * 3)
    for counter_grass in range(num_terrain):
        board.generate_terrain()

    # generating place for first fruit
    for i in range(NUM_FRUITS):
        board.generate_fruit()

    for terrain in board.terrains:  # removing terrain that under fruit or snake
        if (board.snake.x, board.snake.y) == (terrain.x, terrain.y):
            board.terrains.remove(terrain)
            break
    try:
        for sec in range(3, 0, -1):  # waiting loop
            for event in pygame.event.get():
                # Check for QUIT event
                if event.type == pygame.QUIT:
                    running = False
            if not running:
                break

            # clearing screen from all thing by filling screen with background
            board.background((0, 255, 128), (0, 204, 102))  # drawing background
            board.draw_terrain()  # drawing terrain
            board.snake.draw_snake()  # drawing snake
            board.print_score()  # drawing score

            num_surface = clip_and_slice.create_text_with_outline(Waiting_font, f'{sec}', (255, 255, 255),
                                                                  (0, 0, 0), SCALE * 2)

            width, height = num_surface.get_size()

            screen.blit(num_surface, (board.length * 15 * SCALE - width / 2,
                                      board.length * SCALE * 15 - height / 2))

            pygame.display.update()  # Updating Screen

            clock.tick(1)  # waiting a second before drawing next second in countdown

        pygame.event.get()  # emptying buffer

        while running:  # main loop
            if background_sound.get_num_channels() == 0:
                background_sound.play()
            tick += 1  # increasing tick by 1
            if tick >= 232792560:  # 232792560 can be divided by all numbers between 1 and 20
                tick = 0  # resetting to prevent overflow (may cause some jumping in animations but only when resetting)
            elif tick % TERRAIN_PER_TICKS == 0:
                board.generate_terrain()

            if ate:
                eating_sound.play()  # playing funny sound when getting a point by eating

                # generating new place for new fruit
                board.generate_fruit()

                # generating new obstacle
                # checking if score % DIFFICULTY is 0 adding 1 because the length of the snake hasn't yet increased
                if (len(board.snake.parts) - board.snake.LENGTH + 1) % DIFFICULTY == 0:
                    board.generate_obstacle()  # generating obstacle

            # checking if player touched himself and updating player
            failed = board.snake.update_snake(board.length, ate)

            # checking if player touched borders
            failed = ((board.borders and
                       (board.snake.x <= 0 or board.snake.x >= board.length - 1 or board.snake.y <= 0 or
                        board.snake.y >= board.length - 1)) or failed)

            # checking if player touched obstacle
            failed = failed or board.is_obstacle(board.snake.x, board.snake.y)

            for terrain in board.terrains:  # removing all terrains with the same cords as player's parts
                if (board.snake.x, board.snake.y) == (terrain.x, terrain.y):
                    board.terrains.remove(terrain)

            ate = False
            for fruit in board.fruits:
                ate = board.snake.is_snake(fruit.x, fruit.y)  # checking if player ate or not
                if ate:
                    board.fruits.remove(fruit)
                    break

            if failed and not IMMORTAL:
                losing_sound.play()  # playing losing sound
                break  # exiting game loop
            else:
                # clearing screen from all thing by filling screen with background
                board.background((0, 255, 128), (0, 204, 102))
                board.draw_terrain()  # drawing terrain

                # drawing obstacles
                board.draw_obstacles()

                board.draw_fruits(tick)

                board.snake.draw_snake()  # drawing snake
                board.print_score()  # drawing score

                if ((board.length - BORDERS * 2) ** 2 <=
                        len(board.snake.parts) + len(board.obstacles) + len(board.fruits)):  # Winning
                    break  # exiting game loop

            pygame.display.update()  # Updating Screen

            clock.tick(TICKS_PER_SEC)  # put how many times the screen would update in second

            for event in pygame.event.get():
                # Check for QUIT event
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if board.snake.point != '<':
                            board.snake.point = '>'
                            break
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if board.snake.point != '>':
                            board.snake.point = '<'
                            break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if board.snake.point != '^':
                            board.snake.point = 'v'
                            break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if board.snake.point != 'v':
                            board.snake.point = '^'
                            break

        # finnish statement
        if running:  # if it is a fail / win
            print(f'Finished game. Score: {len(board.snake.parts) - board.snake.LENGTH}')

            text_surface = clip_and_slice.create_text_with_outline(Score_font, f'YOUR SCORE IS:',
                                                                   (255, 255, 255), (0, 0, 0), SCALE * 2)

            score_surface = clip_and_slice.create_text_with_outline(Score_font,
                                                                    f'{len(board.snake.parts) - board.snake.LENGTH}',
                                                                    (255, 255, 255), (0, 0, 0), SCALE * 2)
            width_text, height_text = text_surface.get_size()
            width_score, height_score = score_surface.get_size()

            screen.blit(text_surface,
                        (board.length * 15 * SCALE - width_text / 2,
                         board.length * SCALE * 15 - height_text / 2))

            screen.blit(score_surface,  # drawing final score
                        (board.length * 15 * SCALE - width_score / 2,
                         board.length * SCALE * 15 - height_score / 2 + height_text))

            pygame.display.update()  # Updating Screen
            while True:
                for event in pygame.event.get():
                    # Check for QUIT event
                    if event.type == pygame.QUIT:
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return True

    except KeyboardInterrupt:
        print('Game Crashed')
    except Exception as err:
        print(f'Error: {err}')

    try:
        # quit pygame
        pygame.display.quit()
    except pygame.error:
        pass
    return False


if __name__ == '__main__':
    while main():
        pass
