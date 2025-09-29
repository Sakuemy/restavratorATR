import tkinter as tk
from tkinter import filedialog
import os
import pywintypes
import win32file
import win32con
import datetime
import time
from PIL import Image
from PIL.ExifTags import TAGS
from progress.bar import Bar
import sys

def main():
    m0 = "\033[91mНе выбраны\033[0m"
    m1 = "\033[91mВыключено\033[0m"
    m2 = "\033[91mНе введен\033[0m"
    clear_screen()
    list_f = ''
    a = -1
    a_2 = ""
    while a != 3:
        print("0 для выбора файлов. " + m0)
        print("1 брать дату из даты съемки (Шаблон не будет учитываться). " + m1)
        print("2 для ввода шаблона. " + m2)
        print("3 для применения изменений.")
        print("4 для выхода из программы.")
        print("")
        a = input("Введите номер команды: ")
        clear_screen()
        if a == "0":
            list_f = openfiles()
            if list_f == "":
                m0 = "\033[91mНе выбраны\033[0m"
            else:
                m0 = "\033[92mФайлы выбраны\033[0m"
        if a == "1":
            if m1 == "\033[91mВыключено\033[0m":
                m1 = "\033[92mВключено\033[0m"
            else:
                m1 = "\033[91mВыключено\033[0m"
        if a == "2":
            if m0 == "\033[91mНе выбраны\033[0m":
                print("\033[91m!!!Не выбраны файлы!!!\033[0m")
            else:
                clear_screen()
                a_2 = ""
                while a_2 == "":
                    print("Введите шаблон или 0 для выхода в предидущее меню.")
                    print("")
                    print("Инструкция для указания шаблона.")
                    print('Вам нужно указать где в названии файла содержится дата и время. Для этого Вам нужно ввести шаблон вида "----yymmdd-HHMMSS" для файла "IMG_180412-162313.jpg" (Это пример).')
                    print("Где:")
                    print('"-" используется чтобы пропустить символы не нужные для нас.')
                    print('"y" это год. Может быть yyyy или yy. В случае ввода yy программа допишет 20 сама.')
                    print('"m" это месяц.')
                    print('"d" это день.')
                    print('"H" это час.')
                    print('"M" это минута.')
                    print('"S" это секунда.')
                    print("")
                    print("Несколько выбраных Вами выйлов:")
                    if len(list_f) < 5:
                        len_list = len(list_f)
                    else:
                        len_list = 5
                    i = 0
                    while i != len_list:
                        print(os.path.basename(list_f[i]))
                        i = i + 1
                    print("")
                    a_2 = input("Введите команду или шаблон: ")
                    if a_2 == "0":
                        clear_screen()
                        m2 = "\033[91mНе введен\033[0m"
                    else:
                        clear_screen()
                        rez = testPattern(list_f, a_2, "test")
                        if rez == "True":
                            t = "False"
                            while t != "True":
                                e = input('Введите "Y" если все OK или "N" если нужно переделать шаблон: ')
                                if (e == "Y") or (e == "y"):
                                    m2 = "\033[92mВведен\033[0m"
                                    t = "True"
                                    pattern = a_2
                                    clear_screen()
                                else:
                                    if (e == "N") or (e == "n"):
                                        a_2 = ""
                                        t = "True"
                                        clear_screen()
                        else:
                            clear_screen()
                            a_2 = ""
                            print(rez)
        if (a == "3"):
            if (m0 == "\033[91mНе выбраны\033[0m"):
                a = -1
                print("\033[91m!!!Не выбраны файлы!!!\033[0m")
            else:
                if (m1 == "\033[92mВключено\033[0m"):
                    change_date_creation(list_f, "")
                else:
                    if (m2 == "\033[91mНе введен\033[0m"):
                        a = -1
                        print("\033[91m!!!Не введен шаблон!!!\033[0m")
                    else:
                        change_date_creation(list_f, pattern)
        if a == "4":
            sys.exit()
    change_date_creation(list_f)

