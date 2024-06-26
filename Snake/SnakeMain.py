import pygame
import sys
import random

difficulties = {
    "Invincible": 15,
    "Easy": 15,
    "Medium": 30,
    "Hard": 60,
    "Impossible": 150
}

window_width = 840
window_height = 600

init_status = pygame.init()
if init_status[1] > 0:
    print(f'[!] Had {init_status[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_width, window_height))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

fps_controller = pygame.time.Clock()

snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

square_position = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (window_height // 10)) * 10]
square_spawned = True

current_direction = 'RIGHT'
next_direction = current_direction

score = 0

def display_score(position, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if position == 1:
        score_rect.midtop = (window_width / 10, 15)
    else:
        score_rect.midtop = (window_width / 2, window_height / 1.25)
    game_window.blit(score_surface, score_rect)

def end_game():
    font = pygame.font.SysFont('consola', 90)
    game_over_surface = font.render('You Lost', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width / 2, window_height / 3)
    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    display_score(0, RED, 'times', 20)

    font = pygame.font.SysFont('consola', 50)
    button_main_menu = pygame.Rect(window_width / 2 - 150, window_height / 2 + 50, 300, 50)
    button_restart = pygame.Rect(window_width / 2 - 150, window_height / 2 + 120, 300, 50)
    
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(game_window, GREEN if button_main_menu.collidepoint(mouse_pos) else WHITE, button_main_menu)
    pygame.draw.rect(game_window, GREEN if button_restart.collidepoint(mouse_pos) else WHITE, button_restart)
    
    main_menu_text = font.render('Main Menu', True, BLACK)
    restart_text = font.render('Restart', True, BLACK)
    
    main_menu_rect_text = main_menu_text.get_rect(center=button_main_menu.center)
    restart_rect_text = restart_text.get_rect(center=button_restart.center)
    
    game_window.blit(main_menu_text, main_menu_rect_text)
    game_window.blit(restart_text, restart_rect_text)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_main_menu.collidepoint(event.pos):
                    return "Main Menu"
                if button_restart.collidepoint(event.pos):
                    return "Restart"

        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(game_window, GREEN if button_main_menu.collidepoint(mouse_pos) else WHITE, button_main_menu)
        pygame.draw.rect(game_window, GREEN if button_restart.collidepoint(mouse_pos) else WHITE, button_restart)
        game_window.blit(main_menu_text, main_menu_rect_text)
        game_window.blit(restart_text, restart_rect_text)
        pygame.display.flip()

def main_menu():
    while True:
        game_window.fill(BLACK)
        font = pygame.font.SysFont('consola', 50)
        title_surface = font.render('Welcome to Snake', True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (window_width / 2, window_height / 5)
        game_window.blit(title_surface, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for idx, (text, diff) in enumerate(difficulties.items()):
            button_rect = pygame.Rect((window_width / 2 - 100, window_height / 2 - 70 + idx * 60, 200, 50))
            pygame.draw.rect(game_window, GREEN if button_rect.collidepoint(mouse_pos) else WHITE, button_rect)
            button_text = font.render(text, True, BLACK)
            button_rect_text = button_text.get_rect(center=button_rect.center)
            game_window.blit(button_text, button_rect_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, (text, diff) in enumerate(difficulties.items()):
                    button_rect = pygame.Rect((window_width / 2 - 100, window_height / 2 - 70 + idx * 60, 200, 50))
                    if button_rect.collidepoint(mouse_pos):
                        return text

        pygame.display.update()

def game_loop(difficulty):
    global snake_position, snake_body, square_position, square_spawned, current_direction, next_direction, score
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    square_position = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (window_height // 10)) * 10]
    square_spawned = True
    current_direction = 'RIGHT'
    next_direction = current_direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    next_direction = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    next_direction = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    next_direction = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    next_direction = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if next_direction == 'UP' and current_direction != 'DOWN':
            current_direction = 'UP'
        if next_direction == 'DOWN' and current_direction != 'UP':
            current_direction = 'DOWN'
        if next_direction == 'LEFT' and current_direction != 'RIGHT':
            current_direction = 'LEFT'
        if next_direction == 'RIGHT' and current_direction != 'LEFT':
            current_direction = 'RIGHT'

        if current_direction == 'UP':
            snake_position[1] -= 10
        if current_direction == 'DOWN':
            snake_position[1] += 10
        if current_direction == 'LEFT':
            snake_position[0] -= 10
        if current_direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == square_position[0] and snake_position[1] == square_position[1]:
            score += 1
            square_spawned = False
        else:
            snake_body.pop()

        if not square_spawned:
            square_position = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (window_height // 10)) * 10]
        square_spawned = True

        game_window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, WHITE, pygame.Rect(square_position[0], square_position[1], 10, 10))

        if difficulty == "Mega Easy":
            if snake_position[0] < 0:
                snake_position[0] = window_width - 10
            elif snake_position[0] > window_width - 10:
                snake_position[0] = 0
            elif snake_position[1] < 0:
                snake_position[1] = window_height - 10
            elif snake_position[1] > window_height - 10:
                snake_position[1] = 0
        else:
            if snake_position[0] < 0 or snake_position[0] > window_width - 10:
                return end_game()
            if snake_position[1] < 0 or snake_position[1] > window_height - 10:
                return end_game()
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    return end_game()

        display_score(1, WHITE, 'consolas', 20)
        pygame.display.update()
        fps_controller.tick(difficulties[difficulty])

def main():
    while True:
        difficulty = main_menu()
        while True:
            result = game_loop(difficulty)
            if result == "Main Menu":
                break
            elif result == "Restart":
                continue

if __name__ == "__main__":
    main()
