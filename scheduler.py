import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, QTime, Qt

tasks = [
    ("09:00", "Morning Exercise"),
    ("10:00", "Team Meeting"),
    ("11:00", "Work on Project A"),
    ("12:00", "Lunch Break"),
    ("13:00", "Read Emails"),
    ("14:00", "Client Call"),
    ("15:15", "Finish Report"),
    ("20:00", "Dinner"),
    ("21:00", "Relax Time"),
    ("22:00", "Prepare for Tomorrow"),
]

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Schedule")
        self.layout = QVBoxLayout()

        self.task_labels = []
        self.task_times = []

        for time, task in tasks:
            task_time = QTime.fromString(time.strip(), "HH:mm")

            if task_time.isValid():
                self.task_times.append((task_time, task))
            else:
                print(f"Invalid time format for {time}")

            task_label = QLabel(f"{time} - {task}")
            task_label.setStyleSheet("background-color: grey; padding: 10px;")
            task_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.layout.addWidget(task_label)
            self.task_labels.append(task_label)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateHighlight)
        self.timer.start(60000)
        self.updateHighlight()  # Initial highlight

        # Add exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.confirm_exit)
        self.layout.addWidget(self.exit_button)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.confirm_exit()

    def updateHighlight(self):
        current_time = QTime.currentTime()

        for i, (task_time, task) in enumerate(self.task_times):
            if i + 1 < len(self.task_times):
                end_time = self.task_times[i + 1][0]
            else:
                end_time = QTime(23, 59)

            if task_time <= current_time < end_time:
                self.task_labels[i].setStyleSheet("background-color: yellow; padding: 10px;")
            else:
                self.task_labels[i].setStyleSheet("background-color: grey; padding: 10px;")

    def confirm_exit(self):
        reply = QMessageBox.question(self, 'Exit Confirmation', 
                                     'Are you sure you want to exit?', 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()  # Quit the application

if __name__ == "__main__":
    app = QApplication(sys.argv)
    schedule = ScheduleWidget()
    schedule.resize(300, 400)
    schedule.show()
    sys.exit(app.exec_())
