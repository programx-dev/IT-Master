from PyQt6 import QtCore, QtGui, QtWidgets
import os
from glob import glob
import xml.etree.ElementTree as ET
from dataclasses import dataclass

@dataclass
class DataPageHome:
    path_course: str

@dataclass
class DataCourse:
    name: str
    path_course: str

class PageHome(QtWidgets.QWidget):
    """Домашняя страница"""
    push_button_clicked_start_test = QtCore.pyqtSignal(DataPageHome)

    def __init__(self, path_courses: str, path_images: str, path_theme: str):
        super().__init__()
        self.setObjectName("page_home")

        self.__path_courses = path_courses
        self.__path_images = path_images
        self.__path_theme = path_theme

        self.__path_selected_course = None

        # главный макет
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
        self.__vbox_layout_internal.setContentsMargins(20, 10, 20, 20)

        self.__frame_internal.setLayout(self.__vbox_layout_internal)

        # метка заголовка
        self.__label_header = QtWidgets.QLabel()
        self.__label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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

        for data_course in self.__get_courses(self.__path_courses):
            item = QtGui.QStandardItem(data_course.name)
            item._path = data_course.path_course
            self.__list_view_model.appendRow(item)

            item.setData(QtGui.QIcon(os.path.join(self.__path_images, r"folder.png")), QtCore.Qt.ItemDataRole.DecorationRole)
        
        self.__list_view.selectionModel().currentChanged.connect(self.__list_view_row_changed)
        self.__list_view.pressed.connect(lambda _: self.__push_button_select_in_explorer.setText("Выбрать в проводнике"))

        self.__vbox_layout_internal.addWidget(self.__list_view)
        self.__vbox_layout_internal.addSpacing(10)

        # кнопка Выбрать в проводнике
        self.__push_button_select_in_explorer = QtWidgets.QPushButton()
        self.__push_button_select_in_explorer.setObjectName("push_button_select_in_explorer")
        self.__push_button_select_in_explorer.clicked.connect(self.__select_course_in_explorer)
        self.__push_button_select_in_explorer.setFont(QtGui.QFont("Segoe UI", 14))
        self.__push_button_select_in_explorer.setIcon(QtGui.QIcon(os.path.join(self.__path_images, r"select_in_explorer.png")))
        self.__push_button_select_in_explorer.setIconSize(QtCore.QSize(20, 20))
        self.__push_button_select_in_explorer.setText("Выбрать в проводнике")
        self.__push_button_select_in_explorer.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__vbox_layout_internal.addWidget(self.__push_button_select_in_explorer)
        self.__vbox_layout_internal.addSpacing(10)

        # кнопка Выбрать урок
        self.__push_button_start_test = QtWidgets.QPushButton()
        self.__push_button_start_test.setObjectName("push_button_start_test")
        self.__push_button_start_test.setEnabled(False)
        self.__push_button_start_test.clicked.connect(self.__start_test)
        self.__push_button_start_test.setFont(QtGui.QFont("Segoe UI", 14))
        self.__push_button_start_test.setText("Выбрать урок")
        self.__push_button_start_test.setFixedHeight(42)
        self.__push_button_start_test.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__vbox_layout_internal.addWidget(self.__push_button_start_test)

    def __list_view_row_changed(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        if current.isValid():
            self.__path_selected_course = self.__list_view_model.item(current.row())._path

            self.__push_button_start_test.setEnabled(True)
            self.__push_button_select_in_explorer.setText("Выбрать в проводнике")

    def __get_courses(self, path_courses: str) -> list[DataCourse]:
        files = [f for x in os.walk(path_courses) for f in glob(os.path.join(x[0], '*.xml'))]
        list_data_courses = list()

        for f in files:
            tree = ET.parse(f)
            root = tree.getroot()

            if (type := root.find("type")) != None and type.text == "IT Master course":
                name = root.find("name").text
                list_data_courses.append(DataCourse(name = name, path_course = f))

        return list_data_courses

    def __start_test(self):
        data_passage = DataPageHome(path_course = self.__path_selected_course)

        self.push_button_clicked_start_test.emit(data_passage)

    def __select_course_in_explorer(self):
        path_file_course = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор курса", self.__path_courses, "XML Файл (*.xml)")[0]

        if os.path.isfile(path_file_course):
            self.__path_selected_course = path_file_course 
            
            name_course = os.path.splitext(os.path.basename(self.__path_selected_course))[0]
            formated_name_course = QtGui.QFontMetrics.elidedText(
                QtGui.QFontMetrics(self.__push_button_select_in_explorer.font()),
                name_course, 
                QtCore.Qt.TextElideMode.ElideRight, 
                (self.__push_button_select_in_explorer.width() - (self.__push_button_select_in_explorer.iconSize().width()\
                    + (x := self.__push_button_select_in_explorer.contentsMargins()).left() + x.right())
                )
            )
            # + QtGui.QFontMetrics.boundingRect(self.__push_button_select_explorer.fontMetrics(), "—").width())

            self.__push_button_start_test.setEnabled(True)
            self.__list_view.clearSelection()
            self.__push_button_select_in_explorer.setText(formated_name_course)
