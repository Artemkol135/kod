import sys
import json
import random
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QComboBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt

class QuoteGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Quote Generator")
        self.setMinimumSize(700, 500)
        
        self.history_file = "history.json"
        
        # Начальный список цитат
        self.base_quotes = [
            {"text": "Поехали!", "author": "Юрий Гагарин", "theme": "Космос"},
            {"text": "Быть или не быть?", "author": "Шекспир", "theme": "Философия"},
            {"text": "Свобода — это осознанная необходимость.", "author": "Гегель", "theme": "Философия"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Сложнее всего начать действовать, остальное зависит только от упорства.", "author": "Амелия Эрхарт", "theme": "Мотивация"}
        ]
        
        self.history = self.load_history()
        self.init_ui()
        self.refresh_history_list()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Секция генерации
        display_frame = QFrame()
        display_frame.setFrameShape(QFrame.Shape.StyledPanel)
        display_layout = QVBoxLayout(display_frame)
        
        self.quote_label = QLabel("Нажмите кнопку, чтобы получить цитату")
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_label.setStyleSheet("font-size: 16px; font-style: italic; padding: 20px;")
        
        self.author_label = QLabel("")
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        gen_btn = QPushButton("🎲 Сгенерировать цитату")
        gen_btn.setFixedHeight(40)
        gen_btn.clicked.connect(self.generate_quote)
        
        display_layout.addWidget(self.quote_label)
        display_layout.addWidget(self.author_label)
        display_layout.addWidget(gen_btn)
        main_layout.addWidget(display_frame)

        # Секция истории и фильтров
        main_layout.addWidget(QLabel("📜 История и поиск:"))
        
        filter_layout = QHBoxLayout()
        self.author_filter = QLineEdit()
        self.author_filter.setPlaceholderText("Фильтр по автору...")
        self.author_filter.textChanged.connect(self.refresh_history_list)
        
        self.theme_filter = QLineEdit()
        self.theme_filter.setPlaceholderText("Фильтр по теме...")
        self.theme_filter.textChanged.connect(self.refresh_history_list)
        
        filter_layout.addWidget(self.author_filter)
        filter_layout.addWidget(self.theme_filter)
        main_layout.addLayout(filter_layout)

        self.history_list = QListWidget()
        main_layout.addWidget(self.history_list)

    def generate_quote(self):
        quote = random.choice(self.base_quotes)
        self.quote_label.setText(f"«{quote['text']}»")
        self.author_label.setText(f"— {quote['author']} ({quote['theme']})")
        
        # Добавляем в историю
        self.history.insert(0, quote) # Новые сверху
        self.save_history()
        self.refresh_history_list()

    def refresh_history_list(self):
        self.history_list.clear()
        author_q = self.author_filter.text().lower()
        theme_q = self.theme_filter.text().lower()

        for q in self.history:
            if author_q in q['author'].lower() and theme_q in q['theme'].lower():
                item = f"[{q['theme']}] {q['author']}: {q['text']}"
                self.history_list.addItem(item)

    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuoteGenerator()
    window.show()
    sys.exit(app.exec())
