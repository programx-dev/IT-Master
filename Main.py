from PyQt6 import QtCore, QtGui, QtWidgets
import StackHomePage
import StackLesson
import StackTesting
import StackResult
import StackTableResults
import Window
import Dialogs
import version
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
    dict_result: dict

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

class Main(Window.Window):
    def __init__(self):
        self.__text_info = """IT Master - это школьный предметный тренажёр по информатике, позволяющий изучить материал урока и закрепить полученные знания, выполнив тест\n
Ведущий разрабочик - Смирнов Н. А., 9 класс, ГБОУ школа №1370\n
Приложение написано на языке программирования Python"""
        self.__path_settings = r"settings.json"
        self.__test_started = False
        self.__current_stack = None

        # получение настроек из файла
        with open(self.__path_settings, "r", encoding = "utf-8") as file:
            self.__data = json.load(file)

        self.__path_theme = self.__data["path_theme"]

        # получение настроек цветовой темы
        with open(self.__path_theme, "r", encoding = "utf-8") as file:
            self.__data_theme = json.load(file)

        self.__path_courses = self.__data["path_courses"]
        self.__path_images = self.__data["path_images"]
        self.__path_database = self.__data["path_database"]
        self.__path_image_logo = os.path.join(self.__path_images, r"logo.png")

        self.__data_loggin = DataLoggin(
            name = None,
            surname = None,
            class_name = None,
            path_course = None
        )

        # создание БД если её нет
        with sqlite3.connect(self.__path_database) as db:
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

        super().__init__(data_theme = self.__data_theme["window"])

        # панель инструментов
        self.toolbar = Window.ToolBar(self.__path_images, self.__data_theme["frame_tool_bar"])
        self.add_widget(self.toolbar)

        Dialogs.__parent__ = self
        StackTesting.__parent__ = self

        self.setWindowTitle("IT Master")
        self.setWindowIcon(QtGui.QIcon(self.__path_image_logo))

        # виджет стеков для страниц
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.add_widget(self.__stacked_widget)

        # присоединение слотов к сигналам
        self.toolbar.tool_button_home_page_cliced.connect(self.__open_home_page)

        # выбрать кнопку Домашняя страница
        self.toolbar.tool_button_home_page.press_tool_button()

    def __open_home_page(self):
        if type(self.__current_stack) == StackHomePage.StackHomePage:
            return
        
        if self.__test_started:
            dialog = Dialogs.Dialog(data_theme = self.__data_theme["dialog"], parent = self.window())
            dialog.set_window_title("Покинуть тестирование")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование?")
            dialog.set_description("Результаты не сохранятся")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() != Dialogs.ButtonRole.accept:
                self.toolbar.tool_button_test.set_selected()
                return  

        self.toolbar.update_style_sheet(Window.PropertyPages.home_page)        

        # удаление старого окна
        if self.__current_stack!= None:
            self.__stacked_widget.removeWidget(self.__current_stack)

        # создание и упаковка окна входа
        self.__current_stack = StackHomePage.StackHomePage(
            path_courses = self.__path_courses, 
            path_images = self.__path_images, 
            path_theme = self.__path_theme,
            data_theme = self.__data_theme["stack_home_page"], 
        )
        self.__current_stack.push_button_clicked_start_test.connect(self.__start)

        self.__stacked_widget.addWidget(self.__current_stack)
        self.__stacked_widget.setCurrentWidget(self.__current_stack)

    def __delete_old_record(self):
        # оставить в БД до 100 записей
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT date_end FROM users""")
            amount_rows = i if (i := len(cursor.fetchall()) - 100) > 0 else 0

            cursor.execute("""DELETE FROM users WHERE date_end IN (SELECT date_end FROM users ORDER BY date_end ASC LIMIT ?)""", (amount_rows, ))

    def __create_record(self, data: DataSave):
        # запись данных о прохождении в БД
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            values = (
                data.date_start.strftime(r"%Y.%m.%d %H:%M"),
                data.date_end.strftime(r"%Y.%m.%d %H:%M"),
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

        self.__delete_old_record()

    def __finish_test(self, data: StackTesting.DataPassage):
        self.__test_started = False

        list_status = [i.status for i in data.list_data_result]

        # получение данных о прохождении
        data_save = DataSave(
            name = self.__data_loggin.name,
            surname = self.__data_loggin.surname,
            class_name = self.__data_loggin.class_name,
            course = os.path.splitext(os.path.basename(self.__data_loggin.path_course))[0],
            date_start = data.date_start,
            date_end = data.date_end,
            points_max = len(list_status),
            points_right = list_status.count(StackTesting.AnswerStatus.right),
            points_wrong = list_status.count(StackTesting.AnswerStatus.wrong),
            points_skip = list_status.count(StackTesting.AnswerStatus.skip)
        )

        data_result = DataResult(
            points_max = data_save.points_max,
            points_right = data_save.points_right,
            points_wrong = data_save.points_wrong,
            points_skip = data_save.points_skip,
            dict_result = data.list_data_result
        )

        self.__create_record(data_save)

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_stack)

        # создание и упаковка окна результата выполнения
        self.__current_stack = StackResult.StackResult(
            data_result = data_result, 
            data_theme = self.__data_theme["stack_result"], 
            func = self.__open_home_page
        )

        self.__stacked_widget.addWidget(self.__current_stack)
        self.__stacked_widget.setCurrentWidget(self.__current_stack)

    def __start_test(self):
        self.toolbar.update_style_sheet(Window.PropertyPages.test_page)
        self.toolbar.tool_button_test.press_tool_button()
        self.toolbar.tool_button_test.show()

        self.__test_started = True

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_stack)

        # создание и упаковка окна с тестом
        self.__current_stack = StackTesting.StackTesting(
            path_course = self.__data_loggin.path_course,
            path_images = self.__path_images, 
            icon_dialogs = QtGui.QPixmap(self.__path_image_logo),
            data_theme = self.__data_theme["stack_testing"] 
        )
        self.__current_stack.push_button_finish_cliced.connect(self.__finish_test)

        self.__stacked_widget.addWidget(self.__current_stack)
        self.__stacked_widget.setCurrentWidget(self.__current_stack)

    def __open_table_result(self, data: StackHomePage.DataHomePage):
        # проверить пустая ли таблица
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT date_end FROM users""")
            amount = len(cursor.fetchall())

        if amount != 0:
            self.data_loggin = DataLoggin(
                name = data.name,
                surname = data.surname,
                class_name = data.class_name,
                path_course = data.path_course
            )

            # удаление старого окна
            self.__stacked_widget.removeWidget(self.__current_stack)

            # создание и упаковка окна с таблицей результатов
            self.__current_stack = StackTableResults.StackTableResults(
                path_database = self.__path_database, 
                func = self.__to_main,
                data_theme = self.__data_theme["stack_table_result"]
            )

            self.__stacked_widget.addWidget(self.__current_stack)
            self.__stacked_widget.setCurrentWidget(self.__current_stack)

        else:
            self.__open_dialog_table_results_empty()

    def __start(self, data: StackHomePage.DataHomePage):
        # ?
        self.__data_loggin = DataLoggin(
            name = None,
            surname = None,
            class_name = None,
            path_course = data.path_course
        )
        # ?

        self.__start_test()


        # # определение есть ли урок
        # tree = ET.parse(self.__data_loggin.path_course)
        # root = tree.getroot()

        # if root.find("lesson") != None:
        #     self.__open_lesson()
        # else:
        #     self.__start_test()

    def __open_lesson(self):
        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_stack)

        tree = ET.parse(self.__data_loggin.path_course)
        root = tree.getroot()
        path_lesson = os.path.join(os.path.split(self.__data_loggin.path_course)[0], root.find("lesson").text).replace("\\", "/")

        # создание и упаковка окна урока
        self.__current_stack = StackLesson.StackLesson(
            path_lesson = path_lesson, 
            data_theme = self.__data_theme["stack_lesson"], 
            func = self.__start_test
        )

        self.__stacked_widget.addWidget(self.__current_stack)
        self.__stacked_widget.setCurrentWidget(self.__current_stack)

        # показать урок
        self.__current_stack.load_lesson()
        
    def __to_main(self):
        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_stack)

        # создание и упаковка окна входа
        self.__current_stack = StackHomePage.StackLogin(
            path_theme = self.__path_theme,
            path_courses = self.__path_courses, 
            path_images = self.__path_images, 
            data_theme = self.__data_theme["stack_login"], 
            func_start = self.__start, 
            func_table_results = self.__open_table_result, 
            surname = self.__data_loggin.surname, 
            name = self.__data_loggin.name,
            class_name = self.__data_loggin.class_name
        )

        self.__stacked_widget.addWidget(self.__current_stack)
        self.__stacked_widget.setCurrentWidget(self.__current_stack)

    def __open_dialog_info(self):
        dialog = Dialogs.DialogInfo(
            data_theme = self.__data_theme["dialog_info"],
            version = f"Версия {version.__version__}",
            name = "IT Master",
            text_info = self.__text_info,
            path_logo = self.__path_image_logo,
            parent = self
        )

    def __open_dialog_table_results_empty(self):
        dialog = Dialogs.DialogTableResultsEmpty(
            data_theme = self.__data_theme["dialog_table_results_empty"], 
            parent = self
        )

    def __exit_test(self):
        self.__test_started = False

        self.__to_main()

    def __close_window(self):
        if self.__test_started:
            dialog = Dialogs.DialogExit(
                data_theme = self.__data_theme["dialog_exit_test"], 
                parent = self
            )
            dialog.push_button_clicked_exit.connect(self.__exit_test)
        else:
            super().close_window()

if __name__ == "__main__":
    # https://doc.qt.io/qt-5/highdpi.html
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    #     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    #     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_QUICK_BACKEND"] = "software"

    # QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # os.environ["QT_SCALE_FACTOR"]             = "1"

    app = QtWidgets.QApplication(sys.argv)
    # app.setAttribute(QtCore.Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    window_main = Main()
    # window_main.set_window_flags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
    window_main.show_maximized()
    # window_main.show_normal()

    sys.exit(app.exec())