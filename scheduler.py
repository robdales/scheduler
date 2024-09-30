import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer, QTime

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
            task_time = QTime.fromString(time.strip(), "HH:mm")  # Military time format

            if task_time.isValid():
                self.task_times.append((task_time, task))  # Append time and task
            else:
                print(f"Invalid time format for {time}")  # Debugging line

            task_label = QLabel(f"{time} - {task}")
            task_label.setStyleSheet("background-color: grey; padding: 10px;")
            task_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.layout.addWidget(task_label)
            self.task_labels.append(task_label)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateHighlight)
        self.timer.start(60000)  # Check every minute(60,000 miliseconds)
        self.updateHighlight()  # Initial highlight

    def updateHighlight(self):
        current_time = QTime.currentTime()

        for i, (task_time, task) in enumerate(self.task_times):
            # Determine the end time for the current task
            if i + 1 < len(self.task_times):
                end_time = self.task_times[i + 1][0]  # Use the next task's start time
            else:
                end_time = QTime(23, 59)  # Last task ends at 11:59 PM

            # Highlight if the current time is between the task's start time and the next task's start time
            if task_time <= current_time < end_time:
                self.task_labels[i].setStyleSheet("background-color: yellow; padding: 10px;")
            else:
                self.task_labels[i].setStyleSheet("background-color: grey; padding: 10px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    schedule = ScheduleWidget()
    schedule.resize(300, 400)
    schedule.show()
    sys.exit(app.exec_())
