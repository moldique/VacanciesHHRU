from src.api_class import HHVacancies
from src.jsonSaver import JSONVacancyManager


def main():
    print("Добро пожаловать в программу поиска вакансий!")

    # Инициализация менеджера вакансий
    manager = JSONVacancyManager("vacancies.json")

    while True:
        print("\nМеню:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Поиск вакансий по ключевому слову в описании")
        print("4. Удалить вакансии по ключевому слову")
        print("5. Выход")

        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            search_query = input("Введите поисковый запрос: ")
            try:
                hh = HHVacancies(search_query)
                raw_vacancies = hh.get_vacancies()
                vacancies = hh.parse_vacancies(raw_vacancies)
                manager.add_vacancy(vacancies)
                manager.save_to_file()
                print(f"Найдено и сохранено {len(vacancies)} вакансий.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            try:
                n = int(input("Введите количество вакансий для отображения: "))
                all_vacancies = manager.load_from_file()
                all_vacancies.sort(reverse=True)
                top_n = all_vacancies[:n]
                for i, vacancy in enumerate(top_n, 1):
                    print(f"\nВакансия #{i}")
                    print(vacancy)
            except ValueError:
                print("Пожалуйста, введите корректное число.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ")
            try:
                filtered = manager.get_vacancies(keyword.lower())
                for i, vacancy in enumerate(filtered, 1):
                    print(f"\nВакансия #{i}")
                    print(vacancy)
                print(f"\nНайдено {len(filtered)} вакансий.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "4":
            keyword = input("Введите ключевое слово для удаления вакансий: ")
            try:
                before = len(manager.vacancies)
                manager.delete_vacancies_by_keyword(keyword)
                after = len(manager.vacancies)
                print(f"Удалено {before - after} вакансий.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")


if __name__ == "__main__":
    main()
