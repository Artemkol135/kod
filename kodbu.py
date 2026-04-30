import sys
import json
import os
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox,
                             QHeaderView, QComboBox)
from PyQt6.QtCore import Qt

class TrainingPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Training Planner Pro")
        self.setMinimumSize(900, 600)
        self.file_path = "trainings.json"
        self.trainings = self.load_data()
        
        self.init_ui()
        self.apply_filters()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Панель управления
        controls_layout = QVBoxLayout()
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("ДД.ММ.ГГГГ")
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Силовая", "Кардио", "Йога", "Плавание", "Растяжка"])
        self.type_input.setEditable(True)
        
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Минуты (напр. 60)")
        
        # Форма
        for label, widget in [("Дата тренировки:", self.date_input), 
                              ("Тип тренировки:", self.type_input),
                              ("Длительность (мин):", self.duration_input)]:
            controls_layout.addWidget(QLabel(label))
            controls_layout.addWidget(widget)
        
        add_btn = QPushButton("➕ Добавить тренировку")
        add_btn.clicked.connect(self.add_training)
        add_btn.setStyleSheet("background-color: #3498db; color: white; height: 40px;")
        controls_layout.addWidget(add_btn)

        # Фильтры
        controls_layout.addSpacing(30)
        controls_layout.addWidget(QLabel("🔍 Фильтр по типу:"))
        self.type_filter = QLineEdit()
        self.type_filter.textChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.type_filter)

        controls_layout.addWidget(QLabel("📅 Фильтр по дате:"))
        self.date_filter = QLineEdit()
        self.date_filter.setPlaceholderText("Поиск по дате...")
        self.date_filter.textChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.date_filter)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, 1)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Дата", "Тип", "Длительность (мин)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table, 3)

    def load_data(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            return []
        return []

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")

    def validate_input(self, date, duration):
        # Проверка даты (ДД.ММ.ГГГГ)
        date_pattern = r"^\d{2}\.\d{2}\.\d{4}$"
        if not re.match(date_pattern, date):
            QMessageBox.warning(self, "Ошибка", "Введите дату в формате ДД.ММ.ГГГГ")
            return False
        
        # Проверка длительности
        if not duration.isdigit() or int(duration) <= 0:
            QMessageBox.warning(self, "Ошибка", "Длительность должна быть положительным числом")
            return False
        
        return True

    def add_training(self):
        date = self.date_input.text().strip()
        t_type = self.type_input.currentText().strip()
        duration = self.duration_input.text().strip()

        if not date or not t_type or not duration:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if self.validate_input(date, duration):
            self.trainings.append({
                "date": date,
                "type": t_type,
                "duration": int(duration)
            })
            self.save_data()
            self.apply_filters()
            self.date_input.clear()
            self.duration_input.clear()

    def apply_filters(self):
        type_txt = self.type_filter.text().lower()
        date_txt = self.date_filter.text().lower()

        filtered = [t for t in self.trainings 
                    if type_txt in t['type'].lower() 
                    and date_txt in t['date'].lower()]
        
        self.table.setRowCount(len(filtered))
        for r, t in enumerate(filtered):
            self.table.setItem(r, 0, QTableWidgetItem(t['date']))
            self.table.setItem(r, 1, QTableWidgetItem(t['type']))
            self.table.setItem(r, 2, QTableWidgetItem(str(t['duration'])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainingPlanner()
    window.show()
    sys.exit(app.exec())
