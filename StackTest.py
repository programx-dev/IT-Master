from PyQt5 import QtCore, QtGui, QtWidgets
import os
import datetime
import xml.etree.ElementTree as ET
import re
from dataclasses import dataclass

@dataclass
class DataPassage:
    date_start: datetime.datetime
    date_end: datetime.datetime
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int

class PushButtonNavigation(QtWidgets.QPushButton):
    push_button_current = None
    def __init__(self, number: int, data_theme: dict, func: callable):
        super().__init__()

        self.func = func
        self.number = number
        self.data_theme = data_theme

        self.init_variables()

        self.setObjectName("push_button_navigation")
        self.setText(f"{self.number + 1}")
        self.setFont(self.font)
        self.setFixedSize(self.min_size)
        self.clicked.connect(self.push_button_press)

        self.set_style_sheet()

    def init_variables(self):
        self.min_size = QtCore.QSize(50, 50)
        self.font = QtGui.QFont("Segoe UI", 12)

        self.dict_style_sheet_settings = {
            "answered": False,
            "current": False
        }

        self.style_answered = {
            "background": self.data_theme["background_answered"],
            "color": self.data_theme["color"],
            "border_color": "transparent",
            "radius": self.min_size.width() // 2
        }
        self.style_not_answered = {
            "background": self.data_theme["background"],
            "color": self.data_theme["color"],
            "border_color": "transparent",
            "radius": self.min_size.width() // 2
        }
        self.style_current = {
            "border_color": self.data_theme["color_border_current"],
            "radius": self.min_size.width() // 2
        }
        self.style_not_current = {
            "border_color": "transparent",
            "radius": self.min_size.width() // 2
        }

    def push_button_press(self):
        if self != PushButtonNavigation.push_button_current and PushButtonNavigation.push_button_current:
            PushButtonNavigation.push_button_current.set_style_sheet_not_current()

        PushButtonNavigation.push_button_current = self
        self.set_style_sheet_current()

        self.func(self.number)

    def set_style_sheet_current(self):
        self.dict_style_sheet_settings["current"] = True

        self.set_style_sheet()

    def set_style_sheet_not_current(self):
        self.dict_style_sheet_settings["current"] = False

        self.set_style_sheet()

    def set_style_sheet_answered(self):
        self.dict_style_sheet_settings["answered"] = True

        self.set_style_sheet()

    def set_style_sheet_not_answered(self):
        self.dict_style_sheet_settings["answered"] = False

        self.set_style_sheet()

    def set_style_sheet(self):
        if self.dict_style_sheet_settings["answered"]:
            temp_style_sheet_answered = self.style_answered
        else:
            temp_style_sheet_answered = self.style_not_answered

        if self.dict_style_sheet_settings["current"]:
            temp_style_sheet_current = self.style_current
        else:
            temp_style_sheet_current = self.style_not_current

        temp_style_sheet = temp_style_sheet_answered | temp_style_sheet_current

        self.setStyleSheet("""
        #push_button_navigation {
            outline: 0;
            border: 3px solid;
            border-radius: %(radius)spx;
            background-color: %(background)s;
            border-color: %(border_color)s;
            color: %(color)s;
        } """ % temp_style_sheet)

class BarNavigation(QtWidgets.QWidget):
    def __init__(self, len_course: int, data_theme: dict, func: callable):
        super().__init__()

        self.len_course = len_course
        self.data_theme = data_theme
        self.func = func

        self.init_variables()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(10)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        for i in range(self.len_course):
            push_button = PushButtonNavigation(number = i, data_theme = self.data_theme, func = self.func)
            self.list_answered[i][0] = push_button
            self.hbox_layout_main.addWidget(push_button)

    def change_answered(self, number: int):
        self.list_answered[number][1] = True
        self.list_answered[number][0].set_style_sheet_answered()

    def push_button_press(self, number: int):
        self.list_answered[number][0].push_button_press()

    def init_variables(self):
        self.list_answered = {i: [None, False] for i in range(self.len_course)}

