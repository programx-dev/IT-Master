from PyQt5 import QtCore, QtGui, QtWidgets
import StackLogin
import StackLesson
import StackTest
import StackResult
import StackTableResults
import Dialogs
import os
import sys
import json
import sqlite3  
import datetime    
from dataclasses import dataclass
import xml.etree.ElementTree as ET

@dataclass
class DataResult:
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int

@dataclass
class DataSave:
    date_start: datetime.datetime
    date_end: datetime.datetime
    name: str
    surname: str
    class_name: str
    course: str
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int

@dataclass
class DataLoggin:
    name: str
    surname: str
    class_name: str
    path_course: str   

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_window")
        self.setWindowTitle("IT Master")

        self.init_variables()

        self.setWindowIcon(QtGui.QIcon(self.path_image_logo))

        # создание страницы входа
        self.current_stack = StackLogin.StackLogin(path_cources = self.path_cources, path_imgs = self.path_imgs, data_theme = self.data_theme["stack_login"], func_start = self.open_lesson, func_table_results = self.open_table_result)

        # виджет стеков для страниц
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")

        self.setCentralWidget(self.stacked_widget)

        # добавление страницы входа в виджет стеков
        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def init_variables(self):
        self.path_settings = r"settings.json"

        # получение настроек
        with open(self.path_settings, "r", encoding = "utf-8") as file:
            self.data = json.load(file)

        self.path_theme = self.data["path_theme"]

        # получение настроек темы
        with open(self.path_theme, "r", encoding = "utf-8") as file:
            self.data_theme = json.load(file)

        self.path_cources = self.data["path_cources"]
        self.path_imgs = self.data["path_imgs"]
        self.path_database = self.data["path_database"]
        self.path_image_logo = os.path.join(self.path_imgs, r"logo.png")

        self.data_loggin = None

        # создание БД
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                date_start VARCHAR,
                date_end VARCHAR,
                name VARCHAR,
                surname VARCHAR,
                class_name VARCHAR,
                course VARCHAR,
                points_max INTEGER,
                points_right INTEGER,
                points_wrong INTEGER,
                points_skip INTEGER,
                result INTEGER
            ) """)

    def delete_old_record(self):
        # оставить в БД <= 100 записей
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT * FROM users""")
            amount_rows = i if (i := len(cursor.fetchall()) - 100) > 0 else 0

            cursor.execute("""DELETE FROM users WHERE date_end IN (SELECT date_end FROM users ORDER BY date_end ASC LIMIT ?)""", (amount_rows, ))

    def create_record(self, data: DataSave):
        # запись данных о прохождении в БД
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            values = (
                data.date_start.strftime(r"%d.%m.%Y %H:%M"),
                data.date_end.strftime(r"%d.%m.%Y %H:%M"),
                data.name,
                data.surname,
                data.class_name,
                data.course,
                data.points_max,
                data.points_right,
                data.points_wrong,
                data.points_skip,
                round(data.points_right / data.points_max * 100),
            )

            cursor.execute("""
            INSERT INTO users(
                date_start,
                date_end,
                name,
                surname,
                class_name,
                course,
                points_max,
                points_right,
                points_wrong,
                points_skip,
                result) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """, values)

        self.delete_old_record()

    def finish_test(self, data: StackTest.DataPassage):
        # получение данных о прохождении
        data_save = DataSave(
            name = self.data_loggin.name,
            surname = self.data_loggin.surname,
            class_name = self.data_loggin.class_name,
            course = os.path.splitext(os.path.basename(self.data_loggin.path_course))[0],
            date_start = data.date_start,
            date_end = data.date_end,
            points_max = data.points_max,
            points_right = data.points_right,
            points_wrong = data.points_wrong,
            points_skip = data.points_skip
        )

        data_result = DataResult(
            points_max = data.points_max,
            points_right = data.points_right,
            points_wrong = data.points_wrong,
            points_skip = data.points_skip
        )

        self.create_record(data_save)

        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка нового окна
        self.current_stack = StackResult.StackResult(data = data_result, data_theme = self.data_theme["stack_result"], func = self.to_main)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def start_test(self):
        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка нового окна
        self.current_stack = StackTest.StackTest(func = self.finish_test, path_imgs = self.path_imgs, data_theme = self.data_theme["stack_test"], path_course = self.data_loggin.path_course)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def open_table_result(self):
         # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка нового окна
        self.current_stack = StackTableResults.StackTableResults(path_database = self.path_database, func = self.to_main, data_theme = self.data_theme["stack_table_result"])

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def open_lesson(self, data: StackLogin.DataPassage):
        self.data_loggin = DataLoggin(
            name = data.name,
            surname = data.surname,
            class_name = data.class_name,
            path_course = data.path_course
        )

        # определение есть ли урок
        tree = ET.parse(self.data_loggin.path_course)
        root = tree.getroot()

        if root.find("lesson") != None:
            # удаление старого окна
            self.stacked_widget.removeWidget(self.current_stack)

            # создание и упаковка нового окна
            self.current_stack = StackLesson.StackLesson(path_course = self.data_loggin.path_course, data_theme = self.data_theme["stack_lesson"], func = self.start_test)

            self.stacked_widget.addWidget(self.current_stack)
            self.stacked_widget.setCurrentWidget(self.current_stack)

            self.current_stack.load_lesson()
        else:
            self.start_test()

    def to_main(self):
        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

         # создание и упаковка нового окна
        if self.data_loggin != None:
            self.current_stack = StackLogin.StackLogin(path_cources = self.path_cources, path_imgs = self.path_imgs, data_theme = self.data_theme["stack_login"], func_start = self.open_lesson, func_table_results = self.open_table_result, name = self.data_loggin.name, surname = self.data_loggin.surname, class_name = self.data_loggin.class_name)
        else:
            self.current_stack = StackLogin.StackLogin(path_cources = self.path_cources, path_imgs = self.path_imgs, data_theme = self.data_theme["stack_login"], func_start = self.open_lesson, func_table_results = self.open_table_result)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.open_dialog_menu()

    def open_dialog_info(self):
        dialog = Dialogs.DialogInfo(data_theme = self.data_theme["dialog_info"], path_logo = self.path_image_logo, parent = self)

    def open_dialog_menu(self):
        dialog = Dialogs.DialogMenu(data_theme = self.data_theme["dialog_menu"], parent = self)

        dialog.clicked_exit.connect(sys.exit)
        dialog.clicked_info.connect(self.open_dialog_info)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window_main = Main()

    # window_main.showMaximized()
    window_main.showFullScreen()

    sys.exit(app.exec_())
