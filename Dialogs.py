from PyQt5 import QtCore, QtGui, QtWidgets

class DialogMenu(QtWidgets.QDialog):
    clicked_exit = QtCore.pyqtSignal()
    clicked_info = QtCore.pyqtSignal()
    clicked_cancel = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, parent = None):
        self.parent = parent

        super().__init__(self.parent)

        self.data_theme = data_theme

        self.init_variables()
        
        self.setWindowTitle('Меню')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.FramelessWindowHint
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
        self.frame_main.setMinimumWidth(300)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка меню
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Меню")
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_header)
        self.vbox_layout_internal.addSpacing(20)

        # кнопка отменить
        self.push_button_cancel = QtWidgets.QPushButton()
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.push_button_cancel.clicked.connect(self.clicked_push_button_cancel)
        self.push_button_cancel.setFont(self.font_widgets)
        self.push_button_cancel.setFixedHeight(self.fixed_height)
        self.push_button_cancel.setText("Отмена")
        self.push_button_cancel.setFocusPolicy(QtCore.Qt.NoFocus)

        self.vbox_layout_internal.addWidget(self.push_button_cancel)
        self.vbox_layout_internal.addSpacing(15)

        # кнопка о программе
        self.push_button_info = QtWidgets.QPushButton()
        self.push_button_info.setObjectName("push_button_info")
        self.push_button_info.clicked.connect(self.clicked_push_button_info)
        self.push_button_info.setFont(self.font_widgets)
        self.push_button_info.setFixedHeight(self.fixed_height)
        self.push_button_info.setText("О программе")
        self.push_button_info.setFocusPolicy(QtCore.Qt.NoFocus)

        self.vbox_layout_internal.addWidget(self.push_button_info)
        self.vbox_layout_internal.addSpacing(15)

        # кнопка выход
        self.push_button_exit = QtWidgets.QPushButton()
        self.push_button_exit.setObjectName("push_button_exit")
        self.push_button_exit.clicked.connect(self.clicked_push_button_exit)
        self.push_button_exit.setFont(self.font_widgets)
        self.push_button_exit.setFixedHeight(self.fixed_height)
        self.push_button_exit.setText("Выйти")
        self.push_button_exit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.vbox_layout_internal.addWidget(self.push_button_exit)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_exit(self):
        self.close()
        self.clicked_exit.emit()

    def clicked_push_button_info(self):
        self.close()
        self.clicked_info.emit()

    def clicked_push_button_cancel(self):
        self.close()
        self.clicked_cancel.emit()

    def init_variables(self):
        self.fixed_height = 42
        self.font_widgets = QtGui.QFont("Segoe UI", 14)
        self.font_label_header = QtGui.QFont("Segoe UI", 24, weight = QtGui.QFont.Bold)

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: 1px solid;
            border-color: %(color_border)s;
            background-color: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["label_header"])

        # кнопка остаться
        self.push_button_cancel.setStyleSheet("""
        #push_button_cancel {
            outline: 0;
            border-radius: 7px;
            border: none;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_cancel"])

        # кнопка о программе
        self.push_button_info.setStyleSheet("""
        #push_button_info {
            outline: 0;
            border-radius: 7px;
            border: none;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_info"])

        # кнопка выйти
        self.push_button_exit.setStyleSheet("""
        #push_button_exit {
            outline: 0;
            border-radius: 7px;
            border: none;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_exit"])

class DialogInfo(QtWidgets.QDialog):
    clicked_ok = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, path_logo: str, parent = None):
        self.parent = parent

        super().__init__(self.parent)

        self.data_theme = data_theme
        self.path_logo = path_logo

        self.init_variables()
        
        self.setWindowTitle('О программе')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.FramelessWindowHint
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

        # метка с логотипом
        self.label_logo = QtWidgets.QLabel()
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)

        self.logo = QtGui.QPixmap(self.path_logo)
        self.logo = self.logo.scaled(110, 110)

        self.label_logo.setPixmap(self.logo)
        self.label_logo.setFixedSize(self.logo.width(), self.logo.height())

        self.hbox_layout_header.addWidget(self.label_logo)

        # макет меток заголовка и версии
        self.vbox_layout_text_header = QtWidgets.QVBoxLayout()
        self.vbox_layout_text_header.setSpacing(0)
        self.vbox_layout_text_header.setContentsMargins(0, 0, 0, 0)

        self.hbox_layout_header.addLayout(self.vbox_layout_text_header)

        self.vbox_layout_text_header.addStretch(1)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("IT Master")
        self.label_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_header)
        self.vbox_layout_text_header.addSpacing(10)

        # метка версии
        self.label_version = QtWidgets.QLabel()
        self.label_version.setFont(self.font_label_version)
        self.label_version.setObjectName("label_version")
        self.label_version.setText("Версия 2.2")
        self.label_version.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_version)
        self.vbox_layout_text_header.addStretch(1)

        self.vbox_layout_internal.addSpacing(10)

        # метка с текстом с информацией
        self.label_text_info = QtWidgets.QLabel()
        self.label_text_info.setFont(self.font_label_text)
        self.label_text_info.setObjectName("label_text_info")
        self.label_text_info.setWordWrap(True)
        self.label_text_info.setText(self.info_test)
        self.label_text_info.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

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
        self.push_button_ok.setFont(self.font_widgets)
        self.push_button_ok.setFixedSize(self.fixed_width, self.fixed_height)
        self.push_button_ok.setText("Оk")
        self.push_button_ok.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())
       
    def init_variables(self):
        self.fixed_width = 142
        self.fixed_height = 42
        self.font_widgets = QtGui.QFont("Segoe UI", 12)
        self.font_label_version = QtGui.QFont("Segoe UI", 11)
        self.font_label_header = QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold)
        self.font_label_text = QtGui.QFont("Segoe UI", 11)

        self.info_test = """IT Master - это школьный предметный тренажёр по информатике, позволяющий изучить материал урока и закрепить полученные знания, выполнив тест\n
Ведущий программист - Смирнов Н. А., 9 класс, ГБОУ школа №1370\n
Приложение написано на языке программирования Python"""

    def clicked_push_button_ok(self):
        self.close()
        self.clicked_ok.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: 1px solid;
            border-color: %(color_border)s;
            background-color: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["label_header"])

        # метка версии
        self.label_version.setStyleSheet("""
        #label_version {
            color: %(color)s;
        } """ % self.data_theme["label_version"])

        # метка с текстом с информацией
        self.label_text_info.setStyleSheet("""
        #label_text_info {
            color: %(color)s;
        } """ % self.data_theme["label_text_info"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_ok"])