class RadiobuttonAnswers(QtWidgets.QRadioButton):
    def __init__(self, text: str, path_imgs: str, data_theme: dict):
        self.text = text
        self.data_theme = data_theme
        self.path_imgs = path_imgs

        self.init_variables()

        super().__init__()
        self.setObjectName("radio_button")
        self.setText(self.text)
        self.setFont(self.font)

        self.set_style_sheet()

    def init_variables(self):
        self.font = QtGui.QFont("Segoe UI", 14)
        self.path_img_checked = os.path.join(self.path_imgs, "radiobutton_checked.png").replace("\\", "/")
        self.path_img_unchecked = os.path.join(self.path_imgs, "radiobutton_unchecked.png").replace("\\", "/")

    def set_style_sheet(self):
        self.data_theme["path_img_checked"] = self.path_img_checked
        self.data_theme["path_img_unchecked"] = self.path_img_unchecked

        self.setStyleSheet("""
        #radio_button {
            outline: 0;
            background-color: %(background)s;
        }
        #radio_button::title {
            color: %(color)s;
        }
        #radio_button::indicator {
            width: 22;
            height: 22;
        }
        #radio_button::indicator:checked {
            border-image: url("%(path_img_checked)s");
        }
        #radio_button::indicator:unchecked {
            border-image: url("%(path_img_unchecked)s");
        } """ % self.data_theme)

class CheckboxAnswers(QtWidgets.QCheckBox):
    def __init__(self, text: str, path_imgs: str, data_theme: dict):
        self.text = text
        self.data_theme = data_theme
        self.path_imgs = path_imgs

        self.init_variables()

        super().__init__(self.text)
        self.setObjectName("checkbox")
        self.setFont(self.font)

        self.set_style_sheet()

    def init_variables(self):
        self.font = QtGui.QFont("Segoe UI", 14)
        self.path_img_checked = os.path.join(self.path_imgs, "checkbox_checked.png").replace('\\', '/')
        self.path_img_unchecked = os.path.join(self.path_imgs, "checkbox_unchecked.png").replace('\\', '/')

    def set_style_sheet(self):
        self.data_theme["path_img_checked"] = self.path_img_checked
        self.data_theme["path_img_unchecked"] = self.path_img_unchecked

        self.setStyleSheet("""
        #checkbox {
            outline: 0;
            background-color: %(background)s;
        }
        #checkbox::title {
            color: %(color)s;
        }
        #checkbox::indicator {
            width: 22;
            height: 22;
        }
        #checkbox::indicator:checked {
            border-image: url("%(path_img_checked)s");
        }
        #checkbox::indicator:unchecked {
            border-image: url("%(path_img_unchecked)s");
        } """ % self.data_theme)

