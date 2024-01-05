from PyQt6 import QtCore, QtGui, QtWidgets
import PageHome
import PageTesting
import PageResultTesting
import PageHistory
import Window
import Dialogs
import StyleSheet
from utils import ImageViewer
import os
import sys
import json
import PropertyPages
import re
import sqlite3  
import datetime    
from dataclasses import dataclass
import pickle
from utils import Logging
import logging

__version__ = "3.6.3"

__text_about__ = """Предметный тренажер по информатике, позволяющий изучить теорию и закрепить полученные знания, выполнив тест.<br/><br/>Эта программа лицензирована под General Public License v3.0."""

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

class SwitchableToolButtonToolbar(QtWidgets.QToolButton):
    """Переключаемая кнопка панели инструментов"""
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
        # self.setProperty("page", PropertyPages.PropertyPages.page_home.value)

        self.setObjectName("switchable_tool_button")
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.clicked.connect(self.press_tool_button)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.setIcon(self.__image)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setText(self.__text)
        self.setFont(QtGui.QFont("Segoe UI", 10))

        # self.set_style_sheet()

    def press_tool_button(self):
        if self != SwitchableToolButtonToolbar.tool_button_selected and SwitchableToolButtonToolbar.tool_button_selected is not None:
            SwitchableToolButtonToolbar.tool_button_selected.__set_selected(False)

        if self != SwitchableToolButtonToolbar.tool_button_selected:
            SwitchableToolButtonToolbar.tool_button_selected = self
            self.__set_selected(True)

            self.tool_button_clicked.emit()

    def __set_selected(self, selected: bool):
        self.__selected = selected

        self.setProperty("selected", self.__selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_selected(self):
        SwitchableToolButtonToolbar.tool_button_selected.__set_selected(False)
        SwitchableToolButtonToolbar.tool_button_selected = self
        self.__set_selected(True)

    def update_style_sheet(self, property: PropertyPages.PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_button {{
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
        }}
        #tool_button[page=\"{PropertyPages.PropertyPages.page_home.value}\"][selected="true"] {{ 
            background: {self.__data_theme["home_page"]["selected"]["background"]};
            color: {self.__data_theme["home_page"]["selected"]["color"]};
        }} 
         #tool_button[page=\"{PropertyPages.PropertyPages.page_home.value}\"][selected="false"] {{ 
            background: {self.__data_theme["home_page"]["not_selected"]["background"]};
            color: {self.__data_theme["home_page"]["not_selected"]["color"]};
        }}

        #tool_button[page=\"{PropertyPages.PropertyPages.page_testing.value}\"][selected="true"] {{ 
            background: {self.__data_theme["test_page"]["selected"]["background"]};
            color: {self.__data_theme["test_page"]["selected"]["color"]};
        }}
        #tool_button[page=\"{PropertyPages.PropertyPages.page_testing.value}\"][selected="false"] {{ 
            background: {self.__data_theme["test_page"]["not_selected"]["background"]};
            color: {self.__data_theme["test_page"]["not_selected"]["color"]};
        }} """)

class ToolButtonToolbar(QtWidgets.QToolButton):
    """Кнопка панели инструментов"""
    tool_button_clicked = QtCore.pyqtSignal()

    def __init__(self, path_image: str, text: str, data_theme: dict):
        super().__init__()

        self.__path_image = path_image
        self.__image = QtGui.QIcon(self.__path_image)
        self.__text = text
        self.__data_theme = data_theme
        self.__selected = False

        # self.setProperty("page", PropertyPages.PropertyPages.page_home.value)

        self.setObjectName("tool_button")
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.clicked.connect(self.press_tool_button)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.setIcon(self.__image)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setText(self.__text)
        self.setFont(QtGui.QFont("Segoe UI", 10))

    def press_tool_button(self):
        self.tool_button_clicked.emit()

    def set_selected(self):
        SwitchableToolButtonToolbar.tool_button_selected.__set_selected(False)
        SwitchableToolButtonToolbar.tool_button_selected = self
        self.__set_selected(True)

class ToolBar(QtWidgets.QFrame):
    """Панель инструментов"""
    tool_button_home_page_cliced = QtCore.pyqtSignal()
    tool_button_results_cliced = QtCore.pyqtSignal()
    tool_button_test_cliced = QtCore.pyqtSignal()
    tool_button_history_cliced = QtCore.pyqtSignal()
    tool_button_settings_cliced = QtCore.pyqtSignal()
    tool_button_info_cliced = QtCore.pyqtSignal()

    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme
        self.__list_tool_buttons = list()

        self.setObjectName("tool_bar")
        self.setProperty("page", PropertyPages.PropertyPages.page_home.value)

        # макет панели инструментов
        self.__vbox_layout_toolbar = QtWidgets.QVBoxLayout()
        self.__vbox_layout_toolbar.setContentsMargins(5, 5, 5, 5)
        self.__vbox_layout_toolbar.setSpacing(0)

        self.setLayout(self.__vbox_layout_toolbar)

        data_theme_tool_buttons = {
            "home_page": self.__data_theme["page_home"]["tool_button"],
            "test_page": self.__data_theme["page_testing"]["tool_button"]
        }

        # кнопка Домашняя страница
        self.tool_button_home_page = SwitchableToolButtonToolbar(
            os.path.join(self.__path_images, r"home_page.png"), 
            "Домашняя\nстраница", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_home_page)
        self.tool_button_home_page.tool_button_clicked.connect(self.__press_tool_button_home_page)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_home_page)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Результаты
        self.tool_button_results = SwitchableToolButtonToolbar(
            os.path.join(self.__path_images, r"results.png"), 
            "Результаты", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_results)
        self.tool_button_results.tool_button_clicked.connect(self.__press_tool_button_results)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_results)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Тест
        self.tool_button_test = SwitchableToolButtonToolbar(
            os.path.join(self.__path_images, r"test.png"), 
            "Тест", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_test)
        self.tool_button_test.tool_button_clicked.connect(self.__press_tool_button_test)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_test)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка История
        self.tool_button_history = SwitchableToolButtonToolbar(
            os.path.join(self.__path_images, r"history.png"), 
            "История", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_history)
        self.tool_button_history.tool_button_clicked.connect(self.__press_tool_button_history)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_history)
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

    def __press_tool_button_home_page(self):
        self.tool_button_home_page_cliced.emit()

    def __press_tool_button_results(self):
        self.tool_button_results_cliced.emit()

    def __press_tool_button_test(self):
        self.tool_button_test_cliced.emit()

    def __press_tool_button_history(self):
        self.tool_button_history_cliced.emit()

    def __press_tool_button_settings(self):
        self.tool_button_settings_cliced.emit()

    def __press_tool_button_info(self):
        self.tool_button_info_cliced.emit()

    def update_style_sheet(self, property: PropertyPages.PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

        for i in self.__list_tool_buttons:
            i.style().unpolish(i)
            i.style().polish(i)

class Main(Window.Window):
    """Главный класс"""

    def __init__(self):
        super().__init__()
        self.setObjectName("main")
        
        self.__text_info = """Предметный тренажер по информатике, позволяющий изучить теорию и закрепить полученные знания, выполнив тест\nПриложение написано на языке программирование Python, интерфейс на PyQt6"""
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

        self.__dir_theme = self.__data["dir_theme"]
        self.__amount_records = self.__data["amount_records"]
        self.__path_courses = self.__data["path_courses"]
        self.__path_images = self.__data["path_images"]
        self.__path_database = self.__data["path_database"]
        self.__path_image_logo = os.path.join(self.__path_images, r"logo.png")

        ImageViewer.data_image_viewer = self.__get_data_image_viewer()

        # SQLite - это библиотека на основе языка C, предоставляющая переносимый и бессерверный движок базы данных SQL. Он имеет файловую архитектуру; следовательно, он выполняет чтение и запись на диск. Поскольку SQLite является базой данных с нулевой конфигурацией, перед ее использованием не требуется установка или конфигурирование. Начиная с Python 2.5.x, SQLite3 по умолчанию поставляется с python.

        # создание БД если её нет
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history(
                date_start TEXT,
                date_end TEXT,
                path_course TEXT,
                list_data_result  BLOB
            ) """)

        # панель инструментов
        self.__toolbar = ToolBar(self.__path_images, self.__data_theme["tool_bar"])
        self.add_widget(self.__toolbar)

        self.setWindowTitle("IT-Master")
        self.setWindowIcon(QtGui.QIcon(self.__path_image_logo))

        # виджет стеков для страниц
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.add_widget(self.__stacked_widget)

        # присоединение слотов к сигналам
        self.__toolbar.tool_button_home_page_cliced.connect(self.__open_home_page)
        self.__toolbar.tool_button_settings_cliced.connect(self.__open_dialog_settings)
        self.__toolbar.tool_button_info_cliced.connect(self.__open_dialog_about)
        self.__toolbar.tool_button_history_cliced.connect(self.__open_page_history)

        # выбрать кнопку Домашняя страница
        self.__toolbar.tool_button_home_page.press_tool_button()

        self.set_style_sheet()

    def __open_home_page(self):
        if type(self.__current_page) == PageHome.PageHome:
            return
        
        if self.__test_started:
            dialog = Dialogs.Dialog(self)
            dialog.set_window_title("Покинуть тестирование")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование и выйти\nна домашнюю страницу?")
            dialog.set_description("Результаты не сохранятся!")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() == Dialogs.ButtonRole.reject:
                self.__toolbar.tool_button_test.set_selected()
                return  
            else:
                self.__current_page.close_dialog_image_viewer()

        self.__test_started = False

        self.__toolbar.tool_button_test.hide()
        self.__toolbar.tool_button_results.hide()
        self.__toolbar.tool_button_history.show()
        self.__toolbar.update_style_sheet(PropertyPages.PropertyPages.page_home)        

        # удаление старого окна
        if self.__current_page is not None:
            if isinstance(self.__current_page, PageTesting.PageTesting):
                self.__current_page.close_dialog_image_viewer()
            self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна входа
        self.__current_page = PageHome.PageHome(
            path_courses = self.__path_courses, 
            path_images = self.__path_images, 
            path_theme = self.__path_theme, 
        )
        self.__current_page.push_button_clicked_start_test.connect(self.__start_test)

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __save_result(self, data_result_testing: PageTesting.DataResultTesting):
        # запись данных о прохождении в БД
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            values = (
                data_result_testing.date_start.strftime(r'%d.%m.%Y %H:%M'),
                data_result_testing.date_end.strftime(r'%d.%m.%Y %H:%M'),
                data_result_testing.path_course,
                pickle.dumps(data_result_testing.list_data_result)
            )

            cursor.execute("""INSERT INTO history(date_start, date_end, path_course, list_data_result) VALUES(?, ?, ?, ?)""", values)

        self.__delete_old_records()

    def __delete_old_records(self):
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT COUNT (*) FROM history""")
            result = cursor.fetchone()[0]
            amount_rows = i if (i := result - self.__amount_records) > 0 else 0

            cursor.execute("""DELETE FROM history WHERE rowid IN (SELECT rowid FROM history ORDER BY rowid ASC LIMIT ?)""", (amount_rows, ))

        if isinstance(self.__current_page, PageHistory.PageHistory):
            with sqlite3.connect(self.__path_database) as db:
                cursor = db.cursor()

                cursor.execute("""SELECT * FROM history""")

                list_data_result_testing = list(map(list, cursor.fetchall()))
                for i in range(len(list_data_result_testing)):
                    list_data_result_testing[i][3] = pickle.loads(list_data_result_testing[i][3])
                    list_data_result_testing[i] = PageTesting.DataResultTesting(
                        date_start = datetime.datetime.strptime(list_data_result_testing[i][0], r'%d.%m.%Y %H:%M'),
                        date_end = datetime.datetime.strptime(list_data_result_testing[i][1], r'%d.%m.%Y %H:%M'),
                        path_course = list_data_result_testing[i][2],
                        list_data_result = list_data_result_testing[i][3]
                    )
                self.__current_page.update_list_data_result_testing(list_data_result_testing)

    def __clear_database(self):
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT COUNT (*) FROM history""")
            amount_rows = cursor.fetchone()[0]

            cursor.execute("""DELETE FROM history WHERE rowid IN (SELECT rowid FROM history ORDER BY rowid ASC LIMIT ?)""", (amount_rows, ))

        if isinstance(self.__current_page, PageHistory.PageHistory):
            self.__current_page.update_list_data_result_testing(list())

    def __finish_test(self, data_result_testing: PageTesting.DataResultTesting):
        self.__toolbar.tool_button_test.hide()
        self.__toolbar.tool_button_history.show()
        self.__test_started = False
        
        self.__save_result(data_result_testing)

        self.__open_result_testing(data_result_testing)

    def __start_test(self, data_page_test: PageTesting.DataPageTest):
        self.__toolbar.update_style_sheet(PropertyPages.PropertyPages.page_testing)
        self.__toolbar.tool_button_test.press_tool_button()
        self.__toolbar.tool_button_test.show()
        self.__toolbar.tool_button_history.hide()

        self.__test_started = True

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна с тестом
        self.__current_page = PageTesting.PageTesting(
            path_course = data_page_test.path_course,
            path_images = self.__path_images
        )
        self.__current_page.push_button_finish_cliced.connect(self.__finish_test)

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __open_result_testing(self, data_result_testing: PageTesting.DataResultTesting):
        if not os.path.isfile(data_result_testing.path_course):
            dialog = Dialogs.Dialog()
            dialog.set_window_title("Ошибка")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning)
            dialog.set_text("Не удается найти тест!")
            dialog.set_description("Тест удален или перемещен")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)

            dialog.run_modal()

            return

        self.__toolbar.update_style_sheet(PropertyPages.PropertyPages.page_result_testing)  
        self.__toolbar.tool_button_results.press_tool_button()
        self.__toolbar.tool_button_results.show()

        # удаление старого окна
        self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна результата выполнения
        self.__current_page = PageResultTesting.PageResultTesting(
            data_result_testing = data_result_testing, 
            path_images = self.__path_images,
            data_page_viewer_result_testing = self.__get_data_page_viewer_result_testing()
        )

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __open_page_history(self):
        with sqlite3.connect(self.__path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT * FROM history""")

            list_data_result_testing = list(map(list, cursor.fetchall()))
            for i in range(len(list_data_result_testing)):
                list_data_result_testing[i][3] = pickle.loads(list_data_result_testing[i][3])
                list_data_result_testing[i] = PageTesting.DataResultTesting(
                    date_start = datetime.datetime.strptime(list_data_result_testing[i][0], r'%d.%m.%Y %H:%M'),
                    date_end = datetime.datetime.strptime(list_data_result_testing[i][1], r'%d.%m.%Y %H:%M'),
                    path_course = list_data_result_testing[i][2],
                    list_data_result = list_data_result_testing[i][3]
                )
        
        self.__toolbar.update_style_sheet(PropertyPages.PropertyPages.page_history)      
        self.__toolbar.tool_button_results.hide()

        # удаление старого окна
        if self.__current_page is not None:
            self.__stacked_widget.removeWidget(self.__current_page)

        # создание и упаковка окна входа
        self.__current_page = PageHistory.PageHistory(
            list_data_result_testing = list_data_result_testing, 
            path_images = self.__path_images, 
            data_push_button_result_testing = self.__get_data_push_button_result_testing(), 
        )
        self.__current_page.push_button_result_testing_clicked.connect(self.__open_result_testing)

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)    

    def __open_dialog_about(self):
        dialog = Dialogs.DialogAbout(self, QtGui.QPixmap(self.__path_image_logo))
        dialog.setWindowTitle("О программе")
        dialog.setWindowIcon(QtGui.QIcon(os.path.join(self.__path_images, r"info.png")))
        dialog.set_version(f"версия {__version__}")
        dialog.set_text_about(__text_about__.format(color = self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["color_hyperlink"]))
        dialog.run_modal()

    def __open_dialog_clear_database(self):
        dialog = Dialogs.Dialog()
        dialog.set_window_title("Очистить историю")
        dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
        dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
        dialog.set_text("Очистить историю?")
        dialog.set_description("Все записи удалятся безвозвратно!")
        dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
        dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

        if dialog.run_modal() == Dialogs.ButtonRole.accept:
            self.__clear_database()

    def __open_dialog_settings(self):
        dialog = Dialogs.DialogSettings(
            self,
            dir_theme = self.__dir_theme, 
            data_settings = Dialogs.DataSettings(self.__path_theme, self.__amount_records), 
            path_images = self.__path_images
        )
        dialog.setWindowTitle("Настройки")
        dialog.setWindowIcon(QtGui.QIcon(os.path.join(self.__path_images, r"settings.png")))
        dialog.push_button_clear_clicked.connect(self.__open_dialog_clear_database)
        result = dialog.run_modal()

        if result.amount_records is not None and result.amount_records != self.__amount_records:
            self.__amount_records = result.amount_records

            self.__data["amount_records"] = self.__amount_records

            with open(self.__path_settings, "w", encoding = "utf-8") as file:
                json.dump(self.__data, file, indent = 4)

            self.__delete_old_records()

        if result.path_theme is not None and result.path_theme != self.__path_theme:
            self.__path_theme = result.path_theme

            self.__data["path_theme"] = self.__path_theme

            with open(self.__path_settings, "w", encoding = "utf-8") as file:
                json.dump(self.__data, file, indent = 4)

            with open(self.__path_theme, "r", encoding = "utf-8") as file:
                self.__data_theme = json.load(file)            

            self.set_style_sheet()

    def close_window(self):
        if self.__test_started:
            dialog = Dialogs.Dialog()
            dialog.set_window_title("Выход")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование и закрыть окно?")
            dialog.set_description("Результаты не сохранятся!")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() == Dialogs.ButtonRole.reject:
                self.__toolbar.tool_button_test.set_selected()
                return  
        super().close_window()

    def __get_data_page_viewer_result_testing(self) -> PageResultTesting.DataPageViewerResultTesting:
        __parser_rgb = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_right"]["color"])
        if parsing_result is not None:
            color_right = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_right = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_right"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_wrong"]["color"])
        if parsing_result is not None:
            color_wrong = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_wrong = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_wrong"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_skip"]["color"])
        if parsing_result is not None:
            color_skip = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_skip = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_skip"]["color"])
        
        data_page_viewer_result_testing = PageResultTesting.DataPageViewerResultTesting(
            color_right = color_right,
            color_wrong = color_wrong,
            color_skip = color_skip
        )

        return data_page_viewer_result_testing

    def __get_data_push_button_result_testing(self) -> PageHistory.DataPushButtonResultTesting:
        __parser_rgb = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

        parsing_result = __parser_rgb.search(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_right"]["color"])
        if parsing_result is not None:
            color_right = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_right = QtGui.QColor(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_right"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_wrong"]["color"])
        if parsing_result is not None:
            color_wrong = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_wrong = QtGui.QColor(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_wrong"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_skip"]["color"])
        if parsing_result is not None:
            color_skip = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_skip = QtGui.QColor(self.__data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["chart"]["pie_slice_skip"]["color"])
        
        data_push_button_result_testing = PageHistory.DataPushButtonResultTesting(
            color_right = color_right,
            color_wrong = color_wrong,
            color_skip = color_skip
        )

        return data_push_button_result_testing

    def __get_data_image_viewer(self) -> ImageViewer.DataImageViewer:
        __parser_rgb = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

        parsing_result = __parser_rgb.search(self.__data_theme["dialog_image_viewer"]["frame_widgets"]["frame_main"]["image_viewer"]["background"])
        if parsing_result is not None:
            color_background = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_background = QtGui.QColor(self.__data_theme["dialog_image_viewer"]["frame_widgets"]["frame_main"]["image_viewer"]["background"])
           
        data_image_viewer = ImageViewer.DataImageViewer(color_background = color_background)

        return data_image_viewer

    def set_style_sheet(self):
        if isinstance(self.__current_page, PageResultTesting.PageResultTesting):
            self.__current_page.change_data_page_viewer_result_testing(self.__get_data_page_viewer_result_testing())
        elif isinstance(self.__current_page, PageHistory.PageHistory):
            self.__current_page.change_data_push_button_result_testing(self.__get_data_push_button_result_testing())
        
        ImageViewer.data_image_viewer = self.__get_data_image_viewer()

        QtWidgets.QApplication.instance().setStyleSheet(StyleSheet.get_style_sheet(self.__data_theme, self.__path_theme, self.__path_images))

def excepthook(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    
    Logging.logger.error("Неперехваченное исключение", exc_info = (exc_type, exc_value, exc_tb))
    
    # print("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

    dlg = QtWidgets.QMessageBox()
    dlg.setWindowIcon(QtGui.QIcon("icon.ico"))
    dlg.setWindowTitle("Ошибка!")
    dlg.setText("Произошла непредвиденная ошибка")
    dlg.setInformativeText(f"Лог ошибки записан в файл {os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), r'logs/log.log'))}")
    dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    dlg.exec()
 
if __name__ == "__main__": 
    Logging.logger.setLevel(logging.DEBUG)
    Logging.c_handler.setLevel(logging.DEBUG)

    sys.excepthook = excepthook

    # https://doc.qt.io/qt-5/highdpi.html
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_QUICK_BACKEND"] = "software"

    # QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # os.environ["QT_SCALE_FACTOR"]             = "1"

    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show_maximized()

    sys.exit(app.exec())
