from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import datetime 
import string
import re

class DeltaTemplate(string.Template):
    delimiter = "%"

class StackTableResults(QtWidgets.QWidget):
    def __init__(self, path_database: str, func: callable, data_theme: dict):
        super().__init__()

        self.path_database = path_database
        self.func = func
        self.data_theme = data_theme
        
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

        # главный макет
        self.vbox_layout_main = QtWidgets.QVBoxLayout()
        self.vbox_layout_main.setSpacing(0)
        self.vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_main)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(self.font_label_header)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Таблица результатов")
        self.label_header.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label_header.setMinimumHeight(self.min_height_label_header)
        self.label_header.setContentsMargins(10, 0, 10, 0)

        self.vbox_layout_main.addWidget(self.label_header)

        # таблица результатов
        self.table_results = QtWidgets.QTableWidget()
        self.table_results.setObjectName("table_results")
        self.table_results.setColumnCount(10)
        self.table_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.table_results.setFont(self.font_table_results)
        self.table_results.horizontalHeader().setFont(self.font_table_results)
        self.table_results.verticalHeader().setFont(self.font_table_results)

        self.vbox_layout_main.addWidget(self.table_results)

        # рамка панели инстументов
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")
        
        self.vbox_layout_main.addWidget(self.frame_tools)

        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка на главную
        self.push_button_to_main = QtWidgets.QPushButton()
        self.push_button_to_main.setObjectName("push_button_to_main")
        self.push_button_to_main.clicked.connect(self.func)
        self.push_button_to_main.setFont(self.font_push_button_to_main)
        self.push_button_to_main.setMinimumHeight(self.min_height)
        self.push_button_to_main.setText("На главную")

        self.hbox_layout_tools.addWidget(self.push_button_to_main)
        self.hbox_layout_tools.addStretch(1)

        # заполнение таблицы
        self.create_table_results()

        self.set_style_sheet()

    def init_variables(self):
        self.min_height = 42
        self.min_height_label_header = 54
        self.font_push_button_to_main = QtGui.QFont("Segoe UI", 14)
        self.font_label_header = QtGui.QFont("Segoe UI", 17, weight = QtGui.QFont.Bold)
        self.font_table_results = QtGui.QFont("Segoe UI", 12)

        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.background_item1_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["table_results"]["background_item1_table"])[1:-1]])
        self.color_item1_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["table_results"]["color_item1_table"])[1:-1]])

        self.background_item2_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["table_results"]["background_item2_table"])[1:-1]])
        self.color_item2_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["table_results"]["color_item2_table"])[1:-1]])

    def strfdelta(self, td: datetime.timedelta, fmt: str) -> str:
        sec = abs(td).total_seconds()

        days, rem = divmod(sec, 86400)
        hours, rem = divmod(rem, 3600)
        mins, sec = divmod(rem, 60)

        t = DeltaTemplate(fmt)
        return t.substitute(
            D = "{:d}".format(int(days)),
            H = "{:02d}".format(int(hours)),
            M = "{:02d}".format(int(mins)),
            S = "{:02d}".format(int(sec))
        )

    def create_table_results(self):
        self.table_results.setHorizontalHeaderLabels([
            "Время начала",
            "Время прохождения",
            "Имя",
            "Фамилия",
            "Класс",
            "Курс",
            "результат, %",
            "Верных",
            "Неверных",
            "Пропущенных"
        ])

        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT * FROM users""")

            list_users = cursor.fetchall()
            list_users.sort(key = lambda x: x[0], reverse = True) 

            self.table_results.setRowCount(len(list_users))

            for row in range(len(list_users)):
                data = list_users[row]
                # дата начала
                table_item = QtWidgets.QTableWidgetItem(data[0])
                self.table_results.setItem(row, 0, table_item)

                # время прохождения
                date_start = datetime.datetime.strptime(data[0], r"%d.%m.%Y %H:%M")
                date_end = datetime.datetime.strptime(data[1], r"%d.%m.%Y %H:%M")

                time_delta = date_end - date_start
                time_duration = self.strfdelta(td = time_delta, fmt = r"%H:%M:%S")

                table_item = QtWidgets.QTableWidgetItem(time_duration)
                self.table_results.setItem(row, 1, table_item)

                # фамилия
                table_item = QtWidgets.QTableWidgetItem(data[2])
                self.table_results.setItem(row, 2, table_item)

                # имя
                table_item = QtWidgets.QTableWidgetItem(data[3])
                self.table_results.setItem(row, 3, table_item)

                # класс
                table_item = QtWidgets.QTableWidgetItem(data[4])
                self.table_results.setItem(row, 4, table_item)

                # курс
                table_item = QtWidgets.QTableWidgetItem(data[5])
                self.table_results.setItem(row, 5, table_item)

                # результат, %
                table_item = QtWidgets.QTableWidgetItem(str(data[10]))
                self.table_results.setItem(row, 6, table_item)

                # верных
                table_item = QtWidgets.QTableWidgetItem(str(data[7]))
                self.table_results.setItem(row, 7, table_item)

                # неверных
                table_item = QtWidgets.QTableWidgetItem(str(data[8]))
                self.table_results.setItem(row, 8, table_item)

                # пропущенных
                table_item = QtWidgets.QTableWidgetItem(str(data[9]))
                self.table_results.setItem(row, 9, table_item)

                if row % 2 == 0:
                    background = QtGui.QColor(222, 234, 246)
                    color = QtGui.QColor(0, 0, 0)
                else:
                    background = QtGui.QColor(255, 255, 255)
                    color = QtGui.QColor(0, 0, 0)

                # установить цвет
                if row % 2 == 0:
                    background = self.background_item1_table
                    color = self.color_item1_table
                else:
                    background = self.background_item2_table
                    color = self.color_item2_table

                for i in range(10):
                    self.table_results.item(row, i).setBackground(background)
                    self.table_results.item(row, i).setForeground(color)

        self.table_results.resizeColumnsToContents()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background-color: %(background_frame_main)s;
        } """ % self.data_theme)

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
            background-color: %(background)s;
            color: %(color)s;
        } """ % self.data_theme["label_header"])

        # рамка панели инстументов
        self.frame_tools.setStyleSheet("""
        #frame_tools {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background-color: %(background)s;
        } """ % self.data_theme["frame_tools"])

        # кнопка на главную
        self.push_button_to_main.setStyleSheet("""
        #push_button_to_main {
            outline: 0;
            border-radius: 7px; 
            padding-left: 10px;
            padding-right: 10px;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_tools"]["push_button_to_main"])

        # таблица результатов
        self.table_results.horizontalHeader().setStyleSheet("""
        ::section:horizontal {
            background-color: %(background_header_table)s;
            color: %(color_header_table)s;
            border: none;
        } """ % self.data_theme["table_results"])

        self.table_results.verticalHeader().setStyleSheet("""
        ::section:vertical {
            background-color:  %(background_header_table)s;
            color: %(color_header_table)s;
            border: none;
        } """ % self.data_theme["table_results"])

        self.table_results.setStyleSheet("""
        #table_results {
            background: %(background)s;
            gridline-color: %(color_border)s;
            border: none;
        } """ % self.data_theme["table_results"])

    # полоса прокрутки
        self.setStyleSheet("""
        QScrollBar:vertical {
            background-color: %(background)s;
            width: 20px;
            margin: 0px 0px 0px 0px;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: %(background_handle)s;         
            min-height: 20px;
            border-radius: 10px;
        }
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::add-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
            border: none;
            background: none;
        }
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
            border: none;
            background: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QScrollBar:horizontal {
            background-color: %(background)s;
            height: 20px;
            margin: 0px 0px 0px 0px;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background-color: %(background_handle)s;         
            min-width: 20px;
            border-radius: 10px;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::add-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {
            border: none;
            background: none;
        }
        QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
            border: none;
            background: none;
        }
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """ % self.data_theme["table_results"]["scrollbar"])