class WidgetTest(QtWidgets.QWidget):
    def __init__(self, question: str, path_imgs: str, started: bool, answer, data_theme: dict, number: int, len_course: int, func_changed: callable):
        super().__init__()

        self.started = started
        self.answer = answer
        self.question = question
        self.data_theme = data_theme
        self.path_imgs = path_imgs
        self.number = number
        self.len_course = len_course
        self.func_changed = func_changed
        
        self.init_variables()

        # главный макет
        self.grid_layout_main = QtWidgets.QGridLayout(self)
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(2, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(2, 0)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # макет для виджетов теста
        self.vbox_layout =  QtWidgets.QVBoxLayout()
        self.vbox_layout.setSpacing(0)
        self.vbox_layout.setContentsMargins(20, 20, 20, 20)

        self.frame_main.setLayout(self.vbox_layout)

        # метка номера задания
        self.label_numder_question = QtWidgets.QLabel()
        self.label_numder_question.setObjectName("label_numder_question")
        self.label_numder_question.setFont(self.font_promt)
        self.label_numder_question.setText(f"Вопрос {self.number + 1}")

        self.vbox_layout.addWidget(self.label_numder_question)

        # метра с вопросом
        self.label_question = QtWidgets.QLabel()
        self.label_question.setObjectName("label_question")
        self.label_question.setWordWrap(True)
        self.label_question.setFont(self.font_widgets)
        self.label_question.setText(self.question.find("title").text)

        self.vbox_layout.addWidget(self.label_question)

        # метка типа задания
        self.label_type_question = QtWidgets.QLabel()
        self.label_type_question.setObjectName("label_type_question")
        self.label_type_question.setFont(self.font_promt)

        self.vbox_layout.addWidget(self.label_type_question)
        self.vbox_layout.addSpacing(5)

        # создание виджетов ответов
        if self.question.find("questions").find("type").text == "radiobutton":
            self.label_type_question.setText("Укажите правильный вариант ответа:")

            self.create_radio_buttons(list_radio_buttons = self.question.find("questions").findall("question"))

        elif self.question.find("questions").find("type").text == "checkbox":
            self.label_type_question.setText("Укажите правильные варианты ответа:")

            self.create_checkboxes(list_checkboxes = self.question.find("questions").findall("question"))

        elif self.question.find("questions").find("type").text == "input":
            self.label_type_question.setText("Введите правильный ответ:")
            
            self.line_edit_answer = QtWidgets.QLineEdit()
            self.line_edit_answer.setObjectName("line_edit_answer")
            self.line_edit_answer.textChanged.connect(self.line_edit_text_changed)
            self.line_edit_answer.setFont(self.font_widgets)
            self.line_edit_answer.setMinimumHeight(self.min_height)

            if self.answer:
                self.line_edit_answer.insert(self.answer)

            self.vbox_layout.addWidget(self.line_edit_answer)

            temp_data_theme_not_focus = self.data_theme["line_edit"]["not_focus"]
            temp_data_theme_focus = self.data_theme["line_edit"]["focus"]

            temp_data_theme = {
                "color_border_not_focus": temp_data_theme_not_focus["color_border"],
                "background_not_focus": temp_data_theme_not_focus["background"], 
                "color_not_focus": temp_data_theme_not_focus["color"], 
                "color_border_focus": temp_data_theme_focus["color_border"],
                "background_focus": temp_data_theme_focus["background"], 
                "color_focus": temp_data_theme_focus["color"]}

            self.line_edit_answer.setStyleSheet("""
            #line_edit_answer {
                border-radius: 7px; 
                border: 2px solid %(color_border_not_focus)s; 
                background-color: %(background_not_focus)s; 
                color: %(color_not_focus)s;
            } 
            #line_edit_answer:focus {
                border: 2px solid %(color_border_focus)s; 
                background-color: %(background_focus)s; 
                color: %(color_focus)s;
            } """ % temp_data_theme)

        self.vbox_layout.addStretch(1)
        
        self.set_style_sheet()

    def init_variables(self):
        self.min_height = 42
        self.font_widgets = QtGui.QFont("Segoe UI", 14)
        self.font_promt = QtGui.QFont("Segoe UI", 12)

    def radio_button_clicked(self, radio_button):
        self.answer = radio_button.text

        self.func_changed(self.number)

    def ceckbox_clicked(self):
        if not self.sender().isChecked() and self.sender().text in self.answer:
            self.answer.remove(self.sender().text)
        else:
            self.answer.append(self.sender().text)

        self.func_changed(self.number)

    def line_edit_text_changed(self):
        self.answer = self.line_edit_answer.text()

        self.func_changed(self.number)

    def create_radio_buttons(self, list_radio_buttons: list):
        # макет радиокнопок
        self.vbox_layout_radio_buttons = QtWidgets.QVBoxLayout()
        self.vbox_layout_radio_buttons.setSpacing(10)
        self.vbox_layout_radio_buttons.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout.addLayout(self.vbox_layout_radio_buttons)

        # группа радио кнопок
        self.group_radio_buttons = QtWidgets.QButtonGroup()

        # создание и упаковка радиокнопок
        for element in list_radio_buttons:
            radio_button = RadiobuttonAnswers(path_imgs = self.path_imgs, text = element.text, data_theme = self.data_theme["radio_button"])

            if self.answer and element.text == self.answer:
                radio_button.setChecked(True)

            self.group_radio_buttons.addButton(radio_button)

            self.vbox_layout_radio_buttons.addWidget(radio_button)

        self.group_radio_buttons.buttonClicked.connect(self.radio_button_clicked)
    
    def create_checkboxes(self, list_checkboxes: list):
        # макет переключателей
        self.vbox_layout_checkboxes = QtWidgets.QVBoxLayout()
        self.vbox_layout_checkboxes.setSpacing(10)
        self.vbox_layout_checkboxes.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout.addLayout(self.vbox_layout_checkboxes)

        # создание и упаковка радиокнопок
        for element in list_checkboxes:
            checkbox = CheckboxAnswers(path_imgs = self.path_imgs, text = element.text, data_theme = self.data_theme["checkbox"])

            if any(self.answer) and element.text in self.answer:
                checkbox.setChecked(True)

            self.vbox_layout_checkboxes.addWidget(checkbox)
            
            checkbox.stateChanged.connect(self.ceckbox_clicked)

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main{
            background-color: %(background)s;
        } """ % self.data_theme)

        # метка номера задания
        self.label_question.setStyleSheet("""
        #label_question{
            color: %(color)s;}""" 
        % self.data_theme)

        # метка вопроса
        self.label_numder_question.setStyleSheet("""
        #label_numder_question{
            background-color: %(background)s;
            color: %(color_prompt)s;}""" 
        % self.data_theme)

        # метка типа задания
        self.label_type_question.setStyleSheet("""
        #label_type_question{
            background-color: %(background)s;
            color: %(color_prompt)s;}""" 
        % self.data_theme)

class StackTest(QtWidgets.QWidget):
    def __init__(self, data_theme: dict, path_imgs: str, path_course: str, func: callable):
        super().__init__()

        self.data_theme = data_theme
        self.path_imgs = path_imgs
        self.path_course = path_course
        self.func = func

        self.init_variables()

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout(self)
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(2, 0)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # главный макет
        self.vbox_layout_main = QtWidgets.QVBoxLayout()
        self.vbox_layout_main.setSpacing(0)
        self.vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_main)

        # сетка тестов
        self.grid_layout_test = QtWidgets.QGridLayout()
        self.grid_layout_test.setSpacing(0)
        self.grid_layout_test.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_test.setRowStretch(0, 0)
        self.grid_layout_test.setRowStretch(2, 0)
        self.grid_layout_test.setColumnStretch(0, 0)
        self.grid_layout_test.setColumnStretch(2, 0)

        self.vbox_layout_main.addLayout(self.grid_layout_test)

        # виджет стеков для страниц теста
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")

        self.grid_layout_test.addWidget(self.stacked_widget, 1, 1)

        # главная панель инструментов и навигации
        self.frame_bottom = QtWidgets.QFrame()
        self.frame_bottom.setObjectName("frame_bottom")
        
        self.vbox_layout_main.addWidget(self.frame_bottom)

        self.hbox_layout_bottom = QtWidgets.QHBoxLayout()
        self.hbox_layout_bottom.setSpacing(0)
        self.hbox_layout_bottom.setContentsMargins(20, 10, 20, 10)

        self.frame_bottom.setLayout(self.hbox_layout_bottom)

        self.hbox_layout_bottom.addStretch(1)

        # панель навигации с кнопками
        self.bar_navigation = BarNavigation(len_course = self.len_course, data_theme = self.data_theme["frame_bottom"]["push_button_navigation"], func = self.switch_question)

        self.hbox_layout_bottom.addWidget(self.bar_navigation)
        self.hbox_layout_bottom.addStretch(1)

        # кнопка завершить тест
        self.push_button_finish = QtWidgets.QPushButton()
        self.push_button_finish.setObjectName("push_button_finish")
        self.push_button_finish.clicked.connect(self.finish_test)
        self.push_button_finish.setText("Завершить")
        self.push_button_finish.setFont(self.font_widgets)
        self.push_button_finish.setFixedHeight(self.min_size.height())

        self.hbox_layout_bottom.addWidget(self.push_button_finish)

        # создать страницу теста
        self.switch_question(self.current_question)
        self.bar_navigation.push_button_press(number = self.current_question)

        self.set_style_sheet()

    def finish_test(self):
        # получение ответа текущей страницы
        self.dict_answers[self.current_stack.number] = self.current_stack.answer

        # подсчёт количества верных, неверных и пропущенных ответ
        points_right = 0
        points_wrong = 0
        points_skip = 0

        for i in range(self.len_course):
            user_answer = self.dict_answers[i]
            right_answer = list(i.text for i in self.root.findall("exercise")[i].find("answers").findall("answer"))
            type = self.root.findall("exercise")[i].find("questions").find("type").text

            if self.dict_started[i]:
                # если радиокнопка
                if type == "radiobutton":
                    if user_answer == right_answer[0]:
                        points_right += 1
                    else:
                        points_wrong += 1

                # если переключатель
                elif type == "checkbox":
                    right_answer.sort()
                    user_answer.sort()

                    if user_answer == right_answer:
                        points_right += 1
                    else:
                        points_wrong += 1

                # если ввод ответа
                elif type == "input":
                    settings = None
                    right_answer = right_answer[0]

                    if self.root.findall("exercise")[i].find("answers").find("settings") != None:
                        settings = self.root.findall("exercise")[i].find("answers").find("settings").attrib
                    
                    if settings and user_answer != None:
                        # убирает пробелы
                        if "including_space" in settings:
                            if settings["including_space"] == "False":
                                pattern = re.compile(r"^\s*|\s*$")

                                right_answer = pattern.sub(r"", right_answer)
                                user_answer = pattern.sub(r"", user_answer)

                        if "type" in settings:
                            if settings["type"] == "number":
                                # заменаяет , на .
                                right_answer = right_answer.replace(",", ".")
                                user_answer = user_answer.replace(",", ".")

                                # проверка на число
                                pattern = re.compile("^-?\d+(\.d+)?$")

                                # если это число, то приводит к дробному типу
                                if (right_answer_ := pattern.match(right_answer)) and (user_answer_ := pattern.match(user_answer)):
                                    if right_answer_.group(0) and user_answer_.group(0):
                                        right_answer = str(float(right_answer))
                                        user_answer = str(float(user_answer))

                    if right_answer == user_answer:
                        points_right += 1
                    else:
                        points_wrong += 1

            else:
                points_skip += 1

        data_passage = DataPassage(
            date_start = self.time_start,
            date_end = datetime.datetime.now(),
            points_max = self.len_course,
            points_right = points_right,
            points_wrong = points_wrong,
            points_skip = points_skip
        )

        self.func(data_passage)

    def switch_question(self, number: int):
        current_question = self.root.findall("exercise")[number]

        if self.current_stack != None:
            # сохранение ответа
            self.dict_answers[self.current_stack.number] = self.current_stack.answer

            # удаление старой страницы
            self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка новой страницы
        self.current_stack = WidgetTest(question = current_question, path_imgs = self.path_imgs, started = self.dict_started[number], answer = self.dict_answers[number], data_theme = self.data_theme["test_tab"],  number = number, len_course = self.len_course, func_changed = self.func_changed)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def func_changed(self, number: int):
        self.bar_navigation.change_answered(number)
        self.dict_started[number] = True

    def init_variables(self):
        self.current_stack = None
        self.current_question = 0

        self.tree = ET.parse(self.path_course)
        self.root = self.tree.getroot()

        self.len_course = len(self.root.findall("exercise"))
        self.dict_answers = {}
        self.dict_started = {i: False for i in range(self.len_course)}
        for i in range(self.len_course):
            temp = self.root.findall("exercise")[i].find("questions").find("type").text
            if temp == "checkbox":
                self.dict_answers[i] = []
            elif temp == "radiobutton":
                self.dict_answers[i] = None
            elif temp == "input":
                self.dict_answers[i] = None

        self.time_start = datetime.datetime.now()

        self.min_size = QtCore.QSize(42, 42)
        self.font_widgets = QtGui.QFont("Segoe UI", 12)

    def set_style_sheet(self):
        # панель инструментов и навигации
        self.frame_bottom.setStyleSheet("""
        #frame_bottom {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background-color: %(background)s;
        } """ % self.data_theme["frame_bottom"])

        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background-color: %(background)s;
        } """ % self.data_theme["frame_main"])

        # кнопка завершить тест
        self.push_button_finish.setStyleSheet("""
        #push_button_finish {
            outline: 0;
            border-top-left-radius: 7px;
            border-top-right-radius: 25px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            padding-left: 10px;
            padding-right: 10px;
            color: %(color)s;
            background-color: %(background)s; 
        } """ % self.data_theme["frame_bottom"]["push_button_send"])
