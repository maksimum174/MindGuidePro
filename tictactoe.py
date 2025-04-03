#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe Game for Android
----------------------------
Simple yet engaging Tic-Tac-Toe game with a clean GUI, designed for Android deployment.
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock

# Set the kivy version requirement
kivy.require('2.0.0')

# Setting color scheme
BACKGROUND_COLOR = get_color_from_hex('#FFFFFF')  # White background
GRID_COLOR = get_color_from_hex('#2C3E50')        # Dark blue-gray for grid
X_COLOR = get_color_from_hex('#E74C3C')           # Red for X
O_COLOR = get_color_from_hex('#3498DB')           # Blue for O
TEXT_COLOR = get_color_from_hex('#2C3E50')        # Dark blue-gray for text
BUTTON_COLOR = get_color_from_hex('#ECF0F1')      # Light gray for buttons


class TicTacToeButton(Button):
    """Custom button for the Tic-Tac-Toe grid cells."""
    
    def __init__(self, **kwargs):
        super(TicTacToeButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = BUTTON_COLOR
        self.font_size = dp(40)
        self.color = TEXT_COLOR
        self.border = (4, 4, 4, 4)


class TicTacToeGrid(GridLayout):
    """The game grid containing the 3x3 buttons."""
    
    def __init__(self, **kwargs):
        super(TicTacToeGrid, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = dp(4)
        self.padding = dp(4)
        self.buttons = []
        self.create_board()
    
    def create_board(self):
        """Creates the 3x3 grid of buttons."""
        for i in range(9):
            button = TicTacToeButton(font_size=dp(40))
            button.bind(on_release=self.button_pressed)
            self.add_widget(button)
            self.buttons.append(button)
    
    def button_pressed(self, button):
        """Handles button press events."""
        if button.text == '' and not self.parent.game_over:
            if self.parent.current_player == 'X':
                button.text = 'X'
                button.color = X_COLOR
                # Add subtle animation
                anim = Animation(background_color=X_COLOR[:3] + [0.2], duration=0.1) + \
                       Animation(background_color=BUTTON_COLOR, duration=0.1)
                anim.start(button)
            else:
                button.text = 'O'
                button.color = O_COLOR
                # Add subtle animation
                anim = Animation(background_color=O_COLOR[:3] + [0.2], duration=0.1) + \
                       Animation(background_color=BUTTON_COLOR, duration=0.1)
                anim.start(button)
            
            self.parent.check_game_over()
            if not self.parent.game_over:
                self.parent.switch_player()
                
                # If playing against AI and it's AI's turn
                if self.parent.vs_ai and self.parent.current_player == 'O':
                    # Schedule AI move with a small delay to make it feel more natural
                    Clock.schedule_once(lambda dt: self.parent.ai_move(), 0.5)


class TicTacToeGame(BoxLayout):
    """Main game layout that contains the grid and game controls."""
    
    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # Game state
        self.current_player = 'X'
        self.game_over = False
        self.vs_ai = True  # Default to playing against AI
        
        # Set background color
        Window.clearcolor = BACKGROUND_COLOR
        
        # Create the header with game name
        self.header = Label(
            text='Крестики-Нолики',
            font_size=dp(32),
            size_hint=(1, 0.15),
            color=TEXT_COLOR
        )
        self.add_widget(self.header)
        
        # Create status display
        self.status = Label(
            text='Ход: Игрок X',
            font_size=dp(20),
            size_hint=(1, 0.1),
            color=TEXT_COLOR
        )
        self.add_widget(self.status)
        
        # Create the game grid
        self.grid = TicTacToeGrid(size_hint=(1, 0.65))
        self.add_widget(self.grid)
        
        # Create control buttons
        self.controls = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        # New Game button
        self.new_game_btn = Button(
            text='Новая игра',
            background_normal='',
            background_color=GRID_COLOR,
            color=(1, 1, 1, 1),
            font_size=dp(18)
        )
        self.new_game_btn.bind(on_release=self.new_game)
        self.controls.add_widget(self.new_game_btn)
        
        # Toggle AI button
        self.toggle_ai_btn = Button(
            text='Против ИИ: Вкл',
            background_normal='',
            background_color=GRID_COLOR,
            color=(1, 1, 1, 1),
            font_size=dp(18)
        )
        self.toggle_ai_btn.bind(on_release=self.toggle_ai)
        self.controls.add_widget(self.toggle_ai_btn)
        
        self.add_widget(self.controls)
    
    def switch_player(self):
        """Switches the current player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status.text = f'Ход: Игрок {self.current_player}'
    
    def check_game_over(self):
        """Checks if the game is over (win or draw)."""
        b = self.grid.buttons
        
        # Check rows
        for i in range(0, 9, 3):
            if b[i].text and b[i].text == b[i+1].text == b[i+2].text:
                self.game_won(b[i].text)
                return
        
        # Check columns
        for i in range(3):
            if b[i].text and b[i].text == b[i+3].text == b[i+6].text:
                self.game_won(b[i].text)
                return
        
        # Check diagonals
        if b[0].text and b[0].text == b[4].text == b[8].text:
            self.game_won(b[0].text)
            return
        if b[2].text and b[2].text == b[4].text == b[6].text:
            self.game_won(b[2].text)
            return
        
        # Check for draw
        if all(button.text for button in b):
            self.game_draw()
    
    def game_won(self, player):
        """Handles game won state."""
        self.game_over = True
        self.status.text = f'Игрок {player} победил!'
        
        # Show popup with animation
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text=f'Игрок {player} победил!',
            font_size=dp(24),
            color=X_COLOR if player == 'X' else O_COLOR
        ))
        btn = Button(
            text='Новая игра',
            size_hint=(1, 0.4),
            background_normal='',
            background_color=GRID_COLOR,
            color=(1, 1, 1, 1)
        )
        
        popup = Popup(
            title='Конец игры',
            content=content,
            size_hint=(0.75, 0.4),
            auto_dismiss=True
        )
        
        btn.bind(on_release=lambda x: self.new_game(None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        
        Clock.schedule_once(lambda dt: popup.open(), 0.5)
    
    def game_draw(self):
        """Handles game draw state."""
        self.game_over = True
        self.status.text = 'Ничья!'
        
        # Show popup with animation
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(
            text='Ничья!',
            font_size=dp(24)
        ))
        btn = Button(
            text='Новая игра',
            size_hint=(1, 0.4),
            background_normal='',
            background_color=GRID_COLOR,
            color=(1, 1, 1, 1)
        )
        
        popup = Popup(
            title='Конец игры',
            content=content,
            size_hint=(0.75, 0.4),
            auto_dismiss=True
        )
        
        btn.bind(on_release=lambda x: self.new_game(None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        
        Clock.schedule_once(lambda dt: popup.open(), 0.5)
    
    def new_game(self, instance):
        """Resets the game to start a new one."""
        for button in self.grid.buttons:
            button.text = ''
            button.color = TEXT_COLOR
            button.background_color = BUTTON_COLOR
        
        self.game_over = False
        self.current_player = 'X'
        self.status.text = 'Ход: Игрок X'
    
    def toggle_ai(self, instance):
        """Toggles AI opponent on/off."""
        self.vs_ai = not self.vs_ai
        instance.text = f'Против ИИ: {"Вкл" if self.vs_ai else "Выкл"}'
        self.new_game(None)
    
    def ai_move(self):
        """AI makes a move using a simple algorithm."""
        if self.game_over:
            return
        
        # Get the state of the board
        board = [button.text for button in self.grid.buttons]
        
        # Check for winning move
        move_index = self.find_winning_move(board, 'O')
        
        # If no winning move, check to block opponent
        if move_index is None:
            move_index = self.find_winning_move(board, 'X')
        
        # If no blocking move, try to take center
        if move_index is None and board[4] == '':
            move_index = 4
        
        # If center taken, try corners
        elif move_index is None:
            corners = [0, 2, 6, 8]
            empty_corners = [c for c in corners if board[c] == '']
            if empty_corners:
                move_index = empty_corners[0]
        
        # Otherwise, take any available spot
        if move_index is None:
            for i, spot in enumerate(board):
                if spot == '':
                    move_index = i
                    break
        
        # Make the move
        if move_index is not None:
            self.grid.button_pressed(self.grid.buttons[move_index])
    
    def find_winning_move(self, board, player):
        """Finds a winning move for the given player."""
        # Check rows
        for i in range(0, 9, 3):
            if (board[i] == board[i+1] == player and board[i+2] == '') or \
               (board[i] == board[i+2] == player and board[i+1] == '') or \
               (board[i+1] == board[i+2] == player and board[i] == ''):
                for j in range(3):
                    if board[i+j] == '':
                        return i+j
        
        # Check columns
        for i in range(3):
            if (board[i] == board[i+3] == player and board[i+6] == '') or \
               (board[i] == board[i+6] == player and board[i+3] == '') or \
               (board[i+3] == board[i+6] == player and board[i] == ''):
                for j in range(0, 7, 3):
                    if board[i+j] == '':
                        return i+j
        
        # Check diagonal top-left to bottom-right
        if (board[0] == board[4] == player and board[8] == '') or \
           (board[0] == board[8] == player and board[4] == '') or \
           (board[4] == board[8] == player and board[0] == ''):
            for i in [0, 4, 8]:
                if board[i] == '':
                    return i
        
        # Check diagonal top-right to bottom-left
        if (board[2] == board[4] == player and board[6] == '') or \
           (board[2] == board[6] == player and board[4] == '') or \
           (board[4] == board[6] == player and board[2] == ''):
            for i in [2, 4, 6]:
                if board[i] == '':
                    return i
        
        return None


class TicTacToeApp(App):
    """Main app class for Tic-Tac-Toe."""
    
    def build(self):
        """Builds the app interface."""
        self.title = 'Крестики-Нолики'
        self.icon = 'icon.png'  # Default icon - will be replaced
        return TicTacToeGame()


if __name__ == '__main__':
    TicTacToeApp().run()