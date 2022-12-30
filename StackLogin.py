from PyQt5 import QtCore, QtGui, QtWidgets
import os
from dataclasses import dataclass

@dataclass
class DataPassage:
    name: str
    surname: str
    class_name: str
    path_course: str

class PushButtonCourse(QtWidgets.QWidget):
    def __init__(self, path_imgs: str, data_theme: dict, func: callable):
        super().__init__()

        self.path_imgs = path_imgs
        self.data_theme = data_theme
        self.func = func

        self.init_variables()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout(self)
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # кнопка с название курса
        self.push_button_title = QtWidgets.QPushButton()
        self.push_button_title.setObjectName("push_button_title")
        self.push_button_title.clicked.connect(self.press_push_button)
        self.push_button_title.setText("Выбрать курс")
        self.push_button_title.setFont(self.font_widgets)
        self.push_button_title.setMinimumHeight(self.height_push_button)
        self.push_button_title.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_main.addWidget(self.push_button_title)

        # кнопка выбора курса
        self.push_button_download = QtWidgets.QPushButton()
        self.push_button_download.setObjectName("push_button_download")
        self.push_button_download.clicked.connect(self.press_push_button)
        self.push_button_download.setFont(self.font_widgets)
        self.push_button_download.setFixedSize(self.height_push_button, self.height_push_button)

        self.hbox_layout_main.addWidget(self.push_button_download)

        self.set_style_sheet()

    def change_text(self, text: str):
        self.push_button_title.setText(text)

    def press_push_button(self):
        self.func()

    def init_variables(self):
        self.height_push_button = 42
        self.font_widgets = QtGui.QFont("Segoe UI", 12)

        self.img_download = QtGui.QIcon(os.path.join(self.path_imgs, "download.png"))

    def set_style_sheet(self):
        # кнопка с название курса
        self.data_theme["padding"] = self.height_push_button

        self.push_button_title.setStyleSheet("""
        #push_button_title{ 
            outline: 0;
            border-top-left-radius: 7px; 
            border-bottom-left-radius: 7px; 
            padding-left :%(padding)s; 
            background-color: %(background)s;
            color: %(color)s;}""" 
        % self.data_theme)

        # кнопка выбора курса
        temp_data_theme = self.data_theme["push_button_download"]
        self.push_button_download.setStyleSheet("""
        #push_button_download{
            outline: 0;
            border-top-right-radius: 7px; 
            border-bottom-right-radius: 7px; 
            background-color: %(background)s; 
            color: %(color)s;}"""
        % self.data_theme)
        
        self.push_button_download.setIcon(self.img_download)
        self.push_button_download.setIconSize(QtCore.QSize(self.height_push_button - 14, self.height_push_button - 14))

