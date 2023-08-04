from PyQt6 import QtCore, QtGui, QtWidgets
import PageHome
import StackLesson
import PageTesting
import StackResult
import StackTableResults
import Window
import Dialogs
import version
import os
import sys
import json
import enum
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

class PropertyPages(enum.Enum):
    home_page = 0
    test_page = 1

class ToolButtonToolbar(QtWidgets.QToolButton):
    """Кнопка панели инструментов"""
    tool_button_selected = None
    tool_button_clicked = QtCore.pyqtSignal()

    def __init__(self, path_image: str, text: str, data_theme: dict):
        super().__init__()

        self.__path_image = path_image
        self.__image = QtGui.QIcon(self.__path_image)
        self.__text = text
        self.__data_theme = data_theme
        self.__selected = False

        self.setProperty("selected", self.__selected)
        self.setProperty("page", PropertyPages.home_page.value)

        self.setObjectName("tool_button")
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.clicked.connect(self.press_tool_button)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setIcon(self.__image)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setText(self.__text)
        self.setFont(QtGui.QFont("Segoe UI", 10))

        self.set_style_sheet()

    def press_tool_button(self):
        if self != ToolButtonToolbar.tool_button_selected and ToolButtonToolbar.tool_button_selected != None:
            ToolButtonToolbar.tool_button_selected.__set_selected(False)

        if self != ToolButtonToolbar.tool_button_selected:
            ToolButtonToolbar.tool_button_selected = self
            self.__set_selected(True)

            self.tool_button_clicked.emit()

    def __set_selected(self, selected: bool):
        self.__selected = selected

        self.setProperty("selected", self.__selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_selected(self):
        ToolButtonToolbar.tool_button_selected.__set_selected(False)
        ToolButtonToolbar.tool_button_selected = self
        self.__set_selected(True)

    def update_style_sheet(self, property: PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_button[page=\"{PropertyPages.home_page.value}\"][selected="true"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["home_page"]["selected"]["background"]};
            color: {self.__data_theme["home_page"]["selected"]["color"]};
        }} 
         #tool_button[page=\"{PropertyPages.home_page.value}\"][selected="false"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["home_page"]["not_selected"]["background"]};
            color: {self.__data_theme["home_page"]["not_selected"]["color"]};
        }}

        #tool_button[page=\"{PropertyPages.test_page.value}\"][selected="true"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["test_page"]["selected"]["background"]};
            color: {self.__data_theme["test_page"]["selected"]["color"]};
        }}
        #tool_button[page=\"{PropertyPages.test_page.value}\"][selected="false"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["test_page"]["not_selected"]["background"]};
            color: {self.__data_theme["test_page"]["not_selected"]["color"]};
        }} """)

class ToolBar(QtWidgets.QFrame):
    """Панель инструментов"""
    tool_button_home_page_cliced = QtCore.pyqtSignal()
    tool_button_results_cliced = QtCore.pyqtSignal()
    tool_button_test_cliced = QtCore.pyqtSignal()
    tool_button_settings_cliced = QtCore.pyqtSignal()
    tool_button_info_cliced = QtCore.pyqtSignal()

    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme
        self.__list_tool_buttons = list()

        self.setObjectName("tool_bar")
        self.setProperty("page", PropertyPages.home_page.value)

        # макет панели инструментов
        self.__vbox_layout_toolbar = QtWidgets.QVBoxLayout()
        self.__vbox_layout_toolbar.setContentsMargins(5, 5, 5, 5)
        self.__vbox_layout_toolbar.setSpacing(0)

        self.setLayout(self.__vbox_layout_toolbar)

        data_theme_tool_buttons = {
            "home_page": self.__data_theme["home_page"]["tool_button"],
            "test_page": self.__data_theme["test_page"]["tool_button"]
        }

        # кнопка Домашняя страница
        self.tool_button_home_page = ToolButtonToolbar(
            os.path.join(self.__path_images, r"home_page.png"), 
            "Домашняя\nстраница", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_home_page)
        self.tool_button_home_page.tool_button_clicked.connect(self.__press_tool_button_home_page)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_home_page)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Результаты
        self.tool_button_results = ToolButtonToolbar(
            os.path.join(self.__path_images, r"results.png"), 
            "Результаты", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_results)
        self.tool_button_results.tool_button_clicked.connect(self.__press_tool_button_results)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_results)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Тест
        self.tool_button_test = ToolButtonToolbar(
            os.path.join(self.__path_images, r"test.png"), 
            "Тест", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_test)
        self.tool_button_test.tool_button_clicked.connect(self.__press_tool_button_test)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_test)
        self.__vbox_layout_toolbar.addStretch(1)

        # кнопка Настройка
        self.tool_button_settings = ToolButtonToolbar(
            os.path.join(self.__path_images, r"settings.png"),
            "Настройка", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_settings)
        self.tool_button_settings.tool_button_clicked.connect(self.__press_tool_button_settings)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_settings)

        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Справка
        self.tool_button_info = ToolButtonToolbar(
            os.path.join(self.__path_images, r"info.png"),
            "Справка",
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_info)
        self.tool_button_info.tool_button_clicked.connect(self.__press_tool_button_info)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_info)

        self.set_style_sheet()

    def __press_tool_button_home_page(self):
        self.tool_button_home_page_cliced.emit()

    def __press_tool_button_results(self):
        self.tool_button_results_cliced.emit()

    def __press_tool_button_test(self):
        self.tool_button_test_cliced.emit()

    def __press_tool_button_settings(self):
        self.tool_button_settings_cliced.emit()

    def __press_tool_button_info(self):
        self.tool_button_info_cliced.emit()

    def update_style_sheet(self, property: PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

        for i in self.__list_tool_buttons:
            i.update_style_sheet(property)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_bar[page=\"{PropertyPages.home_page.value}\"] {{
            background: {self.__data_theme["home_page"]["background"]};
        }} 
        #tool_bar[page=\"{PropertyPages.test_page.value}\"] {{
            background: {self.__data_theme["test_page"]["background"]};
        }} """ )

