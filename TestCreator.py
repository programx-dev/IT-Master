import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Comment


class TestCreator:
    def __init__(self):
        self.count_question = 0

    def add_new_question(self):
        self.count_question += 1
        comment = Comment(f" {self.count_question} ")
        root.append(comment)

        self.question_sub = ET.SubElement(root, "question")

    def add_title(self, title: str):
        self.title_sub = ET.SubElement(self.question_sub, "title")
        self.title_sub.text = title

    def add_image(self, path_image: str):
        self.image_sub = ET.SubElement(self.question_sub, "image")
        self.image_sub.text = path_image

    def __add_type(self, type: str):
        self.type_exercise_sub = ET.SubElement(self.question_sub, "type")
        self.type_exercise_sub.text = type

    def add_input_answer(self, correct_answer: str):
        self.__add_type(type="input_answer")

        correct_answer_sub = ET.SubElement(self.question_sub, "correct_answer")
        correct_answer_sub.text = correct_answer

    def add_selectable_answer(self, answer_option: list[str], correct_answer: str):
        self.__add_type(type="selectable_answer")

        correct_answer_sub = ET.SubElement(self.question_sub, "correct_answer")
        correct_answer_sub.text = correct_answer

        for i in answer_option:
            answer_option_sub = ET.SubElement(self.question_sub, "answer_option")
            answer_option_sub.text = i

        correct_answer_sub = ET.SubElement(self.question_sub, "correct_answer")
        correct_answer_sub.text = correct_answer

    def add_multiple_selectable_answers(self, answer_option: list[str], correct_answer: list[str]):
        self.__add_type(type="multiple_selectable_answers")

        for i in answer_option:
            answer_option_sub = ET.SubElement(self.question_sub, "answer_option")
            answer_option_sub.text = i

        for i in correct_answer:
            correct_answer_sub = ET.SubElement(self.question_sub, "correct_answer")
            correct_answer_sub.text = i

    def add_comparison_table(self, header: list[str], cells_type: list[str], cells_text: list[str], cells_answer: list[str]):
        self.__add_type(type="comparison_table")

        for i in header:
            header_sub = ET.SubElement(self.question_sub, "header")
            header_sub.text = i

        for i in range(len(cells_type)):
            row_sub = ET.SubElement(self.question_sub, "row")

            for j in range(len(cells_type[i])):
                cell_sub = ET.SubElement(row_sub, "cell")

                cell_sub.set("type", cells_type[i][j])

                if cells_type[i][j] == "label":
                    cell_sub.set("text", cells_text[i][j])

            for j in range(len(cells_type[i])):
                if cells_type[i][j] == "input":
                    correct_answer_sub = ET.SubElement(row_sub, "correct_answer")
                    correct_answer_sub.text = cells_answer[i][j]


def uniquify(path: str):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path


def save(path_file: str):
    output_file = open(path_file, "wb")
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def get_number(msg: str):
    while True:
        val = input(msg)

        if val.isdigit():
            return int(val)


path_dir = os.path.expanduser("~/Desktop")

root = ET.Element("main")
tree = ET.ElementTree(root)

type_sub = ET.SubElement(root, "type")
type_sub.text = "IT Master course"

name_sub = ET.SubElement(root, "name")
name_test = input("Введите наименование теста: ")
name_sub.text = name_test

path_dir = uniquify(os.path.normpath(os.path.join(path_dir, name_test)))
os.makedirs(path_dir)

path_file = os.path.join(path_dir, f"{name_test}.xml")

save(path_file)

print(f"\nТест сохранен по пути: {path_file}\n")
print("Все последующие ресурсы для теста сохраняйте в директорию с тестом и указывайте пути кним относительно этого каталога")

lesson_sub = ET.SubElement(root, "lesson")
lesson_sub.text = input("Введите имя теоретической части (.pdf): ") or "None"

print()

_continue = ""
test_creator = TestCreator()

