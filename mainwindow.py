from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDateTime
from PyQt5 import uic
from database import get_connection, create_table
from dialogs import TaskDialog

class ToDoApp(QWidget):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        uic.loadUi("design/main_window.ui", self)  # Загрузка интерфейса

        # Подключение к базе данных
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        create_table(self.conn)

        # Привязка сигналов к методам
        self.search_input.textChanged.connect(self.refresh_table)
        self.status_filter.currentIndexChanged.connect(self.refresh_table)
        self.btn_add.clicked.connect(self.add_task)
        self.btn_edit.clicked.connect(self.edit_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.btn_refresh.clicked.connect(self.refresh_table)

        # Настройка таблицы
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['Заголовок', 'Описание', 'Статус', 'Создано', 'Изменено']
        )
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        self.refresh_table()  # Показать задачи

    def get_filtered_tasks(self):
        """Получить задачи с учетом фильтра и поиска"""
        status = self.status_filter.currentText()
        keyword = self.search_input.text()
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if status != "Все":
            query += " AND status = ?"
            params.append(status)

        if keyword:
            query += " AND title LIKE ?"
            params.append(f"%{keyword}%")

        return self.cursor.execute(query, params).fetchall()

    def refresh_table(self):
        """Обновить таблицу задач"""
        tasks = self.get_filtered_tasks()
        self.table.setRowCount(0)
        for row_data in tasks:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col in range(1, 6):
                self.table.setItem(row, col - 1, QTableWidgetItem(str(row_data[col])))

    def add_task(self):
        """Добавить новую задачу"""
        dialog = TaskDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            now = QDateTime.currentDateTime().toString()
            self.cursor.execute("""
                INSERT INTO tasks (title, description, status, created, updated)
                VALUES (?, ?, ?, ?, ?)
            """, (data['title'], data['description'], data['status'], now, now))
            self.conn.commit()
            self.refresh_table()

    def edit_task(self):
        """Редактировать выбранную задачу"""
        selected = self.table.currentRow()
        if selected >= 0:
            title = self.table.item(selected, 0).text()
            task_data = self.cursor.execute(
                "SELECT * FROM tasks WHERE title = ?", (title,)
            ).fetchone()
            if task_data:
                dialog = TaskDialog(self, {
                    'title': task_data[1],
                    'description': task_data[2],
                    'status': task_data[3]
                })
                if dialog.exec_():
                    new_data = dialog.get_data()
                    now = QDateTime.currentDateTime().toString()
                    self.cursor.execute("""
                        UPDATE tasks SET title = ?, description = ?, status = ?, updated = ?
                        WHERE id = ?
                    """, (
                        new_data['title'],
                        new_data['description'],
                        new_data['status'],
                        now,
                        task_data[0]
                    ))
                    self.conn.commit()
                    self.refresh_table()

    def delete_task(self):
        """Удалить выбранную задачу"""
        selected = self.table.currentRow()
        if selected >= 0:
            title = self.table.item(selected, 0).text()
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы действительно хотите удалить задачу '{title}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM tasks WHERE title = ?", (title,))
                self.conn.commit()
                self.refresh_table()