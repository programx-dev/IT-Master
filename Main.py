from PyQt6 import QtCore, QtGui, QtWidgets
import PageHome
import PageTesting
import PageResultTesting
import StackTableResults
import Window
import Dialogs
import version
import os
import sys
import json
import enum
import re
import sqlite3  
import datetime    
from glob import glob
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import GlobalSenderEvents

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
    page_home = 0
    page_testing = 1

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
        # self.setProperty("page", PropertyPages.page_home.value)

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
        if self != SwitchableToolButtonToolbar.tool_button_selected and SwitchableToolButtonToolbar.tool_button_selected != None:
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

    def update_style_sheet(self, property: PropertyPages):
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
        #tool_button[page=\"{PropertyPages.page_home.value}\"][selected="true"] {{ 
            background: {self.__data_theme["home_page"]["selected"]["background"]};
            color: {self.__data_theme["home_page"]["selected"]["color"]};
        }} 
         #tool_button[page=\"{PropertyPages.page_home.value}\"][selected="false"] {{ 
            background: {self.__data_theme["home_page"]["not_selected"]["background"]};
            color: {self.__data_theme["home_page"]["not_selected"]["color"]};
        }}

        #tool_button[page=\"{PropertyPages.page_testing.value}\"][selected="true"] {{ 
            background: {self.__data_theme["test_page"]["selected"]["background"]};
            color: {self.__data_theme["test_page"]["selected"]["color"]};
        }}
        #tool_button[page=\"{PropertyPages.page_testing.value}\"][selected="false"] {{ 
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

        # self.setProperty("page", PropertyPages.page_home.value)

        self.setObjectName("tool_button")
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
        self.tool_button_clicked.emit()

    def set_selected(self):
        SwitchableToolButtonToolbar.tool_button_selected.__set_selected(False)
        SwitchableToolButtonToolbar.tool_button_selected = self
        self.__set_selected(True)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_button {{
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
        }}
        #tool_button[page=\"{PropertyPages.page_home.value}\"] {{ 
            background: {self.__data_theme["home_page"]["not_selected"]["background"]};
            color: {self.__data_theme["home_page"]["not_selected"]["color"]};
        }} 
        #tool_button[page=\"{PropertyPages.page_testing.value}\"] {{ 
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
        self.setProperty("page", PropertyPages.page_home.value)

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

        # self.set_style_sheet()

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
            i.style().unpolish(i)
            i.style().polish(i)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_bar[page=\"{PropertyPages.page_home.value}\"] {{
            background: {self.__data_theme["home_page"]["background"]};
        }} 
        #tool_bar[page=\"{PropertyPages.page_testing.value}\"] {{
            background: {self.__data_theme["test_page"]["background"]};
        }} """ )

class Main(Window.Window):
    """Главный класс"""

    def __init__(self):
        super().__init__()
        self.setObjectName("main")
        
        self.__text_info = """\
