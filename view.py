

class View:

    def __init__(self):
        self.COMMON_MENU = {
            "-h": "\tПоказать команды",
            "-e": "\tВыход"
        }
        self.MAIN_MENU = {
            "-u":  "\tОбновить данные",
            "-t":  "\tПоказать все теги",
            "-ap": "Поиск статей по тегу за период",
            "-aw": "Показать статьи за последнюю неделю",
            "-tt": "10 самых популярных тегов",
            "-ta": "10 самых популярных авторов"
        }
        self.GREETING = "Программа 'Аналитика ХАБРАХАБРА'"
        self.MAIN = "\nВведите команду или -h:"
        self.WAIT = "Обновление базы. Подождите..."
        self.ALL_TAGS = "Список всех тегов:\n"
        self.TOP_TAGS = "10 самых популярных тегов:\n"
        self.TOP_AUTHORS = "10 самых популярных авторов:\n"
        self.INPUT_TAG = "Введите тег для поиска статей"
        self.START_DAY = "Введите дату начала поиска в формате DD-MM-YY"
        self.END_DAY = "Введите дату конца поиска в формате DD-MM-YY"
        self.TITLE = "Название:"
        self.AUTHOR = "Автор:"
        self.DATE = "Дата публикации:"
        self.TAGS = "Теги:"
        self.UNKNOWN_COMMAND = "неизвестная команда"
        self.UPDATED = "База обновлена!"
        self.NOT_UPDATED = "сбой обновления. Проверьте соединение с Интернет"
        self.DB_CONNECTED = "Соединение с БД установлено:"
        self.ESCAPE = " или -e:"
        self.ERROR = "Ошибка: "
        self.NO_CONNECTION = "нет соединения с базой"
        self.WRONG_TAG = "данного тега в базе не найдено"
        self.WRONG_DATE = "неправильный формат даты"
        self.EXIT = "Приложение остановлено"

    @staticmethod
    def print_dict(dict_, header=None):
        if header:
            print(header)
        for key, value in dict_.items():
            print("{}:\t{}".format(key, value))

    @staticmethod
    def print_result(result):
        for item in result:
            print(item[0])

    @staticmethod
    def print_count_result(result):
        for item in result:
            print('{} ({})'.format(item[0], item[1]))

    def print_row(self, result):
        for item in result:
            print('\n{}\n\t{}\n{}\n\t{}\n{}\n\t{}\n{}'.format(self.TITLE, item[1], self.AUTHOR, item[2], self.DATE, item[3], self.TAGS))
            for tag in item[4]:
                print('\t{}'.format(tag))

    @staticmethod
    def app_print(item):
        print(item)

    def print_menu(self, menu):
        self.print_dict(menu)
        self.print_dict(self.COMMON_MENU)

    def print_error(self, error):
        print(self.ERROR + error)
