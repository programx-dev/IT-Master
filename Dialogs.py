from PyQt6 import QtCore, QtGui, QtWidgets
import Window
import re
import enum
import typing

class ButtonRole(enum.Enum):
    accept = 0
    reject = 1
    
class Dialog(Window.Dialog):
    """Настраиваемое диалоговое окно"""
    
    def __init__(self, data_theme: dict):
        self.__data_theme = data_theme
        self.__icon = None
        self.__text = None
        self.__description = None
        self.__list_push_buttons = list()
        self.__defaul_push_button = None
        self.__value = None
        self.__event_loop = None

        super().__init__(data_theme = self.__data_theme)
        super().set_window_flags(QtCore.Qt.WindowType.WindowCloseButtonHint)
        super().setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        super().set_resizeable(False)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.add_widget(self.__frame_main)

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.__frame_main.setLayout(self.__vbox_layout_main)

        # макет с информацией
        self.__hbox_layout_info = QtWidgets.QHBoxLayout()
        self.__hbox_layout_info.setSpacing(0)
        self.__hbox_layout_info.setContentsMargins(15, 15, 15, 15)

        self.__vbox_layout_main.addLayout(self.__hbox_layout_info)

        # метка со значком
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setFixedSize(40, 40)

        self.__label_icon.hide()
        self.__hbox_layout_info.addWidget(self.__label_icon)
        self.__hbox_layout_info.addSpacing(20)

        # внутренний макет
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.__hbox_layout_info.addLayout(self.__vbox_layout_internal)

        # метка с текстом
        self.__label_text = QtWidgets.QLabel()
        self.__label_text.setFont(QtGui.QFont("Segoe UI", 11))
        self.__label_text.setObjectName("label_text")
        # self.__label_text.setWordWrap(True)
        self.__label_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__label_text.hide()
        self.__vbox_layout_internal.addWidget(self.__label_text)
        self.__vbox_layout_internal.addSpacing(10)

        # метка с описанием
        self.__label_description = QtWidgets.QLabel()
        self.__label_description.setFont(QtGui.QFont("Segoe UI", 11))
        self.__label_description.setObjectName("label_description")
        # self.__label_description.setWordWrap(True)
        self.__label_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__label_description.hide()
        self.__vbox_layout_internal.addWidget(self.__label_description)

        # макет с кнопками
        self.__hbox_layout_push_buttons = QtWidgets.QHBoxLayout()
        self.__hbox_layout_push_buttons.setSpacing(0)
        self.__hbox_layout_push_buttons.setContentsMargins(15, 0, 15, 15)
        self.__hbox_layout_push_buttons.addStretch(1)

        self.__vbox_layout_main.addLayout(self.__hbox_layout_push_buttons)

        # подключение слотов к сигналам
        self.title_bar_window.window_close.connect(self.__exit_window)

        self.set_style_sheet()
    
    def __exit_window(self):
        if self.__event_loop:
            self.__event_loop.exit()
        
    def run_modal(self):
        self.__event_loop = QtCore.QEventLoop()
        self.show()
        self.__event_loop.exec()
        self.close()
        return self.__value

    def set_window_title(self, title: str):
        super().set_window_title(title)

    def set_icon(self, icon: QtGui.QIcon | QtWidgets.QStyle.StandardPixmap):
        if isinstance(icon, QtGui.QIcon):
            self.__icon = icon.pixmap(40, 40)
        elif isinstance(icon, QtWidgets.QStyle.StandardPixmap):
            self.__icon =  QtWidgets.QApplication.style().standardIcon(icon).pixmap(40, 40)
        self.__label_icon.setPixmap(self.__icon)
        self.__label_icon.show()

    def set_text(self, text: str):
        self.__text = text
        self.__label_text.setText(self.__text)
        self.__label_text.show()

    def set_description(self, description: str):
        self.__description = description
        self.__label_description.setText(self.__description)
        self.__label_description.show()

    def __push_button_pressed(self, role: ButtonRole | typing.Any):
        self.__value = role
        if self.__event_loop:
            self.__event_loop.exit()

    def get_value(self) -> ButtonRole | typing.Any:
        return self.__value

    def add_push_button(self, text: str, role: ButtonRole | typing.Any = None, default: bool = False):
        push_button = QtWidgets.QPushButton()
        push_button.setText(text)
        push_button.setFont(QtGui.QFont("Segoe UI", 10))
        push_button.setFixedHeight(28)
        push_button.setMinimumWidth(75)
        push_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        push_button.clicked.connect(lambda: self.__push_button_pressed(role))
        if self.__defaul_push_button == None:
            self.__defaul_push_button = push_button
            push_button.setDefault(True)
        elif default:
            self.__defaul_push_button.setDefault(False)
            push_button.setDefault(True)
        self.__list_push_buttons.append(push_button)

        push_button.setStyleSheet(f"""
        QPushButton {{
            border: none;
            outline: 0;
            padding-left: 15px;
            padding-right: 15px;
            border-radius: 5px; 
            background: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
            color: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
        }} 
        QPushButton:default {{
            background: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
            color: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
        }}""")

        if self.__hbox_layout_push_buttons.count() > 0:
            self.__hbox_layout_push_buttons.addSpacing(10)
        self.__hbox_layout_push_buttons.addWidget(push_button)

    def set_style_sheet(self):
        self.__frame_main.setStyleSheet(f"""
        #frame_main {{
            background: {self.__data_theme["frame_widgets"]["frame_main"]["background"]};
        }} """)

        self.__label_text.setStyleSheet(f"""
        #label_text {{
            background: transparent;
            color: {self.__data_theme["frame_widgets"]["frame_main"]["label_text"]["color"]};
        }} """)

        self.__label_description.setStyleSheet(f"""
        #label_description {{
            background: transparent;
            color: {self.__data_theme["frame_widgets"]["frame_main"]["label_description"]["color"]};
        }} """)

