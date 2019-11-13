from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

        self.MAIN_MENU = {
            "-u":  self.update_data,
            "-t":  self.get_tags,
            "-ap": self.get_articles,
            "-aw": self.get_articles_week,
            "-tt": self.top_tags,
            "-ta": self.top_authors,
            "-h":  self.print_main_menu,
            "-e":  self.close_app
        }

    def start_app(self):
        self.view.app_print(self.view.GREETING)
        if self.model.conn_error:
            self.close_app(self.model.conn_error)
        else:
            self.view.app_print(self.view.DB_CONNECTED)
            self.view.app_print(self.model.DB_VERS)
            self.update_data()
        while 1:
            command = input(self.view.MAIN).strip()
            if command in self.MAIN_MENU.keys():
                self.MAIN_MENU[command]()
            else:
                self.view.print_error(self.view.UNKNOWN_COMMAND)

    def print_main_menu(self):
        self.view.print_menu(self.view.MAIN_MENU)

    def update_data(self):
        self.view.app_print(self.view.WAIT)
        if self.model.update_data():
            self.view.app_print(self.view.UPDATED)
        else:
            self.view.print_error(self.view.NOT_UPDATED)

    def get_tags(self):
        result = self.model.get_tags()
        self.view.app_print(self.view.ALL_TAGS)
        self.view.print_result(result)

    def top_tags(self):
        result = self.model.top_tags()
        self.view.app_print(self.view.TOP_TAGS)
        self.view.print_count_result(result)

    def top_authors(self):
        result = self.model.top_authors()
        self.view.app_print(self.view.TOP_AUTHORS)
        self.view.print_count_result(result)

    def get_articles(self):
        while 1:
            command = input(self.view.INPUT_TAG + self.view.ESCAPE).strip()
            if command == "-e":
                return
            elif not self.model.check_wrong_tag(command):
                self.view.print_error(self.view.WRONG_TAG)
            else:
                tag = command
                while 1:
                    command = input(self.view.START_DAY + self.view.ESCAPE).strip()
                    if command == "-e":
                        return
                    start = self.model.convert_date(command)
                    if type(start) is ValueError:
                        self.view.print_error(self.view.WRONG_DATE)
                        continue

                    while 1:
                        command = input(self.view.END_DAY + self.view.ESCAPE).strip()
                        if command == "-e":
                            return
                        end = self.model.convert_date(command)
                        if type(end) is ValueError:
                            self.view.print_error(self.view.WRONG_DATE)
                            continue

                        result = self.model.find_articles(tag, start, end)
                        self.view.print_row(result)
                        return

    def get_articles_week(self):
        result = self.model.get_articles_week()
        self.view.print_row(result)

    def close_app(self, error=''):
        if error:
            self.view.print_error(str(error))
        self.view.app_print(self.view.EXIT)
        exit()
