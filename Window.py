from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os
import enum
from ctypes.wintypes import LPRECT, MSG
import win32con
import win32gui
from src import win32utils
from src.c import LPNCCALCSIZE_PARAMS
from ctypes import cast

@enum.unique
class PropertyPages(enum.Enum):
    home_page = "home_page"
    test_page = "test_page"

class TitileBarWindow(QtWidgets.QWidget):
    """Рамка заголовка для окна"""
    window_close = QtCore.pyqtSignal()
    window_show_minimized = QtCore.pyqtSignal()
    window_show_maximized = QtCore.pyqtSignal()
    window_show_normal = QtCore.pyqtSignal()

    mouse_double_click = QtCore.pyqtSignal()
    mouse_press = QtCore.pyqtSignal()
    mouse_move = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, data_theme):
        super().__init__()

        self.__title = None
        self.__icon = None
        self.__window_type = QtCore.Qt.WindowType.WindowMinMaxButtonsHint
        self.__window_state = QtCore.Qt.WindowState.WindowNoState
        self.__mouse_pos = None

        self.__data_theme = data_theme

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)
        self.__vbox_layout_main.setSpacing(0)

        self.setLayout(self.__vbox_layout_main)

        # рамка заголовка
        self.__frame_header = QtWidgets.QFrame()
        self.__frame_header.setObjectName("frame_header")
        self.__frame_header.setFixedHeight(36)

        self.__vbox_layout_main.addWidget(self.__frame_header)

        # макет рамки заголовка
        self.__hbox_layout_header = QtWidgets.QHBoxLayout()
        self.__hbox_layout_header.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_header.setSpacing(0)

        self.__frame_header.setLayout(self.__hbox_layout_header)

        # рамка титла
        self.__frame_title = QtWidgets.QFrame()
        self.__frame_title.setObjectName("frame_title")

        self.__hbox_layout_header.addWidget(self.__frame_title)
        self.__hbox_layout_header.addStretch(1)

        # макет рамки титла
        self.__hbox_layout_title = QtWidgets.QHBoxLayout()
        self.__hbox_layout_title.setContentsMargins(5, 0, 0, 0)
        self.__hbox_layout_title.setSpacing(0)

        self.__frame_title.setLayout(self.__hbox_layout_title)

        # метка иконки
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_icon.setFixedSize(25, 25)

        self.__hbox_layout_title.addWidget(self.__label_icon)
        self.__hbox_layout_title.addSpacing(5)

        # метка титла
        self.__label_title = QtWidgets.QLabel()
        self.__label_title.setObjectName("label_title")
        self.__label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__label_title.setFont(QtGui.QFont("Segoe UI", 12))

        self.__hbox_layout_title.addWidget(self.__label_title)

        # рамка кнопок заголока
        self.__frame_header_buttons = QtWidgets.QFrame()
        self.__frame_header_buttons.setObjectName("frame_header_button")

        self.__hbox_layout_header.addWidget(self.__frame_header_buttons)

        # макет рамки кнопок заголока
        self.__hbox_header_buttons = QtWidgets.QHBoxLayout()
        self.__hbox_header_buttons.setContentsMargins(0, 0, 0, 0)
        self.__hbox_header_buttons.setSpacing(0)

        self.__frame_header_buttons.setLayout(self.__hbox_header_buttons)

        # кнопка свернуть
        self.__push_button_minimize = QtWidgets.QPushButton()
        self.__push_button_minimize.setObjectName("push_button_minimize")
        self.__push_button_minimize.clicked.connect(self.__press_push_button_minimize)
        self.__push_button_minimize.setFont(QtGui.QFont("Webdings", 9))
        self.__push_button_minimize.setText("0")
        self.__push_button_minimize.setFixedSize(58, 36)
        self.__push_button_minimize.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_minimize)

        # кнопка максимизировать / нормализировать
        self.__push_button_maximize = QtWidgets.QPushButton()
        self.__push_button_maximize.setObjectName("push_button_maximize")
        self.__push_button_maximize.clicked.connect(self.__press_push_button_maximize)
        self.__push_button_maximize.setFont(QtGui.QFont("Webdings", 9))
        self.__push_button_maximize.setText("1")
        self.__push_button_maximize.setFixedSize(58, 36)
        self.__push_button_maximize.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_maximize)

        # кнопка закрыть
        self.__push_button_close = QtWidgets.QPushButton()
        self.__push_button_close.setObjectName("push_button_close")
        self.__push_button_close.clicked.connect(self.__press_push_button_close)
        self.__push_button_close.setFont(QtGui.QFont("Webdings", 9))
        self.__push_button_close.setText("r")
        self.__push_button_close.setFixedSize(58, 36)
        self.__push_button_close.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_close)

        self.set_style_sheet()

    def __press_push_button_minimize(self):
        self.window_show_minimized.emit()

    def __press_push_button_maximize(self):
        if self.__window_state == QtCore.Qt.WindowState.WindowNoState:
            self.__push_button_maximize.setText("2")
            self.window_show_maximized.emit()
        else:
            self.__push_button_maximize.setText("1")
            self.window_show_normal.emit()

    def __press_push_button_close(self):
        self.window_close.emit()

    def set_icon(self, icon: QtGui.QPixmap):
        self.__icon = icon.scaled(25, 25, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
        self.__label_icon.setPixmap(self.__icon)

    def set_title(self, title: str):
        self.__title = title
        self.__label_title.setText(self.__title)
        self.update_title()

    def update_title(self, title: str = None):
        if title is None:
            title = self.__title

        width = self.__label_title.width() - self.__hbox_layout_title.getContentsMargins()[0]

        self.__label_title.setText(self.fontMetrics().elidedText(title, QtCore.Qt.TextElideMode.ElideRight, width))

    def window_type_changed(self, type: QtCore.Qt.WindowType):
        self.__window_type =type
        if self.__window_type & QtCore.Qt.WindowType.WindowMinimizeButtonHint:
            self.__push_button_minimize.show()
        else:
            self.__push_button_minimize.hide()

        if self.__window_type & QtCore.Qt.WindowType.WindowMaximizeButtonHint:
            self.__push_button_maximize.show()
        else:
            self.__push_button_maximize.hide()

    def window_state_changed(self, state: QtCore.Qt.WindowState):
        self.__window_state = state
        self.__push_button_maximize.setText("2" if self.__window_state == QtCore.Qt.WindowState.WindowMaximized else "1")

    def get_mouse_pos(self) -> QtCore.QPoint | None:
        return self.__mouse_pos

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse_double_click.emit()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__mouse_pos = event.scenePosition().toPoint()
            self.mouse_press.emit()

    def mouseReleaseEvent(self, event):
        self.__mouse_pos = None

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.__mouse_pos:
            pos = event.globalPosition().toPoint() - self.__mouse_pos
            self.mouse_move.emit(pos)

    def set_style_sheet(self):
        # рамка заголовка
        self.__frame_header.setStyleSheet("""
        #frame_header {
            background: %(background)s;
        } """ % self.__data_theme)

        # метка титла
        self.__label_title.setStyleSheet("""
        #label_title {
            color: %(color)s;
        } """ % self.__data_theme["label_title"])

        # кнопка свернуть
        temp_data_theme = {
            "background_normal": self.__data_theme["push_button"]["normal"]["background"],
            "color_normal": self.__data_theme["push_button"]["normal"]["color"], 
            "background_hover": self.__data_theme["push_button"]["hover"]["background"], 
            "color_hover": self.__data_theme["push_button"]["hover"]["color"],
            "background_press": self.__data_theme["push_button"]["press"]["background"], 
            "color_press": self.__data_theme["push_button"]["press"]["color"]
        }

        self.__push_button_minimize.setStyleSheet("""
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

        self.__push_button_maximize.setStyleSheet("""
        #push_button_maximize {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_maximize::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_maximize::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # кнопка закрыть программу
        temp_data_theme = {
            "background_normal": self.__data_theme["push_button_close"]["normal"]["background"],
            "color_normal": self.__data_theme["push_button_close"]["normal"]["color"], 
            "background_hover": self.__data_theme["push_button_close"]["hover"]["background"], 
            "color_hover": self.__data_theme["push_button_close"]["hover"]["color"],
            "background_press": self.__data_theme["push_button_close"]["press"]["background"], 
            "color_press": self.__data_theme["push_button_close"]["press"]["color"]
        }

        self.__push_button_close.setStyleSheet("""
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

        self.setProperty("selected", self.__selected)
        self.setProperty("page", PropertyPages.home_page.value)

        self.setObjectName("tool_button")
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.clicked.connect(self.press_tool_button)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.setIcon(self.__image)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setText(self.__text)
        self.setFont(QtGui.QFont("Segoe UI", 10))

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

        self.setProperty("selected", self.__selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def update_style_sheet(self, property: PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_button[page={PropertyPages.home_page.value}][selected="true"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["home_page"]["selected"]["background"]};
            color: {self.__data_theme["home_page"]["selected"]["color"]};
        }}
        #tool_button[page={PropertyPages.home_page.value}][selected="false"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["home_page"]["not_selected"]["background"]};
            color: {self.__data_theme["home_page"]["not_selected"]["color"]};
        }}

        #tool_button[page={PropertyPages.test_page.value}][selected="true"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["test_page"]["selected"]["background"]};
            color: {self.__data_theme["test_page"]["selected"]["color"]};
        }}
        #tool_button[page={PropertyPages.test_page.value}][selected="false"] {{ 
            padding: 0px;
            outline: 0;
            border-radius: 10px; 
            background: {self.__data_theme["test_page"]["not_selected"]["background"]};
            color: {self.__data_theme["test_page"]["not_selected"]["color"]};
        }} """)

class ToolBar(QtWidgets.QFrame):
    """Панель инструментов"""
    tool_button_home_page_cliced = QtCore.pyqtSignal()
    tool_button_results_cliced = QtCore.pyqtSignal()
    tool_button_test_cliced = QtCore.pyqtSignal()
    tool_button_settings_cliced = QtCore.pyqtSignal()
    tool_button_info_cliced = QtCore.pyqtSignal()

    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme
        self.__list_tool_buttons = list()

        self.setObjectName("tool_bar")
        self.setProperty("page", PropertyPages.home_page.value)

        # макет панели инструментов
        self.__vbox_layout_toolbar = QtWidgets.QVBoxLayout()
        self.__vbox_layout_toolbar.setContentsMargins(5, 5, 5, 5)
        self.__vbox_layout_toolbar.setSpacing(0)

        self.setLayout(self.__vbox_layout_toolbar)

        data_theme_tool_buttons = {
            PropertyPages.home_page.value: self.__data_theme["home_page"]["tool_button"],
            PropertyPages.test_page.value: self.__data_theme["test_page"]["tool_button"]
        }

        # кнопка Домашняя страница
        self.tool_button_home_page = ToolButtonToolbar(
            os.path.join(self.__path_images, r"home_page.png"), 
            "Домашняя\nстраница", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_home_page)
        self.tool_button_home_page.tool_button_clicked.connect(self.__press_tool_button_home_page)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_home_page)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Результаты
        self.tool_button_results = ToolButtonToolbar(
            os.path.join(self.__path_images, r"results.png"), 
            "Результаты", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_results)
        self.tool_button_results.tool_button_clicked.connect(self.__press_tool_button_results)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_results)
        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Тест
        self.tool_button_test = ToolButtonToolbar(
            os.path.join(self.__path_images, r"test.png"), 
            "Тест", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_test)
        self.tool_button_test.tool_button_clicked.connect(self.__press_tool_button_test)

        self.__vbox_layout_toolbar.addWidget(self.tool_button_test)
        self.__vbox_layout_toolbar.addStretch(1)

        # кнопка Настройка
        self.tool_button_settings = ToolButtonToolbar(
            os.path.join(self.__path_images, r"settings.png"),
            "Настройка", 
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_settings)
        self.tool_button_settings.tool_button_clicked.connect(self.__press_tool_button_settings)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_settings)

        self.__vbox_layout_toolbar.addSpacing(5)

        # кнопка Справка
        self.tool_button_info = ToolButtonToolbar(
            os.path.join(self.__path_images, r"info.png"),
            "Справка",
            data_theme_tool_buttons
        )
        self.__list_tool_buttons.append(self.tool_button_info)
        self.tool_button_info.tool_button_clicked.connect(self.__press_tool_button_info)
        self.__vbox_layout_toolbar.addWidget(self.tool_button_info)

        self.set_style_sheet()

    def __press_tool_button_home_page(self):
        self.tool_button_home_page_cliced.emit()

    def __press_tool_button_results(self):
        self.tool_button_results_cliced.emit()

    def __press_tool_button_test(self):
        self.tool_button_test_cliced.emit()

    def __press_tool_button_settings(self):
        self.tool_button_settings_cliced.emit()

    def __press_tool_button_info(self):
        self.tool_button_info_cliced.emit()

    def update_style_sheet(self, property: PropertyPages):
        self.setProperty("page", property.value)
        self.style().unpolish(self)
        self.style().polish(self)

        for i in self.__list_tool_buttons:
            i.update_style_sheet(property)

    def set_style_sheet(self):
        self.setStyleSheet(f"""
        #tool_bar[page={PropertyPages.home_page.value}] {{
            background: {self.__data_theme["home_page"]["background"]};
        }} 
        #tool_bar[page={PropertyPages.test_page.value}] {{
            background: {self.__data_theme["test_page"]["background"]};
        }} """ )

