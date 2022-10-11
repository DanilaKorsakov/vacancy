import requests


def predict_hh_rub_salary(sallaries):

		sallary_result = []

		for salary in sallaries:
				if salary == None:
						sallary_result.append(None)
				elif salary['currency'] != 'RUR':
						sallary_result.append(None)
				elif salary['from'] !=None and salary['to'] !=None:
						sallary_result.append((salary['from'] + salary['to'])/2)
				elif salary['from'] !=None:
						sallary_result.append(salary['from']*1.2)
				else:
						sallary_result.append(salary['to']*0.8)

		return sallary_result


def get_hh_vacancies(text, page):

		url = 'https://api.hh.ru/vacancies/'

		payload = {
				'text': text,
				'period': 30,
				'area':1,
				'page': page,
				'per_page':100,
				'specialization': 1.221
		}

		response = requests.get(url, params=payload)
		response.raise_for_status()

		vacancies = response.json()['items']

		sallary_infos =[]
		count = 0

		for vacany in vacancies:
				sallary_infos.append(vacany['salary'])
				count+=1

		return sallary_infos, count


def get_hh_info(languages):

		languages_info = {}

		for language in languages:

				vacancy_info = {
						'vacancies_found': 0
				}

				vacancies_processed = 0
				vacancies_average = 0

				for page in range(20):

						salary_for_language, vacancies_counter = get_hh_vacancies(language, page)

						salary_average = predict_hh_rub_salary(salary_for_language)

						for salary in salary_average:
								if salary != None:
										vacancies_processed+=1
										vacancies_average += salary

						vacancy_info['vacancies_found'] += vacancies_counter

				vacancy_info['vacancies_processed'] = vacancies_processed

				if vacancies_processed !=0:
						vacancy_info['average_salary'] = int(vacancies_average/vacancies_processed)
				else:
						vacancy_info['average_salary'] = 0

				languages_info[language] = vacancy_info

		return languages_info