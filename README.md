# crush_them_all_bot

pyinstaller --onefile main.py main_window.py screen.py testing.py backend.py loger.py

* v. 1.1 - Добавлен черный список рекламы и строка состояния
* v. 1.1.1 - Исправлено сравнение изображений черного списка и опечатка в методе сохранения
* v. 1.2 - Добавлено логирование, произведен рефакторинг функции поиска сундуков, добавлен подсчет числа "найденных сундуков" в логах
* v. 1.2.1 - Увеличены задержки между кликами перезагрузки, переписана функция сравнения изображений черного списка, исправлена логика добавления в ЧС
* v. 1.2.2 - Исправление логирования подсчета сундуков и ошибок перезапуска, логирование пропусков исключений, увеличение задержек
                между кликами закрытия рекламы чтобы не попасть в промежуток между закрытием рекламы и появлением "получалки"
* v. 1.2.3 - Исправлен запуск воспроизведения. Доработан процесс логирования. Добавлено сохранение проблемных экранов
* v. 1.2.4 - Возврат к старой системе подсчета золотых сундуков, с оставлением индикации нахождения,
            добавлено опциональное отображение времени событий в логах (для однострочных сообщений теперь не показываем время)
* v. 1.3.0 - Добавлен поиск крылатых сундуков по аналогии с золотыми с отдельной зоной поиска и флагом отключения опции
            логирование также доработано в связи с нововведением
            Добавлены бустеры с возможностью отключения опции.