class StackLogin(QtWidgets.QWidget):
    def __init__(self, path_cources: str, path_imgs: str, data_theme: dict, func_start: callable, func_table_results: callable, name: str = None, surname: str = None, class_name: str = None):
        super().__init__()

        self.path_cources = path_cources
        self.path_imgs = path_imgs
        self.data_theme = data_theme
        self.func_start = func_start
        self.func_table_results = func_table_results

        self.name = name
        self.surname = surname
        self.class_name = class_name

        self.init_variables()

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(2, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренняя сетка
        self.grid_layout_data = QtWidgets.QGridLayout()
        self.grid_layout_data.setSpacing(0)
        self.grid_layout_data.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_data.setColumnStretch(0, 1)
        self.grid_layout_data.setColumnStretch(2, 1)
        self.grid_layout_data.setRowStretch(0, 1)
        self.grid_layout_data.setRowStretch(2, 1)

        self.frame_main.setLayout(self.grid_layout_data)

        # внутренняя рамка формы
        self.frame_data = QtWidgets.QFrame()
        self.frame_data.setObjectName("frame_data")
        self.frame_data.setMinimumWidth(360)

        self.grid_layout_data.addWidget(self.frame_data, 1, 1)

         # главный макет
        self.vbox_layout_main = QtWidgets.QVBoxLayout()
        self.vbox_layout_main.setSpacing(0)
        self.vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.frame_data.setLayout(self.vbox_layout_main)

        # макет для полей и кнопок
        self.vbox_layout_data = QtWidgets.QVBoxLayout()
        self.vbox_layout_data.setSpacing(0)
        self.vbox_layout_data.setContentsMargins(20, 20, 20, 0)

        self.vbox_layout_main.addLayout(self.vbox_layout_data)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Вход")
        self.label_header.setAlignment(QtCore.Qt.AlignHCenter)

        self.vbox_layout_data.addWidget(self.label_header)
        self.vbox_layout_data.addSpacing(10)

        # строка ввода фамилии
        self.line_edit_surname = QtWidgets.QLineEdit()
        self.line_edit_surname.setObjectName("line_edit_surname")
        self.line_edit_surname.setFont(self.font_widgets)
        self.line_edit_surname.setPlaceholderText("Фамилия")
        self.line_edit_surname.setMinimumHeight(self.min_height)

        if self.surname != None:
            self.line_edit_surname.insert(self.surname)

        self.vbox_layout_data.addWidget(self.line_edit_surname)
        self.vbox_layout_data.addSpacing(5)

        # строка ввода имени
        self.line_edit_name = QtWidgets.QLineEdit()
        self.line_edit_name.setObjectName("line_edit_name")
        self.line_edit_name.setFont(self.font_widgets)
        self.line_edit_name.setPlaceholderText("Имя")
        self.line_edit_name.setMinimumHeight(self.min_height)

        if self.name != None:
            self.line_edit_name.insert(self.name)

        self.vbox_layout_data.addWidget(self.line_edit_name)
        self.vbox_layout_data.addSpacing(5)

        # строка ввода класса
        self.line_edit_class = QtWidgets.QLineEdit()
        self.line_edit_class.setObjectName("line_edit_class")
        self.line_edit_class.setFont(self.font_widgets)
        self.line_edit_class.setPlaceholderText("Класс")
        self.line_edit_class.setMinimumHeight(self.min_height)

        if self.class_name != None:
            self.line_edit_class.insert(self.class_name)

        self.vbox_layout_data.addWidget(self.line_edit_class)
        self.vbox_layout_data.addSpacing(5)

        # кнопка выбора курса
        self.push_button_course = PushButtonCourse(path_imgs = self.path_imgs, data_theme = self.data_theme["push_button_cource"], func = self.get_path_course)

        self.vbox_layout_data.addWidget(self.push_button_course)
        self.vbox_layout_data.addSpacing(5)

        # кнопка входа
        self.push_button_enter = QtWidgets.QPushButton()
        self.push_button_enter.setObjectName("push_button_enter")
        self.push_button_enter.setEnabled(False)
        self.push_button_enter.clicked.connect(self.start_test)
        self.push_button_enter.setFont(self.font_widgets)
        self.push_button_enter.setText("Войти")
        self.push_button_enter.setMinimumHeight(self.min_height)

        self.vbox_layout_data.addWidget(self.push_button_enter)

        # кнопка посмотреть таблицу результатов
        self.vbox_layout_main.addSpacing(10)

        self.push_button_table_results = QtWidgets.QPushButton()
        self.push_button_table_results.setObjectName("push_button_table_results")
        self.push_button_table_results.clicked.connect(self.func_table_results)
        self.push_button_table_results.setFont(self.font_widgets)
        self.push_button_table_results.setText("Таблица результатов")
        self.push_button_table_results.setMinimumHeight(self.min_height)

        self.vbox_layout_main.addWidget(self.push_button_table_results)

        # валидация ввода данных
        self.line_edit_surname.textChanged.connect(self.check_data)
        self.line_edit_name.textChanged.connect(self.check_data)
        self.line_edit_class.textChanged.connect(self.check_data)

        self.set_style_sheet()

    def start_test(self):
        data_dict = DataPassage(
            name = self.line_edit_name.text(),
            surname = self.line_edit_surname.text(),
            class_name = self.line_edit_class.text(),
            path_course = self.path_course
        )

        self.func_start(data = data_dict)

    def get_path_course(self):
        # диалог выбора файла с курсом
        path_file_course = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор курса", self.path_cources, "XML Файл (*.xml)")[0]

        if os.path.isfile(path_file_course):
            self.path_course = path_file_course

            self.check_data()
            
            name_course = os.path.splitext(os.path.basename(self.path_course))[0]
            name_course = (name_course[:self.max_len] + "…") if len(name_course) > self.max_len else name_course
            self.push_button_course.change_text(name_course)
            self.push_button_course.choosed = True

    def check_data(self):
        # проверка данных
        if self.line_edit_name.text() != "" and self.line_edit_surname.text() != "" and self.line_edit_class.text() != "" and self.path_course != None:
            if os.path.isfile(self.path_course):
                self.push_button_enter.setEnabled(True)
        else:
            self.push_button_enter.setEnabled(False)

    def init_variables(self):
        self.max_len = 19
        self.path_course = None
        self.min_height = 42
        self.font_widgets = QtGui.QFont("Segoe UI", 12)
        self.font_label_header = QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold)

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background-color: %(background_frame_main)s;
        } """ % self.data_theme)

        # внутренняя рамка формы
        self.frame_data.setStyleSheet("""
        #frame_data {
            border-radius: 14px;
            background-color: %(background_frame)s;
        } """ % self.data_theme)

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            background-color: %(background)s; 
            color: %(color)s
        } """ % self.data_theme["label_header"])
        
        temp_data_theme_not_focus = self.data_theme["line_edit"]["not_focus"]
        temp_data_theme_focus = self.data_theme["line_edit"]["focus"]
        temp_data_theme = {
            "color_border_not_focus": temp_data_theme_not_focus["color_border"],
            "background_not_focus": temp_data_theme_not_focus["background"], 
            "color_not_focus": temp_data_theme_not_focus["color"], 
            "color_border_focus": temp_data_theme_focus["color_border"],
            "background_focus": temp_data_theme_focus["background"], 
            "color_focus": temp_data_theme_focus["color"]}
        
        # строка ввода фамилии
        self.line_edit_surname.setStyleSheet("""
        #line_edit_surname {
            border-radius: 7px; 
            border: 2px solid %(color_border_not_focus)s; 
            background-color: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_surname:focus {
            border: 2px solid %(color_border_focus)s; 
            background-color: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)

        # строка ввода имени
        self.line_edit_name.setStyleSheet("""
        #line_edit_name {
            border-radius: 7px; 
            border: 2px solid %(color_border_not_focus)s; 
            background-color: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_name:focus {
            border: 2px solid %(color_border_focus)s; 
            background-color: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)
        
        # строка ввода класса
        self.line_edit_class.setStyleSheet("""
        #line_edit_class {
            border-radius: 7px;
            border: 2px solid %(color_border_not_focus)s; 
            background-color: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_class:focus {
            border: 2px solid %(color_border_focus)s; 
            background-color: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)
        
        # кнопка входа
        self.push_button_enter.setStyleSheet("""
        #push_button_enter {
            outline: 0;
            border-radius: 7px; 
            background-color: %(background)s; 
            color: %(color)s;
        } 
        #push_button_enter::pressed {
            background-color: %(background_active)s; 
            color: %(color)s;
        }
        #push_button_enter::disabled {
            background-color: %(background_disabled)s;
            color: %(color)s;
        } """ % self.data_theme["push_button_enter"])

        # кнопка посмотреть таблицу результатов
        self.push_button_table_results.setStyleSheet("""
        #push_button_table_results {
            outline: 0;
            border-bottom-left-radius: 14px; 
            border-bottom-right-radius: 14px; 
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_table_results"])
