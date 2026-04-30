import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox)

class BookTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Tracker")
        self.setMinimumSize(800, 500)
        self.file_path = "books.json"
        self.books = self.load_data()
        
        self.init_ui()
        self.update_table(self.books)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая панель (Форма)
        form_layout = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.pages_input = QLineEdit()
        
        form_layout.addWidget(QLabel("Название книги:"))
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(QLabel("Автор:"))
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(QLabel("Жанр:"))
        form_layout.addWidget(self.genre_input)
        form_layout.addWidget(QLabel("Количество страниц:"))
        form_layout.addWidget(self.pages_input)
        
        add_btn = QPushButton("Добавить книгу")
        add_btn.clicked.connect(self.add_book)
        form_layout.addWidget(add_btn)

        form_layout.addSpacing(20)
        form_layout.addWidget(QLabel("Фильтр по жанру:"))
        self.genre_filter = QLineEdit()
        self.genre_filter.textChanged.connect(self.apply_filters)
        form_layout.addWidget(self.genre_filter)

        self.pages_checkbox = QCheckBox("Более 200 страниц")
        self.pages_checkbox.stateChanged.connect(self.apply_filters)
        form_layout.addWidget(self.pages_checkbox)
        
        form_layout.addStretch()
        main_layout.addLayout(form_layout, 1)

        # Правая панель (Таблица)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Страницы"])
        main_layout.addWidget(self.table, 3)

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        pages = self.pages_input.text()

        if not all([title, author, genre, pages]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            QMessageBox.warning(self, "Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }
        
        self.books.append(new_book)
        self.save_data()
        self.apply_filters()
        
        # Очистка полей
        for field in [self.title_input, self.author_input, self.genre_input, self.pages_input]:
            field.clear()

    def apply_filters(self):
        genre_text = self.genre_filter.text().lower()
        only_big_books = self.pages_checkbox.isChecked()

        filtered = [
            b for b in self.books 
            if genre_text in b['genre'].lower() 
            and (not only_big_books or b['pages'] > 200)
        ]
        self.update_table(filtered)

    def update_table(self, data_list):
        self.table.setRowCount(len(data_list))
        for row, book in enumerate(data_list):
            self.table.setItem(row, 0, QTableWidgetItem(book['title']))
            self.table.setItem(row, 1, QTableWidgetItem(book['author']))
            self.table.setItem(row, 2, QTableWidgetItem(book['genre']))
            self.table.setItem(row, 3, QTableWidgetItem(str(book['pages'])))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookTracker()
    window.show()
    sys.exit(app.exec())