class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = [
        "__title",
        "__location",
        "__link",
        "__salary",
        "__employer",
        "__description",
        "__experience",
        "__source",
    ]

    def __init__(self, **kwargs):
        self.__title: str = kwargs["title"]
        self.__location: str = kwargs["location"]
        self.__link: str = kwargs["link"]
        self.__salary: dict | str = kwargs["salary"]
        self.__employer: str = kwargs.get("employer", "Не указан")
        self.__description: str = kwargs["description"]
        self.__experience: str = kwargs["experience"]
        self.__source: str = kwargs["source"]

        self.__validate()

    def __str__(self):
        description = self.__description.replace("\n", " ")

        if len(description) > 150:
            description = description[:147] + "..."

        result = (
            f"Вакансия: {self.__title}\n"
            f"Город: {self.__location}\n"
            f"Зарплата: {self.get_salary()}\n"
            f"Описание: {description}\n"
            f"Опыт работы: {self.__experience}\n"
            f"Ссылка на вакансию: {self.__link}\n"
            f"Источник: {self.__source}\n"
        )

        return result

    @property
    def title(self) -> str:
        return self.__title

    @property
    def location(self) -> str:
        return self.__location

    @property
    def employer(self) -> str:
        return self.__employer

    @property
    def description(self) -> str:
        return self.__description

    @property
    def experience(self) -> str:
        return self.__experience

    @property
    def link(self) -> str:
        return self.__link

    @property
    def source(self) -> str:
        return self.__source

    @property
    def salary_from(self) -> int:
        if isinstance(self.__salary, dict):
            return self.__salary.get("from", 0)
        else:
            salary_parts = self.__salary.split(" -> ")
            return int(float(salary_parts[0]))

    @property
    def salary_to(self) -> int:
        if isinstance(self.__salary, dict):
            return self.__salary.get("to", 0)
        else:
            salary_parts = self.__salary.split(" -> ")
            return int(float(salary_parts[1]))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты класса Vacancy.")
        return self.salary_from == other.salary_from

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError("Можно сравнивать только объекты класса Vacancy.")
        return self.salary_from < other.salary_from

    def get_salary(self) -> str:
        if isinstance(self.__salary, str):
            return self.__salary

        currency = self.__salary.get("currency", "RUB")
        salary_from = self.__salary.get("from", 0)
        salary_to = self.__salary.get("to", 0)

        return f"{salary_from} -> {salary_to} {currency}"

    def __validate(self) -> None:
        """Приватный метод валидации данных."""

        # Валидация salary
        if self.__salary is None:
            self.__salary = {"from": 0, "to": 0, "currency": "RUB"}
        elif isinstance(self.__salary, str):
            try:
                salary_parts = self.__salary.split(" -> ")
                self.__salary = {
                    "from": int(float(salary_parts[0])),
                    "to": int(float(salary_parts[1])),
                    "currency": "RUB",
                }
            except (IndexError, ValueError):
                self.__salary = {"from": 0, "to": 0, "currency": "RUB"}

        # Валидация остальных полей
        self.__title = str(self.__title) if self.__title else "Не указано"
        self.__location = str(self.__location) if self.__location else "Не указан"
        self.__link = str(self.__link) if self.__link else "Не указана"
        self.__description = (
            str(self.__description) if self.__description else "Не указано"
        )
        self.__experience = str(self.__experience) if self.__experience else "Не указан"
        self.__source = str(self.__source) if self.__source else "Не указан"

    def validate(self) -> None:
        """Публичный метод для валидации данных."""
        self.__validate()
