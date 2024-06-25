import pygame
import sys
import time
from random import randint

WINDOW_SIZE = 700
SQUARE_SIZE = WINDOW_SIZE // 3
INF = float('inf')
vec2 = pygame.math.Vector2
CELL_CENTER = vec2(SQUARE_SIZE / 2)

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 50, True)
        self.button_font = pygame.font.SysFont('Arial', 18, True)
        self.title_text = self.font.render("Welcome to Tic-Tac-Toe", True, 'white')
        self.friend_button_text = self.button_font.render("Play with a Friend", True, 'white')
        self.friend_button_rect = pygame.Rect(WINDOW_SIZE // 2 - 300, WINDOW_SIZE // 2 - 30, 250, 80)
        self.computer_button_text = self.button_font.render("Play against the Computer", True, 'white')
        self.computer_button_rect = pygame.Rect(WINDOW_SIZE // 2 + 50, WINDOW_SIZE // 2 - 30, 250, 80)

    def draw_text_centered(self, text, rect):
        text_rect = text.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
        self.game.screen.blit(text, text_rect)

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(self.title_text, (WINDOW_SIZE // 2 - self.title_text.get_width() // 2, WINDOW_SIZE // 4))
        pygame.draw.rect(self.game.screen, 'blue', self.friend_button_rect)
        self.draw_text_centered(self.friend_button_text, self.friend_button_rect)
        pygame.draw.rect(self.game.screen, 'blue', self.computer_button_rect)
        self.draw_text_centered(self.computer_button_text, self.computer_button_rect)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.friend_button_rect.collidepoint(event.pos):
                    self.game.start_loading()
                elif self.computer_button_rect.collidepoint(event.pos):
                    print("Play against the Computer button clicked")

    def run(self):
        self.draw()
        self.check_events()

class LoadingScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 50, True)
        self.text = self.font.render("Loading...", True, 'white')

    def run(self):
        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(self.text, (WINDOW_SIZE // 2 - self.text.get_width() // 2, WINDOW_SIZE // 2 - self.text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)
        self.game.start_game()

class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.board = self.image_fetching('img/board.jpg', [WINDOW_SIZE]*2)
        self.O = self.image_fetching('img/O.png', [SQUARE_SIZE]*2)
        self.X = self.image_fetching('img/X.png', [SQUARE_SIZE]*2)

        self.game_array = [[INF,INF,INF],
                           [INF,INF,INF],
                           [INF,INF,INF]]

        self.player = randint(0,1)

        self.possible_win_array = [[(0,0), (0,1), (0,2)],
                                   [(1,0), (1,1), (1,2)],
                                   [(2,0), (2,1), (2,2)],
                                   [(0,0), (1,0), (2,0)],
                                   [(0,1), (1,1), (2,1)],
                                   [(0,2), (1,2), (2,2)],
                                   [(0,0), (1,1), (2,2)],
                                   [(0,2), (1,1), (2,0)]]
        
        self.winner = None
        self.game_steps = 0
        self.font = pygame.font.SysFont('Arial', SQUARE_SIZE // 4, True)

    def check_win(self):
       for line_ind in self.possible_win_array:
           sum_line = sum([self.game_array[i][j] for i,j in line_ind])
           if sum_line in {0,3}:
               self.winner = 'XO'[sum_line == 0]
               self.winner_line = [vec2(line_ind[0][::-1])* SQUARE_SIZE + CELL_CENTER,
                                   vec2(line_ind[2][::-1])* SQUARE_SIZE + CELL_CENTER]

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) // SQUARE_SIZE
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_win()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X if obj else self.O, vec2(x,y) * SQUARE_SIZE)

    def draw_winner(self):
        if self.winner:
            pygame.draw.line(self.game.screen, 'red', *self.winner_line, SQUARE_SIZE // 8)
            label = self.font.render(f'PLAYER "{self.winner}" WINS', True, 'white', 'black')
            self.game.screen.blit(label, (WINDOW_SIZE // 2 - label.get_width() // 2, WINDOW_SIZE //  4))

    def draw(self):
        self.game.screen.blit(self.board, (0,0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def image_fetching(path, res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, res)
    
    def caption(self):
        pygame.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pygame.display.set_caption(f'Player "{self.winner}" has won! Press Space for a rematch!')
        elif self.game_steps == 9:
             pygame.display.set_caption(f'TIE!!! Press Space to Restart')
    
    def run(self):
        self.caption()
        self.draw()
        self.run_game_process()

class StartUp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
        self.timer = pygame.time.Clock()
        self.main_menu = MainMenu(self)
        self.loading_screen = LoadingScreen(self)
        self.tictactoe = TicTacToe(self)
        self.state = "menu"

    def start_loading(self):
        self.state = "loading"

    def start_game(self):
        self.tictactoe = TicTacToe(self)
        self.state = "game"

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == "game" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_loading()

    def start(self):
        while True:
            if self.state == "menu":
                self.main_menu.run()
            elif self.state == "loading":
                self.loading_screen.run()
            elif self.state == "game":
                self.tictactoe.run()
            self.check()
            pygame.display.update()
            self.timer.tick(120)

if __name__ == '__main__':
    game = StartUp()
    game.start()
