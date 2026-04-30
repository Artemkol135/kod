import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox,
                             QHeaderView)

class BookTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Tracker Pro")
        self.setMinimumSize(900, 600)
        self.file_path = "books.json"
        self.books = self.load_data()
        
        self.init_ui()
        self.apply_filters()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая панель: Ввод и Управление
        controls_layout = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.pages_input = QLineEdit()
        
        # Поля ввода
        for label, widget in [("Название:", self.title_input), 
                              ("Автор:", self.author_input),
                              ("Жанр:", self.genre_input),
                              ("Страницы:", self.pages_input)]:
            controls_layout.addWidget(QLabel(label))
            controls_layout.addWidget(widget)
        
        # Кнопки действий
        add_btn = QPushButton("➕ Добавить / Обновить")
        add_btn.clicked.connect(self.add_or_update_book)
        add_btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        controls_layout.addWidget(add_btn)

        del_btn = QPushButton("🗑 Удалить выбранное")
        del_btn.clicked.connect(self.delete_book)
        controls_layout.addWidget(del_btn)

        # Фильтры
        controls_layout.addSpacing(30)
        controls_layout.addWidget(QLabel("🔍 Фильтр по жанру:"))
        self.genre_filter = QLineEdit()
        self.genre_filter.textChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.genre_filter)

        self.pages_checkbox = QCheckBox("Более 200 страниц")
        self.pages_checkbox.stateChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.pages_checkbox)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, 1)

        # Правая панель: Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Страницы"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemDoubleClicked.connect(self.load_to_edit) # Редактирование по двойному клику
        main_layout.addWidget(self.table, 3)

    def load_data(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось прочитать базу данных: {e}")
        return []

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Ошибка сохранения", f"Не удалось записать файл: {e}")

    def add_or_update_book(self):
        title, author = self.title_input.text().strip(), self.author_input.text().strip()
        genre, pages = self.genre_input.text().strip(), self.pages_input.text().strip()

        if not all([title, author, genre, pages]):
            QMessageBox.warning(self, "Валидация", "Заполните все поля!")
            return
        
        if not pages.isdigit():
            QMessageBox.warning(self, "Валидация", "Страницы должны быть числом!")
            return

        # Если книга с таким названием уже есть — обновляем её (редактирование)
        for b in self.books:
            if b['title'].lower() == title.lower():
                b.update({"author": author, "genre": genre, "pages": int(pages)})
                break
        else:
            self.books.append({"title": title, "author": author, "genre": genre, "pages": int(pages)})

        self.save_data()
        self.apply_filters()
        self.clear_inputs()

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        title = self.table.item(selected_row, 0).text()
        self.books = [b for b in self.books if b['title'] != title]
        
        self.save_data()
        self.apply_filters()

    def load_to_edit(self, item):
        row = item.row()
        self.title_input.setText(self.table.item(row, 0).text())
        self.author_input.setText(self.table.item(row, 1).text())
        self.genre_input.setText(self.table.item(row, 2).text())
        self.pages_input.setText(self.table.item(row, 3).text())

    def apply_filters(self):
        g_text = self.genre_filter.text().lower()
        big_only = self.pages_checkbox.isChecked()

        filtered = [b for b in self.books 
                    if g_text in b['genre'].lower() 
                    and (not big_only or b['pages'] > 200)]
        
        self.table.setRowCount(len(filtered))
        for r, b in enumerate(filtered):
            self.table.setItem(r, 0, QTableWidgetItem(b['title']))
            self.table.setItem(r, 1, QTableWidgetItem(b['author']))
            self.table.setItem(r, 2, QTableWidgetItem(b['genre']))
            self.table.setItem(r, 3, QTableWidgetItem(str(b['pages'])))

    def clear_inputs(self):
        for w in [self.title_input, self.author_input, self.genre_input, self.pages_input]:
            w.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookTracker()
    window.show()
    sys.exit(app.exec())
