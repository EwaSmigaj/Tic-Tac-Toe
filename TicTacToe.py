# klasa Gracz
# klasa Plansza
# klasa Gra
from typing import Optional, Any

import pygame
import sys

pygame.font.init()


class Player:

    def __init__(self, is_human, sign):
        self.is_human = bool(is_human)
        self.sign = sign
        self.last_move = -1


class Game:

    def __init__(self, width=600, height=600):
        self._p1 = Player(True, "O")
        self._p2 = Player(True, "X")
        self._board = Board(width, height)
        self.state = True  # true if it isn't end of the game
        self.turn = self._p1.sign

    def next_turn(self):
        if self.turn == self._p1.sign:
            self.turn = self._p2.sign
            print("zmieniam tureeee")
        else:
            self.turn = self._p1.sign

    def is_end(self):
        for i in range(0, 3):
            if i == 0 and self._board.get_field(i) == self._board.get_field(i+4) \
                    and self._board.get_field(i) != 0:         # check cross1
                if self._board.get_field(i+4) == self._board.get_field(i+8):
                    return self._board.get_field(i)
            if i == 2 and self._board.get_field(i+2) == self._board.get_field(i) \
                    and self._board.get_field(i) != 0:         # check cross2
                if self._board.get_field(i+2) == self._board.get_field(i+4):
                    return self._board.get_field(i)
            if self._board.get_field(i*3) == self._board.get_field(i*3+1) \
                    and self._board.get_field(i*3) != 0:                # check rows
                if self._board.get_field(i*3+1) == self._board.get_field(i*3+2):
                    return self._board.get_field(i*3)
            if self._board.get_field(i) == self._board.get_field(i+3) \
                    and self._board.get_field(i) != 0:                    # check columns
                if self._board.get_field(i+3) == self._board.get_field(i+6):
                    return self._board.get_field(i)
        if self._board.is_full() is True:
            return 0
        return False

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                return self._board.click(x, y, self.turn)
                print(" klik  ")
        return False

    def play(self):
        while True:
            if self.handle_event() is not False:
                self.next_turn()
            if self.is_end() is False:
                self._board.display_game()
            else:
                self._board.display_end(self.is_end())


class Board:

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._fields = {}
        self._field_x = self._width // 3
        self._field_y = self._height // 3
        self._screen = pygame.display.set_mode((self._width, self._height))
        for i in range(0, 9):
            self._fields[i] = 0  # 0-empty, O-player1, X-player2

    def get_field(self, i):
        return self._fields[i]

    def click(self, pos_x, pos_y, sign):
        x = pos_x // self._field_x
        y = pos_y // self._field_y
        field_nb = x + 3*y

        return self.change_filed(field_nb, sign)

    def change_filed(self, field_nb, sign):
        # if self._fields[field_nb] == 0:
        self._fields[field_nb] = sign
        print(self._fields[field_nb])
        print(field_nb)
        print(self._fields)
        print(" ")
        # else:
        #     return False

    def is_full(self):
        empty = 0
        for i in range(0, 9):
            if self._fields[i] == 0:
                empty += 1
        if empty != 0:
            return False
        else:
            return True

    def draw_x(self, pos_x, pos_y, screen):
        pygame.draw.line(screen, (255, 255, 255), (pos_x + 10, pos_y + 10),
                         (pos_x + self._field_x - 10, pos_y + self._field_y - 10), 6)
        pygame.draw.line(screen, (255, 255, 255), (pos_x+10, pos_y+self._field_y-10),
                         (pos_x+self._field_x-10, pos_y+10), 6)

    def draw_o(self, pos_x, pos_y, screen):
        x = self._field_x//2
        y = self._field_y//2
        r = x
        if x != y:
            if x < y:
                r = x/2
            else:
                r = y/2
        pygame.draw.circle(screen, (255, 255, 255), (pos_x + x, pos_y + y), r-10, 6)

    def display_game(self):
        pygame.Surface.fill(self._screen, (0, 0, 0))
        for i in range(0, 3):
            for j in range(0, 3):
                pygame.draw.rect(self._screen, (255, 255, 255), pygame.Rect(self._field_x * i, self._field_y * j,
                                                                            self._field_x, self._field_y), 4)
                if self._fields[i+j*3] != 0:
                    if self._fields[i+j*3] == 'X':
                        self.draw_x(self._field_x*i, self._field_y*j, self._screen)
                    elif self._fields[i+j*3] == 'O':
                        self.draw_o(self._field_x*i, self._field_y*j, self._screen)
        pygame.display.flip()

    def display_end(self, winner):
        self._screen.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 72)
        if winner is not 0:
            text = font.render(f"{winner} WON", True, (0, 0, 0))
        else:
            text = font.render("DRAW", True, (0, 0, 0))
        self._screen.blit(text, ((self._width - text.get_width()) / 2, (self._height - text.get_height()) / 2))

        pygame.display.flip()


g = Game()
g.play()

