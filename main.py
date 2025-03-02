import pygame
import random
import os
import json

# Инициализация pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()

# Путь к файлу с рекордами
RECORDS_FILE = "records.json"

# Загрузка рекордов
def load_records():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r") as file:
            return json.load(file)
    return []

# Сохранение рекорда
def save_record(score):
    records = load_records()
    records.append(score)
    records.sort(reverse=True)
    with open(RECORDS_FILE, "w") as file:
        json.dump(records[:10], file)  # Сохраняем топ-10 рекордов

# Отображение рекордов
def show_records():
    records = load_records()
    screen.fill(BLACK)
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render("Топ рекордов:", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    for i, record in enumerate(records):
        text = font.render(f"{i + 1}. {record}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + i * 30))
    pygame.display.flip()
    pygame.time.wait(3000)

# Функция для отображения многострочного текста
def draw_multiline_text(surface, text, font, color, x, y, line_height):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * line_height))

# Основная функция игры
def game(difficulty):
    # Настройка скорости в зависимости от сложности
    if difficulty == "низкий":
        FPS = 5
    elif difficulty == "средний":
        FPS = 10
    elif difficulty == "сложный":
        FPS = 15
    else:
        FPS = 10

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    score = 0

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                if event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                if event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                if game_over and event.key == pygame.K_SPACE:  # Рестарт игры
                    difficulty = choose_difficulty()  # Выбор сложности перед рестартом
                    game(difficulty)
                if game_over and event.key == pygame.K_q:  # Выход из игры
                    running = False

        if not game_over:
            # Движение змейки
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # Проверка на столкновение с границами (только для сложного уровня)
            if difficulty == "сложный":
                if (new_head[0] < 0 or new_head[0] >= WIDTH or
                    new_head[1] < 0 or new_head[1] >= HEIGHT):
                    game_over = True
                    save_record(score)
            else:
                # Прохождение сквозь границы (для низкого и среднего уровня)
                new_head = (
                    new_head[0] % WIDTH,
                    new_head[1] % HEIGHT
                )

            snake.insert(0, new_head)

            # Проверка на столкновение с едой
            if snake[0] == food:
                score += 1
                food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
            else:
                snake.pop()

            # Проверка на столкновение с собой
            if snake[0] in snake[1:]:
                game_over = True
                save_record(score)

        # Отрисовка
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.ellipse(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))  # Скруглённая змейка
        pygame.draw.ellipse(screen, RED, (*food, CELL_SIZE, CELL_SIZE))  # Скруглённая еда

        # Отображение счета
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Сообщение о завершении игры
        if game_over:
            font = pygame.font.SysFont("comicsans", 20)  # Уменьшаем шрифт для длинного текста
            message = (
                "Игра окончена!\n"
                "Нажмите ПРОБЕЛ для рестарта\n"
                "или Q для выхода"
            )
            draw_multiline_text(screen, message, font, RED, WIDTH // 4, HEIGHT // 2, 30)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Выбор сложности
def choose_difficulty():
    screen.fill(BLACK)
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Выберите уровень сложности:", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    # Отображение лучшего результата
    records = load_records()
    best_score = records[0] if records else 0
    text = font.render(f"Лучший результат: {best_score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

    options = ["низкий", "средний", "сложный"]
    selected = 0  # Индекс выбранного пункта

    while True:
        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE  # Подсветка выбранного пункта
            text = font.render(f"{i + 1}. {option}", True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "низкий"
                elif event.key == pygame.K_2:
                    return "средний"
                elif event.key == pygame.K_3:
                    return "сложный"
                elif event.key == pygame.K_UP:  # Перемещение вверх по меню
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:  # Перемещение вниз по меню
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Выбор текущего пункта
                    return options[selected]

# Запуск игры
if __name__ == "__main__":
    difficulty = choose_difficulty()
    game(difficulty)