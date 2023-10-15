import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Comment

def uniquify(path: str):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path

path_documents = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Documents" , "OutputTests")

if not os.path.exists(path_documents): 
    os.makedirs(path_documents) 

root = ET.Element("main")

# тип документа
type_sub = ET.SubElement(root, "type")
type_sub.text = "IT Master course"

# наименование урока
name_sub = ET.SubElement(root, "name")
name_test = input("Наименование теста: ")
name_sub.text = name_test

path_file = uniquify(os.path.normpath(os.path.join(path_documents, name_test + ".xml")))

# путь к .pdf уроку
lesson_sub = ET.SubElement(root, "lesson")
lesson = input("Теоретическая часть (.pdf): ")
if lesson == "": 
    lesson = "None"
lesson_sub.text = lesson

tree = ET.ElementTree(root)

count_question = 0

_continue = ""

while True:
    count_question += 1
    comment = Comment(f" {count_question} ")
    root.append(comment)

    print(f"Вопрос №{count_question}")

    # вопрос
    question_sub = ET.SubElement(root, "question")

    # заголовок
    # title = input("Вопрос: ")
    print("Вопрос: ", end = "")
    title = "\n".join(iter(input, ""))

    title_sub = ET.SubElement(question_sub, "title")
    title_sub.text = title
    
    # изображений
    path_image = input("Изображение (.png; .jpg; .gpeg; и т.д.): ")
    if path_image == "": 
        path_image = "None"

    image_sub = ET.SubElement(question_sub, "image")
    image_sub.text = path_image
    
    # типаж  вопроса
    print("Типажи вопроса:")
    print("\tВвод в строку ввода: 1")
    print("\tВыбор одного вырианта ответа: 2")
    print("\tВыбор нескольких вариантов ответа: 3")
    print("\tСопоставление в табличной форме: 4")

    type_exercise = int(input("Типаж вопроса: "))
    type_exercise_sub = ET.SubElement(question_sub, "type")

    match type_exercise:
        case 1: # ввод ответа в строку ввода
            type_exercise_sub.text = "input_answer"

            # верный ответ
            correct_answer = input("Ответ: ")

            correct_answer_sub = ET.SubElement(question_sub, "correct_answer")
            correct_answer_sub.text = correct_answer
            print()
        case 2: # выбор одного правильного ответа
            type_exercise_sub.text = "selectable_answer"

            # варианты ответа
            answer_option = ""
            amount_answer_option = int(input("Количество вариантов ответа: "))

            for i in range(amount_answer_option):
                answer_option = input("Вариант ответа: ")

                answer_option_sub = ET.SubElement(question_sub, "answer_option")
                answer_option_sub.text = answer_option

            # верный ответ
            correct_answer = input("Верный ответ: ")

            correct_answer_sub = ET.SubElement(question_sub, "correct_answer")
            correct_answer_sub.text = correct_answer
            print()

        case 3: # выбор нескольких правильных ответов
            type_exercise_sub.text = "multiple_selectable_answers"

            amount_answer_option = int(input("Количество вариантов ответа: "))

            # варианты ответа
            for i in range(amount_answer_option):
                answer_option = input("Вариант ответа: ")

                answer_option_sub = ET.SubElement(question_sub, "answer_option")
                answer_option_sub.text = answer_option

            amount_correct_answer = int(input("Количество верных ответов: "))

            # верные ответы
            for i in range(amount_correct_answer):
                correct_answer = input("Верный ответ: ")

                correct_answer_sub = ET.SubElement(question_sub, "correct_answer")
                correct_answer_sub.text = correct_answer
            print()

        case 4: # сопоставление в виде таблицы
            type_exercise_sub.text = "comparison_table"

            amount_columns = int(input("Количество столбцов: "))
            amount_row = int(input("Количество строк (без учета шапки таблицы): "))

            # шапка таблицы
            for i in range(amount_columns):
                header = input(f"Cтолбец {i + 1} заголовок: ")

                header_sub = ET.SubElement(question_sub, "header")
                header_sub.text = header

            list_cell_sub = list()
            list_row_sub = list()
            list_count_input = list()
            list_count_label = list()
            list_label = list()

            print()

            for i in range(amount_row):
                row_sub = ET.SubElement(question_sub, "row")
                list_row_sub.append(row_sub)
                
                list_cell_sub.append(list())
                list_label.append(list())
                count_input = 0
                count_label = 0
                print(f"Cтрока {i + 1}")
                print("Типы ячеек:")
                print("\t1 - ввод ответа в ячейку")
                print("\t2 - не редактируема ячейка (метка)")
                for j in range(amount_columns):
                    type = int(input(f"Cтолбец {j + 1} тип ячейки: "))

                    cell_sub = ET.SubElement(row_sub, "cell")

                    match type:
                        case 1:
                            type = "input"
                            count_input += 1
                        case 2:
                            type = "label"
                            list_label[i].append(j)
                            count_label += 1

                    cell_sub.set("type", type)
                    list_cell_sub[i].append(cell_sub)
                list_count_input.append(count_input)
                list_count_label.append(count_label)
                print()

            for i in range(amount_row):
                print(f"Cтрока {i + 1}")
                for j in list_label[i]:
                    text = input(f"Cтолбец {j + 1} текст ячейки: ")

                    list_cell_sub[i][j].set("text", text)
                if j > 0: 
                    print()

                for j in range(list_count_input[i]):
                    # верные ответы
                    correct_answer = input(f"Cтолбец {j + 1} верный ответ: ")

                    correct_answer_sub = ET.SubElement(list_row_sub[i], "correct_answer")
                    correct_answer_sub.text = correct_answer
                print()

    # Запись в файл:
    output_file = open(path_file , "wb")
    ET.indent(tree, space = "\t", level = 0)
    tree.write(output_file, encoding = "utf-8", xml_declaration = True)

    print(f"Тест сохранен в: {path_file}\n")

    _continue = input("любой символ - для продолжения (\"-\" - чтобы выйти): ")
    if _continue == "-":
        break