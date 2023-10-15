import PageTesting
import PropertyPages
import os

def get_style_sheet(data_theme: dict, path_theme: str, path_images: str):
        return f"""
        /* PageHome */
            /* главная рамка */
            #page_home #frame_main {{
                background: {data_theme["page_home"]["frame_main"]["background"]};
                border-image: url({os.path.join(os.path.split(path_theme)[0], data_theme["page_home"]["frame_main"]["background_image"]).replace(chr(92), "/")});
                background-repeat: no-repeat; 
                background-position: center;
            }}

            /* внутренняя рамка формы */
            #page_home #frame_internal {{
                border-radius: 14px;
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["background"]};
            }}

            /* метка заголовка */
            #page_home #label_header {{ 
                background: transparent; 
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["label_header"]["color"]}
            }} 

            /* список уроков */
            #page_home #list_view {{
                outline: 0;
                border: 0px;
                background: transparent;
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["color"]};
            }}
            #page_home #list_view::item {{
                margin: 0px 14px 0px 0px;
            }}
            #page_home #list_view::item:selected {{
                border-radius: 6px;
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["selected"]["background"]};
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["selected"]["color"]};;
            }}  
            #page_home #list_view::item:hover:!selected {{
                border-radius: 6px;
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["hover"]["background"]};
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["item"]["hover"]["color"]};;
            }}                        
        
            #page_home #list_view QScrollBar:vertical {{              
                border: transparent;
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_home #list_view QScrollBar::handle:vertical {{
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_home #list_view QScrollBar::add-line:vertical, #page_home #list_view QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_home #list_view QScrollBar::add-page:vertical, #page_home #list_view QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_home #list_view QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_home #list_view QScrollBar::handle:horizontal {{
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_home #list_view QScrollBar::add-line:horizontal, #page_home #list_view QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_home #list_view QScrollBar::add-page:horizontal, #page_home #list_view QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* кнопка Выбрать в проводнике */
            #page_home #push_button_select_in_explorer {{
                outline: 0;                                         
                text-align: left;
                border-radius: 7px; 
                background: transparent; 
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_select_in_explorer"]["color"]};
            }} 

            /* кнопка входа */
            #page_home #push_button_start_test {{
            outline: 0;
                border-radius: 7px; 
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["background"]}; 
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["color"]};
            }} 
            #page_home #push_button_start_test::pressed {{
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["pressed"]["background"]}; 
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["pressed"]["color"]};
            }}
            #page_home #push_button_start_test::disabled {{
                background: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["disabled"]["background"]};
                color: {data_theme["page_home"]["frame_main"]["frame_internal"]["push_button_start_test"]["disabled"]["color"]};
            }}

        /* PageTesting */
            /* главная рамка */
            #page_testing #frame_main {{
                background: {data_theme["page_testing"]["frame_main"]["background"]};
            }} 

            /* панель инструментов и навигации */
            #page_testing #frame_tools {{               
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["background"]};
            }} 

            /* прокручиваемая область для станица теста */
            #page_testing #scroll_area_page_test {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["background"]};
                border: none;
            }}
            
            #page_testing #scroll_area_page_test QScrollBar:vertical {{              
                border: transparent;
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::handle:vertical {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_testing #scroll_area_page_test QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::handle:horizontal {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-line:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_testing #scroll_area_page_test QScrollBar::add-page:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }} 

            /* прокручиваемая область для кнопок навигации по вопросам */
            #page_testing #scroll_area_push_button_questions {{
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["background"]};
                border: none;
                margin: 0px, 0px, 0px, 0px;
            }} 

            #page_testing #scroll_area_push_button_questions QScrollBar:vertical {{
                width: 0px;
            }}
            
            #page_testing #scroll_area_push_button_questions QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::handle:horizontal {{
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::add-line:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_testing #scroll_area_push_button_questions QScrollBar::add-page:horizontal, #page_testing #scroll_area_push_button_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }} 

            /* рамка кнопок навигации по вопросам */
            #page_testing #frame_push_button_questions {{
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["background"]};
                margin: 0px, 17px, 0px, 0px;
            }}

            /* кнопка завершить тест */
            #page_testing #push_button_finish {{
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 15px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_finish"]["background"]}; 
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_finish"]["color"]};
            }} 

        /* PageTesting PageQuestion */
            /* главная рамка */
            #page_testing #page_question #frame_main {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["background"]};
            }} 

            /* метка номера вопроса */
            #page_testing #page_question #label_numder_question {{
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_numder_question"]["color"]};   
            }} 

            /* метка вопроса */
            #page_testing #page_question #label_question {{
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["color"]};
                background: transparent;
                selection-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["selection_color"]};
                selection-background-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_question"]["selection_background_color"]};
            }} 

            /* метка типа задания */
            #page_testing #page_question #label_type_question {{ 
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_type_question"]["color"]};
            }}

        /* PageTesting PageQuestion PushButtonImage */
            /* кнопка с изображением */
            #page_testing #page_question #push_button_image {{ 
                outline: 0;
                border-radius: 14px;
                border-style: solid;
                border-width: 1px;
                border-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["push_button_image"]["border_color"]};
                background: transparent; 
            }} 

            /* кнопка сохранения */
            #page_testing #page_question #push_button_image #push_buttton_save_image {{ 
                outline: 0;
                border-radius: 14px; 
                background: transparent; 
            }} 

        /* PageTesting PageQuestion RadioButtonAnswer */
            /* кнопка с флажком */
            #page_testing #page_question #radio_button_answer #push_button_flag {{
                padding-left: 2px;
                padding-top: 5px;
                padding-bottom: 5px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_testing #page_question #radio_button_answer #push_button_flag[hover="true"] {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_testing #page_question #radio_button_answer #label_text {{
                padding-left: 5px;
                padding-top: 5px;
                padding-bottom: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["normal"]["color"]};
            }}

            #page_testing #page_question #radio_button_answer #label_text[hover="true"] {{
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["color"]};
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

        /* PageTesting PageQuestion CheckboxAnswer */
            /* кнопка с флажком */
            #page_testing #page_question #checkbox_answer #push_button_flag {{
                padding-left: 2px;
                padding-top: 5px;
                padding-bottom: 5px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_testing #page_question #checkbox_answer #push_button_flag[hover="true"] {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_testing #page_question #checkbox_answer #label_text {{
                padding-left: 5px;
                padding-top: 5px;
                padding-bottom: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["normal"]["color"]};
            }}

            #page_testing #page_question #checkbox_answer #label_text[hover="true"] {{
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["color"]};
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

        /* PageTesting PageQuestion LineEditAnswer */
            /* строка ввода ответов */
            #page_testing #page_question #line_edit_answer {{
            border-radius: 7px; 
            border-width: 1px;
            border-style: solid; 
            selection-background-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["selection_background_color"]};
            selection-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["selection_color"]};
            border-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["color_border"]};
            background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["background"]}; 
            color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["normal"]["color"]};
            }} 
            #page_testing #page_question #line_edit_answer:focus {{
            selection-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["selection_color"]};
                selection-background-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["selection_background_color"]};
                border-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["color_border"]};
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["background"]}; 
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["line_edit"]["focus"]["color"]};
            }}

            /* PageTesting PageQuestion TableAnswer */
                /* метки заголовка */
                #page_testing #page_question #table_answer #label_header {{
                    background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["label_header"]["background"]};
                    color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["label_header"]["color"]};
                    border-style: solid;
                    border-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["label_header"]["color_border"]};
                    border-top-width: 1px;
                    border-left-width: 1px;
                    border-bottom-width: 1px;
                    border-right-width: 0px;
                }}

                #page_testing #page_question #table_answer #label_header[first="true"] {{
                    border-top-left-radius: 10px;
                }}

                #page_testing #page_question #table_answer #label_header[last="true"] {{
                    border-top-right-radius: 10px;
                    border-right-width: 1px;
                }}

                #page_testing #page_question #table_answer #label_header[only-one="true"] {{
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    border-right-width: 1px;
                }}

                /* поля ввода */
                #page_testing #page_question #table_answer #line_edit_answer {{
                    background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["line_edit"]["background"]};
                    color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["line_edit"]["color"]};
                    selection-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["line_edit"]["selection_color"]};
                    selection-background-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["line_edit"]["selection_background_color"]};
                    border-style: solid;
                    border-color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["table_answer"]["line_edit"]["color_border"]};
                    border-radius: 0px;
                    border-top-width: 0px;
                    border-left-width: 1px;
                    border-bottom-width: 1px;
                    border-right-width: 0px;
                }}

                #page_testing #page_question #table_answer #line_edit_answer[last="true"], #page_testing #page_question #table_answer #line_edit_answer[only-one="true"] {{
                    border-right-width: 1px;
                }}

        /* PageTesting PageQuestion LabelPromt */
            /* главная рамка */
            #page_testing #page_question #label_promt {{
                background: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["background"]};
                border-radius: 3px;
            }} 

            /* цветная полоска */
            #page_testing #page_question #label_line {{
                background:{data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["line"]["background"]};
                border-top-left-radius: 3px;
                border-bottom-left-radius: 3px;
            }} 

            /* метка со значком*/
            #page_testing #page_question #label_icon {{
                background: transparent;
            }} 

            /* метка с информативным текстом */
            #page_testing #page_question #label_text {{
                background: transparent;
                color: {data_theme["page_testing"]["frame_main"]["scroll_area_page_test"]["page_question"]["frame_main"]["label_promt"]["warning"]["color"]};
            }} 

        /* PageTesting PageQuestion PushButtonLesson */
            /* кнопка для открытия теоретической части */
            #page_testing #push_button_lesson[current="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["current"]["color"]};
            }} 
            #page_testing #push_button_lesson[current="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["push_button_lesson"]["not_current"]["color"]};
            }} 

        /* PageTesting PageQuestion PushButtonQuestion */
            /* кнопка для навигации по вопросам теста */
            #page_testing #push_button_question[current="true"][answered="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="true"][answered="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["current"]["not_answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="false"][answered="true"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["answered"]["color"]};
            }} 
            #page_testing #push_button_question[current="false"][answered="false"] {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
                background: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["background"]};
                border-color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["color_border"]};
                color: {data_theme["page_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_questions"]["frame_push_button_questions"]["push_button_qestion"]["not_current"]["not_answered"]["color"]};
            }} 

        /* AbstractWindow */
            /* абстрактное виджет-окно */
            #main #frame_widgets {{
                background: {data_theme["window"]["frame_widgets"]["background"]};
            }} 

        /* AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #main #titile_bar_window #frame_header {{
                background: {data_theme["window"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #main #titile_bar_window #label_title {{
                background: transparent;
                color: {data_theme["window"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #main #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_minimize::hover {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_minimize::pressed {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #main #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_maximize::hover {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_maximize::pressed {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #main #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {data_theme["window"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #main #titile_bar_window #push_button_close::hover {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #main #titile_bar_window #push_button_close::pressed {{
                background: {data_theme["window"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {data_theme["window"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* PageResultTesting */
            /* главная рамка */
            #page_result_testing #frame_main {{
                background: {data_theme["page_result_testing"]["frame_main"]["background"]};
            }} 

            /* панель инструментов и навигации */
            #page_result_testing #frame_tools {{               
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["background"]};
            }} 

            /* прокручиваемая область для станица теста */
            #page_result_testing #scroll_area_page_result_test {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["background"]};
                border: none;
            }}
            
            #page_result_testing #scroll_area_page_result_test QScrollBar:vertical {{              
                border: transparent;
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::handle:vertical {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-line:vertical, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-page:vertical, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_result_testing #scroll_area_page_result_test QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::handle:horizontal {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-line:horizontal, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_result_testing #scroll_area_page_result_test QScrollBar::add-page:horizontal, #page_result_testing #scroll_area_page_result_test QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* прокручиваемая область для кнопок навигации по вопросам */
            #page_result_testing #scroll_area_push_button_result_questions {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["background"]};
                border: none;
                margin: 0px, 0px, 0px, 0px;
            }} 

            #page_result_testing #scroll_area_push_button_result_questions QScrollBar:vertical {{
                width: 0px;
            }}
            
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::handle:horizontal {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::add-line:horizontal, #page_result_testing #scroll_area_push_button_result_questions QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #page_result_testing #scroll_area_push_button_result_questions QScrollBar::add-page:horizontal, #page_result_testing #scroll_area_push_button_result_questions QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            /* рамка кнопок для навигации по результатам вопросов */
            #page_result_testing #frame_push_button_result_questions {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["background"]};
                margin: 0px, 17px, 0px, 0px;
            }} 

        /* PageResultTesting PageResultQuestion */
            /* главная рамка */
            #page_result_testing #page_result_question #frame_main {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["background"]};
            }} 

            /* метка номера вопроса */
            #page_result_testing #page_result_question #label_numder_question {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_numder_question"]["color"]};   
            }} 

            /* метка статуса выполнения */
            #page_result_testing #page_result_question #label_status {{
                border-radius: 7px;
                padding-left: 7px;
                padding-right: 7px; 
            }}
            #page_result_testing #page_result_question #label_status[status="right"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["right"]["background"]};
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["right"]["color"]};   
            }} 
            #page_result_testing #page_result_question #label_status[status="wrong"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["wrong"]["background"]};
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["wrong"]["color"]};
            }} 
            #page_result_testing #page_result_question #label_status[status="skip"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["skip"]["background"]};
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_status"]["skip"]["color"]}; 
            }} 

            /* метка вопроса */
            #page_result_testing #page_result_question #label_question {{
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["color"]};
                background: transparent;
                selection-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["selection_color"]};
                selection-background-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_question"]["selection_background_color"]};
            }} 

            /* метка верный ответ */
            #page_result_testing #page_result_question #label_right_answer {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_right_answer"]["color"]};
            }}

            /* метка ваш ответ */
            #page_result_testing #page_result_question #label_user_answer {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_user_answer"]["color"]};
            }}

            /* метка типа задания */
            #page_result_testing #page_result_question #label_type_question {{ 
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["label_type_question"]["color"]};
            }} 

        /* PageResultTesting PageViewerResultTesting */
            /* главна рамка */
            #page_result_testing #page_viewer_result_testing #frame_main {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["background"]};
            }} 

            /* метка названия теста */
            #page_result_testing #page_viewer_result_testing #label_name_test {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_name_test"]["color"]};
            }} 

            /* метка даты проходжения */
            #page_result_testing #page_viewer_result_testing #label_date_passing {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_date_passing"]["color"]};
            }} 

            /* метка времени прохождения */
            #page_result_testing #page_viewer_result_testing #label_time_passing {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["label_time_passing"]["color"]};
            }} 

            /* диаграмма */
            #chart_view {{
                background: transparent;
            }}

            /* рамка легенды */
            #page_result_testing #page_viewer_result_testing #frame_legend {{
                border-style: solid;
                border-width: 1px;
                border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["border_color"]};
                border-radius: 14px;
            }} 

            /* метка результата */
            #page_result_testing #page_viewer_result_testing #label_result {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_result"]["color"]};
            }} 

            /* метка заголовка */
            #page_result_testing #page_viewer_result_testing #label_header {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_header"]["color"]};
            }} 

        /* PageResultTesting PageViewerResultTesting LabelLegend */
            /* метка с кружком */
            #page_result_testing #page_viewer_result_testing #label_legend #label_pixmap {{
                background: transparent;
            }}

            /* метка с текстом легенды правильно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.right.value}\"] #label_text {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_right"]["color"]};
            }} 

            /* метка с текстом легенды неправильно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.wrong.value}\"] #label_text {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_wrong"]["color"]};
            }} 

            /* метка с текстом легенды пропущенно */
            #page_result_testing #page_viewer_result_testing #label_legend[status=\"{PageTesting.AnswerStatus.skip.value}\"] #label_text {{
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_testing"]["frame_main"]["frame_legend"]["label_legend_skip"]["color"]};
            }} 

        /* PageResultTesting PushButtonResultTesting */
            /* кнопка открытия резутатов тестирования */
            #page_result_testing #push_button_result_testing {{
                outline: 0;
                border: 3px solid;
                border-radius: 10px;
            }}
            #page_result_testing #push_button_result_testing[current="true"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["current"]["color"]};
            }} 
            #page_result_testing #push_button_result_testing[current="false"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["push_button_resul_testing"]["not_current"]["color"]};
            }} 

        /* PageResultTesting PushButtonResultQuestion */
            #page_result_testing #push_button_result_question {{
                outline: 0;
                border: 3px solid;
                border-radius: 25px;
            }}
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.right.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["right"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.wrong.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["wrong"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="true"][status=\"{PageTesting.AnswerStatus.skip.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["current"]["skip"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.right.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["right"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.wrong.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["wrong"]["color"]};
            }} 
            #page_result_testing #push_button_result_question[current="false"][status=\"{PageTesting.AnswerStatus.skip.value}\"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["background"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["color_border"]};
                color: {data_theme["page_result_testing"]["frame_main"]["frame_tools"]["scroll_area_push_button_result_questions"]["frame_push_button_result_questions"]["push_button_resul_question"]["not_current"]["skip"]["color"]};
            }} 

        /* PageResultTesting PageQuestion PushButtonImage */
            /* кнопка с изображением */
            #page_result_testing #page_result_question #push_button_image {{ 
                outline: 0;
                border-radius: 14px;
                border-style: solid;
                border-width: 1px;
                border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["push_button_image"]["border_color"]};
                background: transparent; 
            }} 

            /* кнопка сохранения */
            #page_result_testing #page_result_question #push_button_image #push_buttton_save_image {{ 
                outline: 0;
                border-radius: 14px; 
                background: transparent; 
            }} 

        /* PageResultTesting PageQuestion RadioButtonAnswer */
            /* кнопка с флажком */
            #page_result_testing #page_result_question #radio_button_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_result_testing #page_result_question #radio_button_answer #push_button_flag[hover="true"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_result_testing #page_result_question #radio_button_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["normal"]["color"]};
            }}

            #page_result_testing #page_result_question #radio_button_answer #label_text[hover="true"] {{
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["color"]};
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["radio_button"]["hover"]["background"]};
            }} 

        /* PageResultTesting PageQuestion CheckboxAnswer */
            /* кнопка с флажком */
            #page_result_testing #page_result_question #checkbox_answer #push_button_flag {{
                padding-left: 2px;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                outline: 0;
                border: none;
                background: transparent;
            }}
            #page_result_testing #page_result_question #checkbox_answer #push_button_flag[hover="true"] {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

            /* кликабельная метка c текстом */
            #page_result_testing #page_result_question #checkbox_answer #label_text {{
                padding-left: 5px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: transparent;
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["normal"]["color"]};
            }}

            #page_result_testing #page_result_question #checkbox_answer #label_text[hover="true"] {{
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["color"]};
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["checkbox"]["hover"]["background"]};
            }} 

        /* PageResultTesting PageQuestion LineEditAnswer */
            /* строка ввода ответов */
            #page_result_testing #page_result_question #line_edit_answer {{
            border-radius: 7px; 
            border-width: 1px;
            border-style: solid; 
            selection-background-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["selection_background_color"]};
            selection-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["selection_color"]};
            border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["color_border"]};
            background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["background"]}; 
            color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["normal"]["color"]};
            }} 
            #page_result_testing #page_result_question #line_edit_answer:focus {{
            selection-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["selection_color"]};
                selection-background-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["selection_background_color"]};
                border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["color_border"]};
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["background"]}; 
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["line_edit"]["focus"]["color"]};
            }}  

        /* PageResultTesting PageQuestion TableAnswer */
            /* метки заголовка */
            #page_result_testing #page_result_question #table_answer #label_header {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["label_header"]["background"]};
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["label_header"]["color"]};
                border-style: solid;
                border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["label_header"]["color_border"]};
                border-top-width: 1px;
                border-left-width: 1px;
                border-bottom-width: 1px;
                border-right-width: 0px;
            }}

            #page_result_testing #page_result_question #table_answer #label_header[first="true"] {{
                border-top-left-radius: 10px;
            }}

            #page_result_testing #page_result_question #table_answer #label_header[last="true"] {{
                border-top-right-radius: 10px;
                border-right-width: 1px;
            }}

            #page_result_testing #page_result_question #table_answer #label_header[only-one="true"] {{
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-right-width: 1px;
            }}

            /* поля ввода */
            #page_result_testing #page_result_question #table_answer #line_edit_answer {{
                background: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["line_edit"]["background"]};
                color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["line_edit"]["color"]};
                selection-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["line_edit"]["selection_color"]};
                selection-background-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["line_edit"]["selection_background_color"]};
                border-style: solid;
                border-color: {data_theme["page_result_testing"]["frame_main"]["scroll_area_page_result_test"]["page_result_question"]["frame_main"]["table_answer"]["line_edit"]["color_border"]};
                border-radius: 0px;
                border-top-width: 0px;
                border-left-width: 1px;
                border-bottom-width: 1px;
                border-right-width: 0px;
            }}

            #page_result_testing #page_result_question #table_answer #line_edit_answer[last="true"], #page_result_testing #page_result_question #table_answer #line_edit_answer[only-one="true"] {{
                border-right-width: 1px;
            }}

        /* DialogImageViewer */ 
            /* Диалоговое окно для просмотра изображений */
            #dialog_image_viewer #frame_widgets {{
                background: {data_theme["dialog_image_viewer"]["frame_widgets"]["background"]};
            }} 

            /* главная рамка */
            #dialog_image_viewer #frame_main {{
                background: {data_theme["dialog_image_viewer"]["frame_widgets"]["frame_main"]["background"]};
            }}

        /* DialogImageViewer AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog_image_viewer #titile_bar_window #frame_header {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog_image_viewer #titile_bar_window #label_title {{
                background: transparent;
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog_image_viewer #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_minimize::hover {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_minimize::pressed {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog_image_viewer #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_maximize::hover {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_maximize::pressed {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog_image_viewer #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_close::hover {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog_image_viewer #titile_bar_window #push_button_close::pressed {{
                background: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {data_theme["dialog_image_viewer"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* Dialog */  
            /* рамка виджетов */
            #dialog #frame_widgets {{
                background: {data_theme["dialog"]["frame_widgets"]["background"]};
            }} 
        
            /* главная рамка */
            #dialog #frame_main {{
                background: {data_theme["dialog"]["frame_widgets"]["frame_main"]["background"]};
            }} 

            /* метка с текстом */
            #dialog #label_text {{
                background: transparent;
                color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["label_text"]["color"]};
            }} 

            /* метка с описанием */
            #dialog #label_description {{
                background: transparent;
                color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["label_description"]["color"]};
            }} 

            /* кнопки диалога*/
            #dialog #push_button_dialog {{
                border-width: 1px;
                border-style: solid;
                border-color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog #push_button_dialog:default {{
                border-width: 2px;
                border-color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {data_theme["dialog"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* Dialog AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog #titile_bar_window #frame_header {{
                background: {data_theme["dialog"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog #titile_bar_window #label_title {{
                background: transparent;
                color: {data_theme["dialog"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_minimize::hover {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_minimize::pressed {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_maximize::hover {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_maximize::pressed {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_close::hover {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog #titile_bar_window #push_button_close::pressed {{
                background: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {data_theme["dialog"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 
        
        /* ToolBar */
            /* рамка-панель инструментов */
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_home.value}\"] {{
                background: {data_theme["tool_bar"]["page_home"]["background"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_testing.value}\"] {{
                background: {data_theme["tool_bar"]["page_testing"]["background"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_result_testing.value}\"] {{
                background: {data_theme["tool_bar"]["page_result_testing"]["background"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_history.value}\"] {{
                background: {data_theme["tool_bar"]["page_history"]["background"]};
            }} 

        /* ToolBar SwitchableToolButtonToolbar */
            #tool_bar #switchable_tool_button {{
                padding: 0px;
                outline: 0;
                border-radius: 10px; 
            }}
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_home.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {data_theme["tool_bar"]["page_home"]["tool_button"]["selected"]["background"]};
                color: {data_theme["tool_bar"]["page_home"]["tool_button"]["selected"]["color"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_home.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["color"]};
            }}

            #tool_bar[page=\"{PropertyPages.PropertyPages.page_testing.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {data_theme["tool_bar"]["page_testing"]["tool_button"]["selected"]["background"]};
                color: {data_theme["tool_bar"]["page_testing"]["tool_button"]["selected"]["color"]};
            }}
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_testing.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["color"]};
            }} 

            #tool_bar[page=\"{PropertyPages.PropertyPages.page_result_testing.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["selected"]["background"]};
                color: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["selected"]["color"]};
            }}
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_result_testing.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["not_selected"]["color"]};
            }} 

            #tool_bar[page=\"{PropertyPages.PropertyPages.page_history.value}\"] #switchable_tool_button[selected="true"] {{ 
                background: {data_theme["tool_bar"]["page_history"]["tool_button"]["selected"]["background"]};
                color: {data_theme["tool_bar"]["page_history"]["tool_button"]["selected"]["color"]};
            }}
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_history.value}\"] #switchable_tool_button[selected="false"] {{ 
                background: {data_theme["tool_bar"]["page_history"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_history"]["tool_button"]["not_selected"]["color"]};
            }} 

        /* ToolBar ToolButtonToolbar */
            #tool_bar #tool_button {{
                padding: 0px;
                outline: 0;
                border-radius: 10px; 
            }}
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_home.value}\"] #tool_button {{ 
                background: {data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_home"]["tool_button"]["not_selected"]["color"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_testing.value}\"] #tool_button {{ 
                background: {data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_testing"]["tool_button"]["not_selected"]["color"]};
            }} 

            #tool_bar[page=\"{PropertyPages.PropertyPages.page_result_testing.value}\"] #tool_button {{ 
                background: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_result_testing"]["tool_button"]["not_selected"]["color"]};
            }} 
            #tool_bar[page=\"{PropertyPages.PropertyPages.page_history.value}\"] #tool_button {{ 
                background: {data_theme["tool_bar"]["page_history"]["tool_button"]["not_selected"]["background"]};
                color: {data_theme["tool_bar"]["page_history"]["tool_button"]["not_selected"]["color"]};
            }} 

        /* DialogAbout */ 
            /* рамка виджетов */
            #dialog_about #frame_widgets {{
                background: {data_theme["dialog_about"]["frame_widgets"]["background"]};
            }} 

            /* главная рамка */
            #dialog_about #frame_main {{
                background: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["background"]};
            }}

            /* метка с иконкой */
            #dialog_about #frame_main > #label_icon {{
                background: transparent;
            }}

            /* метка с названием программы */
            #dialog_about #label_name {{
                background: transparent;
                color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_name"]["color"]};
            }}

            /* метка с версией программы */
            #dialog_about #label_version {{
                background: transparent;
                color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_version"]["color"]};
            }}

            /* метка с описанием */
            #dialog_about #label_about {{
                background: transparent;
                color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["color"]};
                selection-color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["selection_color"]};
                selection-background-color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["label_about"]["selection_background_color"]};
            }}

            #dialog_about #push_button_accept {{
                border-width: 1px;
                border-style: solid;
                border-color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog_about #push_button_accept:default {{
                border-width: 2px;
                border-color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* DialogAbout AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog_about #titile_bar_window #frame_header {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog_about #titile_bar_window #label_title {{
                background: transparent;
                color: {data_theme["dialog_about"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog_about #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_minimize::hover {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_minimize::pressed {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog_about #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_maximize::hover {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_maximize::pressed {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog_about #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_close::hover {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog_about #titile_bar_window #push_button_close::pressed {{
                background: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {data_theme["dialog_about"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* DialogSettings */ 
            /* рамка виджетов */
            #dialog_settings #frame_widgets {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["background"]};
            }} 

            /* главная рамка */
            #dialog_settings #frame_main {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["background"]};
            }}

            /* виджет с вкладками */
            #dialog_settings #tab_widget_settings::pane {{ 
                border-width: 1px;
                border-style: solid;
                border-color:  {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["pane"]["border_color"]};
                margin-top: -1px;
                border-radius: 5px;
                border-top-left-radius: 0px;
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["normal"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["normal"]["color"]};
                border-width: 1px;
                border-style: solid;
                border-color:  {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["normal"]["border_color"]};
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8px;
                padding: 2px;
                padding-left: 5px;
                padding-right: 5px;
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:hover {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["hover"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["hover"]["color"]};
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["hover"]["border_color"]};
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:selected {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["selected"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["selected"]["color"]};
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["selected"]["border_color"]};
                border-bottom-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["tab"]["selected"]["background"]}; 
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:!selected {{
                margin-top: 2px; 
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:selected {{
                margin-left: -4px;
                margin-right: -4px;
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:first:selected {{
                margin-left: 0;
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:last:selected {{
                margin-right: 0;
            }}

            #dialog_settings #tab_widget_settings QTabBar::tab:only-one {{
                margin: 0; 
            }}

            /* метка заголовка истории */
            #dialog_settings #label_header_history {{
                background: transparent;
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["label_header_history"]["color"]};
            }}

            /* виджет ввода целых чисел */
            #dialog_settings #spin_box_amount_records {{
                padding-right: 15px;
                border-width: 1;
                border-style: solid;
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["normal"]["color_border"]};
                border-radius: 5px;

                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["normal"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["normal"]["color"]};
                selection-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["normal"]["selection_color"]};
                selection-background-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["normal"]["selection_background_color"]};
            }}

            #dialog_settings #spin_box_amount_records:focus {{
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["focus"]["color_border"]};
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["focus"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["focus"]["color"]};
                selection-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["focus"]["selection_color"]};
                selection-background-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["focus"]["selection_background_color"]};
            }}

            #dialog_settings #spin_box_amount_records::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;

                background: transparent;

                margin-top: 1px;
                margin-right: 1px;

                width: 20px;
                border-top-right-radius: 5px;
            }}

            #dialog_settings #spin_box_amount_records::up-button:hover {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["push_button"]["hover"]["background"]};
            }}
            
            #dialog_settings #spin_box_amount_records::up-button:pressed {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["push_button"]["pressed"]["background"]};
            }}

            #dialog_settings #spin_box_amount_records::up-arrow {{
                image: url({os.path.join(path_images, "arrow_up.png").replace(chr(92), "/")});
                width: 9px;
                height: 9px;
            }}

            #dialog_settings #spin_box_amount_records::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;

                background: transparent;

                margin-bottom: 1px;
                margin-right: 1px;

                width: 20px;
                border-bottom-right-radius: 5px;
            }}

            #dialog_settings #spin_box_amount_records::down-button:hover {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["push_button"]["hover"]["background"]};
            }}

            #dialog_settings #spin_box_amount_records::down-button:pressed {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["spin_box_amount_records"]["push_button"]["pressed"]["background"]};
            }}

            #dialog_settings #spin_box_amount_records::down-arrow {{
                image: url({os.path.join(path_images, "arrow_down.png").replace(chr(92), "/")});
                width: 9px;
                height: 9px;
            }}

            /* кнопка Очистить историю */
            #dialog_settings #push_button_clear {{
                border-width: 1px;
                border-style: solid;
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["push_button_clear"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["push_button_clear"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_history"]["push_button_clear"]["color"]};
            }} 


            /* список цветовых тем */
            #dialog_settings #list_view {{
                outline: 0;
                border: 0px;
                background: transparent;
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["color"]};
            }}
            #dialog_settings #list_view::item {{
                margin: 0px 14px 0px 0px;
            }}
            #dialog_settings #list_view::item:selected {{
                border-radius: 6px;
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["item"]["selected"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["item"]["selected"]["color"]};;
            }}  
            #dialog_settings #list_view::item:hover:!selected {{
                border-radius: 6px;
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["item"]["hover"]["background"]};
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["item"]["hover"]["color"]};;
            }}                        
        
            #dialog_settings #list_view QScrollBar:vertical {{              
                border: transparent;
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #dialog_settings #list_view QScrollBar::handle:vertical {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #dialog_settings #list_view QScrollBar::add-line:vertical, #dialog_settings #list_view QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #dialog_settings #list_view QScrollBar::add-page:vertical, #dialog_settings #list_view QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #dialog_settings #list_view QScrollBar:horizontal {{              
                border: transparent;
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["scrollbar"]["background"]};
                height: 14px;
                border-radius: 6px;
                padding: 4px;
                margin: 0px 0px 0px 0px;
            }}
            #dialog_settings #list_view QScrollBar::handle:horizontal {{
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["tab_widget_settings"]["page_settings_theme"]["list_view"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-width: 30px;
            }}
            #dialog_settings #list_view QScrollBar::add-line:horizontal, #dialog_settings #list_view QScrollBar::sub-line:horizontal {{
                background: transparent;
                width: 0px;
            }}
            #dialog_settings #list_view QScrollBar::add-page:horizontal, #dialog_settings #list_view QScrollBar::sub-page:horizontal {{
                background: transparent;
            }}

            #dialog_settings #push_button_accept, #dialog_settings #push_button_reject {{
                border-width: 1px;
                border-style: solid;
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color_border"]};
                outline: 0;
                padding-left: 15px;
                padding-right: 15px;
                border-radius: 5px; 
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["normal"]["color"]};
            }} 
            #dialog_settings #push_button_accept:default, #dialog_settings #push_button_reject:default {{
                border-width: 2px;
                border-color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color_border"]};
                background: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_widgets"]["frame_main"]["push_button"]["default"]["color"]};
            }}

        /* DialogSettings AbstractWindow TitileBarWindow */
            /* рамка заголовка */
            #dialog_settings #titile_bar_window #frame_header {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["background"]};
            }} 

            /* метка титла */
            #dialog_settings #titile_bar_window #label_title {{
                background: transparent;
                color: {data_theme["dialog_settings"]["frame_title_bar"]["label_title"]["color"]};
            }} 

            /* кнопка для минимизации окна */
            #dialog_settings #titile_bar_window #push_button_minimize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["normal"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_minimize::hover {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["hover"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_minimize::pressed {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_minimize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для максимизации окна */
            #dialog_settings #titile_bar_window #push_button_maximize {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["normal"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_maximize::hover {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["hover"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_maximize::pressed {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["pressed"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_maximize"]["pressed"]["color"]}; 
            }} 

            /* кнопка для закрытия окна */
            #dialog_settings #titile_bar_window #push_button_close {{
                outline: 0;
                border: none;
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["normal"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["normal"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_close::hover {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["hover"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["hover"]["color"]};
            }}
            #dialog_settings #titile_bar_window #push_button_close::pressed {{
                background: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["pressed"]["background"]}; 
                color: {data_theme["dialog_settings"]["frame_title_bar"]["push_button_close"]["pressed"]["color"]}; 
            }} 

        /* PageHistory */
            /* главная рамка */
            #page_history #frame_main {{
                background: {data_theme["page_history"]["frame_main"]["background"]};
            }}

            #page_history #widget_stub #label_icon {{
                background: transparent;
            }}

            #page_history #widget_stub #label_text {{
                background: transparent;
                color: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["widget_stub"]["color"]};
            }}

            /* прокручиваемая область для кнопок просмотра и открытия результатов тестирования */
            #page_history #scroll_area_push_button_result_testing {{
                background: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["background"]};
                border: none;
            }}
            
            #page_history #scroll_area_push_button_result_testing QScrollBar:vertical {{              
                border: transparent;
                background: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["scrollbar"]["background"]};
                width: 14px;
                border-radius: 6px;
                padding: 4px;
            }}
            #page_history #scroll_area_push_button_result_testing QScrollBar::handle:vertical {{
                background: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["scrollbar"]["handle"]["background"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            #page_history #scroll_area_push_button_result_testing QScrollBar::add-line:vertical, #page_history #scroll_area_push_button_result_testing QScrollBar::sub-line:vertical {{
                background: transparent;
                height: 0px;
            }}
            #page_history #scroll_area_push_button_result_testing QScrollBar::add-page:vertical, #page_history #scroll_area_push_button_result_testing QScrollBar::sub-page:vertical {{
                background: transparent;
            }} 

            #page_history #scroll_area_push_button_result_testing QScrollBar:horizontal {{              
                height: 0px;
            }}

            /* рамка для кнопок просмотра и открытия результатов тестирования */
            #page_history #frame_push_button_result_testing {{
                background: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["background"]};
            }}

            /* кнопка просмотра и открытия результатов тестирования */
            #page_history #push_button_result_testing {{
                background: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["background"]};
                border-radius: 12px;
                border-style: solid;
                border-width: 1px;
                border-color: gray;
            }}

            /* метка результата теста */
            #page_history #push_button_result_testing #label_result {{
                background: transparent;
                color: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["label_result"]["color"]};
            }}

            /* метка названия теста */
            #page_history #push_button_result_testing #label_name_test {{
                background: transparent;
                color: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["label_name_test"]["color"]};
            }}
            
            /* метка даты прохождения */
            #page_history #push_button_result_testing #label_date_passing {{
                background: transparent;
                color: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["label_date_passing"]["color"]};
            }}
            
            /* метка подробнее */
            #page_history #push_button_result_testing #label_detail {{
                background: transparent;
                color: {data_theme["page_history"]["frame_main"]["scroll_area_push_button_result_testing"]["frame_push_button_result_testing"]["push_button_result_testing"]["label_detail"]["color"]};
            }}
        """
