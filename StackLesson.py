from PyQt5 import QtCore, QtGui, QtWidgets
import xml.etree.ElementTree as ET
import os
import re

class LessonGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, path_lesson: str, data_theme: dict):
        super().__init__()

        self.data_theme = data_theme
        self.path_lesson = path_lesson

        self.init_variables()

        self.image = QtWidgets.QGraphicsPixmapItem()
        self.image.setTransformationMode(QtCore.Qt.SmoothTransformation) 

        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.graphics_scene.addItem(self.image)

        self.setScene(self.graphics_scene)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing)

        self.set_style_sheet()

    def init_variables(self):
        self.min_zoom = None
        self.max_zoom = None
        self.zoom = None

        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.background = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["background"])[1:-1]])

    def fit_in_view(self):
        rect = QtCore.QRectF(self.image.pixmap().rect())

        self.setSceneRect(rect)

        unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        view_rect = self.viewport().rect()
        scene_rect = self.transform().mapRect(rect)

        self.min_zoom = min(view_rect.width() / scene_rect.width(), view_rect.height() / scene_rect.height())
        self.max_zoom = max(view_rect.width() / scene_rect.width(), view_rect.height() / scene_rect.height()) * 0.9

        self.zoom = self.max_zoom

        self.scale(self.zoom, self.zoom)

    def set_image(self):
        self.image.setPixmap(QtGui.QPixmap(self.path_lesson))

        self.fit_in_view()

    def wheelEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            current_zoom = self.zoom
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.zoom *= factor
                if self.zoom > self.max_zoom:
                    self.zoom = self.max_zoom
                    factor = self.zoom / current_zoom
            else:
                factor = 0.8
                self.zoom *= factor
                if self.zoom < self.min_zoom:
                    self.zoom = self.min_zoom
                    factor = self.zoom / current_zoom

            self.scale(factor, factor)
        else:
            super().wheelEvent(event)

    def set_style_sheet(self):
        # фоновый цвет холста
        self.setBackgroundBrush(self.background)

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
        } """ % self.data_theme["scrollbar"])

class StackLesson(QtWidgets.QWidget):
    def __init__(self, path_course: str, func: callable, data_theme: dict):
        super().__init__()

        self.path_course = path_course
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
        self.label_header.setText("Теоретическая часть")
        self.label_header.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label_header.setMinimumHeight(self.min_height_label_header)
        self.label_header.setContentsMargins(10, 0, 10, 0)

        self.vbox_layout_main.addWidget(self.label_header)

        # виджет просмотра изображений
        self.lesson_viewer = LessonGraphicsView(path_lesson = self.path_lesson, data_theme = self.data_theme["lesson_graphics_view"])

        self.vbox_layout_main.addWidget(self.lesson_viewer)

        # рамка панели инстументов
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")
        
        self.vbox_layout_main.addWidget(self.frame_tools)

        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка начать тест
        self.push_button_start = QtWidgets.QPushButton()
        self.push_button_start.setObjectName("push_button_start")
        self.push_button_start.clicked.connect(self.func)
        self.push_button_start.setFont(self.font_push_button_start)
        self.push_button_start.setMinimumHeight(self.min_height)
        self.push_button_start.setText("Начать тест")

        self.hbox_layout_tools.addWidget(self.push_button_start)
        self.hbox_layout_tools.addStretch(1)

        self.set_style_sheet()

    def load_lesson(self):
        self.lesson_viewer.set_image()

    def init_variables(self):
        self.tree = ET.parse(self.path_course)
        self.root = self.tree.getroot()

        self.path_lesson = os.path.join(os.path.split(self.path_course)[0], self.root.find("lesson").text).replace("\\", "/")

        self.min_height = 42
        self.min_height_label_header = 54
        self.font_push_button_start = QtGui.QFont("Segoe UI", 14)
        self.font_label_header = QtGui.QFont("Segoe UI", 17, weight = QtGui.QFont.Bold)

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

        # кнопка начать тест
        self.push_button_start.setStyleSheet("""
        #push_button_start {
            outline: 0;
            border-radius: 7px; 
            padding-left: 10px;
            padding-right: 10px;
            background-color: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_tools"]["push_button_start"])
