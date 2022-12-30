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
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 20, 30, 30)
        self.frame_main.setMinimumWidth(300)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.setSpacing(0)
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout)

        # метка меню
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Меню")
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout.addWidget(self.label_header)
        self.vbox_layout.addSpacing(20)

        # кнопка отменить
        self.push_button_cancel = QtWidgets.QPushButton()
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.push_button_cancel.clicked.connect(self.clicked_push_button_cancel)
        self.push_button_cancel.setFont(self.font_widgets)
        self.push_button_cancel.setMinimumHeight(self.min_height)
        self.push_button_cancel.setText("Отмена")

        self.vbox_layout.addWidget(self.push_button_cancel)
        self.vbox_layout.addSpacing(15)

        # кнопка о программе
        self.push_button_info = QtWidgets.QPushButton()
        self.push_button_info.setObjectName("push_button_info")
        self.push_button_info.clicked.connect(self.clicked_push_button_info)
        self.push_button_info.setFont(self.font_widgets)
        self.push_button_info.setMinimumHeight(self.min_height)
        self.push_button_info.setText("О программе")

        self.vbox_layout.addWidget(self.push_button_info)
        self.vbox_layout.addSpacing(15)

        # кнопка выход
        self.push_button_exit = QtWidgets.QPushButton()
        self.push_button_exit.setObjectName("push_button_exit")
        self.push_button_exit.clicked.connect(self.clicked_push_button_exit)
        self.push_button_exit.setFont(self.font_widgets)
        self.push_button_exit.setMinimumHeight(self.min_height)
        self.push_button_exit.setDefault(True)
        self.push_button_exit.setText("Выйти")

        self.vbox_layout.addWidget(self.push_button_exit)

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
        self.min_height = 42
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
    clicked_cancel = QtCore.pyqtSignal()
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
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 30, 30, 30)
        self.frame_main.setMinimumWidth(1000)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # главный макет
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_layout.setSpacing(0)
        self.hbox_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.hbox_layout)

        # макет метки с логотипом
        self.vbox_layout_logo = QtWidgets.QVBoxLayout()
        self.vbox_layout_logo.setSpacing(0)
        self.vbox_layout_logo.setContentsMargins(30, 30, 30, 30)

        self.hbox_layout.addLayout(self.vbox_layout_logo)

        # метка с логотипом
        self.label_logo = QtWidgets.QLabel()
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)

        self.logo = QtGui.QPixmap(self.path_logo)
        self.logo = self.logo.scaled(200, 200)

        self.label_logo.setPixmap(self.logo)
        self.label_logo.setFixedSize(self.logo.width(), self.logo.height())

        self.vbox_layout_logo.addWidget(self.label_logo)

        # макет для текста
        self.vbox_layout_text = QtWidgets.QVBoxLayout()
        self.vbox_layout_text.setSpacing(0)
        self.vbox_layout_text.setContentsMargins(0, 0, 0, 0)

        self.hbox_layout.addLayout(self.vbox_layout_text)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("IT Master")
        self.label_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_text.addWidget(self.label_header)
        self.vbox_layout_text.addSpacing(30)

        # метка с текстом
        self.label_text = QtWidgets.QLabel()
        self.label_text.setFont(self.font_label_text)
        self.label_text.setObjectName("label_text")
        self.label_text.setText(self.info_test)
        self.label_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_text.setWordWrap(True)

        self.vbox_layout_text.addWidget(self.label_text)
        self.vbox_layout_text.addSpacing(30)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_text.addLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка ок
        self.push_button_ok = QtWidgets.QPushButton()
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_ok.clicked.connect(self.clicked_push_button_cancel)
        self.push_button_ok.setFont(self.font_widgets)
        self.push_button_ok.setMinimumHeight(self.min_height)
        self.push_button_ok.setMinimumWidth(self.min_width)
        self.push_button_ok.setDefault(True)
        self.push_button_ok.setText("ОК")

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())
       
    def init_variables(self):
        self.min_height = 42
        self.min_width = 142
        self.font_widgets = QtGui.QFont("Segoe UI", 12)
        self.font_label_header = QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold)
        self.font_label_text = QtGui.QFont("Segoe UI", 12)

        self.info_test = """Версия 2.1
Ведущий программист - Смирнов Н. А., 9 класс, ГБОУ школа №1370\n
IT Master - это школьный предметный тренажёр по информатике, позволяющий прочитать урок по теме и закрепить полученные знания, выполнив тест\n
Приложение написано на языке программирования Python"""

    def clicked_push_button_cancel(self):
        self.close()
        self.clicked_cancel.emit()

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

        # метка с текстом
        self.label_text.setStyleSheet("""
        #label_text {
            color: %(color)s;
        } """ % self.data_theme["label_text"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["push_button_ok"])