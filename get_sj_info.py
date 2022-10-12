import requests

from get_average_salaries import get_average_salaries


def get_sj_vacancies(key, keyword, page):

    headers = {
        'X-Api-App-Id': key
    }

    specialization_id = 48
    vacancies_for_page = 100

    params = {
        "town": "Moscow",
        "catalogues": specialization_id,
        "keyword": keyword,
        "count": vacancies_for_page,
        "page": page
    }

    url = "https://api.superjob.ru/2.0/vacancies/"

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()['objects']


def predict_rub_salary_for_superJob(vacancies):

    average_salaries = []

    for vacancy in vacancies:

        if vacancy['currency'] != 'rub':
            average_salaries.append(None)
        else:
            average_salaries.append(get_average_salaries(vacancy['payment_from'], vacancy['payment_to']))

    return average_salaries


def get_sj_statistic(languages, sj_secret_key):

    key = sj_secret_key

    sj_statistic = {}
    pages = 5

    for language in languages:

        language_statistic = {
            'vacancies_found': 0
        }

        found_vacancies = 0
        processed_vacancies = 0
        average_vacancies = 0

        for page in range(pages):
            vacancies = get_sj_vacancies(key, language, page)
            sj_average_salary = predict_rub_salary_for_superJob(vacancies)

            for salary in sj_average_salary:
                if salary:
                    processed_vacancies+=1
                    average_vacancies += salary
                found_vacancies += 1

        language_statistic['vacancies_found'] = found_vacancies
        language_statistic['vacancies_processed'] = processed_vacancies

        if processed_vacancies:
            language_statistic['average_salary'] = int(average_vacancies/processed_vacancies)
        else:
            language_statistic['average_salary'] = 0

        sj_statistic[language] = language_statistic

    return sj_statistic