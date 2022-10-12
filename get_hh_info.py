import requests

from get_average_salaries import get_average_salaries


def predict_hh_rub_salary(salaries):

    average_salaries = []

    for salary in salaries:
        if not salary:
            average_salaries.append(None)
        elif salary['currency'] != 'RUR':
            average_salaries.append(None)
        else:
            average_salaries.append(get_average_salaries(salary['from'], salary['to']))

    return average_salaries


def get_hh_vacancies(text, page):

    url = 'https://api.hh.ru/vacancies/'

    area_id = 1
    vacancies_for_page = 100
    specialization_id = 1.221
    time_period = 30

    payload = {
        'text': text,
        'period': time_period,
        'area': area_id,
        'page': page,
        'per_page': vacancies_for_page,
        'specialization': specialization_id
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    vacancies = response.json()['items']

    salaries = []

    for vacancy in vacancies:
        salaries.append(vacancy['salary'])

    return salaries, len(vacancies)


def get_hh_statistic(languages):

    hh_statistic = {}
    pages=20

    for language in languages:

        language_statistic = {
            'vacancies_found': 0
        }

        processed_vacancies = 0
        average_vacancies = 0

        for page in range(pages):

            salary_for_language, vacancies_counter = get_hh_vacancies(language, page)

            hh_average_salary = predict_hh_rub_salary(salary_for_language)

            for salary in hh_average_salary:
                if salary:
                    processed_vacancies += 1
                    average_vacancies += salary

            language_statistic['vacancies_found'] += vacancies_counter

        language_statistic['vacancies_processed'] = processed_vacancies

        if processed_vacancies:
            language_statistic['average_salary'] = int(average_vacancies/processed_vacancies)
        else:
            language_statistic['average_salary'] = 0

        hh_statistic[language] = language_statistic

    return hh_statistic