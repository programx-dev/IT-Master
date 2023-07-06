from PyQt6 import QtCore, QtGui, QtWidgets
import os
from glob import glob
import xml.etree.ElementTree as ET
from dataclasses import dataclass

@dataclass
class DataHomePage:
    path_course: str

@dataclass
class DataCourse:
    text: str
    path: str

class PushButtonCourse(QtWidgets.QWidget):
    push_button_clicked_choose_course = QtCore.pyqtSignal()
    
    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.path_images = path_images
        self.data_theme = data_theme

        self.init_variables()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout(self)
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # кнопка с название курсаNoFocusw
        self.push_button_title = QtWidgets.QPushButton()
        self.push_button_title.setObjectName("push_button_title")
        self.push_button_title.clicked.connect(self.press_choose_course)
        self.push_button_title.setText("Выбрать урок")
        self.push_button_title.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_title.setFixedHeight(42)
        self.push_button_title.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_main.addWidget(self.push_button_title)

        # кнопка со значком выбора курса
        self.push_button_download = QtWidgets.QPushButton()
        self.push_button_download.setObjectName("push_button_download")
        self.push_button_download.clicked.connect(self.press_choose_course)
        self.push_button_download.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_download.setFixedSize(42, 42)
        self.push_button_download.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.hbox_layout_main.addWidget(self.push_button_download)

        self.set_style_sheet()

    def change_title(self, text: str):
        self.push_button_title.setText(text)

    def press_choose_course(self):
        self.push_button_clicked_choose_course.emit()

    def init_variables(self):
        self.img_download = QtGui.QIcon(os.path.join(self.path_images, "download.png"))

    def set_style_sheet(self):
        # кнопка с название курса
        self.push_button_title.setStyleSheet("""
        #push_button_title { 
            outline: 0;
            border-top-left-radius: 7px; 
            border-bottom-left-radius: 7px;
            padding-left: 42px;
            background: %(background)s;
            color: %(color)s;
        } """ % self.data_theme)

        # кнопка со значком выбора курса
        self.push_button_download.setStyleSheet("""
        #push_button_download {
            outline: 0;
            border-top-right-radius: 7px; 
            border-bottom-right-radius: 7px; 
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme)
        
        self.push_button_download.setIcon(self.img_download)
        self.push_button_download.setIconSize(QtCore.QSize(42 - 14, 42 - 14))

class StackHomePage(QtWidgets.QWidget):
    push_button_clicked_start_test = QtCore.pyqtSignal(DataHomePage)

    def __init__(self, path_courses: str, path_images: str, path_theme: str, data_theme: dict):
        super().__init__()

        self.__path_courses = path_courses
        self.__path_images = path_images
        self.__data_theme = data_theme
        self.__path_theme = path_theme

        self.__path_selected_course = None

        # главвный макет
        self.__hbox_layout_main = QtWidgets.QHBoxLayout()
        self.__hbox_layout_main.setSpacing(0)
        self.__hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__hbox_layout_main)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__hbox_layout_main.addWidget(self.__frame_main)

        # внутренняя сетка
        self.__grid_layout_internal = QtWidgets.QGridLayout()
        self.__grid_layout_internal.setSpacing(0)
        self.__grid_layout_internal.setContentsMargins(0, 0, 0, 0)
        self.__grid_layout_internal.setColumnStretch(0, 1)
        self.__grid_layout_internal.setColumnStretch(1, 0)
        self.__grid_layout_internal.setColumnStretch(2, 1)
        self.__grid_layout_internal.setRowStretch(0, 1)
        self.__grid_layout_internal.setRowStretch(1, 0)
        self.__grid_layout_internal.setRowStretch(2, 1)

        self.__frame_main.setLayout(self.__grid_layout_internal)

        # внутренняя рамка формы
        self.__frame_internal = QtWidgets.QFrame()
        self.__frame_internal.setObjectName("frame_internal")
        self.__frame_internal.setFixedSize(380, 380)

        self.__grid_layout_internal.addWidget(self.__frame_internal, 1, 1)

        # макет внутри внутренней рамки
        self.__vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.__vbox_layout_internal.setSpacing(0)
        self.__vbox_layout_internal.setContentsMargins(20, 20, 20, 20)

        self.__frame_internal.setLayout(self.__vbox_layout_internal)

        # метка заголовка
        self.__label_header = QtWidgets.QLabel()
        self.__label_header.setFont(QtGui.QFont("Segoe UI", 14))
        self.__label_header.setObjectName("label_header")
        self.__label_header.setText("Каталог уроков")
        self.__label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__vbox_layout_internal.addWidget(self.__label_header)
        self.__vbox_layout_internal.addSpacing(10)

        # список уроков
        self.__list_view = QtWidgets.QListView()
        self.__list_view.setObjectName("list_view")
        self.__list_view.setFont(QtGui.QFont("Segoe UI", 14))
        self.__list_view.setIconSize(QtCore.QSize(20, 20))
        self.__list_view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__list_view_model = QtGui.QStandardItemModel()
        self.__list_view.setModel(self.__list_view_model) 

        for i, data_course in enumerate(self.__get_courses(self.__path_courses)):
            item = QtGui.QStandardItem(data_course.text)
            item.path = data_course.path
            self.__list_view_model.appendRow(item)

            item.setData(QtGui.QIcon(os.path.join(self.__path_images, "folder.png")), QtCore.Qt.ItemDataRole.DecorationRole)
        
        self.__list_view.selectionModel().currentChanged.connect(self.__list_view_row_changed)

        self.__vbox_layout_internal.addWidget(self.__list_view)
        self.__vbox_layout_internal.addSpacing(10)

        # кнопка Выбрать в проводнике
        self.__push_button_select_explorer = QtWidgets.QPushButton()
        self.__push_button_select_explorer.setObjectName("push_button_select_explorer")
        self.__push_button_select_explorer.clicked.connect(self.__choose_course)
        self.__push_button_select_explorer.setFont(QtGui.QFont("Segoe UI", 14))
        self.__push_button_select_explorer.setIcon(QtGui.QIcon(os.path.join(self.__path_images, "select_in_explorer.png")))
        self.__push_button_select_explorer.setIconSize(QtCore.QSize(20, 20))
        self.__push_button_select_explorer.setText("Выбрать в проводнике")
        self.__push_button_select_explorer.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__vbox_layout_internal.addWidget(self.__push_button_select_explorer)
        self.__vbox_layout_internal.addSpacing(10)

        # кнопка Выбрать урок
        self.__push_button_start_test = QtWidgets.QPushButton()
        self.__push_button_start_test.setObjectName("push_button_enter")
        self.__push_button_start_test.setEnabled(False)
        self.__push_button_start_test.clicked.connect(self.__start_test)
        self.__push_button_start_test.setFont(QtGui.QFont("Segoe UI", 14))
        self.__push_button_start_test.setText("Выбрать урок")
        self.__push_button_start_test.setFixedHeight(42)
        self.__push_button_start_test.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__vbox_layout_internal.addWidget(self.__push_button_start_test)

        self.set_style_sheet()

    def __list_view_row_changed(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        if current.isValid():
            self.__path_selected_course = self.__list_view_model.item(current.row()).path

            self.__push_button_start_test.setEnabled(True)

    def __get_courses(self, path_courses: str) -> list[DataCourse]:
        files = [f for x in os.walk(path_courses) for f in glob(os.path.join(x[0], '*.xml'))]
        list_data_courses = list()

        for f in files:
            tree = ET.parse(f)
            root = tree.getroot()

            if root.find("type") != None and root.find("type").text == "IT Master course":
                text = root.find("name").text
                list_data_courses.append(DataCourse(text = text, path = f))

        return list_data_courses

    def __start_test(self):
        data_passage = DataHomePage(
            path_course = self.__path_selected_course
        )

        self.push_button_clicked_start_test.emit(data_passage)

    def __choose_course(self):
        # диалог выбора файла с курсом
        path_file_course = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор курса", self.__path_courses, "XML Файл (*.xml)")[0]

        if os.path.isfile(path_file_course):
            self.__path_selected_course = path_file_course

            self.__push_button_start_test.setEnabled(True)
            
            name_course = os.path.splitext(os.path.basename(self.__path_selected_course))[0]
            formated_name_course = QtGui.QFontMetrics.elidedText(
                QtGui.QFontMetrics(self.__push_button_select_explorer.font()),
                name_course, 
                QtCore.Qt.TextElideMode.ElideRight, 
                (self.__push_button_select_explorer.width() - (self.__push_button_select_explorer.iconSize().width()\
                    + (x := self.__push_button_select_explorer.contentsMargins()).left() + x.right())
                )
            )
            # + QtGui.QFontMetrics.boundingRect(self.__push_button_select_explorer.fontMetrics(), "—").width())

            self.__push_button_select_explorer.setText(formated_name_course)

    def set_style_sheet(self):
        self.__data_theme["frame_main"]["path_background_image"] = os.path.join(os.path.split(self.__path_theme)[0], self.__data_theme["frame_main"]["background_image"]).replace("\\", "/")

        # главная рамка
        self.__frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
            border-image: url(%(path_background_image)s);
            background-repeat: no-repeat; 
            background-position: center;
        } """ % self.__data_theme["frame_main"])

        # внутренняя рамка формы
        self.__frame_internal.setStyleSheet("""
        #frame_internal {
            border-radius: 14px;
            background: %(background)s;
        } """ % self.__data_theme["frame_main"]["frame_internal"])

        # метка заголовка
        self.__label_header.setStyleSheet("""
        #label_header {
            background: %(background)s; 
            color: %(color)s
        } """ % self.__data_theme["frame_main"]["frame_internal"]["label_header"])

        # список уроков
        temp_data_theme = self.__data_theme["frame_main"]["frame_internal"]["list_view"]
        temp_data_theme["scrollbar_background"] = temp_data_theme["scrollbar"]["background"]
        temp_data_theme["scrollbar_background_handle"] = temp_data_theme["scrollbar"]["handle"]["background"]
        
        self.__list_view.setStyleSheet("""
        #list_view {
            border: 0px;
            background: %(background)s; 
            color: %(color)s;
        }
        
        QScrollBar:vertical {              
            border: none;
            background: %(scrollbar_background)s;
            width: 14px;
            border-radius: 6px;
            padding: 4px;
            margin: 14px 0px 14px 0px;
        }
        QScrollBar::handle:vertical {
            background: %(scrollbar_background_handle)s;
            border-radius: 3px;
            min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        } 

        QScrollBar:horizontal {              
            border: none;
            background: %(scrollbar_background)s;
            height: 14px;
            border-radius: 6px;
            padding: 4px;
            margin: 0px 14px 0px 14px;
        }
        QScrollBar::handle:horizontal {
            background: %(scrollbar_background_handle)s;
            border-radius: 3px;
            min-width: 30px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: none;
            width: 0px;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        } """ % temp_data_theme)
        
        # кнопка Выбрать в проводнике
        self.__push_button_select_explorer.setStyleSheet("""
        #push_button_select_explorer {
            outline: 0;
            text-align: left;
            border-radius: 7px; 
            background: transparent; 
            color: %(color)s;
        } """ % self.__data_theme["frame_main"]["frame_internal"]["push_button_select_explorer"])

        # кнопка входа
        self.__push_button_start_test.setStyleSheet("""
        #push_button_enter {
            outline: 0;
            border-radius: 7px; 
            background: %(background)s; 
            color: %(color)s;
        } 
        #push_button_enter::pressed {
            background: %(background_pressed)s; 
            color: %(color)s;
        }
        #push_button_enter::disabled {
            background: %(background_disabled)s;
            color: %(color)s;
        } """ % self.__data_theme["frame_main"]["frame_internal"]["push_button_start_test"])
