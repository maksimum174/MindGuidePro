#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe Game (Command Line Version)
---------------------------------------
Simple yet engaging Tic-Tac-Toe game in the command line interface.
This version can be tested on any environment, including Replit.
"""

import os
import random
import time

class TicTacToeGame:
    """Простая игра Крестики-Нолики в консольном интерфейсе."""
    
    def __init__(self):
        """Инициализация игры."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.vs_ai = True
        self.game_over = False
        self.winner = None

    def display_board(self):
        """Отрисовка игрового поля."""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n\033[1;36m Крестики-Нолики \033[0m\n")
        
        print(" {} | {} | {} ".format(self.board[0], self.board[1], self.board[2]))
        print("-----------")
        print(" {} | {} | {} ".format(self.board[3], self.board[4], self.board[5]))
        print("-----------")
        print(" {} | {} | {} ".format(self.board[6], self.board[7], self.board[8]))
        
        # Отобразим информацию о текущем ходе
        if not self.game_over:
            if self.current_player == 'X':
                print("\n\033[1;31mХод игрока X\033[0m")
            else:
                print("\n\033[1;34mХод игрока O\033[0m")
        else:
            if self.winner:
                if self.winner == 'X':
                    print("\n\033[1;32mИгрок X победил!\033[0m")
                else:
                    print("\n\033[1;32mИгрок O победил!\033[0m")
            else:
                print("\n\033[1;33mНичья!\033[0m")

    def make_move(self, position):
        """Сделать ход."""
        if position < 0 or position > 8:
            return False
        
        if self.board[position] != ' ' or self.game_over:
            return False
        
        self.board[position] = self.current_player
        self.check_game_over()
        
        if not self.game_over:
            self.switch_player()
        
        return True

    def switch_player(self):
        """Переключить текущего игрока."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_game_over(self):
        """Проверка на завершение игры."""
        # Проверка строк
        for i in range(0, 9, 3):
            if self.board[i] != ' ' and self.board[i] == self.board[i+1] == self.board[i+2]:
                self.game_over = True
                self.winner = self.board[i]
                return
        
        # Проверка столбцов
        for i in range(3):
            if self.board[i] != ' ' and self.board[i] == self.board[i+3] == self.board[i+6]:
                self.game_over = True
                self.winner = self.board[i]
                return
        
        # Проверка диагоналей
        if self.board[0] != ' ' and self.board[0] == self.board[4] == self.board[8]:
            self.game_over = True
            self.winner = self.board[0]
            return
        
        if self.board[2] != ' ' and self.board[2] == self.board[4] == self.board[6]:
            self.game_over = True
            self.winner = self.board[2]
            return
        
        # Проверка на ничью
        if ' ' not in self.board:
            self.game_over = True
            self.winner = None
            return

    def ai_move(self):
        """ИИ делает ход."""
        # Проверка на выигрышный ход
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_win('O'):
                    return i
                self.board[i] = ' '
        
        # Проверка на блокирующий ход
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_win('X'):
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        
        # Центр
        if self.board[4] == ' ':
            return 4
        
        # Углы
        corners = [0, 2, 6, 8]
        empty_corners = [c for c in corners if self.board[c] == ' ']
        if empty_corners:
            return random.choice(empty_corners)
        
        # Стороны
        sides = [1, 3, 5, 7]
        empty_sides = [s for s in sides if self.board[s] == ' ']
        if empty_sides:
            return random.choice(empty_sides)
        
        return None

    def check_win(self, player):
        """Проверка на победу для указанного игрока."""
        # Проверка строк
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                return True
        
        # Проверка столбцов
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                return True
        
        # Проверка диагоналей
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        
        return False

    def reset(self):
        """Сброс игры."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def toggle_ai(self):
        """Переключение режима игры против ИИ."""
        self.vs_ai = not self.vs_ai
        self.reset()


def display_instructions():
    """Отображает инструкции по игре."""
    print("\n\033[1;33mИнструкции по игре:\033[0m")
    print("Используйте цифры от 1 до 9, чтобы сделать ход в соответствующую клетку:")
    print("""
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 
    """)
    print("Команды:")
    print("  n - Новая игра")
    print("  a - Переключить режим игры с ИИ")
    print("  q - Выход из игры")
    print("  h - Показать эту справку")


def main():
    """Основная функция игры."""
    game = TicTacToeGame()
    
    display_instructions()
    
    while True:
        game.display_board()
        
        # Если игра закончена, предложить новую игру
        if game.game_over:
            print("\nНажмите 'n' для новой игры или 'q' для выхода")
            try:
                choice = input("Ваш выбор: ").lower()
                if choice == 'n':
                    game.reset()
                    continue
                elif choice == 'q':
                    break
                continue
            except EOFError:
                print("\nВыход из игры из-за EOFError")
                break
        
        # Ход ИИ
        if game.vs_ai and game.current_player == 'O':
            print("ИИ делает ход...")
            time.sleep(1)
            position = game.ai_move()
            game.make_move(position)
            continue
        
        # Ход игрока
        try:
            move = input("Введите номер клетки (1-9) или команду (n/a/q/h): ").lower()
            
            if move == 'q':
                break
            elif move == 'n':
                game.reset()
                continue
            elif move == 'a':
                game.toggle_ai()
                print(f"Режим игры с ИИ: {'включен' if game.vs_ai else 'выключен'}")
                time.sleep(1)
                continue
            elif move == 'h':
                display_instructions()
                continue
            
            try:
                position = int(move) - 1  # Конвертируем в индекс (0-8)
                if not game.make_move(position):
                    print("Некорректный ход! Попробуйте снова.")
                    time.sleep(1)
            except ValueError:
                print("Пожалуйста, введите число от 1 до 9 или команду.")
                time.sleep(1)
        except EOFError:
            print("\nВыход из игры из-за EOFError")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nИгра завершена. До свидания!")