from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class TaskDialog(QDialog):
    """Диалоговое окно для добавления/редактирования задачи"""
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        uic.loadUi("design/task_dialog.ui", self)  # Загрузка интерфейса

        # Заполнение полей при редактировании
        if task:
            self.title_input.setText(task['title'])
            self.desc_input.setPlainText(task['description'])
            self.status_input.setCurrentText(task['status'])

        # Обработка кнопок
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_data(self):
        """Получить данные из полей формы"""
        return {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'status': self.status_input.currentText()
        }