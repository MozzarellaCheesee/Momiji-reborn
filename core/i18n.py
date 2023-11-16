import disnake

import json
from pathlib import Path

Momiji_dir = Path(__file__).parents[1]


class LocalizationStorage:

    def __init__(self, path: str = None):
        self._loc = {}
        if path:
            self.load(f"locale/in_commands/{path}")

    def load(self, path: str):

        """
        Загружает файл/ы локализации
        :param path: путь к файлу/директории
        :return:
        """

        path = Momiji_dir.joinpath(path)
        if path.is_file():
            self._load_file(path)
        elif path.is_dir():
            for file in path.glob("*.json"):
                if not file.is_file():
                    continue
                self._load_file(file)

    def _load_file(self, file: Path):
        data = json.loads(file.read_text("utf-8"))
        self._loc[file.stem] = data

    def __call__(self, locale: disnake.Locale, command_name: str):
        """
        Возвращает словарь ключей по заданному языку
        :param locale: локализация юзера
        :return:
        """
        localization_dict = self._loc.get(str(locale)) or self._loc.get("en-US")
        return localization_dict[command_name]
