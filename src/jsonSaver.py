import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from src.Vacansies import Vacancy


class VacancyManager(ABC):
    """Абстрактный класс для работы с файлами вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавить вакансию/вакансии в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, query):
        """Получить вакансии по ключевому слову."""
        pass

    @abstractmethod
    def save_to_file(self):
        """Сохранить вакансии в файл."""
        pass

    @abstractmethod
    def load_from_file(self):
        """Загрузить вакансии из файла."""
        pass

    @abstractmethod
    def delete_vacancies_by_keyword(self, keyword):
        """Удалить вакансии по ключевому слову."""
        pass


class JSONVacancyManager(VacancyManager):
    """Класс для работы с вакансиями в JSON-файле."""

    def __init__(self, filename="vacancies.json"):
        self.__filepath = os.path.join(Path(__file__).parent.parent, "data")
        self.__filename = filename
        self.vacancies = []

        os.makedirs(self.__filepath, exist_ok=True)
        self.load_from_file()

    def add_vacancy(self, vacancy_list):
        """Добавляет вакансии, исключая дубликаты."""
        existing_links = {v.link for v in self.vacancies}
        new_vacancies = [v for v in vacancy_list if v.link not in existing_links]
        self.vacancies.extend(new_vacancies)
        self.save_to_file()

    def get_vacancies(self, query=None):
        """Возвращает вакансии, отфильтрованные по запросу."""
        if not query:
            results = self.vacancies.copy()
        else:
            query = query.lower()
            results = [
                v
                for v in self.vacancies
                if (
                    query in v.description.lower()
                    or query in v.title.lower()
                    or query in v.employer.lower()
                )
            ]

        results.sort(reverse=True)
        return results

    def save_to_file(self):
        """Сохраняет вакансии в JSON-файл."""
        data = [
            {
                "title": v.title,
                "location": v.location,
                "employer": v.employer,
                "salary": v.get_salary(),
                "description": v.description,
                "experience": v.experience,
                "link": v.link,
                "source": v.source,
            }
            for v in self.vacancies
        ]

        file_path = os.path.join(self.__filepath, self.__filename)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка ввода-вывода при сохранении файла: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при сохранении файла: {e}")

    def load_from_file(self):
        """Загружает вакансии из JSON-файла."""
        file_path = os.path.join(self.__filepath, self.__filename)
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.vacancies = [Vacancy(**v) for v in data]
                    return self.vacancies
            return []
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден или содержит некорректные данные.")
            return []
        except IOError:
            print("Файл не найден. Будет создан новый при сохранении.")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке файла: {e}")
            return []

    def delete_vacancies_by_keyword(self, keyword):
        """Удаляет вакансии, содержащие ключевое слово."""
        if not keyword:
            return

        keyword = keyword.lower()
        initial_count = len(self.vacancies)
        self.vacancies = [
            v
            for v in self.vacancies
            if (
                keyword not in v.description.lower()
                and keyword not in v.title.lower()
                and keyword not in v.employer.lower()
            )
        ]

        if len(self.vacancies) < initial_count:
            self.save_to_file()
