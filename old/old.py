def __switch_question(self, number: int):
        current_question = self.__root.findall("exercise")[number]

        if self.__page_question != None:
            # сохранение ответа текущей страницы в список ответов
            self.__list_answers[self.__current_number_question] = self.__page_question.answer

            # удаление старой страницы
            self.__stacked_widget.removeWidget(self.__page_question)

        self.__current_number_question = number

        # создание и упаковка новой страницы вопроса
        self.__page_question = PageTest(
            number = self.__current_number_question,
            path_course = self.__path_course, 
            question = current_question,
            answer = self.__list_answers[number], 
            started_passing = self.__dict_questions_started_passing[number],
            icon_dialogs = self.__icon_dialogs,
            path_images = self.__path_images, 
            data_theme = self.__data_theme["frame_main"]["test_tab"]            
        )
        self.__page_question.answer_changed.connect(self.__on_change_answer)

        self.__stacked_widget.addWidget(self.__page_question)
        self.__stacked_widget.setCurrentWidget(self.__page_question)

import PIL.Image
exts = PIL.Image.registered_extensions()
supported_extensions = {ex for ex, f in exts.items() if f in PIL.Image.OPEN}
print(supported_extensions)




 if "type" in settings:
    if settings["type"] == "number":
        # заменаяет , на .
        right_answer = right_answer.replace(",", ".")
        user_answer = user_answer.replace(",", ".")

        # проверка на число
        pattern = re.compile("^-?\d+(\.d+)?$")

        # если это число, то приводит к дробному типу
        if (temp_right_answer := pattern.match(right_answer)) and (temp_user_answer := pattern.match(user_answer)):
            if temp_right_answer.group(0) and temp_user_answer.group(0):
                right_answer = str(float(right_answer))
                user_answer = str(float(user_answer))



class PushButtonImage(QtWidgets.QPushButton):
    """Класс для кнопки с изображением"""
    push_button_image_clicked = QtCore.pyqtSignal()
    
    def __init__(self, path_image: str, data_theme: dict):
        super().__init__()

        self.setObjectName("push_button_image")
        # self.clicked.connect(self.__push_button_image_press)
        # self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.__path_image = path_image
        self.__data_theme = data_theme

        self.__min_size = QtCore.QSize(93, 93)
        self.__max_size = QtCore.QSize(393, 393)

        self.__pixmap = QtGui.QPixmap(self.__path_image)

        zoom = 1

        if self.__pixmap.width() < self.__min_size.width() or self.__pixmap.height()  < self.__min_size.height():
            zoom = max(self.__min_size.width() / self.__pixmap.width(), self.__min_size.height() / self.__pixmap.height())
        if  self.__pixmap.width() > self.__max_size.width() or self.__pixmap.height()  > self.__max_size.height():
            zoom = min(self.__max_size.width() / self.__pixmap.width(), self.__max_size.height() / self.__pixmap.height())

        self.__pixmap = self.__pixmap.scaled(round(self.__pixmap.width() * zoom), round(self.__pixmap.height() * zoom), transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
        
        self.__target = QtGui.QPixmap(self.__pixmap.size())  
        self.__target.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(self.__target)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)

        painter_path = QtGui.QPainterPath()
        painter_path.addRoundedRect(0, 0, self.__pixmap.width(), self.__pixmap.height(), 14, 14)

        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, self.__pixmap)
        painter.end()

        self.__image = QtGui.QIcon(self.__target)

        self.setIcon(self.__image)
        self.setIconSize(self.__target.size())
        self.setFixedSize(max(self.__target.width(), self.__min_size.width()), max(self.__target.height(), self.__min_size.height()))

        self.set_style_sheet()

    def __push_button_image_press(self):
        self.push_button_image_clicked.emit()

    def set_style_sheet(self):
        self.setStyleSheet("""
        #push_button_image {
            outline: 0;
            border-radius: 14px; 
            background: %(background)s; 
        } """ % self.__data_theme)

selected_extension_file = re.search("\.\w+ \(\*\.(\w+)\)", filter).group(1)

if not re.match(f"^(.+?)\.{selected_extension_file}$", path_image):
    path_image = f"{os.path.normpath(path_image)}.{selected_extension_file}"
print(path_image, selected_extension_file)

self.__opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.__opacity_effect.setOpacity(0.9)
        self.__push_buttton_save_image.setGraphicsEffect(self.__opacity_effect)

# # тень
        # self.__shadow = QtWidgets.QGraphicsDropShadowEffect()
        # self.__shadow.setBlurRadius(15)
        # self.__shadow.setOffset(0, 0)
        # self.__shadow.setColor(QtGui.QColor(63, 63, 63, 180))
        # self.setGraphicsEffect(self.__shadow)


# кнопка с текстом
self.__push_button_text = QtWidgets.QPushButton()
self.__push_button_text.setObjectName("push_button_text")
self.__push_button_text.clicked.connect(self.__checkbox_clicked)
self.__push_button_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

self.__hbox_layout_main.addWidget(self.__push_button_text)

# макет внутки кнопки
self.__push_button_text.layout_label_text = QtWidgets.QHBoxLayout()
self.__push_button_text.layout_label_text.setSpacing(0)
self.__push_button_text.layout_label_text.setContentsMargins(0, 0, 0, 0)

self.__push_button_text.setLayout(self.__push_button_text.layout_label_text)