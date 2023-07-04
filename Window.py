from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os

class BaseMainWindow(QtWidgets.QMainWindow):
    """Базовый класс главного окна"""
    window_close = QtCore.pyqtSignal()
    window_minimize = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # главная рамка
        self._frame_main = QtWidgets.QFrame()
        self._frame_main.setObjectName("frame_main")

        self.setCentralWidget(self._frame_main)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setContentsMargins(0, 0, 0, 0)
        self.__vbox_layout_internal.setSpacing(0)

        self._frame_main.setLayout(self.__vbox_layout_internal)

        # рамка заголовка
        self._frame_header = QtWidgets.QFrame()
        self._frame_header.setObjectName("frame_header")
        self._frame_header.setFixedHeight(36)

        self.__vbox_layout_internal.addWidget(self._frame_header)

        # макет рамки заголовка
        self.__hbox_layout_header = QtWidgets.QHBoxLayout()
        self.__hbox_layout_header.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_header.setSpacing(0)

        self._frame_header.setLayout(self.__hbox_layout_header)

        # рамка титла
        self._frame_title = QtWidgets.QFrame()
        self._frame_title.setObjectName("frame_title")

        self.__hbox_layout_header.addWidget(self._frame_title)
        self.__hbox_layout_header.addStretch(1)

        # макет рамки титла
        self.__hbox_layout_title = QtWidgets.QHBoxLayout()
        self.__hbox_layout_title.setContentsMargins(5, 0, 0, 0)
        self.__hbox_layout_title.setSpacing(0)

        self._frame_title.setLayout(self.__hbox_layout_title)

        # метка иконки
        self._label_icon = QtWidgets.QLabel()
        self._label_icon.setObjectName("label_icon")
        self._label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._label_icon.setFixedSize(25, 25)

        self.__hbox_layout_title.addWidget(self._label_icon)
        self.__hbox_layout_title.addSpacing(5)

        # метка титла
        self._label_title = QtWidgets.QLabel()
        self._label_title.setObjectName("label_title")
        self._label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._label_title.setFont(QtGui.QFont("Trebuchet MS", 10, weight = QtGui.QFont.Weight.Bold))

        self.__hbox_layout_title.addWidget(self._label_title)

        # рамка кнопок заголока
        self._frame_header_buttons = QtWidgets.QFrame()
        self._frame_header_buttons.setObjectName("frame_header_button")

        self.__hbox_layout_header.addWidget(self._frame_header_buttons)

        # макет рамки кнопок заголока
        self.__hbox_header_buttons = QtWidgets.QHBoxLayout()
        self.__hbox_header_buttons.setContentsMargins(0, 0, 0, 0)
        self.__hbox_header_buttons.setSpacing(0)

        self._frame_header_buttons.setLayout(self.__hbox_header_buttons)

        # кнопка свернуть
        self._push_button_minimize = QtWidgets.QPushButton()
        self._push_button_minimize.setObjectName("push_button_minimize")
        self._push_button_minimize.clicked.connect(self.__press_push_button_minimize)
        self._push_button_minimize.setFont(QtGui.QFont("Webdings", 9))
        self._push_button_minimize.setText("0")
        self._push_button_minimize.setFixedSize(58, 36)
        self._push_button_minimize.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__hbox_header_buttons.addWidget(self._push_button_minimize)

        # кнопка закрыть программу
        self._push_button_close = QtWidgets.QPushButton()
        self._push_button_close.setObjectName("push_button_close")
        self._push_button_close.clicked.connect(self.__press_push_button_exit)
        self._push_button_close.setFont(QtGui.QFont("Webdings", 9))
        self._push_button_close.setText("r")
        self._push_button_close.setFixedSize(58, 36)
        self._push_button_close.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__hbox_header_buttons.addWidget(self._push_button_close)

        # рамка для виджетов
        self._frame_widgets = QtWidgets.QFrame()
        self._frame_widgets.setObjectName("frame_widgets")

        self.__vbox_layout_internal.addWidget(self._frame_widgets)

        # макет рамки для виджетов
        self.__hbox_layout_widgets = QtWidgets.QHBoxLayout()
        self.__hbox_layout_widgets.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_widgets.setSpacing(0)

        self._frame_widgets.setLayout(self.__hbox_layout_widgets)

        # присоединения слотов к сигналам
        self.window_close.connect(self.close_window)
        self.window_minimize.connect(self.minimize_window)
    
    def __press_push_button_minimize(self):
        self.window_minimize.emit()

    def __press_push_button_exit(self):
        self.window_close.emit()

    def close_window(self):
        sys.exit()

    def minimize_window(self):
        super().showMinimized()

    def show_window(self):
        super().showMaximized()

    def set_icon(self, icon: QtGui.QPixmap):
        icon = icon.scaled(25, 25, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
        self._label_icon.setPixmap(icon)

    def set_title(self, title: str):
        self._label_title.setText(title)

    def add_header_button(self, button: QtWidgets.QPushButton):
        self.__hbox_header_buttons.addWidget(button)

    def insert_header_button(self, index: int, button: QtWidgets.QPushButton):
        self.__hbox_header_buttons.insertWidget(index, button)

    def add_widget(self, widget: QtWidgets.QWidget):
        self.__hbox_layout_widgets.addWidget(widget)

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

        self.setObjectName("tool_button")
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.clicked.connect(self.press_tool_button)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setIcon(self.__image)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setText(self.__text)
        self.setFont(QtGui.QFont("Calibri", 12))

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

        self.set_style_sheet()

    def set_style_sheet(self):
        if self.__selected:
            temp_style_sheet = self.__data_theme["selected"]
        else:
            temp_style_sheet = self.__data_theme["not_selected"]

        self.setStyleSheet("""
        #tool_button { 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: %(background)s;
            color: %(color)s;
        } """ % temp_style_sheet)

class ToolBar(QtWidgets.QFrame):
    """Панель инструментов"""
    tool_button_home_page_cliced = QtCore.pyqtSignal()
    tool_button_results_cliced = QtCore.pyqtSignal()
    tool_button_settings_cliced = QtCore.pyqtSignal()
    tool_button_info_cliced = QtCore.pyqtSignal()

    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme

        self.setObjectName("tool_bar")

        # макет панели инструментов
        self.__vbox_layout_toolbar = QtWidgets.QVBoxLayout()
        self.__vbox_layout_toolbar.setContentsMargins(5, 5, 5, 5)
        self.__vbox_layout_toolbar.setSpacing(0)

        self.setLayout(self.__vbox_layout_toolbar)

        # кнопка Домашняя страница
        self.tool_button_home_page = ToolButtonToolbar(
            os.path.join(self.__path_images, r"home_page.png"), 
            "Домашняя\nстраница", 
            self.__data_theme["tool_button"]
        )
        self.tool_button_home_page.tool_button_clicked.connect(self.__press_tool_button_home_page)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_home_page)

        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Результаты
        self.tool_button_results = ToolButtonToolbar(
            os.path.join(self.__path_images, r"results.png"), 
            "Результаты", 
            self.__data_theme["tool_button"]
        )
        self.tool_button_results.tool_button_clicked.connect(self.__press_tool_button_results)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_results)

        self.__vbox_layout_toolbar.addStretch(1)

        # кнопка Настройка
        self.tool_button_settings = ToolButtonToolbar(
            os.path.join(self.__path_images, r"settings.png"),
            "Настройка", 
            self.__data_theme["tool_button"]
        )
        self.tool_button_settings.tool_button_clicked.connect(self.__press_tool_button_settings)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_settings)

        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Справка
        self.tool_button_info = ToolButtonToolbar(
            os.path.join(self.__path_images, r"info.png"),
            "Справка",
            self.__data_theme["tool_button"]
        )
        self.tool_button_info.tool_button_clicked.connect(self.__press_tool_button_info)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_info)

        self.set_style_sheet()

    def __press_tool_button_home_page(self):
        self.tool_button_home_page_cliced.emit()

    def __press_tool_button_results(self):
        self.tool_button_results_cliced.emit()

    def __press_tool_button_settings(self):
        self.tool_button_settings_cliced.emit()

    def __press_tool_button_info(self):
        self.tool_button_info_cliced.emit()

    def set_style_sheet(self):
        self.setStyleSheet("""
        #tool_bar {
            background: %(background)s;
        } """ % self.__data_theme)