class DialogTableResultsEmpty(QtWidgets.QDialog):
    push_button_clicked_ok = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        
        self.setWindowTitle('Выход')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowType.FramelessWindowHint
        )

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 20, 30, 30)
        self.frame_main.setFixedWidth(440)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Weight.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Действие невозможно")
        self.label_header.setWordWrap(True)
        self.label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_header)
        self.vbox_layout_internal.addSpacing(10)

        # метка подсказки
        self.label_hint = QtWidgets.QLabel()
        self.label_hint.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_hint.setObjectName("label_hint")
        self.label_hint.setText("В таблице результатов ещё нет записей")
        self.label_hint.setWordWrap(True)
        self.label_hint.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_hint)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка ок
        self.push_button_ok = QtWidgets.QPushButton()
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_ok.clicked.connect(self.clicked_push_button_ok)
        self.push_button_ok.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_ok.setFixedSize(142, 42)
        self.push_button_ok.setText("Ок")
        self.push_button_ok.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_ok(self):
        self.close()
        self.push_button_clicked_ok.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка подсказки
        self.label_hint.setStyleSheet("""
        #label_hint {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_hint"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_ok"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)

class DialogExit(QtWidgets.QDialog):
    push_button_clicked_exit = QtCore.pyqtSignal()
    push_button_clicked_cancel = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        
        self.setWindowTitle('Выход')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 20, 30, 30)
        self.frame_main.setFixedWidth(370)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Weight.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Выйти из теста?")
        self.label_header.setWordWrap(True)
        self.label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_header)
        self.vbox_layout_internal.addSpacing(10)

        # метка подсказки
        self.label_hint = QtWidgets.QLabel()
        self.label_hint.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_hint.setObjectName("label_hint")
        self.label_hint.setText("Результаты не сохранятся")
        self.label_hint.setWordWrap(True)
        self.label_hint.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_hint)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        # кнопка отменить
        self.push_button_cancel = QtWidgets.QPushButton()
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.push_button_cancel.clicked.connect(self.clicked_push_button_cancel)
        self.push_button_cancel.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_cancel.setFixedHeight(42)
        self.push_button_cancel.setText("Отмена")
        self.push_button_cancel.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_cancel)
        self.hbox_layout_tools.addSpacing(15)

        # кнопка выход
        self.push_button_exit = QtWidgets.QPushButton()
        self.push_button_exit.setObjectName("push_button_exit")
        self.push_button_exit.clicked.connect(self.clicked_push_button_exit)
        self.push_button_exit.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_exit.setFixedHeight(42)
        self.push_button_exit.setText("Выйти")
        self.push_button_exit.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_exit)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_exit(self):
        self.close()
        self.push_button_clicked_exit.emit()

    def clicked_push_button_cancel(self):
        self.close()
        self.push_button_clicked_cancel.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка подсказки
        self.label_hint.setStyleSheet("""
        #label_hint {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_hint"])

        # кнопка остаться
        self.push_button_cancel.setStyleSheet("""
        #push_button_cancel {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_cancel"])

        # кнопка выйти
        self.push_button_exit.setStyleSheet("""
        #push_button_exit {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_exit"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)

class DialogInfo(QtWidgets.QDialog):
    push_button_clicked_ok = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, version: str, name: str, text_info: str, path_logo: str, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        self.path_logo = path_logo
        self.version = version
        self.name = name
        self.text_info = text_info
        
        self.setWindowTitle('О программе')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(0, 0, 0, 0)
        self.frame_main.setFixedWidth(550)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(30, 30, 30, 30)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # макет логотипа и меток заголовка с версией
        self.hbox_layout_header = QtWidgets.QHBoxLayout()
        self.hbox_layout_header.setSpacing(0)
        self.hbox_layout_header.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_header)
        self.vbox_layout_internal.addSpacing(10)

        # логотип
        self.logo = QtGui.QPixmap(self.path_logo)
        self.logo = self.logo.scaled(110, 110, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)

        # метка с логотипом
        self.label_logo = QtWidgets.QLabel()
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_logo.setPixmap(self.logo)
        self.label_logo.setFixedSize(self.logo.width(), self.logo.height())

        self.hbox_layout_header.addWidget(self.label_logo)

        # макет меток заголовка и версии
        self.vbox_layout_text_header = QtWidgets.QVBoxLayout()
        self.vbox_layout_text_header.setSpacing(0)
        self.vbox_layout_text_header.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout_text_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.hbox_layout_header.addLayout(self.vbox_layout_text_header)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Weight.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText(self.name)
        self.label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_header)
        self.vbox_layout_text_header.addSpacing(10)

        # метка версии
        self.label_version = QtWidgets.QLabel()
        self.label_version.setFont(QtGui.QFont("Segoe UI", 11))
        self.label_version.setObjectName("label_version")
        self.label_version.setText(self.version)
        self.label_version.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_version)

        # метка с текстом с информацией
        self.label_text_info = QtWidgets.QLabel()
        self.label_text_info.setFont(QtGui.QFont("Segoe UI", 11))
        self.label_text_info.setObjectName("label_text_info")
        self.label_text_info.setWordWrap(True)
        self.label_text_info.setText(self.text_info)
        self.label_text_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.vbox_layout_internal.addWidget(self.label_text_info)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка ок
        self.push_button_ok = QtWidgets.QPushButton()
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_ok.clicked.connect(self.clicked_push_button_ok)
        self.push_button_ok.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_ok.setFixedSize(142, 42)
        self.push_button_ok.setText("Ок")
        self.push_button_ok.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_ok(self):
        self.close()
        self.push_button_clicked_ok.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка версии
        self.label_version.setStyleSheet("""
        #label_version {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_version"])

        # метка с текстом с информацией
        self.label_text_info.setStyleSheet("""
        #label_text_info {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_text_info"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_ok"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)
