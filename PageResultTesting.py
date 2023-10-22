from PyQt6 import QtCore, QtGui, QtWidgets
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
import PageTesting

@dataclass
class DataPageResultTest:
    horizontal_scrollbar_value: int = 0
    vertical__scrollbar_value: int = 0

@dataclass
class DataPageViewerResultTesting:
    color_right: QtGui.QColor
    color_wrong: QtGui.QColor
    color_skip: QtGui.QColor

class PushButtonResultQuestion(PageTesting.PushButtonNavigation):
    """Класс для кнопок навигации по вопросам на панели инструменов"""
    push_button_question_clicked = QtCore.pyqtSignal(int)
    
    def __init__(self, number: int):
        super().__init__()

        self.__number = number
        self.__answered = False

        self.setObjectName("push_button_result_question")
        self.setText(f"{self.__number + 1}")
        self.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_navigation_clicked.connect(self.__push_button_question_press)

    def set_status(self, status: PageTesting.AnswerStatus):
        self.setProperty("status", status.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def __push_button_question_press(self):
        self.push_button_question_clicked.emit(self.__number)

class PushButtonResultTesting(PageTesting.PushButtonNavigation):
    """Класс для кнопки для открытия результатов  тестирования"""
    push_button_result_testing_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_images: str):
        super().__init__()

        self.__path_images = path_images

        self.setObjectName("push_button_result_testing")
        self.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"results.png")))
        self.setIconSize(QtCore.QSize(35, 35))
        self.push_button_navigation_clicked.connect(self.__push_button_result_testing_press)

    def __push_button_result_testing_press(self):
        self.push_button_result_testing_clicked.emit()

class LabelLegend(QtWidgets.QWidget):
    """Класс для метки легнды диаграммы с задавыемым цветом кружка"""

    def __init__(self, color: QtGui.QColor, text: str = ""):
        super().__init__()
        self.setObjectName("label_legend")
        
        self.__color = color
        self.__text = text

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # изображение с цветным кружком
        self.__pixmap = QtGui.QPixmap(24, 24)
        self.__pixmap.fill(QtGui.QColor(0, 0, 0, 0))
        
        self.__painter = QtGui.QPainter()
        self.__painter.begin(self.__pixmap)
        self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.__painter.setPen(QtGui.QPen(QtGui.QColor(), 0, QtCore.Qt.PenStyle.NoPen))
        self.__painter.setBrush(QtGui.QBrush(self.__color, QtCore.Qt.BrushStyle.SolidPattern))
        self.__painter.drawEllipse(0, 0, 24, 24)
        self.__painter.end()

        # метка с изображением
        self.__label_pixmap = QtWidgets.QLabel()
        self.__label_pixmap.setObjectName("label_pixmap")
        self.__label_pixmap.setPixmap(self.__pixmap)

        self.__hbox_layout_main.addWidget(self.__label_pixmap)
        self.__hbox_layout_main.addSpacing(10)

        # метка с текстом
        self.__label_text = QtWidgets.QLabel()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 16))
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_text.setText(self.__text)

        self.__hbox_layout_main.addWidget(self.__label_text)

    def change_color(self, color: QtGui.QColor):
        self.__color = color

       # изображение с цветным кружком
        self.__pixmap = QtGui.QPixmap(24, 24)
        self.__pixmap.fill(QtGui.QColor(0, 0, 0, 0))
        
        self.__painter = QtGui.QPainter()
        self.__painter.begin(self.__pixmap)
        self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.__painter.setPen(QtGui.QPen(QtGui.QColor(), 0, QtCore.Qt.PenStyle.NoPen))
        self.__painter.setBrush(QtGui.QBrush(self.__color, QtCore.Qt.BrushStyle.SolidPattern))
        self.__painter.drawEllipse(0, 0, 24, 24)
        self.__painter.end()

        self.__label_pixmap.setPixmap(self.__pixmap)

    def set_text(self, text: str):
        self.__text = text
        self.__label_text.setText(self.__text)

