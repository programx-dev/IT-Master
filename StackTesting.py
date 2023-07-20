from PyQt6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import os
import datetime
import xml.etree.ElementTree as ET
import re
import enum
from PIL import Image
from dataclasses import dataclass
import Dialogs

__parent__ = None

@enum.unique
class AnswerStatus(enum.Enum):
    wrong = 0
    skip = 1
    right = 2

@dataclass
class DataResult:
    status: AnswerStatus
    user_answer: str | list | None
    right_answer: str | list

@dataclass
class DataPassage:
    date_start: datetime.datetime
    date_end: datetime.datetime
    list_data_result: list[DataResult]

@dataclass
class DataPageTest:
    answer: str | list | None
    horizontal_scrollbar_value: int = 0
    vertical__scrollbar_value: int = 0

class PushButtonNavigation(QtWidgets.QPushButton):
    """Базовый класс для кнопок навигации на панели инструменов"""
    push_button_navigation_current = None
    push_button_navigation_change_current = QtCore.pyqtSignal()
    push_button_navigation_clicked = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.__current = False 

        self.setObjectName("push_button_navigation")
        self.setFixedSize(50, 50)
        self.clicked.connect(self.push_button_navigation_press)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

    def push_button_navigation_press(self):
        if self != PushButtonNavigation.push_button_navigation_current and PushButtonNavigation.push_button_navigation_current != None:
            PushButtonNavigation.push_button_navigation_current.__set_current(False)

        if self != PushButtonNavigation.push_button_navigation_current:
            PushButtonNavigation.push_button_navigation_current = self
            self.__set_current(True)

            self.push_button_navigation_clicked.emit()

    def __set_current(self, state: bool):
        self.__current = state

        self.setProperty("current", self.current())
        self.style().unpolish(self)
        self.style().polish(self)

        self.push_button_navigation_change_current.emit()
    
    def current(self) -> bool:
        return self.__current

class PushButtonQuestion(PushButtonNavigation):
    """Класс для кнопок навигации по вопросам на панели инструменов"""
    push_button_question_clicked = QtCore.pyqtSignal(int)
    
    def __init__(self, number: int, data_theme: dict):
        super().__init__()

        self.__number = number
        self.__data_theme = data_theme
        self.__answered = False

        self.setObjectName("push_button_question")
        self.setText(f"{self.__number + 1}")
        self.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_navigation_clicked.connect(self.__push_button_question_press)
        self.setProperty("current", self.current())
        self.setProperty("answered", self.answered())

        self.set_style_sheet()

    def __push_button_question_press(self):
        self.push_button_question_clicked.emit(self.__number)

    def set_answered(self, state: bool):
        self.__answered = state

        self.setProperty("answered", self.answered())
        self.style().unpolish(self)
        self.style().polish(self)
    
    def answered(self) -> bool:
        return self.__answered

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #push_button_question[current="true"][answered="true"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 25px;
            background: {self.__data_theme["current"]["answered"]["background"]};
            border-color: {self.__data_theme["current"]["answered"]["color_border"]};
            color: {self.__data_theme["current"]["answered"]["color"]};
        }} 
        #push_button_question[current="true"][answered="false"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 25px;
            background: {self.__data_theme["current"]["not_answered"]["background"]};
            border-color: {self.__data_theme["current"]["not_answered"]["color_border"]};
            color: {self.__data_theme["current"]["not_answered"]["color"]};
        }} 
        #push_button_question[current="false"][answered="true"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 25px;
            background: {self.__data_theme["not_current"]["answered"]["background"]};
            border-color: {self.__data_theme["not_current"]["answered"]["color_border"]};
            color: {self.__data_theme["not_current"]["answered"]["color"]};
        }} 
        #push_button_question[current="false"][answered="false"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 25px;
            background: {self.__data_theme["not_current"]["not_answered"]["background"]};
            border-color: {self.__data_theme["not_current"]["not_answered"]["color_border"]};
            color: {self.__data_theme["not_current"]["not_answered"]["color"]};
        }} """)

class PushButtonLesson(PushButtonNavigation):
    """Класс для кнопки теоретической части на панели инструменов"""
    push_button_lesson_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme

        self.setObjectName("push_button_lesson")
        self.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"lesson.png")))
        self.setIconSize(QtCore.QSize(35, 35))
        self.push_button_navigation_clicked.connect(self.__push_button_lesson_press)
        self.setProperty("current", self.current())

        self.set_style_sheet()

    def __push_button_lesson_press(self):
        self.push_button_lesson_clicked.emit()

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #push_button_lesson[current="true"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 10px;
            background: {self.__data_theme["current"]["background"]};
            border-color: {self.__data_theme["current"]["color_border"]};
            color: {self.__data_theme["current"]["color"]};
        }} 
        #push_button_lesson[current="false"] {{
            outline: 0;
            border: 3px solid;
            border-radius: 10px;
            background: {self.__data_theme["not_current"]["background"]};
            border-color: {self.__data_theme["not_current"]["color_border"]};
            color: {self.__data_theme["not_current"]["color"]};
        }} """)