Предметный тренажер по информатике, позволяющий изучить метериал и закрепить полученные знания, выполнив тест\n
Приложение написано на языке программирование Python, интерфейс на PyQt6"""
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
        self.__path_courses = self.__data["path_courses"]
        self.__path_images = self.__data["path_images"]
        self.__path_database = self.__data["path_database"]
        self.__path_image_logo = os.path.join(self.__path_images, r"logo.png")

        # создание БД если её нет
        # with sqlite3.connect(self.__path_database) as db:
        #     cursor = db.cursor()

        #     cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS users(
        #         date_start VARCHAR,
        #         date_end VARCHAR,
        #         name VARCHAR,
        #         surname VARCHAR,
        #         class_name VARCHAR,
        #         course VARCHAR,
        #         points_max INTEGER,
        #         points_right INTEGER,
        #         points_wrong INTEGER,
        #         points_skip INTEGER,
        #         result INTEGER
        #     ) """)

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
        self.__toolbar.tool_button_settings_cliced.connect(self.__open_dialog_settings)
        self.__toolbar.tool_button_info_cliced.connect(self.__open_dialog_about)

        # выбрать кнопку Домашняя страница
        self.__toolbar.tool_button_home_page.press_tool_button()

        self.set_style_sheet()

    def __open_home_page(self):
        if type(self.__current_page) == PageHome.PageHome:
            return
        
        if self.__test_started:
            dialog = Dialogs.Dialog()
            dialog.set_window_title("Покинуть тестирование")
            dialog.set_window_icon(QtGui.QIcon(self.__path_image_logo))
            dialog.set_icon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
            dialog.set_text("Покинуть тестирование и выйти\nна домашнюю страницу?")
            dialog.set_description("Результаты не сохранятся!")
            dialog.add_push_button("ОК", Dialogs.ButtonRole.accept)
            dialog.add_push_button("Отмена", Dialogs.ButtonRole.reject, True)

            if dialog.run_modal() != Dialogs.ButtonRole.accept:
                self.__toolbar.tool_button_test.set_selected()
                return  

        self.__test_started = False

        self.__toolbar.tool_button_test.hide()
        self.__toolbar.tool_button_results.hide()
        self.__toolbar.update_style_sheet(PropertyPages.page_home)        

        # удаление старого окна
        if self.__current_page!= None:
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
        self.__toolbar.tool_button_results.press_tool_button()
        self.__toolbar.tool_button_test.hide()
        self.__toolbar.tool_button_results.show()
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
        self.__current_page = PageResultTesting.PageResultTesting(
            data_result_testing = data_result_testing, 
            path_images = self.__path_images,
            data_page_viewer_result_testing = self.__get_data_page_viewer_result_testing()
        )

        self.__stacked_widget.addWidget(self.__current_page)
        self.__stacked_widget.setCurrentWidget(self.__current_page)

    def __start_test(self, data_page_test: PageTesting.DataPageTest):
        self.__toolbar.update_style_sheet(PropertyPages.page_testing)
        self.__toolbar.tool_button_test.press_tool_button()
        self.__toolbar.tool_button_test.show()

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

    def __open_dialog_table_results_empty(self):
        dialog = Dialogs.DialogTableResultsEmpty(
            data_theme = self.__data_theme["dialog_table_results_empty"], 
            parent = self
        )

    def __open_dialog_about(self):
        dialog = Dialogs.DialogAbout(QtGui.QPixmap(self.__path_image_logo))
        dialog.setWindowTitle("О программе")
        dialog.setWindowIcon(QtGui.QIcon(os.path.join(self.__path_images, r"info.png")))
        dialog.set_version(f"версия {version.__version__}")
        dialog.set_text_about(self.__text_info)
        dialog.run_modal()

    def __open_dialog_settings(self):
        dialog = Dialogs.DialogSettings(
            dir_theme = self.__dir_theme, 
            path_current_theme = self.__path_theme, 
            path_images = self.__path_images
        )
        dialog.setWindowTitle("Настройки")
        dialog.setWindowIcon(QtGui.QIcon(os.path.join(self.__path_images, r"settings.png")))
        result = dialog.run_modal()

        if result != None and result != self.__path_theme:
            self.__path_theme = result

            self.__data["path_theme"] = self.__path_theme

            with open(self.__path_settings, "w", encoding = "utf-8") as file:
                json.dump(self.__data, file, indent = 4)

            with open(result, "r", encoding = "utf-8") as file:
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

            if dialog.run_modal() != Dialogs.ButtonRole.accept:
                self.__toolbar.tool_button_test.set_selected()
                return  
        super().close_window()

    def __get_data_page_viewer_result_testing(self) -> PageResultTesting.DataPageViewerResultTesting:
        __parser_rgb = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_right"]["color"])
        if parsing_result != None:
            color_right = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_right = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_right"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_wrong"]["color"])
        if parsing_result != None:
            color_wrong = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_wrong = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_wrong"]["color"])

        parsing_result = __parser_rgb.search(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_skip"]["color"])
        if parsing_result != None:
            color_skip = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        else:
            color_skip = QtGui.QColor(self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["chart"]["pie_slice_skip"]["color"])
        
        data_page_viewer_result_testing = PageResultTesting.DataPageViewerResultTesting(
            color_right = color_right,
            color_wrong = color_wrong,
            color_skip = color_skip
        )

        return data_page_viewer_result_testing

    def set_style_sheet(self):
        GlobalSenderEvents.GlobalSenderEvents().dispatchEvent("change_data_page_viewer_result_testing", self.__get_data_page_viewer_result_testing())

        QtWidgets.QApplication.instance().setStyleSheet(f"""
        /* PageHome */
            /* главная рамка */
            #page_home #frame_main {{
                background: {self.__data_theme["page_home"]["frame_main"]["background"]};
                border-image: url({os.path.join(os.path.split(self.__path_theme)[0], self.__data_theme["page_home"]["frame_main"]["background_image"]).replace(chr(92), "/")});
                background-repeat: no-repeat; 
                background-position: center;
            }}

            /* внутренняя рамка формы */
            #page_home #frame_internal {{
                border-radius: 14px;
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["background"]};
            }}

            /* метка заголовка */
            #page_home #label_header {{ 
                background: transparent; 
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["label_header"]["color"]}
            }} 

            /* список уроков */
            #page_home #list_view {{
                outline: 0;
                border: 0px;
                background: transparent;
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["color"]};
            }}
            #page_home #list_view::item {{
                margin: 0px 14px 0px 0px;
            }}
            #page_home #list_view::item:selected {{
                border-radius: 6px;
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["selected"]["background"]};
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["selected"]["color"]};;
            }}  
            #page_home #list_view::item:hover:!selected {{
                border-radius: 6px;
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["hover"]["background"]};
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["hover"]["color"]};;
            }}                        
        
            #page_home #list_view QScrollBar:vertical {{              
                border: transparent;
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_home #list_view QScrollBar::handle:vertical {{
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_home #list_view QScrollBar::add-line:vertical, #page_home #list_view QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_home #list_view QScrollBar::add-page:vertical, #page_home #list_view QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_home #list_view QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_home #list_view QScrollBar::handle:horizontal {{
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_home #list_view QScrollBar::add-line:horizontal, #page_home #list_view QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_home #list_view QScrollBar::add-page:horizontal, #page_home #list_view QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* кнопка Выбрать в проводнике */
            #page_home #push_button_select_in_explorer {{
                outline: 0;                                         
                text-align: left;
                border-radius: 7px; 
                background: transparent; 
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_select_in_explorer"]["color"]};
            }} 

            /* кнопка входа */
            #page_home #push_button_start_test {{
            outline: 0;
                border-radius: 7px; 
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["background"]}; 
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["color"]};
            }} 
            #page_home #push_button_start_test::pressed {{
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["pressed"]["background"]}; 
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["pressed"]["color"]};
            }}
            #page_home #push_button_start_test::disabled {{
                background: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["disabled"]["background"]};
                color: {self.__data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["disabled"]["color"]};
            }}

        /* PageTesting */
            /* главная рамка */
            #page_testing #frame_main {{
                background: {self.__data_theme["page_testing"]["frame_main"]["background"]};
            }} 

            /* панель инструментов и навигации */
            #page_testing #frame_tools {{               
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["background"]};
            }} 

            /* прокручиваемая область для станица теста */
            #page_testing #scroll_area_page_test {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["background"]};
                border: none;
            }}
            
            #page_testing #scroll_area_page_test QScrollBar:vertical {{              
                border: transparent;
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::handle:vertical {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_testing #scroll_area_page_test QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::handle:horizontal {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-line:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-page:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }} 

            /* прокручиваемая область для кнопок навигации по вопросам */
            #page_testing #scroll_area_push_button_questions {{
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["background"]};
                border: none;
                margin: 0px, 0px, 0px, 0px;
            }} 

            #page_testing #scroll_area_push_button_questions QScrollBar:vertical {{
                width: 0px;
            }}
            
            #page_testing #scroll_area_push_button_questions QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::handle:horizontal {{
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::add-line:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::add-page:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }} 

            /* рамка кнопок навигации по вопросам */
            #page_testing #frame_push_button_questions {{
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["background"]};
                margin: 0px, 17px, 0px, 0px;
            }}

            /* кнопка завершить тест */
            #page_testing #push_button_finish {{
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 15px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_finish"]["background"]}; 
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_finish"]["color"]};
            }} 

        /* PageTesting PageQuestion */
            /* главная рамка */
            #page_testing #page_question #frame_main {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["background"]};
            }} 

            /* метка номера вопроса */
            #page_testing #page_question #label_numder_question {{
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_numder_question"]["color"]};   
            }} 

            /* метка вопроса */
            #page_testing #page_question #label_question {{
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["color"]};
                background: transparent;
                selection-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["selection_color"]};
                selection-background-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["selection_background_color"]};
            }} 

            /* метка типа задания */
            #page_testing #page_question #label_type_question {{ 
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_type_question"]["color"]};
            }}

        /* PageTesting PageQuestion PushButtonImage */
            /* кнопка с изображением */
            #page_testing #page_question #push_button_image {{ 
                outline: 0;
                border-radius: 14px;
                border-style: solid;
                border-width: 1px;
                border-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["push_button_image"]["border_color"]};
                background: transparent; 
            }} 

            /* кнопка сохранения */
            #page_testing #page_question #push_button_image #push_buttton_save_image {{ 
                outline: 0;
                border-radius: 14px; 
                background: transparent; 
            }} 

        /* PageTesting PageQuestion RadioButtonAnswer */
            /* кнопка с флажком */
            #page_testing #page_question #radio_button_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_testing #page_question #radio_button_answer #push_button_flag[hover="true"] {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_testing #page_question #radio_button_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["normal"]["color"]};
            }}

            #page_testing #page_question #radio_button_answer #label_text[hover="true"] {{
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["color"]};
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

        /* PageTesting PageQuestion CheckboxAnswer */
            /* кнопка с флажком */
            #page_testing #page_question #checkbox_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_testing #page_question #checkbox_answer #push_button_flag[hover="true"] {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_testing #page_question #checkbox_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["normal"]["color"]};
            }}

            #page_testing #page_question #checkbox_answer #label_text[hover="true"] {{
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["color"]};
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

        /* PageTesting PageQuestion LineEditAnswer */
            /* строка ввода ответов */
            #page_testing #page_question #line_edit_answer {{
            border-radius: 7px; 
            border: 2px solid; 
            selection-background-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["selection_background_color"]};
            selection-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["selection_color"]};
            border-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["color_border"]};
            background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["background"]}; 
            color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["color"]};
            }} 
            #page_testing #page_question #line_edit_answer:focus {{
            selection-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["selection_color"]};
                selection-background-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["selection_background_color"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["color_border"]};
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["background"]}; 
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["color"]};
            }}

        /* PageTesting PageQuestion LabelPromt */
            /* главная рамка */
            #page_testing #page_question #label_promt {{
                background: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["background"]};
                border-radius: 3px;
            }} 

            /* цветная полоска */
            #page_testing #page_question #label_line {{
                background:{self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["line"]["background"]};
                border-top-left-radius: 3px;
                border-bottom-left-radius: 3px;
            }} 

            /* метка со значком*/
            #page_testing #page_question #label_icon {{
                background: transparent;
            }} 

            /* метка с информативным текстом */
            #page_testing #page_question #label_text {{
                background: transparent;
                color: {self.__data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["color"]};
            }} 

        /* PageTesting PageQuestion PushButtonLesson */
            /* кнопка для открытия теоретической части */
            #page_testing #push_button_lesson[current="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["color"]};
            }} 
            #page_testing #push_button_lesson[current="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["color"]};
            }} 

        /* PageTesting PageQuestion PushButtonQuestion */
            /* кнопка для навигации по вопросам теста */
            #page_testing #push_button_question[current="true"][answered="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="true"][answered="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="false"][answered="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="false"][answered="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["background"]};
                border-color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["color_border"]};
                color: {self.__data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["color"]};
            }} 

        /* AbstractWindow */
            /* абстрактное виджет-окно */
            #main #frame_widgets {{
                background: {self.__data_theme["window"]["frame_widgets"]["background"]};
            }} 

        /* AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #main #titile_bar_window #frame_header {{
                background: {self.__data_theme["window"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #main #titile_bar_window #label_title {{
                background: transparent;
                color: {self.__data_theme["window"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #main #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_minimize::hover {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_minimize::pressed {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #main #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_maximize::hover {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_maximize::pressed {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #main #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_close::hover {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_close::pressed {{
                background: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {self.__data_theme["window"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* PageResultTesting */
            /* главная рамка */
            #page_result_testing #frame_main {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["background"]};
            }} 

            /* панель инструментов и навигации */
            #page_result_testing #frame_tools {{               
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["background"]};
            }} 

            /* прокручиваемая область для станица теста */
            #page_result_testing #scroll_area_page_result_test {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["background"]};
                border: none;
            }}
            
            #page_result_testing #scroll_area_page_result_test QScrollBar:vertical {{              
                border: transparent;
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::handle:vertical {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-line:vertical, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-page:vertical, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_result_testing #scroll_area_page_result_test QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::handle:horizontal {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-line:horizontal, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-page:horizontal, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* прокручиваемая область для кнопок навигации по вопросам */
            #page_result_testing #scroll_area_push_button_result_questions {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["background"]};
                border: none;
                margin: 0px, 0px, 0px, 0px;
            }} 

            #page_result_testing #scroll_area_push_button_result_questions QScrollBar:vertical {{
                width: 0px;
            }}
            
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::handle:horizontal {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::add-line:horizontal, #page_result_testing #scroll_area_push_button_result_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::add-page:horizontal, #page_result_testing #scroll_area_push_button_result_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* рамка кнопок для навигации по результатам вопросов */
            #page_result_testing #frame_push_button_result_questions {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["background"]};
                margin: 0px, 17px, 0px, 0px;
            }} 

        /* PageResultTesting PageResultQuestion */
            /* главная рамка */
            #page_result_testing #page_result_question #frame_main {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["background"]};
            }} 

            /* метка номера вопроса */
            #page_result_testing #page_result_question #label_numder_question {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_numder_question"]["color"]};   
            }} 

            /* метка статуса выполнения */
            #page_result_testing #page_result_question #label_status {{
                border-radius: 7px;
                padding-left: 7px;
                padding-right: 7px; 
            }}
            #page_result_testing #page_result_question #label_status[status="right"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["right"]["background"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["right"]["color"]};   
            }} 
            #page_result_testing #page_result_question #label_status[status="wrong"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["wrong"]["background"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["wrong"]["color"]};
            }} 
            #page_result_testing #page_result_question #label_status[status="skip"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["skip"]["background"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["skip"]["color"]}; 
            }} 

            /* метка вопроса */
            #page_result_testing #page_result_question #label_question {{
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["color"]};
                background: transparent;
                selection-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["selection_color"]};
                selection-background-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["selection_background_color"]};
            }} 

            /* метка верный ответ */
            #page_result_testing #page_result_question #label_right_answer {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_right_answer"]["color"]};
            }}

            /* метка ваш ответ */
            #page_result_testing #page_result_question #label_user_answer {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_user_answer"]["color"]};
            }}

            /* метка типа задания */
            #page_result_testing #page_result_question #label_type_question {{ 
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_type_question"]["color"]};
            }} 

        /* PageResultTesting PageViewerResultTesting */
            /* главна рамка */
            #page_result_testing #page_viewer_result_testing #frame_main {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["background"]};
            }} 

            /* метка названия теста */
            #page_result_testing #page_viewer_result_testing #label_name_test {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_name_test"]["color"]};
            }} 

            /* метка даты проходжения */
            #page_result_testing #page_viewer_result_testing #label_date_passing {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_date_passing"]["color"]};
            }} 

            /* метка времени прохождения */
            #page_result_testing #page_viewer_result_testing #label_time_passing {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_time_passing"]["color"]};
            }} 

            /* диаграмма */
            #chart_view {{
                background: transparent;
            }}

            /* рамка легенды */
            #page_result_testing #page_viewer_result_testing #frame_legend {{
                border-style: solid;
                border-width: 1px;
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["border_color"]};
                border-radius: 14px;
            }} 

            /* метка результата */
            #page_result_testing #page_viewer_result_testing #label_result {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_result"]["color"]};
            }} 

            /* метка заголовка */
            #page_result_testing #page_viewer_result_testing #label_header {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_header"]["color"]};
            }} 

        /* PageResultTesting PageViewerResultTesting LabelLegend */
            /* метка с кружком */
            #page_result_testing #page_viewer_result_testing #label_legend #label_pixmap {{
                background: transparent;
            }}

            /* метка с текстом легенды правильно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.right.value}\"] #label_text {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_right"]["color"]};
            }} 

            /* метка с текстом легенды неправильно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.wrong.value}\"] #label_text {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_wrong"]["color"]};
            }} 

            /* метка с текстом легенды пропущенно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.skip.value}\"] #label_text {{
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_skip"]["color"]};
            }} 

        /* PageResultTesting PushButtonResultTesting */
            /* кнопка открытия резутатов тестирования */
            #page_result_testing #push_button_result_testing {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
            }}
            #page_result_testing #push_button_result_testing[current="true"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["color"]};
            }} 
            #page_result_testing #push_button_result_testing[current="false"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["color"]};
            }} 

        /* PageResultTesting PushButtonResultQuestion */
            #page_result_testing #push_button_result_question {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
            }}
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.right.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.wrong.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.skip.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.right.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.wrong.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.skip.value}\"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["background"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["color_border"]};
                color: {self.__data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["color"]};
            }} 

        /* PageResultTesting PageQuestion PushButtonImage */
            /* кнопка с изображением */
            #page_result_testing #page_result_question #push_button_image {{ 
                outline: 0;
                border-radius: 14px;
                border-style: solid;
                border-width: 1px;
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["push_button_image"]["border_color"]};
                background: transparent; 
            }} 

            /* кнопка сохранения */
            #page_result_testing #page_result_question #push_button_image #push_buttton_save_image {{ 
                outline: 0;
                border-radius: 14px; 
                background: transparent; 
            }} 

        /* PageResultTesting PageQuestion RadioButtonAnswer */
            /* кнопка с флажком */
            #page_result_testing #page_result_question #radio_button_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_result_testing #page_result_question #radio_button_answer #push_button_flag[hover="true"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_result_testing #page_result_question #radio_button_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["normal"]["color"]};
            }}

            #page_result_testing #page_result_question #radio_button_answer #label_text[hover="true"] {{
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["color"]};
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

        /* PageResultTesting PageQuestion CheckboxAnswer */
            /* кнопка с флажком */
            #page_result_testing #page_result_question #checkbox_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_result_testing #page_result_question #checkbox_answer #push_button_flag[hover="true"] {{
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_result_testing #page_result_question #checkbox_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["normal"]["color"]};
            }}

            #page_result_testing #page_result_question #checkbox_answer #label_text[hover="true"] {{
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["color"]};
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

        /* PageTesting PageQuestion LineEditAnswer */
            /* строка ввода ответов */
            #page_result_testing #page_result_question #line_edit_answer {{
            border-radius: 7px; 
            border: 2px solid; 
            selection-background-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["selection_background_color"]};
            selection-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["selection_color"]};
            border-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["color_border"]};
            background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["background"]}; 
            color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["color"]};
            }} 
            #page_result_testing #page_result_question #line_edit_answer:focus {{
            selection-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["selection_color"]};
                selection-background-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["selection_background_color"]};
                border-color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["color_border"]};
                background: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["background"]}; 
                color: {self.__data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["color"]};
            }}  

        /* Dialog */  
            /* рамка виджетов */
            #dialog #frame_widgets {{
                background: {self.__data_theme["dialog"]["frame_widgets"]["background"]};
            }} 
        
            /* главная рамка */
            #dialog #frame_main {{
                background: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["background"]};
            }} 

            /* метка с текстом */
            #dialog #label_text {{
                background: transparent;
                color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["label_text"]["color"]};
            }} 

            /* метка с описанием */
            #dialog #label_description {{
                background: transparent;
                color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["label_description"]["color"]};
            }} 

            /* кнопки диалога*/
            #dialog #push_button_dialog {{
                border-width: 1px;
                border-style: solid;
                border-color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog #push_button_dialog:default {{
                border-width: 2px;
                border-color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* Dialog AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog #titile_bar_window #frame_header {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog #titile_bar_window #label_title {{
                background: transparent;
                color: {self.__data_theme["dialog"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_minimize::hover {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_minimize::pressed {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_maximize::hover {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_maximize::pressed {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_close::hover {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_close::pressed {{
                background: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 
        
        /* ToolBar */
            /* рамка-панель инструментов */
            #tool_bar[page=\"{PropertyPages.page_home.value}\"] {{
                background: {self.__data_theme["tool_bar"]["page_home"]["background"]};
            }} 
            #tool_bar[page=\"{PropertyPages.page_testing.value}\"] {{
                background: {self.__data_theme["tool_bar"]["page_testing"]["background"]};
            }} 

        /* ToolBar SwitchableToolButtonToolbar */
            #tool_bar #switchable_tool_button {{
                padding: 0px;
                outline: 0;
                border-radius: 10px; 
            }}
            #tool_bar[page=\"{PropertyPages.page_home.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["selected"]["color"]};
            }} 
            #tool_bar[page=\"{PropertyPages.page_home.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["color"]};
            }}

            #tool_bar[page=\"{PropertyPages.page_testing.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["selected"]["color"]};
            }}
            #tool_bar[page=\"{PropertyPages.page_testing.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["color"]};
            }} 

        /* ToolBar ToolButtonToolbar */
            #tool_bar #tool_button {{
                padding: 0px;
                outline: 0;
                border-radius: 10px; 
            }}
            #tool_bar[page=\"{PropertyPages.page_home.value}\"] #tool_button {{ 
                background: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["color"]};
            }} 
            #tool_bar[page=\"{PropertyPages.page_testing.value}\"] #tool_button {{ 
                background: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["background"]};
                color: {self.__data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["color"]};
            }} 

        /* DialogAbout */ 
            /* рамка виджетов */
            #dialog_about #frame_widgets {{
                background: {self.__data_theme["dialog_about"]["frame_widgets"]["background"]};
            }} 

            /* главная рамка */
            #dialog_about #frame_main {{
                background: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["background"]};
            }}

            /* метка с иконкой */
            #dialog_about #frame_main > #label_icon {{
                background: transparent;
            }}

            /* метка с названием программы */
            #dialog_about #label_name {{
                background: transparent;
                color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_name"]["color"]};
            }}

            /* метка с версией программы */
            #dialog_about #label_version {{
                background: transparent;
                color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_version"]["color"]};
            }}

            /* метка с описанием */
            #dialog_about #label_about {{
                background: transparent;
                color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["color"]};
                selection-color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["selection_color"]};
                selection-background-color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["selection_background_color"]};
            }}

            #dialog_about #push_button_accept {{
                border-width: 1px;
                border-style: solid;
                border-color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog_about #push_button_accept:default {{
                border-width: 2px;
                border-color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* DialogAbout AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog_about #titile_bar_window #frame_header {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog_about #titile_bar_window #label_title {{
                background: transparent;
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog_about #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_minimize::hover {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_minimize::pressed {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog_about #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_maximize::hover {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_maximize::pressed {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog_about #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_close::hover {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_close::pressed {{
                background: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* DialogSettings */ 
            /* рамка виджетов */
            #dialog_settings #frame_widgets {{
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["background"]};
            }} 

            /* главная рамка */
            #dialog_settings #frame_main {{
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["background"]};
            }}

            /* метка заголовка */
            #dialog_settings #label_header {{
                background: transparent; 
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["label_header"]["color"]}
            }}

            /* список цветовых тем */
            #dialog_settings #list_view {{
                outline: 0;
                border: 0px;
                background: transparent;
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["color"]};
            }}
            #dialog_settings #list_view::item {{
                margin: 0px 14px 0px 0px;
            }}
            #dialog_settings #list_view::item:selected {{
                border-radius: 6px;
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["item"]["selected"]["background"]};
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["item"]["selected"]["color"]};;
            }}  
            #dialog_settings #list_view::item:hover:!selected {{
                border-radius: 6px;
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["item"]["hover"]["background"]};
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["item"]["hover"]["color"]};;
            }}                        
        
            #dialog_settings #list_view QScrollBar:vertical {{              
                border: transparent;
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #dialog_settings #list_view QScrollBar::handle:vertical {{
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #dialog_settings #list_view QScrollBar::add-line:vertical, #dialog_settings #list_view QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #dialog_settings #list_view QScrollBar::add-page:vertical, #dialog_settings #list_view QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #dialog_settings #list_view QScrollBar:horizontal {{              
                border: transparent;
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #dialog_settings #list_view QScrollBar::handle:horizontal {{
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #dialog_settings #list_view QScrollBar::add-line:horizontal, #dialog_settings #list_view QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #dialog_settings #list_view QScrollBar::add-page:horizontal, #dialog_settings #list_view QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            #dialog_settings #push_button_accept, #dialog_settings #push_button_reject {{
                border-width: 1px;
                border-style: solid;
                border-color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog_settings #push_button_accept:default, #dialog_settings #push_button_reject:default {{
                border-width: 2px;
                border-color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* DialogSettings AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog_settings #titile_bar_window #frame_header {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog_settings #titile_bar_window #label_title {{
                background: transparent;
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog_settings #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_minimize::hover {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_minimize::pressed {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog_settings #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_maximize::hover {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_maximize::pressed {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog_settings #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_close::hover {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_close::pressed {{
                background: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {self.__data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 
        """)

# ["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"] {self.__data_theme["color"]}
if __name__ == "__main__": 
    # https://doc.qt.io/qt-5/highdpi.html
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
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
