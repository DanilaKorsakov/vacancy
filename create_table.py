import os

from terminaltables import  AsciiTable
from dotenv import load_dotenv

from get_hh_info import get_hh_statistic
from get_sj_info import get_sj_statistic


def create_table(title, languages_info):
  
    vacancies_table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    
    for language, vacancies_statistic in languages_info.items():
        vacancies_table.append([
          language,
          vacancies_statistic["vacancies_found"],
          vacancies_statistic["vacancies_processed"],
          vacancies_statistic["average_salary"]
        ])
      
    table = AsciiTable(vacancies_table)
    
    table.title = title
    
    return table.table


def main():

    load_dotenv()

    sj_secret_key = os.getenv('SJ_SECRET_KEY')

    languages = ['JS','Java','Python','Ruby','PHP','C++','C#','TypeScript']

    print(create_table('HeadHunter Moscow', get_hh_statistic(languages)))

    print(create_table('superJob Moscow', get_sj_statistic(languages, sj_secret_key)))


if __name__ == '__main__':
    main()


      

      