class PageViewerResultTesting(QtWidgets.QWidget):
    """Класс просмотра результатов тестирования"""

    def __init__(self, data_result_testing: PageTesting.DataResultTesting, data_page_viewer_result_testing: DataPageViewerResultTesting):
        super().__init__()
        self.setObjectName("page_viewer_result_testing")

        self.__data_result_testing = data_result_testing
        self.__data_page_viewer_result_testing = data_page_viewer_result_testing

        # self.__parser_rgb = re.compile("rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

        self.__points_right = 0
        self.__points_wrong = 0
        self.__points_skip = 0
        self.__amount_question = len(self.__data_result_testing.list_data_result)

        for i in self.__data_result_testing.list_data_result:
            match i.status:
                case PageTesting.AnswerStatus.right:
                    self.__points_right += 1
                case PageTesting.AnswerStatus.wrong:
                    self.__points_wrong += 1
                case _:
                    self.__points_skip += 1

        # parsing_result = self.__parser_rgb.search(self.__data_theme["frame_main"]["chart"]["pie_slice_right"]["color"])
        # if parsing_result != None:
        #     color_right = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        # else:
        #     color_right = QtGui.QColor(self.__data_theme["frame_main"]["chart"]["pie_slice_right"]["color"])

        # parsing_result = self.__parser_rgb.search(self.__data_theme["frame_main"]["chart"]["pie_slice_wrong"]["color"])
        # if parsing_result != None:
        #     color_wrong = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        # else:
        #     color_wrong = QtGui.QColor(self.__data_theme["frame_main"]["chart"]["pie_slice_wrong"]["color"])

        # parsing_result = self.__parser_rgb.search(self.__data_theme["frame_main"]["chart"]["pie_slice_skip"]["color"])
        # if parsing_result != None:
        #     color_skip = QtGui.QColor("#{0:02X}{1:02X}{2:02X}".format(*map(int, parsing_result.groups())))
        # else:
        #     color_skip = QtGui.QColor(self.__data_theme["frame_main"]["chart"]["pie_slice_skip"]["color"])

        self.__tree = ET.parse(self.__data_result_testing.path_course)
        self.__root = self.__tree.getroot()

        # главная сетка
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__hbox_layout_main.addWidget(self.__frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.__frame_main.setLayout(self.__vbox_layout_internal)

        # макет строки с информацией о прохождении
        self.__hbox_layout_info = QtWidgets.QHBoxLayout()
        self.__hbox_layout_info.setSpacing(0)
        self.__hbox_layout_info.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.__vbox_layout_internal.addLayout(self.__hbox_layout_info)
        self.__vbox_layout_internal.addStretch(1)

        # метка названия теста
        name_test = self.__root.find("name").text
        self.__label_name_test = QtWidgets.QLabel()
        self.__label_name_test.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__label_name_test.setObjectName("label_name_test")
        self.__label_name_test.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_name_test.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_name_test.setText(f"{name_test[:40] + (name_test[40:] and '…')}")

        self.__hbox_layout_info.addWidget(self.__label_name_test)
        self.__hbox_layout_info.addSpacing(10)

        # метка даты прохождения
        self.__label_date_passing = QtWidgets.QLabel()
        self.__label_date_passing.setObjectName("label_date_passing")
        self.__label_date_passing.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_date_passing.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_date_passing.setText(f"Дата прохождения: {self.__data_result_testing.date_start.strftime(r'%d.%m.%Y %H:%M')}")

        self.__hbox_layout_info.addWidget(self.__label_date_passing)
        self.__hbox_layout_info.addSpacing(10)

        # метка времени выполнения
        duration = (self.__data_result_testing.date_end - self.__data_result_testing.date_start).total_seconds()
        hours, remains = divmod(duration, 3600)
        minutes, remains = divmod(remains, 60)
        seconds = remains

        self.__label_time_passing = QtWidgets.QLabel()
        self.__label_time_passing.setObjectName("label_time_passing")
        self.__label_time_passing.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_time_passing.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_time_passing.setText(f"Время прохождения: {round(hours):0>2}:{round(minutes):0>2}:{round(seconds):0>2}")

        self.__hbox_layout_info.addWidget(self.__label_time_passing)

        # макет диаграммы и легенды
        self.__hbox_layout_chart = QtWidgets.QHBoxLayout()
        self.__hbox_layout_chart.setSpacing(0)
        self.__hbox_layout_chart.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_chart.addStretch(2)

        self.__vbox_layout_internal.addLayout(self.__hbox_layout_chart)
        self.__vbox_layout_internal.addStretch(1)

        # диаграмма
        self.__pie_series = QPieSeries()
        self.__pie_series.setHoleSize(0.4)

        self.__pie_slice_right = self.__pie_series.append("Правильные", round(self.__points_right / self.__amount_question * 100))
        self.__pie_slice_right.setBrush(self.__data_page_viewer_result_testing.color_right)

        self.__pie_slice_wrong = self.__pie_series.append("Неправильные", round(self.__points_wrong / self.__amount_question * 100))
        self.__pie_slice_wrong.setBrush(self.__data_page_viewer_result_testing.color_wrong)
        
        self.__pie_slice_skip = self.__pie_series.append("Пропущенные", round(self.__points_skip / self.__amount_question * 100))
        self.__pie_slice_skip.setBrush(self.__data_page_viewer_result_testing.color_skip)

        self.__chart = QChart()
        self.__chart.legend().hide()
        self.__chart.layout().setContentsMargins(0, 0, 0, 0)
        self.__chart.setBackgroundRoundness(0)
        self.__chart.setContentsMargins(-82,-82,-82, -82)
        self.__chart.addSeries(self.__pie_series)
        self.__chart.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.transparent))

        self.__chart__view = QChartView(self.__chart)
        self.__chart__view.setFixedSize(QtCore.QSize(293, 293))
        self.__chart__view.setObjectName("chart_view")

        self.__hbox_layout_chart.addWidget(self.__chart__view)
        self.__hbox_layout_chart.addStretch(1)

        # рамка легенды
        self.__frame_legend = QtWidgets.QFrame()
        self.__frame_legend.setObjectName("frame_legend")
        self.__frame_legend.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__frame_legend.setObjectName("frame_legend")
        
        self.__hbox_layout_chart.addWidget(self.__frame_legend)
        self.__hbox_layout_chart.addStretch(2)

        # макет легенды
        self.__vbox_layout_legend = QtWidgets.QVBoxLayout()
        self.__vbox_layout_legend.setContentsMargins(30, 30, 30, 30)
        self.__vbox_layout_legend.setSpacing(0)

        self.__frame_legend.setLayout(self.__vbox_layout_legend)

        # метка количества баллов
        self.__label_result = QtWidgets.QLabel()
        self.__label_result.setObjectName("label_result")
        self.__label_result.setText(f"{round(self.__points_right / self.__amount_question * 100)} / 100")
        self.__label_result.setFont(QtGui.QFont("Segoe UI", 20))
        self.__label_result.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__vbox_layout_legend.addWidget(self.__label_result)
        self.__vbox_layout_legend.addSpacing(10)

        # метка заголовка
        self.__label_header = QtWidgets.QLabel()
        self.__label_header.setObjectName("label_header")
        self.__label_header.setText("Результат теста в баллах")
        self.__label_header.setFont(QtGui.QFont("Segoe UI", 16))
        self.__label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__vbox_layout_legend.addWidget(self.__label_header)
        self.__vbox_layout_legend.addSpacing(10)

        # метка легенды правильно
        self.label_legent_right = LabelLegend(color = self.__data_page_viewer_result_testing.color_right)
        self.label_legent_right.setProperty("status", PageTesting.AnswerStatus.right.value)
        self.label_legent_right.set_text(f"Правильные: {self.__points_right} ({round(self.__points_right / self.__amount_question * 100)}%)")

        self.__vbox_layout_legend.addWidget(self.label_legent_right)
        self.__vbox_layout_legend.setAlignment(self.label_legent_right, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__vbox_layout_legend.addSpacing(10)

        # метка легенды неправильно
        self.label_legent_wrong = LabelLegend(color = self.__data_page_viewer_result_testing.color_wrong)
        self.label_legent_wrong.setProperty("status", PageTesting.AnswerStatus.wrong.value)
        self.label_legent_wrong.set_text(f"Неправильные: {self.__points_wrong} ({round(self.__points_wrong / self.__amount_question * 100)}%)")

        self.__vbox_layout_legend.addWidget(self.label_legent_wrong)
        self.__vbox_layout_legend.setAlignment(self.label_legent_wrong, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__vbox_layout_legend.addSpacing(10)

        # метка легенды пропущенно
        self.label_legent_skip = LabelLegend(color = self.__data_page_viewer_result_testing.color_skip)
        self.label_legent_skip.setProperty("status", PageTesting.AnswerStatus.wrong.skip.value)
        self.label_legent_skip.set_text(f"Пропущенные: {self.__points_skip} ({round(self.__points_skip / self.__amount_question * 100)}%)")

        self.__vbox_layout_legend.addWidget(self.label_legent_skip)
        self.__vbox_layout_legend.setAlignment(self.label_legent_skip, QtCore.Qt.AlignmentFlag.AlignLeft)

    def change_data_page_viewer_result_testing(self, data_page_viewer_result_testing: DataPageViewerResultTesting):
        self.__data_page_viewer_result_testing = data_page_viewer_result_testing

        self.__pie_slice_right.setBrush(self.__data_page_viewer_result_testing.color_right)
        self.__pie_slice_wrong.setBrush(self.__data_page_viewer_result_testing.color_wrong)
        self.__pie_slice_skip.setBrush(self.__data_page_viewer_result_testing.color_skip)

        self.label_legent_right.change_color(self.__data_page_viewer_result_testing.color_right)
        self.label_legent_wrong.change_color(self.__data_page_viewer_result_testing.color_wrong)
        self.label_legent_skip.change_color(self.__data_page_viewer_result_testing.color_skip)

class PageResultQuestion(QtWidgets.QWidget):
    """Класс для просмотра результата выполнения отдельного вопроса"""

    def __init__(self, number: int, path_course: str, question: str, answer: str | list | None, status: PageTesting.AnswerStatus, path_images: str):
        super().__init__()
        self.setObjectName("page_result_question")

        self.__number = number
        self.__path_course = path_course
        self.__question = question
        self.__answer = answer
        self.__status = status
        self.__path_images = path_images
        self.__path_pixmap = None

        if self.__question.find("type").text != "comparison_table":
            self.__rigth_answer = list(i.text for i in self.__question.findall("correct_answer"))
        else:
            self.__rigth_answer = list(element.text for element in self.__question.findall("row")[0].findall("correct_answer"))
        
        # главный макет
        self.__vbox_layout_main = QtWidgets.QGridLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__vbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__vbox_layout_main.addWidget(self.__frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(20, 20, 20, 20)

        self.__frame_main.setLayout(self.__vbox_layout_internal)

        # макет номера задания и статуса выполнения
        self.__hbox_layout_number_and_status = QtWidgets.QHBoxLayout()
        self.__hbox_layout_number_and_status.setSpacing(0)
        self.__hbox_layout_number_and_status.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_number_and_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.__vbox_layout_internal.addLayout(self.__hbox_layout_number_and_status)

        # метка номера задания
        self.__label_numder_question = QtWidgets.QLabel()
        self.__label_numder_question.setObjectName("label_numder_question")
        self.__label_numder_question.setFont(QtGui.QFont("Segoe UI", 12))
        self.__label_numder_question.setText(f"Вопрос {self.__number + 1}")

        self.__hbox_layout_number_and_status.addWidget(self.__label_numder_question)
        self.__hbox_layout_number_and_status.addSpacing(10)

        self.__label_status = QtWidgets.QLabel()
        self.__label_status.setObjectName("label_status")
        self.__label_status.setFont(QtGui.QFont("Segoe UI", 12))

        # метка статуса выполнения
        match self.__status:
            case PageTesting.AnswerStatus.right:
                text_status = "Верный ответ"
                self.__label_status.setProperty("status", "right")
            case PageTesting.AnswerStatus.wrong:
                text_status = "Неверный ответ"
                self.__label_status.setProperty("status", "wrong")
            case _:
                text_status = "Пропущено"
                self.__label_status.setProperty("status", "skip")

        self.__label_status.setText(text_status)

        self.__hbox_layout_number_and_status.addWidget(self.__label_status)

        # метка с вопросом
        self.__label_question = QtWidgets.QLabel()
        self.__label_question.setObjectName("label_question")
        self.__label_question.setWordWrap(True)
        self.__label_question.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_question.setText(self.__question.find("title").text)
        self.__label_question.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__vbox_layout_internal.addWidget(self.__label_question)

        # метка типа задания
        self.__label_type_question = QtWidgets.QLabel()
        self.__label_type_question.setObjectName("label_type_question")
        self.__label_type_question.setFont(QtGui.QFont("Segoe UI", 12))

        self.__vbox_layout_internal.addWidget(self.__label_type_question)
        self.__vbox_layout_internal.addSpacing(5)

        # добавление кнопки с изображением, если оно присутствует
        if (path_pixmap := self.__question.find("image")) is not None and path_pixmap.text != "None":
            self.__path_pixmap = os.path.join(os.path.split(self.__path_course)[0], path_pixmap.text) # .replace("\\", "/")

            self.__push_button_image = PageTesting.PushButtonImage(path_pixmap = self.__path_pixmap, path_images = self.__path_images)

            self.__vbox_layout_internal.addWidget(self.__push_button_image)
            self.__vbox_layout_internal.addSpacing(5)

        # метка верный ответ
        self.__label_right_answer = QtWidgets.QLabel()
        self.__label_right_answer.setObjectName("label_right_answer")
        self.__label_right_answer.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_right_answer.setText("Верный ответ:")

        self.__vbox_layout_internal.addWidget(self.__label_right_answer)

         # метка Ваш ответ
        self.__label_user_answer = QtWidgets.QLabel()
        self.__label_user_answer.setObjectName("label_user_answer")
        self.__label_user_answer.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_user_answer.setText("Ваш ответ:")

        # создание виджетов выбора или ввода ответов
        match self.__question.find("type").text:
            case "selectable_answer":
                self.__label_type_question.setText("Укажите правильный вариант ответа:")

                # группа радио кнопок
                self.__group_radio_buttons_rigth_answer = PageTesting.GroupRadiobuttonsAnswer()

                list_questions = self.__question.findall("answer_option")

                self.__list_radio_buttons_right_answer = list()

                # создание и упаковка радиокнопок верных ответов
                for i, question in enumerate(list_questions):
                    radio_button_right = PageTesting.RadioButtonAnswer(
                        text = question.text,
                        path_images = self.__path_images
                    )
                    radio_button_right.set_enabled(False)

                    self.__list_radio_buttons_right_answer.append(radio_button_right)

                    self.__group_radio_buttons_rigth_answer.add_radio_button_answer(radio_button_right)

                    if question.text == self.__rigth_answer[0]:
                        radio_button_right.set_checked(True)

                    self.__vbox_layout_internal.addWidget(radio_button_right)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)

                self.__vbox_layout_internal.addWidget(self.__label_user_answer)

                # группа радио кнопок
                self.__group_radio_buttons_user_answer = PageTesting.GroupRadiobuttonsAnswer()

                self.__list_radio_buttons_user_answer = list()

                 # создание и упаковка радиокнопок пользовательских ответов
                for i, question in enumerate(list_questions):
                    radio_button_user = PageTesting.RadioButtonAnswer(
                        text = question.text,
                        path_images = self.__path_images
                    )
                    radio_button_user.set_enabled(False)

                    self.__list_radio_buttons_user_answer.append(radio_button_user)

                    self.__group_radio_buttons_user_answer.add_radio_button_answer(radio_button_user)

                    if question.text == self.__answer:
                        radio_button_user.set_checked(True)

                    self.__vbox_layout_internal.addWidget(radio_button_user)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)

            case "multiple_selectable_answers":
                self.__label_type_question.setText("Укажите правильные варианты ответа:")

                list_questions = self.__question.findall("answer_option")

                self.__list_checkboxes_right = list()

                # создание и упаковка чекбоксов верных ответов
                for i, element in enumerate(list_questions):
                    checkbox_right = PageTesting.CheckboxAnswer(
                        text = element.text, 
                        path_images = self.__path_images
                    )
                    checkbox_right.set_enabled(False)

                    self.__list_checkboxes_right.append(checkbox_right)

                    if element.text in self.__rigth_answer:
                        checkbox_right.set_checked(True)

                    self.__vbox_layout_internal.addWidget(checkbox_right)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)

                self.__vbox_layout_internal.addWidget(self.__label_user_answer)

                self.__list_checkboxes_user = list()

                # создание и упаковка чекбоксов пользовательских ответов
                for i, element in enumerate(list_questions):
                    checkbox_user = PageTesting.CheckboxAnswer(
                        text = element.text, 
                        path_images = self.__path_images
                    )
                    checkbox_user.set_enabled(False)

                    self.__list_checkboxes_user.append(checkbox_user)

                    if element.text in self.__answer:
                        checkbox_user.set_checked(True)

                    self.__vbox_layout_internal.addWidget(checkbox_user)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)    
                    
            case "input_answer":
                self.__label_type_question.setText("Введите правильный ответ:")
                
                self.__line_edit_right_answer = PageTesting.LineEditAnswer()
                self.__line_edit_right_answer.set_enabled(False)

                self.__vbox_layout_internal.addWidget(self.__line_edit_right_answer)
                self.__vbox_layout_internal.addSpacing(5)

                self.__line_edit_right_answer.insert(self.__rigth_answer[0])

                self.__vbox_layout_internal.addWidget(self.__label_user_answer)

                self.__line_edit_user_answer = PageTesting.LineEditAnswer()
                self.__line_edit_user_answer.set_enabled(False)

                self.__vbox_layout_internal.addWidget(self.__line_edit_user_answer)

                if self.__answer is not None:
                    self.__line_edit_user_answer.insert(self.__answer)

            case "comparison_table":
                self.__label_type_question.setText("Заполните пустые ячейки таблицы:")

                list_headers = list(element.text for element in self.__question.findall("header"))

                # создание и упаковка таблицы верных ответов
                self.__table_right_answer = PageTesting.TableAnswer(list_headers)
                self.__table_right_answer.set_enabled(False)

                self.__vbox_layout_internal.addWidget(self.__table_right_answer)
                self.__vbox_layout_internal.addSpacing(5)

                self.__vbox_layout_internal.addWidget(self.__label_user_answer)

                for i_row, row in enumerate(self.__question.findall("row")):
                    count_cell_input = 0
                    for i_column, element in enumerate(row.findall("cell")):
                        type = PageTesting.TypeCellTableAnswer.label
                        match element.attrib["type"]:
                            case "label":
                                self.__table_right_answer.set_item(row = i_row, column = i_column, type = type, text = element.attrib["text"])
                            case "input":
                                self.__table_right_answer.set_item(row = i_row, column = i_column, type = type, text = row.findall("correct_answer")[count_cell_input].text)
                                count_cell_input += 1

                # создание и упаковка таблицы пользовательских ответов
                self.__table_user_answer = PageTesting.TableAnswer(list_headers)
                self.__table_user_answer.set_enabled(False)

                for i_row, row in enumerate(self.__question.findall("row")):
                    count_cell_input = 0
                    for i_column, element in enumerate(row.findall("cell")):
                        type = PageTesting.TypeCellTableAnswer.label
                        match element.attrib["type"]:
                            case "label":
                                self.__table_user_answer.set_item(row = i_row, column = i_column, type = type, text = element.attrib["text"])
                            case "input":
                                    if self.__answer != list():
                                        self.__table_user_answer.set_item(row = i_row, column = i_column, type = type, text = self.__answer[i_row][count_cell_input])
                                        count_cell_input += 1

                self.__vbox_layout_internal.addWidget(self.__table_user_answer)

        self.__vbox_layout_internal.addStretch(1)
        
