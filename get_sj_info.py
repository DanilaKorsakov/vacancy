import requests


def get_sj_vacancies(key, keyword, page):

		headers = {
				'X-Api-App-Id': key
		}

		params = {
				"town": "Moscow",
				"catalogues": 48,
				"keyword": keyword,
				"count": 100,
				"page": page
		}

		url = "https://api.superjob.ru/2.0/vacancies/"

		response = requests.get(url, headers=headers, params=params)
		response.raise_for_status()

		return response.json()['objects']


def predict_rub_salary_for_superJob(vacancies):

		sallary_average = []

		for vacancy in vacancies:
				if not vacancy['payment_from'] :
						sallary_average.append(None)
				elif vacancy['currency']!='rub':
						sallary_average.append(None)
				elif not vacancy['payment_to']:
						sallary_average.append(vacancy['payment_from'])
				else:
						sallary_average.append((vacancy['payment_from'] + vacancy['payment_to'])/2)

		return sallary_average


def get_sj_info(languages, sj_secret_key):

		key = sj_secret_key

		languages_info = {}

		for language in languages:

				vacancy_info = {
						'vacancies_found': 0
				}

				vacancies_found = 0
				vacancies_processed = 0
				vacancies_average = 0

				for page in range(5):
						vacancies = get_sj_vacancies(key, language, page)
						sallary_average = predict_rub_salary_for_superJob(vacancies)

						for salary in sallary_average:
								if salary != None:
										vacancies_processed+=1
										vacancies_average += salary
								vacancies_found+=1

				vacancy_info['vacancies_found'] = vacancies_found
				vacancy_info['vacancies_processed'] = vacancies_processed
				vacancy_info['average_salary'] = int(vacancies_average/vacancies_processed)

				languages_info[language] = vacancy_info

		return languages_info