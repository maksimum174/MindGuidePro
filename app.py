#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Веб-интерфейс для игры Крестики-Нолики
"""

import os
import flask
from flask import Flask, render_template, request, jsonify, session
import random
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

class TicTacToeGame:
    """Простая игра Крестики-Нолики."""
    
    def __init__(self):
        """Инициализация игры."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def to_json(self):
        """Конвертирует состояние игры в JSON."""
        return {
            'board': self.board,
            'currentPlayer': self.current_player,
            'gameOver': self.game_over,
            'winner': self.winner
        }
    
    @staticmethod
    def from_json(data):
        """Создает игру из JSON данных."""
        game = TicTacToeGame()
        game.board = data['board']
        game.current_player = data['currentPlayer']
        game.game_over = data['gameOver']
        game.winner = data['winner']
        return game

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
                    self.board[i] = ' '
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


@app.route('/')
def home():
    """Домашняя страница с игрой."""
    # Создаем новую игру, если нет активной
    if 'game' not in session:
        session['game'] = json.dumps(TicTacToeGame().to_json())
        session['vs_ai'] = True
    
    return render_template('index.html')


@app.route('/api/state')
def get_state():
    """Получить текущее состояние игры."""
    if 'game' not in session:
        session['game'] = json.dumps(TicTacToeGame().to_json())
    
    game_data = json.loads(session['game'])
    return jsonify({
        'game': game_data,
        'vsAI': session.get('vs_ai', True)
    })


@app.route('/api/move', methods=['POST'])
def make_move():
    """Сделать ход."""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    data = request.json
    position = data.get('position')
    
    if position is None:
        return jsonify({'error': 'No position provided'}), 400
    
    game = TicTacToeGame.from_json(json.loads(session['game']))
    vs_ai = session.get('vs_ai', True)
    
    if game.make_move(position):
        # Если игра с ИИ и ход ИИ
        if vs_ai and not game.game_over and game.current_player == 'O':
            ai_position = game.ai_move()
            if ai_position is not None:
                game.make_move(ai_position)
    
    session['game'] = json.dumps(game.to_json())
    
    return jsonify({
        'game': game.to_json(),
        'vsAI': vs_ai
    })


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Сбросить игру."""
    game = TicTacToeGame()
    session['game'] = json.dumps(game.to_json())
    
    return jsonify({
        'game': game.to_json(),
        'vsAI': session.get('vs_ai', True)
    })


@app.route('/api/toggle-ai', methods=['POST'])
def toggle_ai():
    """Переключить режим игры с ИИ."""
    session['vs_ai'] = not session.get('vs_ai', True)
    
    # Сбросить игру после переключения режима
    game = TicTacToeGame()
    session['game'] = json.dumps(game.to_json())
    
    return jsonify({
        'game': game.to_json(),
        'vsAI': session.get('vs_ai', True)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)