class PageResultTesting(QtWidgets.QWidget):
    """Главный класс для просмотра результатов тестирования"""

    def __init__(self, data_result_testing: PageTesting.DataResultTesting, path_images: str, data_page_viewer_result_testing: DataPageViewerResultTesting):
        super().__init__()
        self.setObjectName("page_result_testing")

        self.__path_images = path_images
        self.__data_result_testing = data_result_testing
        self.__data_page_viewer_result_testing = data_page_viewer_result_testing

        self.__path_course = self.__data_result_testing.path_course
        self.__list_data_result = self.__data_result_testing.list_data_result

        self.__tree = ET.parse(self.__path_course)
        self.__root = self.__tree.getroot()

        self.__page_result_question = None
        self.__page_result_testing = None
        self.__current_number_page_result_question = 0

        self.__len_course = len(self.__root.findall("question"))
        self.__list_data_page_result_test: list[DataPageResultTest] = list()
        self.__list_push_button_questions = list()

        for i in range(self.__len_course):
            self.__list_data_page_result_test.append(DataPageResultTest())

        # главный макет
        self.__vbox_layout_main = QtWidgets.QGridLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__vbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__vbox_layout_main.addWidget(self.__frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.__frame_main.setLayout(self.__vbox_layout_internal)

        # виджет стеков для страниц результатов вопросов теста
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.__vbox_layout_internal.addWidget(self.__stacked_widget)

        # прокручиваемая область для станица результатов теста
        self.__scroll_area_page_result_test = QtWidgets.QScrollArea()
        self.__scroll_area_page_result_test.setObjectName("scroll_area_page_result_test")
        self.__scroll_area_page_result_test.setWidgetResizable(True)

        self.__stacked_widget.addWidget(self.__scroll_area_page_result_test)

        # панель инструментов
        self.__frame_tools = QtWidgets.QFrame()
        self.__frame_tools.setObjectName("frame_tools")
        
        self.__vbox_layout_internal.addWidget(self.__frame_tools)

        # макет панели инстументов
        self.__hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.__hbox_layout_tools.setSpacing(0)
        self.__hbox_layout_tools.setContentsMargins(20, 10, 20, 0)

        self.__frame_tools.setLayout(self.__hbox_layout_tools)

        # кнопка для открытия результатов тестирования
        self.__push_button_result_testing = PushButtonResultTesting(self.__path_images)
        self.__push_button_result_testing.push_button_result_testing_clicked.connect(self.__open_result_testing)

        self.__hbox_layout_tools.addWidget(self.__push_button_result_testing)
        self.__hbox_layout_tools.addSpacing(10)
        self.__hbox_layout_tools.setAlignment(self.__push_button_result_testing, QtCore.Qt.AlignmentFlag.AlignTop)

        # прокручиваемая область для кнопок навигации по вопросам
        self.__scroll_area_push_button_result_questions = QtWidgets.QScrollArea()
        self.__scroll_area_push_button_result_questions.setObjectName("scroll_area_push_button_result_questions")
        self.__scroll_area_push_button_result_questions.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__scroll_area_push_button_result_questions.verticalScrollBar().setEnabled(False)
        self.__scroll_area_push_button_result_questions.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scroll_area_push_button_result_questions.setWidgetResizable(True)

        self.__hbox_layout_tools.addWidget(self.__scroll_area_push_button_result_questions)
        self.__hbox_layout_tools.addSpacing(10)

        # рамка для кнопок навигации по вопросам
        self.__frame_push_button_result_questions = QtWidgets.QFrame()
        self.__frame_push_button_result_questions.setObjectName("frame_push_button_result_questions")

        self.__scroll_area_push_button_result_questions.setWidget(self.__frame_push_button_result_questions)

        # макет для кнопок навигации по вопросам
        self.__hbox_layout_push_button_result_questions = QtWidgets.QHBoxLayout()
        self.__hbox_layout_push_button_result_questions.setSpacing(0)
        self.__hbox_layout_push_button_result_questions.setContentsMargins(0, 0, 0, 0)

        self.__frame_push_button_result_questions.setLayout(self.__hbox_layout_push_button_result_questions)

        self.__hbox_layout_push_button_result_questions.addStretch(1)

        for i in range(self.__len_course):
            push_button_result_question = PushButtonResultQuestion(number = i)
            push_button_result_question.set_status(self.__list_data_result[i].status)
            push_button_result_question.push_button_question_clicked.connect(self.__switch_result_question)
            self.__list_push_button_questions.append(push_button_result_question)

            self.__hbox_layout_push_button_result_questions.addWidget(push_button_result_question)
            if i < self.__len_course:
                self.__hbox_layout_push_button_result_questions.addSpacing(10)

        self.__hbox_layout_push_button_result_questions.addStretch(1)

        self.__push_button_result_testing.push_button_navigation_press()

    def change_data_page_viewer_result_testing(self, data_page_viewer_result_testing: DataPageViewerResultTesting):
        self.__data_page_viewer_result_testing = data_page_viewer_result_testing
        self.__page_result_testing.change_data_page_viewer_result_testing(self.__data_page_viewer_result_testing)

    def __open_result_testing(self):
        if self.__page_result_testing is None:
            self.__page_result_testing = PageViewerResultTesting(self.__data_result_testing, self.__data_page_viewer_result_testing)
            self.__stacked_widget.addWidget(self.__page_result_testing)

        self.__stacked_widget.setCurrentWidget(self.__page_result_testing)

    def __switch_result_question(self, number: int):
        current_question = self.__root.findall("question")[number]

        if self.__page_result_question is not None:
            # сохранение информации о текущей страницы в список
            self.__list_data_page_result_test[self.__current_number_page_result_question].horizontal_scrollbar_value = self.__scroll_area_page_result_test.horizontalScrollBar().value()
            self.__list_data_page_result_test[self.__current_number_page_result_question].vertical__scrollbar_value = self.__scroll_area_page_result_test.verticalScrollBar().value()

            # удаление старой страницы
            self.__scroll_area_page_result_test.widget().deleteLater()

        self.__current_number_page_result_question = number

        # создание и упаковка новой страницы вопроса
        self.__page_result_question = PageResultQuestion(
            number = self.__current_number_page_result_question,
            path_course = self.__path_course, 
            question = current_question,
            answer = self.__list_data_result[self.__current_number_page_result_question].user_answer, 
            status = self.__list_data_result[self.__current_number_page_result_question].status,
            path_images = self.__path_images         
        )

        self.__scroll_area_page_result_test.setWidget(self.__page_result_question)
        self.__scroll_area_page_result_test.horizontalScrollBar().setValue(self.__list_data_page_result_test[self.__current_number_page_result_question].horizontal_scrollbar_value)
        self.__scroll_area_page_result_test.verticalScrollBar().setValue(self.__list_data_page_result_test[self.__current_number_page_result_question].vertical__scrollbar_value)
        self.__stacked_widget.setCurrentWidget(self.__scroll_area_page_result_test)