class LessonViewer(QtWebEngineWidgets.QWebEngineView):
    """Класс просмотра уроков в формате .pdf"""

    def __init__(self, path_lesson: str):
        super().__init__()

        self.__path_lesson = path_lesson

        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(self.settings().WebAttribute.PdfViewerEnabled, True)

        self.setUrl(QtCore.QUrl.fromLocalFile(self.__path_lesson))

class LabelPromt(QtWidgets.QFrame):
    """Метка с подсказкой"""
    
    def __init__(self, promt: str, path_image: str, data_theme: dict):
        super().__init__()

        self.setObjectName("label_promt")

        self.__promt = promt
        self.__path_image = path_image
        self.__data_theme = data_theme

        self.__pixmap = QtGui.QPixmap(self.__path_image).scaled(18, 18, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # метка с полоской
        self.__label_line = QtWidgets.QLabel()
        self.__label_line.setObjectName("label_line")
        self.__label_line.setFixedSize(4, 30)
        
        self.__hbox_layout_main.addWidget(self.__label_line)
        self.__hbox_layout_main.addSpacing(10)

        # метка с иконкой
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setPixmap(self.__pixmap )
        
        self.__hbox_layout_main.addWidget(self.__label_icon)
        self.__hbox_layout_main.addSpacing(10)

        # метка с текстом
        self.__label_text = QtWidgets.QLabel()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__promt)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 12))
        self.__label_text.setFixedHeight(25)
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.__hbox_layout_main.addWidget(self.__label_text)

        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #label_promt {{
            background: #FFF7A0;
            border-radius: 3px;
        }} """)

        # метка с полоской
        self.__label_line.setStyleSheet(f"""
        #label_line {{
            background: #FFB200;
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
        }} """)

        # метка с иконкой
        self.__label_icon.setStyleSheet(f"""
        #label_text {{
            background: transparent;
        }} """)

        # метка с текстом
        self.__label_text.setStyleSheet(f"""
        #label_text {{
            background: transparent;
            color: #000000;
        }} """)

class LabelClickable(QtWidgets.QLabel):
    """Класс для кликабельной метки"""
    clicked = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit(event)

        return super().mouseReleaseEvent(event)

class CheckboxAnswer(QtWidgets.QWidget):
    """Класс для чекбоксов для ответов с возможностью переноса слов"""
    checkbox_answer_state_changed = QtCore.pyqtSignal(bool)

    def __init__(self, text: str, path_images: str, data_theme: dict):
        super().__init__()
        self.setFixedHeight(32)

        self.__text = text
        self.__data_theme = data_theme
        self.__path_images = path_images
        self.__checked = False

        self.__image_checked = QtGui.QIcon(os.path.join(self.__path_images, "checkbox_checked.png"))
        self.__image_unchecked = QtGui.QIcon(os.path.join(self.__path_images, "checkbox_unchecked.png"))        

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # кнопка с флажком
        self.__push_button_flag = QtWidgets.QPushButton()
        self.__push_button_flag.setObjectName("push_button_flag")
        self.__push_button_flag.clicked.connect(self.__checkbox_clicked)
        self.__push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__push_button_flag.setFixedHeight(25)
        self.__push_button_flag.setIconSize(QtCore.QSize(22, 22))

        self.__hbox_layout_main.addWidget(self.__push_button_flag)
        self.__hbox_layout_main.addSpacing(5)

        # кликабельная метка c текстом
        self.__label_text = LabelClickable()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__text)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_text.setFixedHeight(25)
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__label_text.clicked.connect(self.__checkbox_clicked)
        # self.__label_text.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__hbox_layout_main.addWidget(self.__label_text)

        self.set_style_sheet()

        self.set_checked(checked = False)

    def is_checked(self) -> bool:
        return self.__checked

    def text(self) -> str:
        return self.__text

    def __checkbox_clicked(self):
        if self.__checked == True:
            self.set_checked(checked = False)
        else:
            self.set_checked(checked = True)

    def set_checked(self, checked: bool):
        if checked == True:
            self.__checked = True

            self.__push_button_flag.setIcon(self.__image_checked)

        elif checked == False:
            self.__checked = False

            self.__push_button_flag.setIcon(self.__image_unchecked)

        self.checkbox_answer_state_changed.emit(checked)

    def set_style_sheet(self):
        # кнопка с флажком
        self.__push_button_flag.setStyleSheet(f"""
        #push_button_flag {{
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
            outline: 0;
            border: none;
            background: transparent;
        }}
        #push_button_flag[hover="true"] {{
            background: #CCE8FF;
        }} """)#  % self.__data_theme

        # кликабельная метка c текстом
        self.__label_text.setStyleSheet(f"""
        #label_text {{
            padding-left: 5px;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background: transparent;
            color: #000000;
        }}
        #label_text[hover="true"] {{
            background: #CCE8FF;
        }} """)#  % self.__data_theme

class RadiobuttonAnswer(QtWidgets.QWidget):
    """Класс для радиокнопок для ответов с возможностью переноса слов"""
    radio_button_answer_toggled = QtCore.pyqtSignal(bool)

    def __init__(self, text: str, path_images: str, data_theme: dict):
        super().__init__()
        self.setFixedHeight(32)

        self.__text = text
        self.__data_theme = data_theme
        self.__path_images = path_images

        self.__checked = False

        self.__image_checked = QtGui.QIcon(os.path.join(self.__path_images, "radio_button_checked.png"))
        self.__image_unchecked = QtGui.QIcon(os.path.join(self.__path_images, "radio_button_unchecked.png"))

        # главный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # кнопка с флажком
        self.__push_button_flag = QtWidgets.QPushButton()
        self.__push_button_flag.setObjectName("push_button_flag")
        self.__push_button_flag.clicked.connect(self.__radio_button_clicked)
        self.__push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__push_button_flag.setIconSize(QtCore.QSize(22, 22))

        self.__hbox_layout_main.addWidget(self.__push_button_flag)

        # кликабельная метка c текстом
        self.__label_text = LabelClickable()
        self.__label_text.setObjectName("label_text")
        self.__label_text.setText(self.__text)
        self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.__label_text.clicked.connect(self.__radio_button_clicked)
        # self.__label_text.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__hbox_layout_main.addWidget(self.__label_text)

        self.set_style_sheet()

        self.set_checked(checked = False)

    def text(self) -> str:
        return self.__text

    def is_checked(self) -> bool:
        return self.__checked

    def __radio_button_clicked(self):
        if self.__checked == False:
            self.set_checked(checked = True)

    def enterEvent(self, event: QtGui.QEnterEvent):
        self.__push_button_flag.setProperty("hover", True)
        self.__push_button_flag.style().unpolish(self.__push_button_flag)
        self.__push_button_flag.style().polish(self.__push_button_flag)

        self.__label_text.setProperty("hover", True)
        self.__label_text.style().unpolish(self.__label_text)
        self.__label_text.style().polish(self.__label_text)

        return super().enterEvent(event)

    def leaveEvent(self, event: QtGui.QEnterEvent):
        self.__push_button_flag.setProperty("hover", False)
        self.__push_button_flag.style().unpolish(self.__push_button_flag)
        self.__push_button_flag.style().polish(self.__push_button_flag)

        self.__label_text.setProperty("hover", False)
        self.__label_text.style().unpolish(self.__label_text)
        self.__label_text.style().polish(self.__label_text)

        return super().leaveEvent(event)

    def set_checked(self, checked: bool):
        if checked == True:
            self.__checked = True

            self.__push_button_flag.setIcon(self.__image_checked)
        elif checked == False:
            self.__checked = False

            self.__push_button_flag.setIcon(self.__image_unchecked)

        self.radio_button_answer_toggled.emit(checked)

    def set_style_sheet(self):
        # кнопка с флажком
        self.__push_button_flag.setStyleSheet(f"""
        #push_button_flag {{
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
            outline: 0;
            border: none;
            background: transparent;
        }}
        #push_button_flag[hover="true"] {{
            background: #CCE8FF;
        }} """)#  % self.__data_theme

        # кликабельная метка c текстом
        self.__label_text.setStyleSheet(f"""
        #label_text {{
            padding-left: 5px;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background: transparent;
            color: #000000;
        }}
        #label_text[hover="true"] {{
            background: #CCE8FF;
        }} """)#  % self.__data_theme

class GroupRadiobuttonsAnswer(QtCore.QObject):
    """Класс для группирования RadiobuttonAnswer"""
    radio_button_checked = QtCore.pyqtSignal(RadiobuttonAnswer)
    
    def __init__(self):
        super().__init__()

        self.__list_radio_buttons = []
        self.__checked_radio_button = None

    def __toggle_radio_button_answer(self):
        radio_button = self.sender()

        if radio_button.is_checked() and self.__checked_radio_button != radio_button:
            if self.__checked_radio_button !=  None:
                self.__checked_radio_button.set_checked(checked = False)
            self.__checked_radio_button = radio_button

            self.radio_button_checked.emit(self.__checked_radio_button)

    def add_radio_button_answer(self, radio_button: RadiobuttonAnswer):
        radio_button.radio_button_answer_toggled.connect(self.__toggle_radio_button_answer)
        self.__list_radio_buttons.append(radio_button)

class PushButtonImage(QtWidgets.QPushButton):
    """Класс для кнопки с изображением"""
    push_button_image_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_pixmap: str, path_images: str, data_theme: dict):
        super().__init__()

        self.setObjectName("push_button_image")
        # self.clicked.connect(self.__push_button_image_press)
        # self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.__path_pixmap = path_pixmap
        self.__path_images = path_images
        self.__data_theme = data_theme

        self.__min_size = QtCore.QSize(93, 93)
        self.__max_size = QtCore.QSize(393, 393)

        self.__pixmap = QtGui.QPixmap(self.__path_pixmap)

        zoom = 1

        if self.__pixmap.width() < self.__min_size.width() or self.__pixmap.height()  < self.__min_size.height():
            zoom = max(self.__min_size.width() / self.__pixmap.width(), self.__min_size.height() / self.__pixmap.height())
        if  self.__pixmap.width() > self.__max_size.width() or self.__pixmap.height()  > self.__max_size.height():
            zoom = min(self.__max_size.width() / self.__pixmap.width(), self.__max_size.height() / self.__pixmap.height())

        self.__pixmap = self.__pixmap.scaled(round(self.__pixmap.width() * zoom), round(self.__pixmap.height() * zoom), transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
        
        self.__target = QtGui.QPixmap(self.__pixmap.size())  
        self.__target.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(self.__target)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)

        painter_path = QtGui.QPainterPath()
        painter_path.addRoundedRect(0, 0, self.__pixmap.width(), self.__pixmap.height(), 14, 14)

        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, self.__pixmap)
        painter.end()

        self.__image = QtGui.QIcon(self.__target)

        self.setIcon(self.__image)
        self.setIconSize(self.__target.size())
        self.setFixedSize(max(self.__target.width(), self.__min_size.width()) + 2, max(self.__target.height(), self.__min_size.height()) + 2)

        # макет для кнопки сохранить изображение
        self.__grid_layout_push_button_save = QtWidgets.QGridLayout()
        self.__grid_layout_push_button_save.setSpacing(0)
        self.__grid_layout_push_button_save.setContentsMargins(0, 0, 0, 0)
        self.__grid_layout_push_button_save.setColumnStretch(0, 1)
        self.__grid_layout_push_button_save.setColumnStretch(1, 0)
        self.__grid_layout_push_button_save.setRowStretch(0, 0)
        self.__grid_layout_push_button_save.setRowStretch(1, 1)

        self.setLayout(self.__grid_layout_push_button_save)

        # кнопка сохранить изображение
        self.__push_buttton_save_image = QtWidgets.QPushButton()
        self.__push_buttton_save_image.setObjectName("push_buttton_save_image")
        self.__push_buttton_save_image.clicked.connect(self.__save_image_as)
        self.__push_buttton_save_image.setFixedSize(40, 40)
        self.__push_buttton_save_image.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"save.png")))
        self.__push_buttton_save_image.setIconSize(QtCore.QSize(32, 32))

        self.__push_buttton_save_image.hide()
        self.__grid_layout_push_button_save.addWidget(self.__push_buttton_save_image, 0, 1)
        
        self.set_style_sheet()

    def __push_button_image_press(self):
        self.push_button_image_clicked.emit()

    def enterEvent(self, event):
        self.__push_buttton_save_image.setVisible(True)

    def leaveEvent(self, event):
        self.__push_buttton_save_image.setVisible(False)

    def __save_image_as(self):
        directory_desktop = os.path.abspath(os.path.normpath(os.path.join(os.environ["HOMEPATH"], "Desktop")))
        file_formats = ["jpg", "jpeg", "jpe", "png", "tif", "tiff", "bmp"]
        extension_pixmap = os.path.splitext(self.__path_pixmap)[1][1:]
        if extension_pixmap in file_formats:
            file_formats.remove(extension_pixmap)
        file_formats.insert(0, extension_pixmap)
        file_formats = ";;".join([f".{i} (*.{i})" for i in file_formats])

        path_image, filter = QtWidgets.QFileDialog.getSaveFileName(
            __parent__, 
            "Сохранение изображения", 
            os.path.join(directory_desktop, os.path.basename(self.__path_pixmap)),
            file_formats,
            f".{extension_pixmap}"
        )

        if path_image:
            try:
                # selected_extension_file = re.search("\.\w+ \(\*\.(\w+)\)", filter).group(1)
                # if not re.match(f"^(.+?)\.{selected_extension_file}$", path_image):
                #     path_image = f"{os.path.normpath(path_image)}.{selected_extension_file}"

                pixmap = Image.open(self.__path_pixmap)
                pixmap.save(path_image)
            except Exception as error:
                msg = QtWidgets.QMessageBox(__parent__)
                msg.setWindowTitle("Ошибка")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msg.setText("Неудалось сохранить изображение")
                msg.setInformativeText(str(error))
                msg.exec()
       
    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #push_button_image {{
            outline: 0;
            border-radius: 14px;
            border-style: solid;
            border-width: 1px;
            border-color: #888888;
            background: transparent; 
        }} """)#  % self.__data_theme

        self.__push_buttton_save_image.setStyleSheet(f"""
        #push_buttton_save_image {{
            outline: 0;
            border-radius: 14px; 
            background: transparent; 
        }} """)

