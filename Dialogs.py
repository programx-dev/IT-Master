from PyQt6 import QtCore, QtGui, QtWidgets
import Window
import re
import os
import json
from glob import glob
from dataclasses import dataclass
import enum
import typing

class ButtonRole(enum.Enum):
    accept = 0
    reject = 1
    
@dataclass
class DataTheme:
    name: str
    path_theme: str

@dataclass
class DataSettings:
    path_theme: str
    amount_records: int

class Dialog(Window.Dialog):
    """Настраиваемое диалоговое окно"""
    
    def __init__(self):
        self.__icon = None
        self.__text = None
        self.__description = None
        self.__list_push_buttons = list()
        self.__defaul_push_button = None
        self.__value = None
        self.__event_loop = None

        super().__init__()
        self.setObjectName("dialog")
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

    def __exit_window(self):
        if self.__event_loop:
            self.__event_loop.exit()
        self.close()
        
    def close_window(self):
        if self.__event_loop != None:
            self.__event_loop.exit()

        super().close_window()

    def run_modal(self) -> ButtonRole | typing.Any:
        self.__event_loop = QtCore.QEventLoop()
        self.show()
        self.__event_loop.exec()
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
            self.close()

    def get_value(self) -> ButtonRole | typing.Any:
        return self.__value

    def add_push_button(self, text: str, role: ButtonRole | typing.Any = None, default: bool = False):
        push_button = QtWidgets.QPushButton()
        push_button.setObjectName("push_button_dialog")
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

        # push_button.setStyleSheet(f"""
        # QPushButton {{
        #     border: none;
        #     outline: 0;
        #     padding-left: 15px;
        #     padding-right: 15px;
        #     border-radius: 5px; 
        #     background: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
        #     color: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
        # }} 
        # QPushButton:default {{
        #     background: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
        #     color: {self.__data_theme["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
        # }}""")

        if self.__hbox_layout_push_buttons.count() > 0:
            self.__hbox_layout_push_buttons.addSpacing(10)
        self.__hbox_layout_push_buttons.addWidget(push_button)

class DialogAbout(Window.Dialog):
    """Диалоговое окно О программе"""
    
    def __init__(self, pixmap: QtGui.QPixmap):
        self.__pixmap = pixmap

        super().__init__()
        self.setObjectName("dialog_about")
        super().set_window_flags(QtCore.Qt.WindowType.WindowCloseButtonHint)
        super().setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        super().set_resizeable(False)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")
        self.__frame_main.setFixedWidth(340)

        self.add_widget(self.__frame_main)

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(15, 15, 15, 15)

        self.__frame_main.setLayout(self.__vbox_layout_main)

        # макет иконки и названия программы, версии
        self.__hbox_layout_icon_info = QtWidgets.QHBoxLayout()
        self.__hbox_layout_icon_info.setSpacing(0)
        self.__hbox_layout_icon_info.setContentsMargins(0, 0, 0, 0)

        self.__vbox_layout_main.addLayout(self.__hbox_layout_icon_info)
        self.__vbox_layout_main.addSpacing(10)

        # метка с иконкой
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setFixedSize(64, 64)

        self.__label_icon.setPixmap(self.__pixmap.scaled(64, 64, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation))

        self.__hbox_layout_icon_info.addWidget(self.__label_icon)

        # макет названия программы и версии
        self.__vbox_layout_info = QtWidgets.QVBoxLayout()
        self.__vbox_layout_info.setSpacing(0)
        self.__vbox_layout_info.setContentsMargins(0, 0, 0, 0)

        self.__hbox_layout_icon_info.addLayout(self.__vbox_layout_info)

        # метка с названием программы
        self.__label_name = QtWidgets.QLabel()
        self.__label_name.setObjectName("label_name")
        self.__label_name.setText("IT Master")
        self.__label_name.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__vbox_layout_info.addWidget(self.__label_name)

        # метка версии
        self.__label_version = QtWidgets.QLabel()
        self.__label_version.setObjectName("label_version")
        self.__label_version.setFont(QtGui.QFont("Segoe UI", 11))
        self.__label_version.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.__vbox_layout_info.addWidget(self.__label_version)

        # метка о программе
        self.__label_about  = QtWidgets.QLabel()
        self.__label_about.setObjectName("label_about")
        self.__label_about.setFont(QtGui.QFont("Segoe UI", 11))
        self.__label_about.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__label_about.setWordWrap(True)
        self.__label_about.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__vbox_layout_main.addWidget(self.__label_about)
        self.__vbox_layout_main.addSpacing(10)

        # кнопка Ок
        self.__push_button_accept = QtWidgets.QPushButton()
        self.__push_button_accept.setObjectName("push_button_accept")
        self.__push_button_accept.setText("ОК")
        self.__push_button_accept.setFont(QtGui.QFont("Segoe UI", 11))
        self.__push_button_accept.setFixedHeight(28)
        self.__push_button_accept.setMinimumWidth(75)
        self.__push_button_accept.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.__push_button_accept.setDefault(True)
        self.__push_button_accept.clicked.connect(self.__exit_window)

        self.__vbox_layout_main.addWidget(self.__push_button_accept)
        self.__vbox_layout_main.setAlignment(self.__push_button_accept, QtCore.Qt.AlignmentFlag.AlignRight)

        # подключение слотов к сигналам
        self.title_bar_window.window_close.connect(self.__exit_window)

    def close_window(self):
        if self.__event_loop != None:
            self.__event_loop.exit()

        super().close_window()

    def set_version(self, version: str):
        self.__label_version.setText(version)

    def set_text_about(self, text_about: str):
        self.__label_about.setText(text_about)

    def __exit_window(self):
        if self.__event_loop:
            self.__event_loop.exit()
        self.close()

    def run_modal(self):
        self.__event_loop = QtCore.QEventLoop()
        self.show()
        self.__event_loop.exec()
        self.close()

