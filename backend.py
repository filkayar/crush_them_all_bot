import time
import cv2
import numpy as np
import os
import subprocess
import pyautogui
import wx
import shutil
from pynput.mouse import Controller, Button


def f_click(x, y):
    m = Controller()
    m.position = (x, y)
    m.press(Button.left)
    time.sleep(0.05)
    m.release(Button.left)
    time.sleep(0.1)
    m.position = (0, 0)

def time_label():
    return int(time.time())

def stopwatch(x):
    return int(time.time()) - x

def find_element(image_path, x0, y0, x1, y1, precision=0.8, click=True):
    width = x1 - x0
    height = y1 - y0
    image = pyautogui.locateOnScreen(image_path, region=(x0, y0, width, height), confidence=precision)
    if image:
        x, y = pyautogui.center(image)
        if click:
            f_click(x, y)
        return True
    return False



def show_error_dialog(message):
    # app = wx.App()
    # Создание модального окна с сообщением об ошибке
    dlg = wx.MessageDialog(None, message, "Ошибка", wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()


def find_x(x0, y0, x1, y1, radius, wb_lvl, bx=-1, by=-1, click_back=True):
    width = x1 - x0
    height = y1 - y0
    # Сделать скриншот указанной области экрана
    screenshot = pyautogui.screenshot(region=(x0, y0, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    # Преобразовать скриншот в черно-белую палитру
    grayscale_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # Применить пороговое значение, чтобы сделать все пиксели выше порога белыми
    _, binary_image = cv2.threshold(grayscale_image, wb_lvl, 255, cv2.THRESH_BINARY)
    height, width = binary_image.shape[:2]
    for y in range(radius, height - radius):
        for x in range(radius, width - radius):
            _x = binary_image[y, x]
            _a = binary_image[y - radius, x - radius]
            _b = binary_image[y - radius, x + radius]
            _c = binary_image[y + radius, x - radius]
            _d = binary_image[y + radius, x + radius]
            _e = binary_image[y + radius, x]
            _f = binary_image[y - radius, x]
            _g = binary_image[y, x + radius]
            _h = binary_image[y, x - radius]
            if ( # белый крест
                    _x == 255 and
                    _a == 255 and _b == 255 and _c == 255 and _d == 255 and
                    _e == 0 and _f == 0 and _g == 0 and _h == 0
            ) or ( # черный крест
                    _x == 0 and
                    _a == 0 and _b == 0 and _c == 0 and _d == 0 and
                    _e == 255 and _f == 255 and _g == 255 and _h == 255
            ) or ( # белый next
                    _x == 255 and
                    _a == 255 and _b == 0 and _c == 255 and _d == 0 and
                    _e == 0 and _f == 0 and _h == 0
            ):
                f_click(x0+x, y0+y)
                time.sleep(1)
                return True
    if click_back and bx != -1 and by != -1:
        f_click(bx, by)
        time.sleep(1)
    return False


def open_folder(directory):
    # Проверка существования указанного каталога
    if not os.path.exists(directory):
        show_error_dialog(f"Каталог '{directory}' не существует")
        return
    # Проверка, что указанный путь является каталогом
    if not os.path.isdir(directory):
        show_error_dialog(f"Путь '{directory}' не является каталогом")
        return
    # Открытие каталога в проводнике
    try:
        subprocess.Popen(f'explorer "{directory}"')
    except Exception as e:
        show_error_dialog(f"Ошибка при открытии каталога: {str(e)}")


def check_screenshot_match(cat_screen, precision_image, x0, y0, x1, y1):
    # Сформируем постфикс к общему каталогу скриншотов, чтобы рассортировать изображения по габаритам
    height = y1 - y0
    width = x1 - x0
    temp_catalog = cat_screen + "/TEMP"
    save_catalog = cat_screen + "/" + str(height) + "_x_" + str(width)


    # Проверка наличия каталога и его создание
    if not os.path.exists(save_catalog):
        os.makedirs(save_catalog)
    if not os.path.exists(temp_catalog):
        os.makedirs(temp_catalog)

    # Создание скриншота области экрана
    screenshot = pyautogui.screenshot(region=(x0, y0, x1 - x0, y1 - y0))
    screenshot.save(temp_catalog + '/screenshot.png')

    # Переходим к сравнению изображений

    # № 1
    img1 = cv2.imread(temp_catalog + '/screenshot.png')
    height1, width1, _ = img1.shape
    # Сравнение скриншота с ранее сохраненными
    for filename in os.listdir(save_catalog):
        if filename.endswith('.png'):  # Проверка расширения файла
            # № 2
            img2 = cv2.imread(os.path.join(save_catalog, filename))
            height2, width2, _ = img2.shape

            h = min(height1, height2)
            w = min(width1, width2)

            if check2image(img1, img2, h, w, precision_image):
                return True
    return False  # Совпадений не найдено

def check2image(img1, img2, height, width, precision_image):
    real_diff = 0  # Подсчитываем общее кол-во несовпадающих пикселей
    # Добавим пороговое значение после превышения которого сразу подтверждаем совпадение
    _all = height * width
    _maximum = _all * precision_image  # = Общее число пикселей * точность совпадения

    for y in range(height):
        for x in range(width):
            _ostatok = _all - (y+1)*(x+1)
            # Считаем модульный разброс по каждой компоненте отдельно, чтобы исключить случаи разных цветов одной интенсивности,
            # Также добавим округление в 10 раз, чтобы исключить невидимые расхождения для невооруженного взгляда,
            # т.к. в видеороликах может быть расхождение до 1 секунды между скриншотами из-за разницы в запуске
            diff_b = int(abs(int(img1[y, x, 0]) - int(img2[y, x, 0])) / 10)
            diff_g = int(abs(int(img1[y, x, 1]) - int(img2[y, x, 1])) / 10)
            diff_r = int(abs(int(img1[y, x, 2]) - int(img2[y, x, 2])) / 10)
            real_diff += 1 if diff_b + diff_g + diff_r == 0 else 0

            # Если даже все оставшиеся пиксели совпадут и мы не превысим порог точности, то сканировать дальше нет смысла
            # Говорим, что изображение не то, и идем сканировать следующее
            # Например если порог точности - 80% совпадения, а 30% пикселей уже не совпало, то смысла дальше смотреть нет.
            if real_diff + _ostatok < _maximum:
                return False
            if real_diff >= _maximum:
                return True
    return False



def save_or_clear_screenshot(found_close, cat_screen, x0, y0, x1, y1):
    # Сформируем постфикс к общему каталогу скриншотов, чтобы рассортировать изображения по габаритам
    height = y1 - y0
    width = x1 - x0
    temp_catalog = cat_screen + "/TEMP"
    save_catalog = cat_screen + "/" + str(height) + "_x_" + str(width)

    # Проверка наличия каталога и его создание
    if not os.path.exists(save_catalog):
        os.makedirs(save_catalog)

    if os.path.exists(temp_catalog + '/screenshot.png'):  # Проверка наличия файла
        # Если в прошлой итерации цикла мы не нашли выход, то изображение надо сохранить
        if not found_close:
            # Генерация уникального имени файла
            _name = 'screenshot_{}.png'.format(len(os.listdir(save_catalog)))
            filename = os.path.join(save_catalog, _name)

            # Сохранение текущего скриншота
            shutil.move(temp_catalog + '/screenshot.png', filename)
            return "Изображение сохранено в ЧС под названием: " + _name
        else:
            # Удаление текущего скриншота
            os.remove(temp_catalog + '/screenshot.png')
            return "Буфер ЧС очищен!"

    return ""