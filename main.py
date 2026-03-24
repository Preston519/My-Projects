from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets as qtw
import os
import datetime

def add_year(date: datetime.date):
    date.year += 1
    return date

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BNO date finder")
        self.resize(QtCore.QSize(560, 360))
        
        self.date_ranges = []
        
        # Stuff for highlighting date ranges
        self.date1 = None
        self.date2 = None
        self.highlighter = QtGui.QTextCharFormat()
        self.highlighter.setBackground(QtGui.QBrush(self.palette().highlight()))
        
        # Start page
        start_page_layout = qtw.QVBoxLayout()
        start_page_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        start_text = qtw.QLabel()
        start_text.setText("This is a tool to calculate continuous residence for the purpose of eligibility for Indefinite Leave to Remain (ILR) applications in the UK.\n\nTypically, the required period of continuous residence is 5 or 10 years without more than 180 days spent outside the UK in any 12-month period. For the purpose of adaptability, all inputted periods will be accounted for in calculating continuous residence validity.\n\nAbsences are saved as the absences.sav file in the executable directory. Absence ranges are inclusive.\n")
        # start_text.setText("This is a tool to calculate continuous residence for the purpose of eligibility for Indefinite Leave to Remain (ILR) applications in the UK.\n\nTypically, the required period of continuous residence is 5 or 10 years without more than 180 days spent outside the UK in any 12-month period.\n\nAbsences are saved as the absences.sav file in the executable directory. Absence ranges are inclusive.\n")
        start_text.setWordWrap(True)
        start_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        start_button = qtw.QPushButton("Start")
        start_button.clicked.connect(self.start)
        start_page_layout.addWidget(start_text)
        start_page_layout.addWidget(start_button)
        
        start_page = qtw.QWidget()
        start_page.setLayout(start_page_layout)       
        
        
        # Date page
        date_page_layout = qtw.QHBoxLayout()
        
        rightlayout = qtw.QVBoxLayout()
        self.rightbox = qtw.QTextEdit()
        self.rightbox.setReadOnly(True)
        save_button = qtw.QPushButton("Save absences")
        save_button.clicked.connect(self.save_to_file)
        load_button = qtw.QPushButton("Load absences")
        load_button.clicked.connect(self.load_from_file)
        self.message_box = qtw.QLabel()
        rightlayout.addWidget(save_button)
        rightlayout.addWidget(load_button)
        rightlayout.addWidget(self.rightbox)
        rightlayout.addWidget(self.message_box)
        
        leftlayout = qtw.QVBoxLayout()
        self.calendar = qtw.QCalendarWidget()
        self.calendar.clicked.connect(self.select_date_range)
        button = qtw.QPushButton("Add absence")
        button.clicked.connect(self.add_range)
        delete = qtw.QPushButton("Delete last absence")
        delete.clicked.connect(self.remove_range)
        submit = qtw.QPushButton("Submit dates")
        submit.clicked.connect(self.submit)
        leftlayout.addWidget(self.calendar)
        leftlayout.addWidget(button)
        leftlayout.addWidget(delete)
        leftlayout.addWidget(submit)
        
        date_page_layout.addLayout(leftlayout, stretch=1)
        date_page_layout.addLayout(rightlayout, stretch=1)
        
        date_page = qtw.QWidget()
        date_page.setLayout(date_page_layout)
        
        # Result page
        result_page_layout = qtw.QVBoxLayout()
        result_page_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.result_box = qtw.QLabel()
        self.result_box.setWordWrap(True)
        self.result_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return_button = qtw.QPushButton("Return")
        return_button.clicked.connect(self.return_to_dates)
        result_page_layout.addWidget(self.result_box)
        result_page_layout.addWidget(return_button)
        
        result_page = qtw.QWidget()
        result_page.setLayout(result_page_layout)
        
        
        self.page_manager = qtw.QStackedWidget()
        self.page_manager.addWidget(start_page)
        self.page_manager.addWidget(date_page)
        self.page_manager.addWidget(result_page)
        
        self.setCentralWidget(self.page_manager)

    def start(self):
        # self.period_length = self.period_input.value()
        # self.application_date = self.application_date_input.date()
        self.page_manager.setCurrentIndex(1)

    def return_to_dates(self):
        self.message_box.setText("")
        self.page_manager.setCurrentIndex(1)

    def select_date_range(self, date_value):
        self.highlight_range(QtGui.QTextCharFormat())
        if qtw.QApplication.keyboardModifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier and self.date1:
            self.date2 = date_value
            self.highlight_range(self.highlighter)
        else:
            self.date1 = date_value
            self.date2 = None
        
    def highlight_range(self, format):
        if self.date1 and self.date2:
            d1 = min(self.date1, self.date2)
            d2 = max(self.date1, self.date2)
            while d1.daysTo(d2) >= 0:
                self.calendar.setDateTextFormat(d1, format)
                d1 = d1.addDays(1)
        
    def add_range(self):
        if self.date2:
            d1, d2 = sorted([self.date1, self.date2])
            self.date_ranges.append((d1, d2))
            self.rightbox.insertPlainText(f"{d1.toString()} to {d2.toString()}\n")
        elif self.date1:
            self.date_ranges.append((self.date1, self.date1))
            self.rightbox.insertPlainText(self.date1.toString() + "\n")
        if self.rightbox.toPlainText().endswith("\n\n"):
            self.rightbox.setPlainText(self.rightbox.toPlainText()[:-1])
        if self.date1:
            self.message_box.setText("Absence range added")
        
    def remove_range(self):
        if self.date_ranges:
            self.date_ranges.pop()
            self.rightbox.setPlainText("\n".join(self.rightbox.toPlainText().split("\n")[:-2]) + "\n")
            self.message_box.setText("Absence range removed")
        else:
            self.message_box.setText("No absence ranges available")
            
        
    def submit(self):
        self.message_box.setText("Please Wait. Processing...")
        days = set()
        result = None
        for from_date, to_date in self.date_ranges:
            from_date: QtCore.QDate
            to_date: QtCore.QDate
            while from_date.daysTo(to_date) >= 0:
                days.add(from_date.toPyDate())
                from_date = from_date.addDays(1)
        for _, to_date in sorted(self.date_ranges, reverse=True):
            period_start = to_date.addYears(-1).toPyDate()
            absent_count = sum(1 for _ in filter(lambda x: x > period_start, days))
            if absent_count > 180:
                break_start = period_start
                while break_start not in days:
                    break_start += datetime.timedelta(days=1)
                break_end = break_start - datetime.timedelta(days=1)
                break_end.year += 1
                add_year(break_start + datetime.timedelta(days=-1))
                result = f"Continuous residence limit has been breached.\n\nTotal amount of absent days in the range {break_start.strftime('%d %B %Y')} to {add_year(break_start + datetime.timedelta(days=-1)).strftime('%d %B %Y')} is {absent_count}, which is above 180"
                break
        if result is None:
            result = "Continuous residence limit has not been breached. Your settlement application is valid."
        self.result_box.setText(result)
        self.page_manager.setCurrentIndex(2)
        
    def save_to_file(self):
        with open("absences.sav", "wb") as file:
            file.writelines(f"{from_date.toString('yyyy-MM-dd')}, {to_date.toString('yyyy-MM-dd')}\n".encode("utf-8") for from_date, to_date in self.date_ranges)
        self.message_box.setText("Absences saved to file")
            
    def load_from_file(self):
        if not os.path.exists("absences.sav"):
            self.message_box.setText("Data file not found")
        else:
            date_ranges = []
            try:
                with open("absences.sav", "rb") as file:
                    for line in file.readlines():
                        if len(line) != 23:
                            raise TypeError
                        date_ranges.append((QtCore.QDate.fromString(line[:10].decode(), "yyyy-MM-dd"), QtCore.QDate.fromString(line[12:-1].decode(), "yyyy-MM-dd")))
                self.date_ranges = date_ranges
                self.rightbox.setPlainText("\n".join(f"{from_date.toString()} to {to_date.toString()}" for from_date, to_date in date_ranges) + "\n")
                self.message_box.setText("Absences loaded from file")
            except TypeError:
                self.message_box.setText("Data file is invalid")

app = qtw.QApplication([])

window = MainWindow()
window.show()

app.exec()