class Window(QtWidgets.QMainWindow):
    """Главное окно"""
    
    def __init__(self, path_images: dict, data_theme: dict):
        super().__init__()

        self.__path_images = path_images
        self.__data_theme = data_theme

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.setCentralWidget(self.__frame_main)

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)
        self.__vbox_layout_main.setSpacing(0)

        self.__frame_main.setLayout(self.__vbox_layout_main)

        # рамка с заголовком
        self.__title_bar_window = TitileBarWindow(data_theme = self.__data_theme["frame_header"])
        self.__vbox_layout_main.addWidget(self.__title_bar_window)

        # рамка для виджетов
        self.__frame_widgets = QtWidgets.QFrame()
        self.__frame_widgets.setObjectName("frame_widgets")

        self.__vbox_layout_main.addWidget(self.__frame_widgets)

        # макет рамки для виджетов
        self.__hbox_layout_widgets = QtWidgets.QHBoxLayout()
        self.__hbox_layout_widgets.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_widgets.setSpacing(0)

        self.__frame_widgets.setLayout(self.__hbox_layout_widgets)

        # панель инструментов
        self.toolbar = ToolBar(self.__path_images, self.__data_theme["frame_tool_bar"])
        self.add_widget(self.toolbar)

        # присоединения слотов к сигналам
        self.__title_bar_window.window_close.connect(self.close_window)
        self.__title_bar_window.window_show_maximized.connect(self.show_maximized)
        self.__title_bar_window.window_show_minimized.connect(self.show_minimized)
        self.__title_bar_window.window_show_normal.connect(self.show_normal)

        self.__title_bar_window.mouse_double_click.connect(self.__mouse_double_click)
        # self.__title_bar_window.mouse_move.connect(self.__mouse_move)
        self.__title_bar_window.mouse_press.connect(self.__start_system_move)

        self.set_style_sheet()

    def show_maximized(self):
        super().showMaximized()

    def show_minimized(self):
        super().showMinimized()

    def show_normal(self):
        super().showNormal()

    def changeEvent(self, event):
        if isinstance(event, QtGui.QWindowStateChangeEvent):
            self.__title_bar_window.window_state_changed(self.windowState())

    def resizeEvent(self, event):
        self.__title_bar_window.update_title()

    def close_window(self):
        sys.exit()

    def __mouse_double_click(self):
        if not self.__is_maxizeable() or not self.__is_resizable():
            return
        if super().isMaximized():
            super().showNormal()
        else:
            super().showMaximized()
   
    def __mouse_move(self, pos: QtCore.QPoint):
        if not super().isMaximized():
            super().move(pos)

    def __start_system_move(self):
        super().windowHandle().startSystemMove()
   
    def __is_maxizeable(self) -> bool:
        return super().windowFlags() & QtCore.Qt.WindowType.WindowMaximizeButtonHint

    def __is_minimizeable(self) -> bool:
        return super().windowFlags() & QtCore.Qt.WindowType.WindowMaximizeButtonHint

    def __is_resizable(self) -> bool:
        return super().windowFlags() & QtCore.Qt.WindowType.WindowMaximizeButtonHint

    def set_icon(self, icon: QtGui.QPixmap):
        self.__title_bar_window.set_icon(icon = icon)

    def set_title(self, title: str):
        self.__title_bar_window.set_title(title = title)

    def nativeEvent(self, e, message):
        msg = MSG.from_address(message.__int__())
        # check if it is message from Windows OS
        print(e, msg)
        if msg.hWnd:
            print(msg.message)
            # update cursor shape to resize/resize feature
            # get WM_NCHITTEST message
            # more info - https://learn.microsoft.com/ko-kr/windows/win32/inputdev/wm-nchittest
            if msg.message == win32con.WM_NCHITTEST:
                print(msg.message)
                if self.__is_resizable():
                    print(self.__is_resizable)
                    pos = QtGui.QCursor.pos()
                    x = pos.x() - self.x()
                    y = pos.y() - self.y()

                    w, h = self.width(), self.height()

                    left = x < 5
                    top = y < 5
                    right = x > w - 5
                    bottom = y > h - 5

                    # to support snap layouts
                    # more info - https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/apply-snap-layout-menu
                    # if win32gui.PtInRect((10, 10, 100, 100), (x, y)):
                    #     return True, win32con.HTMAXBUTTON

                    if top and left:
                        return True, win32con.HTTOPLEFT
                    elif top and right:
                        return True, win32con.HTTOPRIGHT
                    elif bottom and left:
                        return True, win32con.HTBOTTOMLEFT
                    elif bottom and right:
                        return True, win32con.HTBOTTOMRIGHT
                    elif left:
                        return True, win32con.HTLEFT
                    elif top:
                        return True, win32con.HTTOP
                    elif right:
                        return True, win32con.HTRIGHT
                    elif bottom:
                        return True, win32con.HTBOTTOM

            # maximize/minimize/full screen feature
            # get WM_NCCALCSIZE message
            # more info - https://learn.microsoft.com/ko-kr/windows/win32/winmsg/wm-nccalcsize
            elif msg.message == win32con.WM_NCCALCSIZE:
                if msg.wParam:
                    rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
                else:
                    rect = cast(msg.lParam, LPRECT).contents

                max_f = win32utils.isMaximized(msg.hWnd)
                full_f = win32utils.isFullScreen(msg.hWnd)

                # adjust the size of window
                if max_f and not full_f:
                    thickness = win32utils.getResizeBorderThickness(msg.hWnd)
                    rect.top += thickness
                    rect.left += thickness
                    rect.right -= thickness
                    rect.bottom -= thickness

                # for auto-hide taskbar
                if (max_f or full_f) and win32utils.Taskbar.isAutoHide():
                    position = win32utils.Taskbar.getPosition(msg.hWnd)
                    if position == win32utils.Taskbar.LEFT:
                        rect.top += win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.BOTTOM:
                        rect.bottom -= win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.LEFT:
                        rect.left += win32utils.Taskbar.AUTO_HIDE_THICKNESS
                    elif position == win32utils.Taskbar.RIGHT:
                        rect.right -= win32utils.Taskbar.AUTO_HIDE_THICKNESS

                result = 0 if not msg.wParam else win32con.WVR_REDRAW
                return True, result
            elif msg.message == win32con.WM_SETTINGCHANGE:
                if self.__detect_theme_flag:
                    self.__setCurrentWindowsTheme()
            # TODO temporary measurement
            # this is just a inevitable workaround
            elif msg.message == win32con.WM_STYLECHANGING:
                self._resizable = not self.isFullScreen()
                self._pressToMove = not self.isFullScreen()
        return super().nativeEvent(e, message)

    def add_widget(self, widget: QtWidgets.QWidget):
        self.__hbox_layout_widgets.addWidget(widget)

    def set_style_sheet(self):
        # рамка для виджетов
        self.__frame_widgets.setStyleSheet("""
        #frame_widgets {
            background: %(background)s;
        } """ % self.__data_theme["frame_widgets"])
