from PyQt6 import QtCore, QtGui, QtWidgets
import os
import datetime
import xml.etree.ElementTree as ET
import re
import enum
from PIL import Image
from dataclasses import dataclass

from PyQt6.QtCore import QEvent, QObject
import Dialogs
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
import PageTesting

@dataclass
class DataPushButtonResultTesting:
    color_right: QtGui.QColor
    color_wrong: QtGui.QColor
    color_skip: QtGui.QColor

class ChartViewClicable(QChartView):
    """Кликабальный просмоторцик диаграмм"""
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self.clicked.emit()

        return super().mouseReleaseEvent(event)

class PushButtonResultTesting(QtWidgets.QFrame):
    """Класс для кнопок просмотра и открытия результатов тестирования"""
    push_button_result_testing_clicked = QtCore.pyqtSignal(PageTesting.DataResultTesting)
    
    def __init__(self, data_result_testing: PageTesting.DataResultTesting, data_push_button_result_testing: DataPushButtonResultTesting):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.installEventFilter(self)
        self.setObjectName("push_button_result_testing")

        self.__data_result_testing = data_result_testing
        self.__data_push_button_result_testing = data_push_button_result_testing

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

        self.__tree = ET.parse(self.__data_result_testing.path_course)
        self.__root = self.__tree.getroot()

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(10, 10, 10, 10)

        self.setLayout(self.__hbox_layout_main)

        # диаграмма
        self.__pie_series = QPieSeries()
        self.__pie_series.setHoleSize(0.4)

        self.__pie_slice_right = self.__pie_series.append("Правильные", round(self.__points_right / self.__amount_question * 100))
        self.__pie_slice_right.setBrush(self.__data_push_button_result_testing.color_right)

        self.__pie_slice_wrong = self.__pie_series.append("Неправильные", round(self.__points_wrong / self.__amount_question * 100))
        self.__pie_slice_wrong.setBrush(self.__data_push_button_result_testing.color_wrong)
        
        self.__pie_slice_skip = self.__pie_series.append("Пропущенные", round(self.__points_skip / self.__amount_question * 100))
        self.__pie_slice_skip.setBrush(self.__data_push_button_result_testing.color_skip)

        self.__chart = QChart()
        self.__chart.legend().hide()
        self.__chart.layout().setContentsMargins(0, 0, 0, 0)
        self.__chart.setBackgroundRoundness(0)
        self.__chart.setContentsMargins(-38, -38, -38, -38)
        self.__chart.addSeries(self.__pie_series)
        self.__chart.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.transparent))

        self.__chart__view = ChartViewClicable(self.__chart)
        self.__chart__view.setFixedSize(QtCore.QSize(85, 85))
        self.__chart__view.setObjectName("chart_view")
        self.__chart__view.clicked.connect(self.__push_button_result_testing_press)

        self.__hbox_layout_main.addWidget(self.__chart__view)
        self.__hbox_layout_main.addSpacing(10)

        # макет результата и названия теста
        self.__vbox_layout_info = QtWidgets.QVBoxLayout()
        self.__vbox_layout_info.setSpacing(0)
        self.__vbox_layout_info.setContentsMargins(0, 0, 0, 0)

        self.__hbox_layout_main.addLayout(self.__vbox_layout_info)
        self.__hbox_layout_main.addSpacing(10)

        # метка результата теста 
        self.__label_result = QtWidgets.QLabel()
        self.__label_result.setObjectName("label_result")
        self.__label_result.setText(f"Результат: {round(self.__points_right / self.__amount_question * 100)}% ({self.__points_right} / {self.__amount_question})")
        self.__label_result.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_result.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__vbox_layout_info.addWidget(self.__label_result)
        self.__vbox_layout_info.addSpacing(10)

        # метка названия теста
        name_test = self.__root.find("name").text
        self.__label_name_test = QtWidgets.QLabel()
        self.__label_name_test.setObjectName("label_name_test")
        self.__label_name_test.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_name_test.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__label_name_test.setText(f"Тест: {name_test[:40] + (name_test[40:] and '…')}")

        self.__vbox_layout_info.addWidget(self.__label_name_test)
        self.__vbox_layout_info.addSpacing(10)

        # метка даты прохождения
        self.__label_date_passing = QtWidgets.QLabel()
        self.__label_date_passing.setObjectName("label_date_passing")
        self.__label_date_passing.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_date_passing.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__label_date_passing.setText(f"Дата: {self.__data_result_testing.date_start.strftime(r'%d.%m.%Y %H:%M')}")

        self.__vbox_layout_info.addWidget(self.__label_date_passing)

        # метка подробнее
        self.__label_detail = QtWidgets.QLabel()
        self.__label_detail.setObjectName("label_detail")
        self.__label_detail.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_detail.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_detail.setText("Подробнее")
        self.__label_detail.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        self.__hbox_layout_main.addWidget(self.__label_detail)
        self.__hbox_layout_main.setAlignment(self.__label_detail, QtCore.Qt.AlignmentFlag.AlignRight)

    def __push_button_result_testing_press(self):
        self.push_button_result_testing_clicked.emit(self.__data_result_testing)

    def change_data_page_viewer_result_testing(self, data_push_button_result_testing: DataPushButtonResultTesting):
        self.__data_push_button_result_testing = data_push_button_result_testing

        self.__pie_slice_right.setBrush(self.__data_push_button_result_testing.color_right)
        self.__pie_slice_wrong.setBrush(self.__data_push_button_result_testing.color_wrong)
        self.__pie_slice_skip.setBrush(self.__data_push_button_result_testing.color_skip)

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            self.__push_button_result_testing_press()

        return super().eventFilter(obj, event)

