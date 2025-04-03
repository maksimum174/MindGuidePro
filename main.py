#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Точка входа для веб-интерфейса игры Крестики-Нолики
"""

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)