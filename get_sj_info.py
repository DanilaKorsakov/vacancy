import requests


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

    salary_average = []

    for vacancy in vacancies:

        if vacancy['currency'] != 'rub':
            salary_average.append(None)
        elif vacancy['payment_from'] and vacancy['payment_to']:
            salary_average.append((vacancy['payment_from'] + vacancy['payment_to'])/2)
        elif vacancy['payment_from']:
            salary_average.append(vacancy['payment_from']*1.2)
        else:
            salary_average.append(vacancy['payment_to']*0.8)

    return salary_average


def get_sj_statistic(languages, sj_secret_key):

    key = sj_secret_key

    sj_statistic = {}
    pages = 5

    for language in languages:

        language_statistic = {
            'vacancies_found': 0
        }

        vacancies_found = 0
        vacancies_processed = 0
        vacancies_average = 0

        for page in range(pages):
            vacancies = get_sj_vacancies(key, language, page)
            sj_average_salary = predict_rub_salary_for_superJob(vacancies)

            for salary in sj_average_salary:
                if salary:
                    vacancies_processed+=1
                    vacancies_average += salary
                vacancies_found += 1

        language_statistic['vacancies_found'] = vacancies_found
        language_statistic['vacancies_processed'] = vacancies_processed

        if vacancies_processed:
            language_statistic['average_salary'] = int(vacancies_average/vacancies_processed)
        else:
            language_statistic['average_salary'] = 0

        sj_statistic[language] = language_statistic

    return sj_statistic