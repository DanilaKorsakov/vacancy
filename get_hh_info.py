import requests


def predict_hh_rub_salary(salaries):

    average_salaries = []

    for salary in salaries:
        if not salary:
            average_salaries.append(None)
        elif salary['currency'] != 'RUR':
            average_salaries.append(None)
        elif salary['from'] and salary['to']:
            average_salaries.append((salary['from'] + salary['to'])/2)
        elif salary['from']:
            average_salaries.append(salary['from']*1.2)
        else:
            average_salaries.append(salary['to']*0.8)

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

        vacancies_processed = 0
        vacancies_average = 0

        for page in range(pages):

            salary_for_language, vacancies_counter = get_hh_vacancies(language, page)

            hh_average_salary = predict_hh_rub_salary(salary_for_language)

            for salary in hh_average_salary:
                if salary:
                    vacancies_processed += 1
                    vacancies_average += salary

            language_statistic['vacancies_found'] += vacancies_counter

        language_statistic['vacancies_processed'] = vacancies_processed

        if vacancies_processed:
            language_statistic['average_salary'] = int(vacancies_average/vacancies_processed)
        else:
            language_statistic['average_salary'] = 0

        hh_statistic[language] = language_statistic

    return hh_statistic