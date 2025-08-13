from src.Vacansies import Vacancy
from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any


class AbstractVacancyAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def parse_vacancies(self, raw_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        pass


class HHVacancies(AbstractVacancyAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self, request: str):
        self._request = request

    def _fetch_vacancies(self) -> List[Dict[str, Any]]:
        """Приватный метод для отправки запроса к API."""
        url = "https://api.hh.ru/vacancies/"
        params = {"text": self._request, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Получить сырые данные вакансий."""
        return self._fetch_vacancies()

    def parse_vacancies(self, raw_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразовать сырые данные в список объектов Vacancy."""
        vacancies_list = []
        for item in raw_data:
            parsed_data = {
                "title": item.get("name", "..."),
                "location": item.get("area", {}).get("name", "..."),
                "link": item.get("alternate_url", "..."),
                "salary": (
                    {
                        "from": item.get("salary", {}).get("from", 0),
                        "to": item.get("salary", {}).get("to", 0),
                        "currency": item.get("salary", {})
                        .get("currency", "RUB")
                        .upper(),
                    }
                    if item.get("salary")
                    else {"from": 0, "to": 0, "currency": "RUB"}
                ),
                "employer": item.get("employer", {}).get("name", "..."),
                "description": item.get("snippet", {}).get("responsibility", "..."),
                "experience": item.get("experience", {}).get("name", "..."),
                "source": "hh.ru",
            }
            vacancy = Vacancy(**parsed_data)
            vacancy.validate()
            vacancies_list.append(vacancy)
        return vacancies_list