class Main(Window.Window):
    """Главный класс"""

    def __init__(self):
        self.__text_info = """IT Master - это школьный предметный тренажёр по информатике, позволяющий изучить материал урока и закрепить полученные знания, выполнив тест\n
Ведущий разрабочик - Смирнов Н. А., 9 класс, ГБОУ школа №1370\n
Приложение написано на языке программирования Python"""
        self.__path_settings = r"settings.json"
        self.__test_started = False
        self.__current_page = None

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
        self.__toolbar = ToolBar(self.__path_images, self.__data_theme["tool_bar"])
        self.add_widget(self.__toolbar)

        self.setWindowTitle("IT Master")
        self.setWindowIcon(QtGui.QIcon(self.__path_image_logo))

        # виджет стеков для страниц
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.add_widget(self.__stacked_widget)

        # присоединение слотов к сигналам
        self.__toolbar.tool_button_home_page_cliced.connect(self.__open_home_page)

        # выбрать кнопку Домашняя страница
        self.__toolbar.tool_button_home_page.press_tool_button()

    def __open_home_page(self):
        if type(self.__current_page) == PageHome.PageHome:
            return
        
        if self.__test_started:
            dialog = Dialogs.Dialog(data_theme = self.__data_theme["dialog"])
            dialog.set_window_title("Покинуть тестирование")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование?")
            dialog.set_description("Результаты не сохранятся")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() != Dialogs.ButtonRole.accept:
                self.__toolbar.tool_button_test.set_selected()
                return  

        self.__test_started = False

        self.__toolbar.tool_button_test.hide()
        self.__toolbar.update_style_sheet(PropertyPages.home_page)        

        # удаление старого окна
        if self.__current_page!= None:
            self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна входа
        self.__current_page = PageHome.PageHome(
            path_courses = self.__path_courses, 
            path_images = self.__path_images, 
            path_theme = self.__path_theme,
            data_theme = self.__data_theme["stack_home_page"], 
        )
        self.__current_page.push_button_clicked_start_test.connect(self.__start)

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

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

    def __finish_test(self, data_result_testing: PageTesting.DataResultTesting):
        self.__toolbar.tool_button_test.hide()
        print(*data_result_testing.list_data_result, sep = "\n")
        self.__test_started = False

        # # получение данных о прохождении
        # data_save = DataSave(
        #     name = self.__data_loggin.name,
        #     surname = self.__data_loggin.surname,
        #     class_name = self.__data_loggin.class_name,
        #     course = os.path.splitext(os.path.basename(self.__data_loggin.path_course))[0],
        #     date_start = data.date_start,
        #     date_end = data.date_end,
        #     points_max = len(list_status),
        #     points_right = list_status.count(StackTesting.AnswerStatus.right),
        #     points_wrong = list_status.count(StackTesting.AnswerStatus.wrong),
        #     points_skip = list_status.count(StackTesting.AnswerStatus.skip)
        # )

        # data_result = DataResult(
        #     points_max = data_save.points_max,
        #     points_right = data_save.points_right,
        #     points_wrong = data_save.points_wrong,
        #     points_skip = data_save.points_skip,
        #     dict_result = data.list_data_result
        # )

        # self.__create_record(data_save)

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна результата выполнения
        self.__current_page = StackResult.PageResultTesting(
            data_result_testing = data_result_testing, 
            path_images = self.__path_images,
            data_theme = self.__data_theme["page_result_testing"]
        )

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __start_test(self):
        self.__toolbar.update_style_sheet(PropertyPages.test_page)
        self.__toolbar.tool_button_test.press_tool_button()
        self.__toolbar.tool_button_test.show()

        self.__test_started = True

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна с тестом
        self.__current_page = PageTesting.PageTesting(
            path_course = self.__data_loggin.path_course,
            path_images = self.__path_images, 
            data_theme = self.__data_theme["page_testing"] 
        )
        self.__current_page.push_button_finish_cliced.connect(self.__finish_test)

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __open_table_result(self, data: PageHome.DataPageHome):
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
            self.__stacked_widget.removeWidget(self.__current_page)

            # создание и упаковка окна с таблицей результатов
            self.__current_page = StackTableResults.StackTableResults(
                path_database = self.__path_database, 
                func = self.__to_main,
                data_theme = self.__data_theme["stack_table_result"]
            )

            self.__stacked_widget.addWidget(self.__current_page)
            self.__stacked_widget.setCurrentWidget(self.__current_page)

        else:
            self.__open_dialog_table_results_empty()

    def __start(self, data: PageHome.DataPageHome):
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
        self.__stacked_widget.removeWidget(self.__current_page)

        tree = ET.parse(self.__data_loggin.path_course)
        root = tree.getroot()
        path_lesson = os.path.join(os.path.split(self.__data_loggin.path_course)[0], root.find("lesson").text).replace("\\", "/")

        # создание и упаковка окна урока
        self.__current_page = StackLesson.StackLesson(
            path_lesson = path_lesson, 
            data_theme = self.__data_theme["stack_lesson"], 
            func = self.__start_test
        )

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

        # показать урок
        self.__current_page.load_lesson()
        
    def __to_main(self):
        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна входа
        self.__current_page = PageHome.StackLogin(
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

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

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

    def close_window(self):
        if self.__test_started:
            dialog = Dialogs.Dialog(data_theme = self.__data_theme["dialog"])
            dialog.set_window_title("Покинуть тестирование и закрыть окно")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование и закрыть окно?")
            dialog.set_description("Результаты не сохранятся")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() != Dialogs.ButtonRole.accept:
                self.__toolbar.tool_button_test.set_selected()
                return  
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