class Window(BaseMainWindow):
    """Главное окно"""
    def __init__(self, path_images: dict, data_theme: dict):
        super().__init__()
        
        self.__path_images = path_images
        self.__data_theme = data_theme

        # панель инструментов
        self.toolbar = ToolBar(self.__path_images, self.__data_theme["frame_tool_bar"])
        self.add_widget(self.toolbar)

        self.set_style_sheet()

    def set_style_sheet(self):
        # рамка заголовка
        self._frame_header.setStyleSheet("""
        #frame_header {
            background: %(background)s;
        } """ % self.__data_theme["frame_header"])

        # метка титла
        self._label_title.setStyleSheet("""
        #label_title {
            color: %(color)s;
        } """ % self.__data_theme["frame_header"]["label_title"])

        # кнопка свернуть
        temp_data_theme = {
            "background_normal": self.__data_theme["frame_header"]["push_button"]["normal"]["background"],
            "color_normal": self.__data_theme["frame_header"]["push_button"]["normal"]["color"], 
            "background_hover": self.__data_theme["frame_header"]["push_button"]["hover"]["background"], 
            "color_hover": self.__data_theme["frame_header"]["push_button"]["hover"]["color"],
            "background_press": self.__data_theme["frame_header"]["push_button"]["press"]["background"], 
            "color_press": self.__data_theme["frame_header"]["push_button"]["press"]["color"]
        }

        self._push_button_minimize.setStyleSheet("""
        #push_button_minimize {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_minimize::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_minimize::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # кнопка закрыть программу
        temp_data_theme = {
            "background_normal": self.__data_theme["frame_header"]["push_button_close"]["normal"]["background"],
            "color_normal": self.__data_theme["frame_header"]["push_button_close"]["normal"]["color"], 
            "background_hover": self.__data_theme["frame_header"]["push_button_close"]["hover"]["background"], 
            "color_hover": self.__data_theme["frame_header"]["push_button_close"]["hover"]["color"],
            "background_press": self.__data_theme["frame_header"]["push_button_close"]["press"]["background"], 
            "color_press": self.__data_theme["frame_header"]["push_button_close"]["press"]["color"]
        }

        self._push_button_close.setStyleSheet("""
        #push_button_close {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_close::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_close::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # рамка для виджетов
        self._frame_widgets.setStyleSheet("""
        #frame_widgets {
            background: %(background)s;
        } """ % self.__data_theme["frame_widgets"])
