from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries
import re

class StackResult(QtWidgets.QWidget):
    def __init__(self, data, data_theme: dict, func: callable):
        super().__init__()

        self.data = data
        self.data_theme = data_theme
        self.func = func

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

        # внутренний макет
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.vbox_layout.setSpacing(0)
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout)

        self.vbox_layout.addStretch(1)

        # макет диаграммы и легенды
        self.hbox_layout_chart = QtWidgets.QHBoxLayout()
        self.hbox_layout_chart.setSpacing(0)
        self.hbox_layout_chart.setContentsMargins(0, 0, 0, 0)

        self.hbox_layout_chart.addStretch(1)

        self.vbox_layout.addLayout(self.hbox_layout_chart)
        self.vbox_layout.addStretch(1)

        # диаграмма
        self.series = QPieSeries()
        self.series.setHoleSize(0.4)

        self.slice_right = self.series.append("Правильные", round(self.data.points_right / self.data.points_max * 100))
        self.slice_right.setBrush(self.color_right)

        self.slice_wrong = self.series.append("Неправильные", round(self.data.points_wrong / self.data.points_max * 100))
        self.slice_wrong.setBrush(self.color_wrong)

        self.slice_skip = self.series.append("Пропущенные", round(self.data.points_skip / self.data.points_max * 100))
        self.slice_skip.setBrush(self.color_skip)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setBackgroundRoundness(0)
        self.chart.setContentsMargins(-82,-82,-82, -82)
        self.chart.addSeries(self.series)

        self.chartview = QChartView(self.chart)
        self.chartview.setFixedSize(QtCore.QSize(293, 293))
        self.chartview.setObjectName("chartview")

        self.hbox_layout_chart.addWidget(self.chartview)
        self.hbox_layout_chart.addStretch(1)

        # рамка легенды
        self.frame_legend = QtWidgets.QFrame()
        self.frame_legend.setObjectName("frame_legend")
        
        self.hbox_layout_chart.addWidget(self.frame_legend)
        self.hbox_layout_chart.addStretch(1)

        # макет легенды
        self.vbox_layout_legend = QtWidgets.QVBoxLayout()
        self.vbox_layout_legend.setSpacing(0)
        self.vbox_layout_legend.setContentsMargins(30, 30, 30, 30)

        self.frame_legend.setLayout(self.vbox_layout_legend)

        # метка количества баллов
        self.label_result = QtWidgets.QLabel()
        self.label_result.setObjectName("label_result")
        self.label_result.setText(f"{round(self.data.points_right / self.data.points_max * 100)} / 100")
        self.label_result.setFont(self.font_label_result)
        self.label_result.setAlignment(QtCore.Qt.AlignHCenter)

        self.vbox_layout_legend.addWidget(self.label_result)
        self.vbox_layout_legend.addSpacing(10)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setObjectName("label_header")
        self.label_header.setText(f"Результат теста в баллах")
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(QtCore.Qt.AlignHCenter)

        self.vbox_layout_legend.addWidget(self.label_header)
        self.vbox_layout_legend.addSpacing(10)

        # макет правильно
        self.hbox_layout_right = QtWidgets.QHBoxLayout()
        self.hbox_layout_right.setSpacing(0)
        self.hbox_layout_right.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_legend.addLayout(self.hbox_layout_right)
        self.vbox_layout_legend.addSpacing(10)

        self.label_color_right = QtWidgets.QLabel()
        self.label_color_right.setObjectName("label_color_right")
        self.label_color_right.setFixedSize(self.size_label_legend)

        self.hbox_layout_right.addWidget(self.label_color_right)
        self.hbox_layout_right.addSpacing(10)

        self.label_right = QtWidgets.QLabel()
        self.setObjectName("label_right")
        self.label_right.setText(f"""Правильные: {self.data.points_right} ({round(self.data.points_right / self.data.points_max * 100)}%)""")
        self.label_right.setFont(self.font_label_legend)

        self.hbox_layout_right.addWidget(self.label_right)

        # макет неправильно
        self.hbox_layout_wrong = QtWidgets.QHBoxLayout()
        self.hbox_layout_wrong.setSpacing(0)
        self.hbox_layout_wrong.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_legend.addLayout(self.hbox_layout_wrong)
        self.vbox_layout_legend.addSpacing(10)

        self.label_color_wrong = QtWidgets.QLabel()
        self.label_color_wrong.setObjectName("label_color_wrong")
        self.label_color_wrong.setFixedSize(self.size_label_legend)

        self.hbox_layout_wrong.addWidget(self.label_color_wrong)
        self.hbox_layout_wrong.addSpacing(5)

        self.label_wrong = QtWidgets.QLabel()
        self.setObjectName("label_wrong")
        self.label_wrong.setText(f"""Неправильные: {self.data.points_wrong} ({round(self.data.points_wrong / self.data.points_max * 100)}%)""")
        self.label_wrong.setFont(self.font_label_legend)

        self.hbox_layout_wrong.addWidget(self.label_wrong)

        # макет пропущенно
        self.hbox_layout_skip = QtWidgets.QHBoxLayout()
        self.hbox_layout_skip.setSpacing(0)
        self.hbox_layout_skip.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_legend.addLayout(self.hbox_layout_skip)

        self.label_color_skip = QtWidgets.QLabel()
        self.label_color_skip.setObjectName("label_color_skip")
        self.label_color_skip.setFixedSize(self.size_label_legend)

        self.hbox_layout_skip.addWidget(self.label_color_skip)
        self.hbox_layout_skip.addSpacing(5)

        self.label_skip = QtWidgets.QLabel()
        self.setObjectName("label_skip")
        self.label_skip.setText(f"""Пропущенные: {self.data.points_skip} ({round(self.data.points_skip / self.data.points_max * 100)}%)""")
        self.label_skip.setFont(self.font_label_legend)

        self.hbox_layout_skip.addWidget(self.label_skip)

        # панель кнопки вернуться на главную
        self.frame_bottom = QtWidgets.QFrame()
        self.frame_bottom.setObjectName("frame_bottom")
        
        self.vbox_layout.addWidget(self.frame_bottom)

        self.hbox_layout_bottom = QtWidgets.QHBoxLayout()
        self.hbox_layout_bottom.setSpacing(0)
        self.hbox_layout_bottom.setContentsMargins(20, 10, 20, 10)

        # макет кнопки вернуться на главную
        self.hbox_layout_pushbutton = QtWidgets.QHBoxLayout()
        self.hbox_layout_pushbutton.setSpacing(0)
        self.hbox_layout_pushbutton.setContentsMargins(20, 14, 20, 14)

        self.frame_bottom.setLayout(self.hbox_layout_pushbutton)

        self.hbox_layout_pushbutton.addStretch(1)

        # кнопка вернуться на главную
        self.pushbutton_to_main = QtWidgets.QPushButton()
        self.pushbutton_to_main.setObjectName("pushbutton_to_main")
        self.pushbutton_to_main.clicked.connect(self.func)
        self.pushbutton_to_main.setFont(self.font_pushbuttons)
        self.pushbutton_to_main.setText("На главную")
        self.pushbutton_to_main.setMinimumHeight(self.min_height)

        self.hbox_layout_pushbutton.addWidget(self.pushbutton_to_main)
        self.hbox_layout_pushbutton.addStretch(1)

        self.set_style_sheet()

    def init_variables(self):
        self.size_label_legend = QtCore.QSize(24, 24)
        self.min_height = 42

        self.font_label_result = QtGui.QFont("Segoe UI", 20)
        self.font_label_header = QtGui.QFont("Segoe UI", 16)
        self.font_label_legend = QtGui.QFont("Segoe UI", 16)
        self.font_pushbuttons  = QtGui.QFont("Segoe UI", 14)

        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.color_right = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["color_right"])[1:-1]])
        self.color_wrong = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["color_wrong"])[1:-1]])
        self.color_skip = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["color_skip"])[1:-1]])
        self.color_background = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["background_frame_main"])[1:-1]])

    def set_style_sheet(self):
        # диаграмма
        self.chartview.chart().setBackgroundBrush(QtGui.QBrush(self.color_background))

        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background-color: %(background_frame_main)s;
        } """ % self.data_theme)

        # рамка легенды
        self.frame_legend.setStyleSheet("""
        #frame_legend {
            border-radius: 14px;
            border: 3px solid;
            border-color: %(color_border_frame_legend)s;
            background-color: %(background_frame_legend)s;
        } """ % self.data_theme)

        temp_data_theme = self.data_theme
        temp_data_theme["radius"] = self.size_label_legend.width() // 2

        # цвет правильно
        self.label_color_right.setStyleSheet("""
        #label_color_right {
            background-color: %(color_right)s;
            border-radius: %(radius)spx;
        } """ % temp_data_theme)

        # цвет неправильно
        self.label_color_wrong.setStyleSheet("""
        #label_color_wrong {
            background-color: %(color_wrong)s;
            border-radius: %(radius)spx;
        } """ % temp_data_theme)

        # цвет пропущенно
        self.label_color_skip.setStyleSheet("""
        #label_color_skip {
            background-color: %(color_skip)s;
            border-radius: %(radius)spx;
        } """ % temp_data_theme)

        # панель кнопки вернуться на главную
        self.frame_bottom.setStyleSheet("""
        #frame_bottom {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background-color: %(background)s;
        } """ % self.data_theme["frame_bottom"])

        # кнопка вернуться на главную
        self.pushbutton_to_main.setStyleSheet("""
        #pushbutton_to_main {
            outline: 0;
            padding-left: 10;
            padding-right: 10;
            border-radius: 7px;
            background-color: %(background)s;
            color: %(color)s;
        } """ % self.data_theme["pushbutton_to_main"])