class DialogSettings(Window.Dialog):
    """Диалоговое окно Настройка"""
    push_button_clear_clicked = QtCore.pyqtSignal()
    
    def __init__(self, dir_theme: str, data_settings: DataSettings, path_images: str):
        self.__data_settings = data_settings
        self.__dir_theme = dir_theme
        self.__path_images = path_images

        super().__init__()
        self.setObjectName("dialog_settings")
        super().set_window_flags(QtCore.Qt.WindowType.WindowCloseButtonHint)
        super().setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        super().set_resizeable(False)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")
        self.__frame_main.setFixedWidth(340)

        self.add_widget(self.__frame_main)

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setSpacing(0)
        self.__vbox_layout_main.setContentsMargins(10, 5, 10, 10)

        self.__frame_main.setLayout(self.__vbox_layout_main)

        # виджет с вкладками
        self.__tab_widget_settings = QtWidgets.QTabWidget()
        self.__tab_widget_settings.setObjectName("tab_widget_settings")
        self.__tab_widget_settings.setFont(QtGui.QFont("Segoe UI", 11))
        self.__tab_widget_settings.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__vbox_layout_main.addWidget(self.__tab_widget_settings)
        self.__vbox_layout_main.addSpacing(10)

        # страница настроек оформления
        self.__page_settings_theme = QtWidgets.QFrame()
        self.__page_settings_theme.setObjectName("page_settings_theme")

        self.__tab_widget_settings.addTab(self.__page_settings_theme, "Оформление")

        # макет страницы настроек цветовой темы
        self.__vbox_layout_settings_theme = QtWidgets.QVBoxLayout()
        self.__vbox_layout_settings_theme.setSpacing(0)
        self.__vbox_layout_settings_theme.setContentsMargins(5, 5, 0, 5)

        self.__page_settings_theme.setLayout(self.__vbox_layout_settings_theme)

        # список цветовых тем
        self.__list_view = QtWidgets.QListView()
        self.__list_view.setObjectName("list_view")
        self.__list_view.setFont(QtGui.QFont("Segoe UI", 13))
        self.__list_view.setIconSize(QtCore.QSize(20, 20))
        self.__list_view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__list_view_model = QtGui.QStandardItemModel()
        self.__list_view.setModel(self.__list_view_model) 

        for data_theme in self.__get_themes(self.__dir_theme):
            item = QtGui.QStandardItem(data_theme.name)
            item._path = data_theme.path_theme
            self.__list_view_model.appendRow(item)

            item.setData(QtGui.QIcon(os.path.join(self.__path_images, r"pallete.png")), QtCore.Qt.ItemDataRole.DecorationRole)
        
        self.__list_view.selectionModel().currentChanged.connect(self.__list_view_row_changed)

        self.__vbox_layout_settings_theme.addWidget(self.__list_view)

         # макет с кнопками
        self.__hbox_layout_push_buttons = QtWidgets.QHBoxLayout()
        self.__hbox_layout_push_buttons.setSpacing(0)
        self.__hbox_layout_push_buttons.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_push_buttons.addStretch(1)

        self.__vbox_layout_main.addLayout(self.__hbox_layout_push_buttons)

        # кнопка Отмена
        self.__push_button_reject = QtWidgets.QPushButton()
        self.__push_button_reject.setObjectName("push_button_reject")
        self.__push_button_reject.setText("Отмена")
        self.__push_button_reject.setFont(QtGui.QFont("Segoe UI", 11))
        self.__push_button_reject.setFixedHeight(28)
        self.__push_button_reject.setMinimumWidth(75)
        self.__push_button_reject.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.__push_button_reject.clicked.connect(self.__reject)

        self.__hbox_layout_push_buttons.addWidget(self.__push_button_reject)
        self.__hbox_layout_push_buttons.addSpacing(10)
        self.__hbox_layout_push_buttons.setAlignment(self.__push_button_reject, QtCore.Qt.AlignmentFlag.AlignRight)

        # кнопка Ок
        self.__push_button_accept = QtWidgets.QPushButton()
        self.__push_button_accept.setObjectName("push_button_accept")
        self.__push_button_accept.setText("ОК")
        self.__push_button_accept.setFont(QtGui.QFont("Segoe UI", 11))
        self.__push_button_accept.setFixedHeight(28)
        self.__push_button_accept.setMinimumWidth(75)
        self.__push_button_accept.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.__push_button_accept.setDefault(True)
        self.__push_button_accept.clicked.connect(self.__exit_window)
        self.__push_button_accept.setEnabled(False)

        self.__hbox_layout_push_buttons.addWidget(self.__push_button_accept)
        self.__hbox_layout_push_buttons.setAlignment(self.__push_button_accept, QtCore.Qt.AlignmentFlag.AlignRight)

        # выделить текущую тему если она есть в списке
        for i in range(self.__list_view_model.rowCount()):
            if self.__list_view_model.item(i)._path == self.__data_settings.path_theme:
                self.__list_view.setCurrentIndex(self.__list_view_model.item(i).index())

        # страница настроек записии результатов прохождения теста
        self.__page_settings_history = QtWidgets.QFrame()
        self.__page_settings_history.setObjectName("page_settings_history")

        self.__tab_widget_settings.addTab(self.__page_settings_history, "История")

        # макет страницы настроек цветовой темы
        self.__vbox_layout_settings_history = QtWidgets.QVBoxLayout()
        self.__vbox_layout_settings_history.setSpacing(0)
        self.__vbox_layout_settings_history.setContentsMargins(7, 7, 7, 7)

        self.__page_settings_history.setLayout(self.__vbox_layout_settings_history)

        # метка заголовка истории
        self.__label_header_history = QtWidgets.QLabel()
        self.__label_header_history.setObjectName("label_header_history")
        self.__label_header_history.setFont(QtGui.QFont("Segoe UI", 13))
        self.__label_header_history.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__label_header_history.setWordWrap(True)
        self.__label_header_history.setText("Максимальное количество записей результатов прохождений тестов (от 1 до 1000)")

        self.__vbox_layout_settings_history.addWidget(self.__label_header_history)
        self.__vbox_layout_settings_history.addSpacing(10)

        # виджет ввода целых чисел
        self.__spin_box_amount_records = QtWidgets.QSpinBox()
        self.__spin_box_amount_records.setObjectName("spin_box_amount_records")
        self.__spin_box_amount_records.setRange(1, 1000)
        self.__spin_box_amount_records.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.__spin_box_amount_records.valueChanged.connect(self.__spin_box_amount_records_value_changed)
        self.__spin_box_amount_records.setFont(QtGui.QFont("Segoe UI", 12))
        self.__spin_box_amount_records.setValue(self.__data_settings.amount_records)
        self.__spin_box_amount_records.setFixedHeight(36)

        self.__vbox_layout_settings_history.addWidget(self.__spin_box_amount_records)
        self.__vbox_layout_settings_history.addSpacing(10)

        # кнопка Очистить историю
        self.__push_button_clear = QtWidgets.QPushButton()
        self.__push_button_clear.setObjectName("push_button_clear")
        self.__push_button_clear.setText("Очистить историю")
        self.__push_button_clear.setFont(QtGui.QFont("Segoe UI", 11))
        self.__push_button_clear.setFixedHeight(28)
        self.__push_button_clear.setMinimumWidth(75)
        self.__push_button_clear.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.__push_button_clear.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__push_button_clear.clicked.connect(self.__push_button_clear_press)

        self.__vbox_layout_settings_history.addWidget(self.__push_button_clear)
        self.__vbox_layout_settings_history.addStretch(1)

        # подключение слотов к сигналам
        self.title_bar_window.window_close.connect(self.__exit_window)

    def __push_button_clear_press(self):
        self.push_button_clear_clicked.emit()

    def __reject(self):
        self.__data_settings.path_theme = None
        self.__exit_window()

    def close_window(self):
        self.__data_settings.path_theme = None
        if self.__event_loop != None:
            self.__event_loop.exit()

        super().close_window()

    def __list_view_row_changed(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        if current.isValid():
            self.__data_settings.path_theme = self.__list_view_model.item(current.row())._path

            self.__push_button_accept.setEnabled(True)

    def __spin_box_amount_records_value_changed(self):
        self.__data_settings.amount_records = self.__spin_box_amount_records.value()

    def __get_themes(self, path_themes: str) -> list[DataTheme]:
        files = [f for x in os.walk(path_themes) for f in glob(os.path.join(x[0], '*.json'))]
        list_data_themes = list()

        for f in files:
            with open(f, "r", encoding = "utf-8") as file_theme:
                data_theme = json.load(file_theme)
                name = data_theme["name"]
                list_data_themes.append(DataTheme(name = name, path_theme = f))
        
        return list_data_themes

    def get_result(self) -> DataSettings:
        return self.__data_settings

    def run_modal(self):
        self.__event_loop = QtCore.QEventLoop()
        self.show()
        self.__event_loop.exec()
        return self.get_result()

    def __exit_window(self):
        if self.__event_loop:
            self.__event_loop.exit()
        self.close()
