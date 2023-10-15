from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import logging
from dataclasses import dataclass
try:
    from . import Logging
except:
    import Logging

@dataclass
class DataImageViewer:
    color_background: QtGui.QColor

data_image_viewer = DataImageViewer(color_background = QtGui.QColor("#1F1F1F"))

class ImageViewer(QtWidgets.QGraphicsView):
    """Класс для сцены просмотра изображений"""
    scale_changed = QtCore.pyqtSignal(float)

    def __init__(self):
        super(ImageViewer, self).__init__()

        self.__zoom = 0
        self.__ZOOM_FACTOR = 1.1
        self.__MAX_ZOOM_FACTOR = 50
        self.__scale_factor = 1
        self.__old_viewrect = QtCore.QRect()
        self.__empty = True
        self.__data_image_viewer = data_image_viewer

        self.__scene = QtWidgets.QGraphicsScene(self)
        self.__image = QtWidgets.QGraphicsPixmapItem()
        self.__scene.addItem(self.__image)

        self.setScene(self.__scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self.setBackgroundBrush(QtGui.QBrush(self.__data_image_viewer.color_background))

    def has_image(self):
        return not self.__empty

    def fit_in_view(self):
        rect = QtCore.QRectF(self.__image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_image():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                self.__old_viewrect = viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.__scale_factor = factor
                self.scale(factor, factor)

            if self.__scale_factor > 1:
               self.__zoom =  1
            else:
                self.__zoom = 0
            
    def __adapt_size_photo(self):
        rect = QtCore.QRectF(self.__image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_image():
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)

                # масштабировать с прилипанием к краям видимой части
                if self.__scale_factor <= 1 and self.__zoom == 0:
                    factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
                    self.__scale_factor *= factor

                    if self.__scale_factor > 1:
                        factor = factor / self.__scale_factor
                        self.__scale_factor = 1
                        self.__zoom = 0

                    self.scale(factor, factor)

                    Logging.logger.debug("масштабировать с прилипанием к краям видимой части")
                    return

                # масштабировать на коэффицент изменения размера
                if self.__zoom > 0:
                    if viewrect.width() / scenerect.width() <= viewrect.height() / scenerect.height():
                        factor = viewrect.width() / self.__old_viewrect.width()
                    else:
                        factor = viewrect.height() / self.__old_viewrect.height()

                    self.__scale_factor *= factor

                    Logging.logger.debug("масштабировать на коэффицент изменения размера")

                    # если масштаб < 100% и изображение меньше размера видимой части и zoom > 0, то восстановить размер = 100%
                    if self.__scale_factor < 1 and self.__zoom > 0 and self.__image.pixmap().width() * self.__scale_factor < viewrect.width() and\
                                                            self.__image.pixmap().height() * self.__scale_factor < viewrect.height():
                        factor = factor / self.__scale_factor
                        self.__scale_factor = 1
                        self.__zoom = 0

                        Logging.logger.debug("если масштаб < 100% и изображение меньше размера видимой части и zoom > 0, то восстановить размер = 100%")

                    # сделать масштаб = 5000, если он > 5000%
                    if self.__scale_factor > self.__MAX_ZOOM_FACTOR:
                        factor = self.__scale_factor / (factor * self.__MAX_ZOOM_FACTOR)
                        self.__scale_factor = self.__MAX_ZOOM_FACTOR

                        Logging.logger.debug("cделать масштаб = 5000, если он > 5000%")
                    
                    self.scale(factor, factor)

    def wheelEvent(self, event):
        if self.has_image():
            viewrect = self.viewport().rect()

            if event.angleDelta().y() > 0:
                factor = self.__ZOOM_FACTOR
                self.__zoom += 1
            else:
                factor = 1 / self.__ZOOM_FACTOR
                self.__zoom -= 1

            # масштабирвать если zoom >= 0
            if self.__zoom >= 0:
                Logging.logger.debug("масштабирвать если zoom >= 0")
                old_scale_factor = self.__scale_factor 
                self.__scale_factor *= factor
                
                # если масштаб < 100% и изображение < размера видимой части и старый размер изображения > видимой части, то масштабировать с прилипанием к краям видимой части
                if self.__scale_factor < 1 and self.__image.pixmap().width() * self.__scale_factor < viewrect.width() and self.__image.pixmap().height() * self.__scale_factor < viewrect.height() and\
                        (self.__image.pixmap().width() * old_scale_factor > viewrect.width() or self.__image.pixmap().height() * old_scale_factor > viewrect.height()):
                    Logging.logger.debug("если масштаб < 100% и изображение меньше размера видимой части, то прилепить к краям видимой части")

                    scenerect = self.transform().mapRect(QtCore.QRectF(self.__image.pixmap().rect()))
                    factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height())
                    self.__scale_factor = old_scale_factor * factor
                    self.__zoom = 0

                # установить масштаб = 100%, если масштаб изображения < 100% и изображение меньше размера видимой части и zoom = 0
                elif self.__scale_factor < 1 and self.__zoom == 0 and self.__image.pixmap().width() * self.__scale_factor < viewrect.width() and self.__image.pixmap().height() * self.__scale_factor < viewrect.height():
                    Logging.logger.debug("установить масштаб = 100%, если масштаб изображения < 100% и изображение меньше размера видимой части")
                    factor = factor / self.__scale_factor
                    self.__scale_factor = 1

                # установить zoom = 1, если масштаб изображения > 100% и zoom = 0 или масштаб изображения < 100% и один из краев изображения > видимой части
                elif (self.__scale_factor > 1 and self.__zoom == 0) or (self.__scale_factor < 1 and (self.__image.pixmap().width() * self.__scale_factor > viewrect.width() or self.__image.pixmap().height() * self.__scale_factor > viewrect.height())):
                    Logging.logger.debug("установить zoom = 1 если масштаб изображения > 100% и zoom = 0 или масштаб изображения < 100% и один из краев изображения > видимой части")
                    self.__zoom = 1
                
                # масштабировать если масштаб <= 5000%
                if self.__scale_factor <= self.__MAX_ZOOM_FACTOR:
                    Logging.logger.debug("масштабировать если масштаб <= 5000%")
                    self.scale(factor, factor)
                # установить масштаб = 5000% если он > 5000% и старый масштаб < 5000%
                elif old_scale_factor < self.__MAX_ZOOM_FACTOR:
                    Logging.logger.debug("установить масштаб = 5000% если он больше")
                    factor = self.__MAX_ZOOM_FACTOR / old_scale_factor
                    self.__scale_factor = self.__MAX_ZOOM_FACTOR
                    self.__zoom = 1

                    self.scale(factor, factor)
                # не масштабировать, если масштаб = 5000%
                else:
                    Logging.logger.debug("не масштабировать, если масштаб = 5000%")
                    self.__scale_factor = self.__MAX_ZOOM_FACTOR
                    self.__zoom = 1 

            # восcтановить масштаб = 100%, если zoom = -1 и масштаб > 1
            elif self.__scale_factor > 1:
                Logging.logger.debug("воcстановить масштаб = 100%, если zoom = -1 и масштаб > 1")
                factor = 1 / self.__scale_factor
                self.__scale_factor = 1
                self.__zoom = 0

                self.scale(factor, factor)

            else:
                Logging.logger.debug("не масштабировать, и установить zoom = 0")
                self.__zoom = 0

    def set_image(self, pixmap: QtGui.QPixmap):
        self.__zoom = 0
        if pixmap and not pixmap.isNull():
            self.__empty = False
            self.__image.setPixmap(pixmap)

            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

            rect = QtCore.QRectF(self.__image.pixmap().rect())
            if not rect.isNull():
                self.__scale_factor = 1
                self.setSceneRect(rect)
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                self.__old_viewrect = viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                            viewrect.height() / scenerect.height())
                if factor < 1:
                    self.__scale_factor = factor
                    self.scale(factor, factor)
                self.__zoom = 0

        else:
            self.__empty = True
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self.__image.setPixmap(QtGui.QPixmap())

    def resizeEvent(self, event):
        if self.__old_viewrect.isEmpty():
            self.__old_viewrect = self.viewport().rect()
        self.__adapt_size_photo()
        self.__old_viewrect = self.viewport().rect()
        return super().resizeEvent(event)

    def scale(self, sx: float, sy: float) -> None:
        self.scale_changed.emit(self.__scale_factor)

        return super().scale(sx, sy)

    def change_data_image_viewer(self, data_image_viewer: DataImageViewer):
        self.__data_image_viewer = data_image_viewer

        self.setBackgroundBrush(QtGui.QBrush(self.__data_image_viewer.color_background))