class PageTest(QtWidgets.QWidget):
    """Класс для страницы с вопросом"""
    answer_changed = QtCore.pyqtSignal(int, bool)

    def __init__(self, number: int, path_course: str, question: str, answer: str | list | None, started_passing: bool, icon_dialogs: QtGui.QPixmap, path_images: str, data_theme: dict):
        super().__init__()

        self.__number = number
        self.__path_course = path_course
        self.__question = question
        self.__answer = answer
        self.__started_passing = started_passing
        self.__icon_dialogs = icon_dialogs
        self.__path_images = path_images
        self.__path_pixmap = None
        self.__data_theme = data_theme
        
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

        # метка номера задания
        self.__label_numder_question = QtWidgets.QLabel()
        self.__label_numder_question.setObjectName("label_numder_question")
        self.__label_numder_question.setFont(QtGui.QFont("Segoe UI", 12))
        self.__label_numder_question.setText(f"Вопрос {self.__number + 1}")

        self.__vbox_layout_internal.addWidget(self.__label_numder_question)

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
        if (path_pixmap := self.__question.find("questions").find("image")) != None:
            self.__path_pixmap = os.path.join(os.path.split(self.__path_course)[0], path_pixmap.text) # .replace("\\", "/")

            self.__push_button_image = PushButtonImage(path_pixmap = self.__path_pixmap, path_images = self.__path_images, data_theme = self.__data_theme["frame_main"]["push_button_image"])
            self.__push_button_image.push_button_image_clicked.connect(self.__show_image)

            self.__vbox_layout_internal.addWidget(self.__push_button_image)
            self.__vbox_layout_internal.addSpacing(5)

        # создание виджетов выбора или ввода ответов
        match self.__question.find("questions").find("type").text:
            case "radio_button":
                self.__label_type_question.setText("Укажите правильный вариант ответа:")

                # группа радио кнопок
                self.__group_radio_buttons = GroupRadiobuttonsAnswer()

                list_questions = self.__question.find("questions").findall("question")
                amount_questions = len(list_questions)

                self.__list_radio_buttons = list()

                # создание и упаковка радиокнопок
                for i, question in enumerate(list_questions):
                    radio_button = RadiobuttonAnswer(
                        text = question.text,
                        path_images = self.__path_images,
                        data_theme = self.__data_theme["frame_main"]["radio_button"]
                    )

                    self.__list_radio_buttons.append(radio_button)

                    self.__group_radio_buttons.add_radio_button_answer(radio_button)
                    self.__group_radio_buttons.radio_button_checked.connect(self.__radio_button_checked)

                    if self.__started_passing and question.text == self.__answer:
                        radio_button.set_checked(True)

                    self.__vbox_layout_internal.addWidget(radio_button)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)

            case "checkbox":
                self.__label_type_question.setText("Укажите правильные варианты ответа:")

                list_questions = self.__question.find("questions").findall("question")
                amount_questions = len(list_questions)

                self.__list_checkboxes = list()

                # создание и упаковка радиокнопок
                for i, element in enumerate(list_questions):
                    checkbox = CheckboxAnswer(
                        text = element.text, 
                        path_images = self.__path_images, 
                        data_theme = self.__data_theme["frame_main"]["checkbox"]
                    )

                    self.__list_checkboxes.append(checkbox)

                    checkbox.checkbox_answer_state_changed.connect(self.__ceckbox_checked)

                    if self.__started_passing and element.text in self.__answer:
                        checkbox.set_checked(True)

                    self.__vbox_layout_internal.addWidget(checkbox)
                    # if i < amount_questions:
                    #     self.__vbox_layout_internal.addSpacing(10)
                    
            case "input":
                self.__label_type_question.setText("Введите правильный ответ:")
                
                self.__line_edit_answer = QtWidgets.QLineEdit()
                self.__line_edit_answer.setObjectName("line_edit_answer")
                self.__line_edit_answer.textChanged.connect(self.__line_edit_text_changed)
                self.__line_edit_answer.setFont(QtGui.QFont("Segoe UI", 14))
                self.__line_edit_answer.setFixedHeight(42)

                self.__vbox_layout_internal.addWidget(self.__line_edit_answer)
                self.__vbox_layout_internal.addSpacing(5)

                # метка с подсказкой
                self.__label_promt = LabelPromt(
                    "Для записи десятичных дробей используется запятая, а не точка.",
                    os.path.join(self.__path_images, "warning.png"),
                    self.__data_theme
                )
                self.__label_promt.hide()

                self.__vbox_layout_internal.addWidget(self.__label_promt)

                if self.__started_passing:
                    self.__line_edit_answer.insert(self.__answer)

                temp_data_theme = {
                "color_border_not_focus": self.__data_theme["frame_main"]["line_edit"]["not_focus"]["color_border"],
                "background_not_focus": self.__data_theme["frame_main"]["line_edit"]["not_focus"]["background"], 
                "color_not_focus": self.__data_theme["frame_main"]["line_edit"]["not_focus"]["color"], 
                "color_border_focus": self.__data_theme["frame_main"]["line_edit"]["focus"]["color_border"],
                "background_focus": self.__data_theme["frame_main"]["line_edit"]["focus"]["background"], 
                "color_focus": self.__data_theme["frame_main"]["line_edit"]["focus"]["color"]
                }

                self.__line_edit_answer.setStyleSheet("""
                #line_edit_answer {
                    border-radius: 7px; 
                    border: 2px solid; 
                    border-color: %(color_border_not_focus)s;
                    background: %(background_not_focus)s; 
                    color: %(color_not_focus)s;
                } 
                #line_edit_answer:focus {
                    border-color: %(color_border_focus)s;
                    background: %(background_focus)s; 
                    color: %(color_focus)s;
                } """ % temp_data_theme)

        self.__vbox_layout_internal.addStretch(1)
        
        self.set_style_sheet()

    def answer(self) -> str | list | None:
        return self.__answer

    def __show_image(self):
        self.__dialog_image = Dialogs.DialogImage(
            path_image = self.__path_pixmap,
            data_theme = self.__data_theme["frame_main"]["dialog_image"]
        )
        self.__dialog_image.set_icon(icon = self.__icon_dialogs)
        self.__dialog_image.set_title(title = "Изображение")

        self.__dialog_image.load_lesson()

    def __radio_button_checked(self, radio_button: RadiobuttonAnswer):
        self.__answer = radio_button.text()

        self.answer_changed.emit(self.__number, True)

    def __ceckbox_checked(self):
        text_sender = self.sender().text()

        if self.sender().is_checked() and text_sender not in self.__answer:
            self.__answer.append(text_sender)
            self.answer_changed.emit(self.__number, True if len(self.__answer) != 0 else False)
        elif not self.sender().is_checked() and text_sender in self.__answer:
            self.__answer.remove(text_sender)
            self.answer_changed.emit(self.__number, True if len(self.__answer) != 0 else False)

    def __line_edit_text_changed(self):
        self.__answer = self.__line_edit_answer.text()

        if re.search("(\d\.)", self.__answer):
            self.__label_promt.show()
        else:
            self.__label_promt.hide()

        self.answer_changed.emit(self.__number, True if self.__answer != "" else False)

    def set_style_sheet(self):
        # главная рамка
        self.__frame_main.setStyleSheet(f"""
        #frame_main {{
            background: #FFFFFF;
        }} """)# % self.__data_theme["frame_main"]

        # метка вопроса
        self.__label_question.setStyleSheet(f"""
        #label_question {{
            color: #000000;
            background: transparent;
            selection-color: #FFFFFF;
            selection-background-color: #3087EF;
        }} """) #  % self.__data_theme["frame_main"]["label_question"]

        # метка номера вопроса
        self.__label_numder_question.setStyleSheet(f"""
        #label_numder_question {{
            color: #9E9E9E;   
        }} """)# % self.__data_theme["frame_main"]["label_numder_question"]

        # метка типа задания
        self.__label_type_question.setStyleSheet(f"""
        #label_type_question {{ 
            color: #9E9E9E;
        }} """)# % self.__data_theme["frame_main"]["label_type_question"]