def testPattern(files_name, pattern, test):
    pattern_set = ["y","m","d","H","M","S"]
    clear_screen()
    print("Таблица соответствия фалов и прочтенной даты:")
    for file_name in files_name:
        date_string = ""
        for pattern_value in pattern_set:
            i = 0
            if pattern_value == "y":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "y":
                        s = s + 1
                    i2 = i2 + 1
                if s == 2:
                    date_string = date_string + "20"
                else:
                    if s != 4:
                        return("\033[91mОшибка! Не правильно введен год!\033[0m")
            if pattern_value == "m":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "m":
                        s = s + 1
                    i2 = i2 + 1
                if s != 2:
                    return("\033[91mОшибка! Не правильно введен месяц!\033[0m")
            if pattern_value == "d":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "d":
                        s = s + 1
                    i2 = i2 + 1
                if s != 2:
                    return("\033[91mОшибка! Не правильно введен день!\033[0m")
            if pattern_value == "H":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "H":
                        s = s + 1
                    i2 = i2 + 1
                if s != 2:
                    return("\033[91mОшибка! Не правильно введен час!\033[0m")
            if pattern_value == "M":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "M":
                        s = s + 1
                    i2 = i2 + 1
                if s != 2:
                    return("\033[91mОшибка! Не правильно введен минуты!\033[0m")
            if pattern_value == "S":
                i2 = 0
                s = 0
                while i2 != len(pattern):
                    if pattern[i2] == "S":
                        s = s + 1
                    i2 = i2 + 1
                if s != 2:
                    return("\033[91mОшибка! Не правильно введены секунды!\033[0m")
            while i != len(pattern):
                if pattern[i] == pattern_value:
                    date_string = date_string + os.path.basename(file_name)[i]
                i = i + 1
        try:
            if date_string != "":
                if test == "test":
                    print(str(os.path.basename(file_name)) + "\t|\t" + str(datetime.datetime.strptime(date_string, "%Y%m%d%H%M%S")))
                else:
                    return(datetime.datetime.strptime(date_string, "%Y%m%d%H%M%S"))
            else:
                return('\033[91mОшибка! Ошибка при чтении даты из "' + os.path.basename(file_name) + " !\033[0m")
        except ValueError as e:
            print(f"\033[91mОшибка парсинга даты у файла'{os.path.basename(file_name)}': {e} !\033[0m")
    return("True")

def openfiles():
    # создаём скрытое окно
    root = tk.Tk()
    root.withdraw()  
    # диалог выбора файлов
    file_paths = filedialog.askopenfilenames(
        title="Выберите файлы",
        filetypes=[("Все файлы", "*.*")]
    )
    return(file_paths)

def change_date_creation(f_paths, pattern):
    bar = Bar('Обработка', max=len(f_paths))
    for f_path in f_paths:
        tm = testm1(pattern, f_path)
        if not isinstance(tm, str):
            new_time = tm
            new_mtime = new_time.timestamp()
            file = win32file.CreateFile(f_path, win32con.GENERIC_WRITE, 0, None, win32con.OPEN_EXISTING, 0, None)
            # Устанавливаем: (creation, access, write)
            win32file.SetFileTime(file, new_time, None, None)
            file.close()
            # Меняем дату изменения. (доступ), (изменение)
            os.utime(f_path, (new_mtime, new_mtime))
        else:
            preint(tm)
        bar.next()
    print("")
    print("")

def testm1(pattern, f_path):
    if pattern == "":
        # Новая дата создания
        capture_time = get_capture_date(f_path)
        if capture_time != None:
            # сначала парсим строку в объект datetime
            return(datetime.datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S"))
            # потом преобразуем в timestamp (float)
            
        else:
            return("\033[91mОшибка при чтении даты съемки у файла: " + f_path + "\033[0m")
    else:
        return(pywintypes.Time(testPattern([f_path,""], pattern, "No")))

def get_capture_date(path):
    image = Image.open(path)
    exif = image._getexif()
    if not exif:
        return None

    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "DateTimeOriginal":  # именно «Дата съёмки»
            return value
    return None

def clear_screen():
    # Для Windows
    if os.name == 'nt':
        os.system('cls')
    # Для Linux и Mac
    else:
        os.system('clear')

main()