while True:
    test_creator.add_new_question()
    print(f"Вопрос {test_creator.count_question}")

    print("Введите текст вопроса (для оконания ввода два <Enter>): ", end="")
    title = "\n".join(iter(input, ""))
    test_creator.add_title(title)

    path_image = input("Введите путь к изображению относительно рабочей дирректории: ")
    print()

    if path_image == "":
        path_image = "None"
    test_creator.add_image(path_image)

    print("Доступные типажи вопросов:")
    print("├ Ввод в строку ввода (1)")
    print("├ Выбор одного вырианта ответа (2)")
    print("├ Выбор нескольких вариантов ответа (3)")
    print("└ Сопоставление в табличной форме (4)")
    print()

    while True:
        type_exercise = input("Введите типаж вопроса (номер): ")

        if type_exercise.isdigit() and 1 <= (tmp := int(type_exercise)) <= 4:
            type_exercise = tmp
            break
    print()

    match type_exercise:
        case 1:
            correct_answer = input("Введите верный ответ: ")
            test_creator.add_input_answer(correct_answer)

        case 2:
            amount_answer_option = get_number("Введите количество вариантов ответа: ")
            print()

            answer_option = list()

            for i in range(amount_answer_option):
                answer_option.append(input(f"Введите вариант ответа ({i + 1}): "))

            correct_answer = input("Введите верный ответ: ")
            test_creator.add_selectable_answer(answer_option, correct_answer)

        case 3:
            amount_answer_option = get_number("Введите количество вариантов ответа: ")
            print()

            answer_option = list()

            for i in range(amount_answer_option):
                answer_option.append(input(f"Введите вариант ответа ({i + 1}): "))

            print()

            amount_correct_answer = get_number("Введите количество верных ответов: ")
            print()

            correct_answer = list()

            for i in range(amount_correct_answer):
                correct_answer.append(input(f"Введите верный ответ ({i + 1}): "))

            test_creator.add_multiple_selectable_answers(answer_option, correct_answer)

        case 4:
            amount_columns = get_number("Введите количество столбцов: ")
            amount_row = get_number("Введите количество строк таблицы (без учета заголовка): ")
            print()

            header = list()
            for i in range(amount_columns):
                header.append(input(f"Введите заголовок (столбец {i + 1}): "))

            print()

            cells_type = list()
            for i in range(amount_row):
                cells_type.append(list())

                print("Доступные типы ячеек:")
                print("├ Доступная для ввода (1)")
                print("└ Метка (2)")
                print()

                for j in range(amount_columns):
                    type = int(input(f"Введите тип ячейки (номер) (строка {i + 1}, cтолбец {j + 1}): "))
                    match type:
                        case 1:
                            cells_type[i].append("input")
                        case 2:
                            cells_type[i].append("label")
                print()

            cells_text = list()
            cells_answer = list()

            for i in range(amount_row):
                cells_text.append(list())
                cells_answer.append(list())

                for j, elem in enumerate(cells_type[i]):
                    match elem:
                        case "input":
                            cells_text[i].append(None)
                            cells_answer[i].append(input(f"Введите верный ответ (строка {i + 1}, столбец {j + 1}): "))
                        case "label":
                            cells_text[i].append(input(f"Введите текст ячейки (строка {i + 1}, столбец {j + 1}): "))
                            cells_answer[i].append(None)

                print()

            test_creator.add_comparison_table(header, cells_type, cells_text, cells_answer)

    print()
    save(path_file)

    print(f"Вопрос добавлен в: {path_file}")
    print()

    _continue = input("\"Y\" - для продолжения (\":q\" - чтобы выйти): ")

    if _continue == ":q":
        print(f"Тест сохранен по пути: {path_file}")
        break
    elif _continue != "Y":
        while _continue != "Y":
            _continue = input("\"Y\" - для продолжения (\":q\" - чтобы выйти): ")
            
    print()