class WidgetStub(QtWidgets.QFrame):
    """Виджет-заглушка"""

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.setObjectName("widget_stub")

        self.__pixmap = None
        self.__text = ""

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)
        self.__vbox_layout_main.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.__vbox_layout_main)

        # метка иконки
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__vbox_layout_main.addWidget(self.__label_icon)
        self.__vbox_layout_main.addSpacing(10)

        # метка с текстом
        self.__label_text = QtWidgets.QLabel()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 16))
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__vbox_layout_main.addWidget(self.__label_text)

    def set_pixmap(self, pixmap: QtGui.QPixmap):
        self.__pixmap = pixmap.scaled(QtCore.QSize(150, 150), aspectRatioMode = QtCore.Qt.AspectRatioMode.KeepAspectRatio, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)

        self.__label_icon.setPixmap(self.__pixmap)

    def set_text(self, text: str):
        self.__text = text

        self.__label_text.setText(self.__text)
        
class PageHistory(QtWidgets.QWidget):
    """Главный класс для просмотра истории результатов тестирования"""
    push_button_result_testing_clicked = QtCore.pyqtSignal(PageTesting.DataResultTesting)

    def __init__(self, list_data_result_testing: list[PageTesting.DataResultTesting], path_images: str, data_push_button_result_testing: DataPushButtonResultTesting):
        super().__init__()
        self.setObjectName("page_history")

        self.__path_images = path_images
        self.__list_data_result_testing = list_data_result_testing
        self.__data_push_button_result_testing = data_push_button_result_testing

        self.__widget_stub = None

        self.__list_push_button_result_testing: list[PushButtonResultTesting] = list()

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

        # прокручиваемая область для станица результатов теста
        self.__scroll_area_push_button_result_testing = QtWidgets.QScrollArea()
        self.__scroll_area_push_button_result_testing.setObjectName("scroll_area_push_button_result_testing")
        self.__scroll_area_push_button_result_testing.setWidgetResizable(True)
        self.__scroll_area_push_button_result_testing.horizontalScrollBar().setEnabled(False)
        self.__scroll_area_push_button_result_testing.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scroll_area_push_button_result_testing.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)

        self.__vbox_layout_internal.addWidget(self.__scroll_area_push_button_result_testing)

        # рамка для кнопок просмотра и открытия результатов тестирования
        self.__frame_push_button_result_testing = QtWidgets.QFrame()
        self.__frame_push_button_result_testing.setObjectName("frame_push_button_result_testing")

        self.__scroll_area_push_button_result_testing.setWidget(self.__frame_push_button_result_testing)

        # макет для кнопок просмотра и открытия результатов тестирования
        self.__vbox_layout_push_button_result_testing = QtWidgets.QVBoxLayout()
        self.__vbox_layout_push_button_result_testing.setSpacing(0)
        self.__vbox_layout_push_button_result_testing.setContentsMargins(5, 5, 5, 0)
        self.__vbox_layout_push_button_result_testing.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.__frame_push_button_result_testing.setLayout(self.__vbox_layout_push_button_result_testing)

        amount_results = len(self.__list_data_result_testing)
        if amount_results > 0:
            for i, element in enumerate(self.__list_data_result_testing):
                push_button_result_testing = PushButtonResultTesting(data_result_testing = element, data_push_button_result_testing = self.__data_push_button_result_testing)
                push_button_result_testing.push_button_result_testing_clicked.connect(self.__push_button_result_testing_press)
                self.__list_push_button_result_testing.append(push_button_result_testing)
                
                self.__vbox_layout_push_button_result_testing.insertWidget(0, push_button_result_testing)

                if i < amount_results:
                    self.__vbox_layout_push_button_result_testing.insertSpacing(1, 5)
        else:
            self.__widget_stub = WidgetStub()
            self.__widget_stub.set_pixmap(QtGui.QPixmap(os.path.join(self.__path_images, r"box_empty.png")))
            self.__widget_stub.set_text("Пока еще нет результатов тестирования")

            self.__vbox_layout_push_button_result_testing.addWidget(self.__widget_stub)

    def showEvent(self, event: QtGui.QShowEvent):
        self.__scroll_area_push_button_result_testing.setMinimumWidth(self.__frame_push_button_result_testing.sizeHint().width() + 5 + 14)

        super().showEvent(event)

    def change_data_push_button_result_testing(self, data_push_button_result_testing: DataPushButtonResultTesting):
        self.__data_push_button_result_testing = data_push_button_result_testing

        for i in self.__list_push_button_result_testing:
            i.change_data_page_viewer_result_testing(self.__data_push_button_result_testing)

    def __push_button_result_testing_press(self, data_result_testing: PageTesting.DataResultTesting):
        self.push_button_result_testing_clicked.emit(data_result_testing)

    def update_list_data_result_testing(self, list_data_result_testing: list[PageTesting.DataResultTesting]):
        self.__list_data_result_testing = list_data_result_testing

        for i in self.__list_push_button_result_testing:
            i.deleteLater()

        self.__list_push_button_result_testing = list()

        amount_results = len(self.__list_data_result_testing)
        if amount_results > 0:
            for i, element in enumerate(self.__list_data_result_testing):
                push_button_result_testing = PushButtonResultTesting(data_result_testing = element, data_push_button_result_testing = self.__data_push_button_result_testing)
                push_button_result_testing.push_button_result_testing_clicked.connect(self.__push_button_result_testing_press)
                self.__list_push_button_result_testing.append(push_button_result_testing)
                
                self.__vbox_layout_push_button_result_testing.insertWidget(0, push_button_result_testing)

                if i < amount_results:
                    self.__vbox_layout_push_button_result_testing.insertSpacing(1, 5)
        else:
            self.__widget_stub = WidgetStub()
            self.__widget_stub.set_pixmap(QtGui.QPixmap(os.path.join(self.__path_images, r"box_empty.png")))
            self.__widget_stub.set_text("Пока еще нет результатов тестирования")

            self.__vbox_layout_push_button_result_testing.addWidget(self.__widget_stub)