class StackTesting(QtWidgets.QWidget):
    """Главный класс тестирования"""
    push_button_finish_cliced = QtCore.pyqtSignal(DataPassage)

    def __init__(self, path_course: str, path_images: str, icon_dialogs: QtGui.QPixmap, data_theme: dict):
        super().__init__()

        self.__data_theme = data_theme
        self.__path_images = path_images
        self.__path_course = path_course
        self.__icon_dialogs = icon_dialogs
        self.__path_lesson = None

        self.__tree = ET.parse(self.__path_course)
        self.__root = self.__tree.getroot()

        lesson = self.__root.find("lesson")
        if lesson != None:
            self.__path_lesson = os.path.abspath(os.path.join(os.path.split(self.__path_course)[0], lesson.text))
        
        self.__page_question = None
        self.__page_lesson = None
        self.__current_number_question = 0

        self.__time_start = datetime.datetime.now()
        self.__len_course = len(self.__root.findall("exercise"))
        self.__list_answers = list()
        self.__list_data_page_test: list[DataPageTest] = list()
        self.__list_push_button_questions = list()
        self.__dict_questions_started_passing = {i: False for i in range(self.__len_course)}

        for i in range(self.__len_course):
            type_question = self.__root.findall("exercise")[i].find("questions").find("type").text
            if type_question == "checkbox":
                self.__list_data_page_test.append(DataPageTest(list()))
            elif type_question in ("radio_button", "input"):
                self.__list_data_page_test.append(DataPageTest(None))

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

        # виджет стеков для страниц вопросов теста
        self.__stacked_widget = QtWidgets.QStackedWidget()
        self.__stacked_widget.setObjectName("stacked_widget")

        self.__vbox_layout_internal.addWidget(self.__stacked_widget)

        # прокручиваемая область для станица теста
        self.__scroll_area_page_test = QtWidgets.QScrollArea()
        self.__scroll_area_page_test.setObjectName("scroll_area_page_test")
        self.__scroll_area_page_test.setWidgetResizable(True)

        self.__stacked_widget.addWidget(self.__scroll_area_page_test)

        # панель инструментов
        self.__frame_tools = QtWidgets.QFrame()
        self.__frame_tools.setObjectName("frame_tools")
        
        self.__vbox_layout_internal.addWidget(self.__frame_tools)

        # макет панели инстументов
        self.__hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.__hbox_layout_tools.setSpacing(0)
        self.__hbox_layout_tools.setContentsMargins(20, 10, 20, 0)

        self.__frame_tools.setLayout(self.__hbox_layout_tools)

        if self.__path_lesson:
            # кнопка для открытия урока в формате .pdf
            self.__push_button_lesson = PushButtonLesson(self.__path_images, self.__data_theme["frame_main"]["frame_tools"]["push_button_lesson"])
            self.__push_button_lesson.push_button_lesson_clicked.connect(self.__open_lesson)

            self.__hbox_layout_tools.addWidget(self.__push_button_lesson)
            self.__hbox_layout_tools.addSpacing(10)
            self.__hbox_layout_tools.setAlignment(self.__push_button_lesson, QtCore.Qt.AlignmentFlag.AlignTop)

        # прокручиваемая область для кнопок навигации по вопросам
        self.__scroll_area_push_button_questions = QtWidgets.QScrollArea()
        self.__scroll_area_push_button_questions.setObjectName("scroll_area_push_button_questions")
        self.__scroll_area_push_button_questions.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__scroll_area_push_button_questions.verticalScrollBar().setEnabled(False)
        self.__scroll_area_push_button_questions.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__scroll_area_push_button_questions.setWidgetResizable(True)

        self.__hbox_layout_tools.addWidget(self.__scroll_area_push_button_questions)
        self.__hbox_layout_tools.addSpacing(10)

        # рамка для кнопок навигации по вопросам
        self.__frame_push_button_questions = QtWidgets.QFrame()
        self.__frame_push_button_questions.setObjectName("frame_push_button_questions")

        self.__scroll_area_push_button_questions.setWidget(self.__frame_push_button_questions)

        # макет для кнопок навигации по вопросам
        self.__hbox_layout_button_questions = QtWidgets.QHBoxLayout()
        self.__hbox_layout_button_questions.setSpacing(0)
        self.__hbox_layout_button_questions.setContentsMargins(0, 0, 0, 0)

        self.__frame_push_button_questions.setLayout(self.__hbox_layout_button_questions)

        self.__hbox_layout_button_questions.addStretch(1)

        for i in range(self.__len_course):
            push_button_question = PushButtonQuestion(number = i, data_theme = self.__data_theme["frame_main"]["frame_tools"]["push_button_navigation"])
            push_button_question.push_button_question_clicked.connect(self.__switch_question)
            self.__list_push_button_questions.append(push_button_question)

            self.__hbox_layout_button_questions.addWidget(push_button_question)
            if i < self.__len_course:
                self.__hbox_layout_button_questions.addSpacing(10)

        self.__hbox_layout_button_questions.addStretch(1)

        # кнопка завершить тест
        self.__push_button_finish = QtWidgets.QPushButton()
        self.__push_button_finish.setObjectName("push_button_finish")
        self.__push_button_finish.clicked.connect(self.__finish_test)
        self.__push_button_finish.setText("Завершить тест")
        self.__push_button_finish.setFont(QtGui.QFont("Segoe UI", 12))
        self.__push_button_finish.setFixedHeight(50)

        self.__hbox_layout_tools.addWidget(self.__push_button_finish)
        self.__hbox_layout_tools.setAlignment(self.__push_button_finish, QtCore.Qt.AlignmentFlag.AlignTop)

        if self.__path_lesson:
            # открыть урок
            self.__push_button_lesson.push_button_navigation_press()
        else:
            # открыть первую страницу теста
            self.__list_push_button_questions[self.__current_number_question].push_button_navigation_press()

        self.set_style_sheet()

    def __open_lesson(self):
        # создание и упаковка новой страницы для просмотра урока в формате .pdf
        if self.__page_lesson == None:
            self.__page_lesson = LessonViewer(path_lesson = self.__path_lesson)

            self.__stacked_widget.addWidget(self.__page_lesson)

        self.__stacked_widget.setCurrentWidget(self.__page_lesson)

    def __finish_test(self):
        # получение ответа текущей страницы
        self.__list_data_page_test[self.__current_number_question].answer = self.__page_question.answer()
        self.__list_data_page_test[self.__current_number_question].horizontal_scrollbar_value = self.__scroll_area_page_test.horizontalScrollBar().value()
        self.__list_data_page_test[self.__current_number_question].vertical__scrollbar_value = self.__scroll_area_page_test.verticalScrollBar().value()

        # подсчёт количества верных, неверных и пропущенных ответ
        points_right = 0
        points_wrong = 0
        points_skip = 0

        list_data_result = list()

        for i in range(self.__len_course):
            user_answer = self.__list_data_page_test[i].answer
            right_answer = list(i.text for i in self.__root.findall("exercise")[i].find("answers").findall("answer"))
            type = self.__root.findall("exercise")[i].find("questions").find("type").text
            status = None

            if self.__dict_questions_started_passing[i]:
                # если один выбираемый ответ
                if type == "radio_button":
                    if user_answer == right_answer[0]:
                        points_right += 1
                        status = AnswerStatus.right
                    else:
                        points_wrong += 1
                        status = AnswerStatus.wrong

                # если несколько выбираемых ответов
                elif type == "checkbox":
                    right_answer.sort()
                    user_answer.sort()

                    if user_answer == right_answer:
                        points_right += 1
                        status = AnswerStatus.right
                    else:
                        points_wrong += 1
                        status = AnswerStatus.wrong

                # если ввод ответа
                elif type == "input":
                    settings = None
                    if (temp_setting := self.__root.findall("exercise")[i].find("answers").find("settings")) != None:
                        settings = temp_setting
                    
                    if settings != None and user_answer != None:
                        # убирает пробелы
                        if "excluding_space" in settings:
                            if settings["excluding_space"] == "true":
                                pattern = re.compile(r"^\s*|\s*$")

                                right_answer = pattern.sub(r"", right_answer)
                                user_answer = pattern.sub(r"", user_answer)

                    if right_answer == user_answer:
                        points_right += 1
                        status = AnswerStatus.right
                    else:
                        points_wrong += 1
                        status = AnswerStatus.wrong

            else:
                points_skip += 1
                status = AnswerStatus.skip

            list_data_result.append(DataResult(
                status = status,
                user_answer = user_answer,
                right_answer = right_answer
            ))

        data_passage = DataPassage(
            date_start = self.__time_start,
            date_end = datetime.datetime.now(),
            list_data_result = list_data_result
        )

        self.push_button_finish_cliced.emit(data_passage)

    def __switch_question(self, number: int):
        current_question = self.__root.findall("exercise")[number]

        if self.__page_question != None:
            # сохранение ответа текущей страницы в список ответов
            self.__list_data_page_test[self.__current_number_question].answer = self.__page_question.answer()
            self.__list_data_page_test[self.__current_number_question].horizontal_scrollbar_value = self.__scroll_area_page_test.horizontalScrollBar().value()
            self.__list_data_page_test[self.__current_number_question].vertical__scrollbar_value = self.__scroll_area_page_test.verticalScrollBar().value()

            # удаление старой страницы
            self.__scroll_area_page_test.widget().deleteLater()

        self.__current_number_question = number

        # создание и упаковка новой страницы вопроса
        self.__page_question = PageTest(
            number = self.__current_number_question,
            path_course = self.__path_course, 
            question = current_question,
            answer = self.__list_data_page_test[number].answer, 
            started_passing = self.__dict_questions_started_passing[number],
            icon_dialogs = self.__icon_dialogs,
            path_images = self.__path_images, 
            data_theme = self.__data_theme["frame_main"]["test_tab"]            
        )
        self.__page_question.answer_changed.connect(self.__on_change_answer)

        self.__scroll_area_page_test.setWidget(self.__page_question)
        self.__scroll_area_page_test.horizontalScrollBar().setValue(self.__list_data_page_test[self.__current_number_question].horizontal_scrollbar_value)
        self.__scroll_area_page_test.verticalScrollBar().setValue(self.__list_data_page_test[self.__current_number_question].vertical__scrollbar_value)
        self.__stacked_widget.setCurrentWidget(self.__scroll_area_page_test)

    def __on_change_answer(self, number: int, answered: bool):
        self.__list_push_button_questions[number].set_answered(answered)
        self.__dict_questions_started_passing[number] = answered

    def set_style_sheet(self):
        # панель инструментов и навигации
        self.__frame_tools.setStyleSheet(f"""
        #frame_tools {{               
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            background: #8C8C8C;
        }} """) # % self.__data_theme["frame_main"]["frame_tools"]

        # главная рамка
        self.__frame_main.setStyleSheet(f"""
        #frame_main {{
            background: #FFFFFF;
        }} """)# % self.__data_theme["frame_main"]
        
        # прокручиваемая область для станица теста
        self.__scroll_area_page_test.setStyleSheet(f"""
        #scroll_area_page_test {{
            background: #FFFFFF;
            border: none;
        }}
        
        QScrollBar:vertical {{              
            border: transparent;
            background: #F2F2F2;
            width: 14px;
            border-radius: 6px;
            padding: 4px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background: #888888;
            border-radius: 3px;
            min-height: 30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            background: transparent;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }} 

        QScrollBar:horizontal {{              
            border: transparent;
            background: #F2F2F2;
            height: 14px;
            border-radius: 6px;
            padding: 4px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: #888888;
            border-radius: 3px;
            min-width: 30px;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            background: transparent;
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
        }} """)

        # прокручиваемая область для кнопок навигации по вопросам
        self.__scroll_area_push_button_questions.setStyleSheet(f"""
        #scroll_area_push_button_questions {{
            background: #8C8C8C;
            border: none;
            margin: 0px, 0px, 0px, 0px;
        }} 

        QScrollBar:vertical {{
            width: 0px;
        }}
        
        QScrollBar:horizontal {{              
            border: transparent;
            background: #F2F2F2;
            height: 14px;
            border-radius: 6px;
            padding: 4px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: #888888;
            border-radius: 3px;
            min-width: 30px;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            background: transparent;
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
        }} """)
   
        self.__frame_push_button_questions.setStyleSheet(f"""
        #frame_push_button_questions {{
            background: #8C8C8C;
            margin: 0px, 17px, 0px, 0px;
        }} """)

        # кнопка завершить тест
        self.__push_button_finish.setStyleSheet(f"""
        #push_button_finish {{
            outline: 0;
            padding-left: 15px;
            padding-right: 15px;
            border-radius: 15px;
            background: #037BFB; 
            color: #FFFFFF;
        }} """)# % self.__data_theme["frame_main"]["frame_tools"]["push_button_finish"]
