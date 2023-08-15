from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os
import enum

class Direction(enum.Enum):
    Left = 0
    Top = 1
    Right = 2
    Bottom = 3
    LeftTop = 4
    RightTop = 5
    LeftBottom = 6
    RightBottom = 7

class LabelMinimizeable(QtWidgets.QLabel):
    """Метка без органичений минимального размера"""

    def minimumSizeHint(self):
        return QtCore.QSize(0, super().minimumSizeHint().height())

class TitileBarWindow(QtWidgets.QWidget):
    """Рамка заголовка для окна"""
    window_close = QtCore.pyqtSignal()
    window_show_minimized = QtCore.pyqtSignal()
    window_show_maximized = QtCore.pyqtSignal()
    window_show_normal = QtCore.pyqtSignal()

    mouse_double_click = QtCore.pyqtSignal()
    mouse_press = QtCore.pyqtSignal()
    mouse_move = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self):
        super().__init__()
        self.setObjectName("titile_bar_window")

        self.__title = None
        self.__icon = None
        self.__window_type = QtCore.Qt.WindowType.WindowMinMaxButtonsHint
        self.__window_state = QtCore.Qt.WindowState.WindowNoState
        self.__mouse_pos = None

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
        # self.__hbox_layout_header.addStretch(1)

        # макет рамки титла
        self.__hbox_layout_title = QtWidgets.QHBoxLayout()
        self.__hbox_layout_title.setContentsMargins(5, 0, 0, 0)
        self.__hbox_layout_title.setSpacing(0)

        self.__hbox_layout_title.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

        self.__frame_title.setLayout(self.__hbox_layout_title)

        # метка иконки
        self.__label_icon = QtWidgets.QLabel()
        self.__label_icon.setObjectName("label_icon")
        self.__label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label_icon.setFixedSize(25, 25)

        self.__hbox_layout_title.addWidget(self.__label_icon)
        self.__hbox_layout_title.addSpacing(5)

        # метка титла
        self.__label_title = LabelMinimizeable()
        self.__label_title.setObjectName("label_title")
        self.__label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.__label_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.__label_title.setFont(QtGui.QFont("Segoe UI", 12))

        self.__label_title.setMinimumWidth(0)

        self.__hbox_layout_title.addWidget(self.__label_title)

        # рамка кнопок заголока
        self.__frame_header_buttons = QtWidgets.QFrame()
        self.__frame_header_buttons.setObjectName("frame_header_button")

        self.__hbox_layout_header.addWidget(self.__frame_header_buttons)
        self.__hbox_layout_header.setAlignment(self.__frame_header_buttons, QtCore.Qt.AlignmentFlag.AlignRight)

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
        self.__push_button_minimize.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_minimize)

        # кнопка максимизировать / нормализировать
        self.__push_button_maximize = QtWidgets.QPushButton()
        self.__push_button_maximize.setObjectName("push_button_maximize")
        self.__push_button_maximize.clicked.connect(self.__press_push_button_maximize)
        self.__push_button_maximize.setFont(QtGui.QFont("Webdings", 9))
        self.__push_button_maximize.setText("1")
        self.__push_button_maximize.setFixedSize(58, 36)
        self.__push_button_maximize.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_maximize)

        # кнопка закрыть
        self.__push_button_close = QtWidgets.QPushButton()
        self.__push_button_close.setObjectName("push_button_close")
        self.__push_button_close.clicked.connect(self.__press_push_button_close)
        self.__push_button_close.setFont(QtGui.QFont("Webdings", 9))
        self.__push_button_close.setText("r")
        self.__push_button_close.setFixedSize(58, 36)
        self.__push_button_close.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.__hbox_header_buttons.addWidget(self.__push_button_close)

        # self.set_style_sheet()

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

    def set_icon(self, icon: QtGui.QIcon):
        self.__icon = icon.pixmap(25, 25)
        self.__label_icon.setPixmap(self.__icon)

    def set_window_title(self, title: str):
        self.__title = title
        self.__label_title.setText(self.__title)
        self.update_title()

    def update_title(self, title: str = None):
        if title is None:
            title = self.__title

        width = self.__label_title.width() - self.__hbox_layout_title.getContentsMargins()[0]
        title = self.__label_title.fontMetrics().elidedText(title, QtCore.Qt.TextElideMode.ElideRight, width)
        if self.__label_title.text() != title:
            self.__label_title.setText(title)

    def window_type_changed(self, type: QtCore.Qt.WindowType):
        self.__window_type = type
        if self.__window_type & QtCore.Qt.WindowType.WindowMinimizeButtonHint:
            self.__push_button_minimize.show()
        else:
            self.__push_button_minimize.hide()

        if self.__window_type & QtCore.Qt.WindowType.WindowMaximizeButtonHint:
            self.__push_button_maximize.show()
        else:
            self.__push_button_maximize.hide()

        if self.__window_type & QtCore.Qt.WindowType.WindowCloseButtonHint:
            self.__push_button_close.show()
        else:
            self.__push_button_close.hide()

    def window_state_changed(self, state: QtCore.Qt.WindowState):
        self.__window_state = state
        self.__push_button_maximize.setText("2" if self.__window_state == QtCore.Qt.WindowState.WindowMaximized else "1")

    def get_mouse_pos(self) -> QtCore.QPoint | None:
        return self.__mouse_pos

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        super().enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse_double_click.emit()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__mouse_pos = event.scenePosition().toPoint()
            self.mouse_press.emit()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.__mouse_pos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.__mouse_pos:
            pos = event.globalPosition().toPoint() - self.__mouse_pos
            self.mouse_move.emit(pos)
        event.accept()

    def paintEvent(self, event):
        self.update_title()
        super().paintEvent(event)

    def set_style_sheet(self):
        # рамка заголовка
        self.__frame_header.setStyleSheet(f"""
        #frame_header {{
            background: {self.__data_theme["background"]};
        }} """)

        # метка титла
        self.__label_title.setStyleSheet(f"""
        #label_title {{
            background: transparent;
            color: {self.__data_theme["label_title"]["color"]};
        }} """)

        self.__push_button_minimize.setStyleSheet(f"""
        #push_button_minimize {{
            outline: 0;
            border: none;
            background: {self.__data_theme["push_button_minimize"]["normal"]["background"]}; 
            color: {self.__data_theme["push_button_minimize"]["normal"]["color"]};
        }}
        #push_button_minimize::hover {{
            background: {self.__data_theme["push_button_minimize"]["hover"]["background"]}; 
            color: {self.__data_theme["push_button_minimize"]["hover"]["color"]};
        }}
        #push_button_minimize::pressed {{
            background: {self.__data_theme["push_button_minimize"]["pressed"]["background"]}; 
            color: {self.__data_theme["push_button_minimize"]["pressed"]["color"]}; 
        }} """)

        self.__push_button_maximize.setStyleSheet(f"""
        #push_button_maximize {{
            outline: 0;
            border: none;
            background: {self.__data_theme["push_button_maximize"]["normal"]["background"]}; 
            color: {self.__data_theme["push_button_maximize"]["normal"]["color"]};
        }}
        #push_button_maximize::hover {{
            background: {self.__data_theme["push_button_maximize"]["hover"]["background"]}; 
            color: {self.__data_theme["push_button_maximize"]["hover"]["color"]};
        }}
        #push_button_maximize::pressed {{
            background: {self.__data_theme["push_button_maximize"]["pressed"]["background"]}; 
            color: {self.__data_theme["push_button_maximize"]["pressed"]["color"]}; 
        }} """)

        self.__push_button_close.setStyleSheet(f"""
        #push_button_close {{
            outline: 0;
            border: none;
            background: {self.__data_theme["push_button_close"]["normal"]["background"]}; 
            color: {self.__data_theme["push_button_close"]["normal"]["color"]};
        }}
        #push_button_close::hover {{
            background: {self.__data_theme["push_button_close"]["hover"]["background"]}; 
            color: {self.__data_theme["push_button_close"]["hover"]["color"]};
        }}
        #push_button_close::pressed {{
            background: {self.__data_theme["push_button_close"]["pressed"]["background"]}; 
            color: {self.__data_theme["push_button_close"]["pressed"]["color"]}; 
        }} """)