class Window(QtWidgets.QWidget):
    """Класс для тестирования окна просмотра изображения"""

    def __init__(self):
        super(Window, self).__init__()

        self.__vbox_layout = QtWidgets.QVBoxLayout(self)

        self.__viewer = ImageViewer()

        self.__vbox_layout.addWidget(self.__viewer)

        self.__hbox_layout = QtWidgets.QHBoxLayout()

        self.__vbox_layout.addLayout(self.__hbox_layout)

        self.__push_button_load = QtWidgets.QPushButton()
        self.__push_button_load.setText("Загрузить")
        self.__push_button_load.clicked.connect(self.__load_image)

        self.__hbox_layout.addWidget(self.__push_button_load)

        self.__push_button_fit_in_view = QtWidgets.QPushButton()
        self.__push_button_fit_in_view.setText("По размеру")
        self.__push_button_fit_in_view.clicked.connect(self.__viewer.fit_in_view)

        self.__hbox_layout.addWidget(self.__push_button_fit_in_view)

        self.__label_scale = QtWidgets.QLabel()
        self.__label_scale.setText("100%")
        self.__viewer.scale_changed.connect(self.__scale_changed)
        
        self.__hbox_layout.addWidget(self.__label_scale)

    def __scale_changed(self, scale_factor: float):
        self.__label_scale.setText(f"{round(scale_factor * 100)}%")

    def __load_image(self):
        self.__viewer.set_image(QtGui.QPixmap(r'C:\MyScripts\Python\Projects\IT-Master\courses\Графические информационные модели\05.png'))

if __name__ == '__main__':
    Logging.logger.setLevel(logging.DEBUG)
    Logging.c_handler.setLevel(logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()

    sys.exit(app.exec())