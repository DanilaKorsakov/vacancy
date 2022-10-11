import os

from terminaltables import  AsciiTable
from dotenv import load_dotenv

from get_hh_info import get_hh_info
from get_sj_info import get_sj_info


def create_table(title, languages_info):
  
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    
    for language, vacancies_info in languages_info.items():
        table_data.append([
          language,
          vacancies_info["vacancies_found"],
          vacancies_info["vacancies_processed"],
          vacancies_info["average_salary"]
        ])
      
    table = AsciiTable(table_data)
    
    table.title = title
    
    return table.table


def main():

    load_dotenv()

    sj_secret_key = os.getenv('SJ_SECRET_KEY')

    languages = ['JS','Java','Python','Ruby','PHP','C++','C#','TypeScript']

    print(create_table('HeadHunter Moscow', get_hh_info(languages)))

    print(create_table('superJob Moscow', get_sj_info(languages, sj_secret_key)))


if __name__ == '__main__':
    main()


      

      