class AbstractWindow(QtWidgets.QWidget):
    """Класс для абстрактного окна"""
    Margins = 5
    
    def __init__(self):
        super().__init__()
        
        self.__pressed  = False
        self.__mouse_pos = None
        self.__direction = None
        self.__resizeable = True

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setMinimumSize(0, 0)

        # макет окна
        self.__layout_window = QtWidgets.QVBoxLayout()
        self.__layout_window.setSpacing(0)
        self.__layout_window.setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)

        self.setLayout(self.__layout_window)

        # главная рамка
        self.__frame_main = QtWidgets.QFrame()
        self.__frame_main.setObjectName("frame_main")

        self.__layout_window.addWidget(self.__frame_main)

        # тень
        self.__shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.__shadow.setBlurRadius(17)
        self.__shadow.setOffset(0, 0)
        self.__shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.__frame_main.setGraphicsEffect(self.__shadow)

        # главный макет
        self.__vbox_layout_main = QtWidgets.QVBoxLayout()
        self.__vbox_layout_main.setContentsMargins(0, 0, 0, 0)
        self.__vbox_layout_main.setSpacing(0)

        self.__frame_main.setLayout(self.__vbox_layout_main)

        # рамка с заголовком
        self.title_bar_window = TitileBarWindow()
        self.__vbox_layout_main.addWidget(self.title_bar_window)

        # рамка для виджетов
        self.__frame_widgets = QtWidgets.QFrame()
        self.__frame_widgets.setObjectName("frame_widgets")
        self.__frame_widgets.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.__frame_widgets.installEventFilter(self)

        self.__vbox_layout_main.addWidget(self.__frame_widgets)

        # макет рамки для виджетов
        self.__hbox_layout_widgets = QtWidgets.QHBoxLayout()
        self.__hbox_layout_widgets.setContentsMargins(0, 0, 0, 0)
        self.__hbox_layout_widgets.setSpacing(0)

        self.__frame_widgets.setLayout(self.__hbox_layout_widgets)

        # присоединения слотов к сигналам
        self.title_bar_window.window_close.connect(self.close_window)
        self.title_bar_window.window_show_maximized.connect(self.show_maximized)
        self.title_bar_window.window_show_minimized.connect(self.show_minimized)
        self.title_bar_window.window_show_normal.connect(self.show_normal)

        self.title_bar_window.mouse_double_click.connect(self.__mouse_double_click)
        # self.__title_bar_window.mouse_move.connect(self.__move)
        self.title_bar_window.mouse_press.connect(self.__start_system_move)
        
        self.windowTitleChanged.connect(self.__title_chaged)
        self.windowIconChanged.connect(self.__icon_changed)

        # self.__set_style_sheet()

    def __title_chaged(self, title: str):
        self.title_bar_window.set_window_title(title)

    def __icon_changed(self, icon: QtGui.QIcon):
        self.title_bar_window.set_icon(icon)

    def set_window_flags(self, flags: QtCore.Qt.WindowType):
        self.title_bar_window.window_type_changed(QtCore.Qt.WindowType.FramelessWindowHint | flags)
        super().setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | flags)

    def show_maximized(self):
        self.__layout_window.setContentsMargins(0, 0, 0, 0)
        super().showMaximized()

    def show_minimized(self):
        super().showMinimized()

    def show_normal(self):
        self.__layout_window.setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)
        super().showNormal()

    def __move(self, pos: QtCore.QPoint):
        if self.windowState() == QtCore.Qt.WindowState.WindowMaximized or self.windowState() == QtCore.Qt.WindowState.WindowFullScreen:
            return
        super().move(pos)

    def changeEvent(self, event):
        if isinstance(event, QtGui.QWindowStateChangeEvent):
            self.title_bar_window.window_state_changed(self.windowState())
        super().changeEvent(event)

    def resizeEvent(self, event):
        if hasattr(self, "__title_bar_window"):
            self.title_bar_window.update_title()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__mouse_pos = event.pos()
            self.__pressed = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.__mouse_pos = None
        self.__pressed = False
        self.__direction = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.__is_resizable():
            return
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.__direction = None
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
            return
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.__pressed:
            self.__resize_window(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # Верхний левый угол
            self.__direction = Direction.LeftTop
            self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # Нижний правый угол
            self.__direction = Direction.RightBottom
            self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # верхний правый угол
            self.__direction = Direction.RightTop
            self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # Нижний левый угол
            self.__direction = Direction.LeftBottom
            self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # Влево
            self.__direction = Direction.Left
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # Право
            self.__direction = Direction.Right
            self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # выше
            self.__direction = Direction.Top
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # ниже
            self.__direction = Direction.Bottom
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)

    def __resize_window(self, pos):
        if self.__direction == None:
            return
        mpos = pos - self.__mouse_pos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = super().geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self.__direction == Direction.LeftTop:          
            if w - xPos >= super().minimumWidth() and w - xPos <= super().maximumWidth():
                x += xPos
                w -= xPos
            elif w - xPos < super().minimumWidth():
                x -= super().minimumWidth() - w
                w = super().minimumWidth()
            else: 
                x -= super().maximumWidth() - w
                w = super().maximumWidth()

            if h - yPos >= super().minimumHeight() and h - yPos <= super().maximumHeight():
                y += yPos
                h -= yPos
            elif h - yPos < super().minimumHeight(): 
                y -= super().minimumHeight() - h
                h = super().minimumHeight()
            else: 
                y -= super().maximumHeight() - h
                h = super().maximumHeight()
        
        elif self.__direction == Direction.RightBottom: 
            if w + xPos >= super().minimumWidth() and w + xPos <= super().maximumWidth():
                w += xPos
                self.__mouse_pos.setX(w)
            elif w + xPos < super().minimumWidth():
                w = super().minimumWidth()
                self.__mouse_pos.setX(super().minimumWidth())
            else:
                w = super().maximumWidth()
                self.__mouse_pos.setX(super().maximumWidth())

            if h + yPos >= super().minimumHeight() and h + yPos <= super().maximumHeight():
                h += yPos
                self.__mouse_pos.setY(h)
            elif h + yPos < super().minimumHeight():
                h = super().minimumHeight()
                self.__mouse_pos.setY(h)
            else:
                h = super().maximumHeight()
                self.__mouse_pos.setY(h)
        
        elif self.__direction == Direction.RightTop:
            if w + xPos >= super().minimumWidth() and w + xPos <= super().maximumWidth():
                w += xPos
                self.__mouse_pos.setX(pos.x())
            elif w + xPos < super().minimumWidth():
                w = super().minimumWidth()
                self.__mouse_pos.setX(w)
            else:
                w = super().maximumWidth()
                self.__mouse_pos.setX(w)

            if h - yPos >= super().minimumHeight() and h - yPos <= super().maximumHeight():
                y += yPos
                h -= yPos
            elif h - yPos < super().minimumHeight():
                y -= super().minimumHeight() - h
                h = super().minimumHeight()
            else:
                y -= super().maximumHeight() - h
                h = super().maximumHeight()

        elif self.__direction == Direction.LeftBottom:     
            if w - xPos >= super().minimumWidth() and w - xPos <= super().maximumWidth():
                x += xPos
                w -= xPos
            elif w - xPos < super().minimumWidth():
                x -= super().minimumWidth() - w
                w = super().minimumWidth()
            else:
                x -= super().maximumWidth() - w
                w = super().maximumWidth()

            if h + yPos >= super().minimumHeight() and h + yPos <= super().maximumHeight():
                h += yPos
                self.__mouse_pos.setY(pos.y())
            elif h + yPos < super().minimumHeight():
                h += super().minimumHeight() - h
                self.__mouse_pos.setY(h)
            else:
                h += super().maximumHeight() - h
                self.__mouse_pos.setY(h)

        elif self.__direction == Direction.Left:            
            if w - xPos >= super().minimumWidth() and w - xPos <= super().maximumWidth():
                x += xPos
                w -= xPos
            elif w - xPos < super().minimumWidth():
                x -= super().minimumWidth() - w
                w = super().minimumWidth()
            else:
                x -= super().maximumWidth() - w
                w = super().maximumWidth()
            
        elif self.__direction == Direction.Right:           
            if w + xPos >= super().minimumWidth() and w + xPos <= super().maximumWidth():
                w += xPos
                self.__mouse_pos = pos
            elif w + xPos < super().minimumWidth():
                w = super().minimumWidth()
                self.__mouse_pos.setX(w)
            else:
                w = super().maximumWidth()
                self.__mouse_pos.setX(w)
            
        elif self.__direction == Direction.Top:             
            if h - yPos >= super().minimumHeight() and h - yPos <= super().maximumHeight():
                y += yPos
                h -= yPos
            elif h - yPos < super().minimumHeight():
                y -= super().minimumHeight() - h
                h = super().minimumHeight()
            else:
                y -= super().maximumHeight() - h
                h = super().maximumHeight()
            
        elif self.__direction == Direction.Bottom:          
            if h + yPos >= super().minimumHeight() and h + yPos <= super().maximumHeight():
                h += yPos
                self.__mouse_pos = pos
            elif h + yPos < super().minimumHeight():
                h = super().minimumHeight()
                self.__mouse_pos.setY(h)
            else:
                h = super().maximumHeight()
                self.__mouse_pos.setY(h)
            
        self.setGeometry(x, y, w, h)

    def eventFilter(self, obj, event):
        if isinstance(event, QtGui.QEnterEvent):
            self.__direction = None
            self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        return super().eventFilter(obj, event)

    def close_window(self):
        self.close()

    def set_resizeable(self, resizeable: bool):
        self.__resizeable = resizeable

    def __mouse_double_click(self):
        if not self.__is_maxizeable() or not self.__is_resizable():
            return
        if super().isMaximized():
            super().showNormal()
        else:
            super().showMaximized()
   
    def __start_system_move(self):
        if super().windowState() == QtCore.Qt.WindowState.WindowMaximized or super().windowState() == QtCore.Qt.WindowState.WindowFullScreen:
            return
        super().windowHandle().startSystemMove()
   
    def __is_maxizeable(self) -> bool:
        return super().windowFlags() & QtCore.Qt.WindowType.WindowMaximizeButtonHint

    def __is_minimizeable(self) -> bool:
        return super().windowFlags() & QtCore.Qt.WindowType.WindowMinimizeButtonHint

    def __is_resizable(self) -> bool:
        return super().minimumSize() != super().maximumSize() and self.__resizeable

    def set_window_icon(self, icon: QtGui.QIcon):
        self.title_bar_window.set_icon(icon = icon)

    def set_window_title(self, title: str):
        self.title_bar_window.set_window_title(title = title)

    def add_widget(self, widget: QtWidgets.QWidget):
        self.__hbox_layout_widgets.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout):
        self.__hbox_layout_widgets.addLayout(layout)

    def __set_style_sheet(self):
        # рамка для виджетов
        self.__frame_widgets.setStyleSheet(f"""
        #frame_widgets {{
            background: {self.__data_theme["frame_widgets"]["background"]};
        }} """)

class Dialog(AbstractWindow):
    """Класс для базового диалогового окна"""
    
    def __init__(self):
        super().__init__()
        super().setWindowFlags(super().windowFlags() | QtCore.Qt.WindowType.Dialog)

class Window(AbstractWindow):
    """Класс для главного окна"""
   
    def __init__(self):
        super().__init__()
        super().setWindowFlags(super().windowFlags() | QtCore.Qt.WindowType.Window)
