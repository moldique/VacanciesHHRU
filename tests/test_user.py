import pytest
from src.jsonSaver import JSONVacancyManager
from src.user import main
from src.Vacansies import Vacancy
from unittest.mock import patch
import builtins


@pytest.fixture
def sample_vacancies():
    """Фикстура создает тестовые вакансии с полным набором обязательных параметров"""
    return [
        Vacancy(
            title="Python Developer",
            location="Москва",
            link="http://example.com/python",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            employer="TechCorp",
            description="Разработка на Python и Django",
            experience="1-3 года",
            source="hh.ru",
        ),
        Vacancy(
            title="Java Developer",
            location="Санкт-Петербург",
            link="http://example.com/java",
            salary={"from": 120000, "to": None, "currency": "RUR"},
            employer="JavaSoft",
            description="Разработка на Java и Spring",
            experience="3-6 лет",
            source="hh.ru",
        ),
    ]


@pytest.fixture
def json_manager(tmp_path):
    """Фикстура создает менеджер вакансий с временным файлом"""
    test_file = tmp_path / "test_vacancies.json"
    return JSONVacancyManager(test_file)


def test_main_menu_option_1(monkeypatch, json_manager):
    """Тест для пункта меню 1 - поиск вакансий"""
    inputs = ["1", "python", "5"]  # Вводим 1, затем "python", затем 5 для выхода
    monkeypatch.setattr(builtins, "input", lambda _: inputs.pop(0))

    with patch("src.user.HHVacancies") as mock_hh:
        mock_instance = mock_hh.return_value
        mock_instance.get_vacancies.return_value = {"items": []}
        mock_instance.parse_vacancies.return_value = []

        with patch("src.user.JSONVacancyManager", return_value=json_manager):
            main()

    mock_hh.assert_called_once_with("python")


def test_main_menu_option_2(monkeypatch, json_manager, sample_vacancies, capsys):
    """Тест для пункта меню 2 - топ N вакансий"""
    inputs = ["2", "2", "5"]  # Вводим 2, затем 2 (количество), затем 5 для выхода
    monkeypatch.setattr(builtins, "input", lambda _: inputs.pop(0))

    with patch("src.user.JSONVacancyManager", return_value=json_manager):
        # Добавляем тестовые вакансии
        json_manager.add_vacancy(sample_vacancies)
        json_manager.save_to_file()

        main()

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "Вакансия: Python Developer" in captured.out
        assert "Вакансия: Java Developer" in captured.out


def test_main_menu_option_3(monkeypatch, json_manager, sample_vacancies, capsys):
    """Тест для пункта меню 3 - поиск по ключевому слову"""
    inputs = ["3", "Python", "5"]  # Вводим 3, затем "Python", затем 5 для выхода
    monkeypatch.setattr(builtins, "input", lambda _: inputs.pop(0))

    with patch("src.user.JSONVacancyManager", return_value=json_manager):
        json_manager.add_vacancy(sample_vacancies)
        json_manager.save_to_file()

        main()

        # Проверяем вывод
        captured = capsys.readouterr()
        assert "Python Developer" in captured.out
        assert "Java Developer" not in captured.out


def test_main_menu_option_4(monkeypatch, json_manager, sample_vacancies, capsys):
    """Тест для пункта меню 4 - удаление вакансий"""
    inputs = ["4", "Java", "5"]  # Вводим 4, затем "Java", затем 5 для выхода
    monkeypatch.setattr(builtins, "input", lambda _: inputs.pop(0))

    with patch("src.user.JSONVacancyManager", return_value=json_manager):
        json_manager.add_vacancy(sample_vacancies)
        initial_count = len(json_manager.vacancies)

        main()

        # Проверяем, что одна вакансия удалена
        assert len(json_manager.vacancies) == initial_count - 1
        assert all("Java" not in vac.title for vac in json_manager.vacancies)


def test_main_menu_invalid_option(monkeypatch, capsys):
    """Тест для неверного пункта меню"""
    inputs = ["6", "5"]  # Вводим неверный вариант 6, затем 5 для выхода
    monkeypatch.setattr(builtins, "input", lambda _: inputs.pop(0))

    main()

    captured = capsys.readouterr()
    assert "Неверный выбор" in captured.out
