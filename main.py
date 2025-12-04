import csv
import argparse
from tabulate import tabulate
from collections import defaultdict
from typing import List


#Функция, которая парсит аргументы командной строки
def parse_arguments():
    parser = argparse.ArgumentParser(description='Обработка CSV-файлов')
    parser.add_argument( '--files', nargs='+', help='Название(-ия) CSV-файла(-ов)')
    parser.add_argument('--report', default='report', help='Название отчёта')

    return parser.parse_args()


def read_csv(files: List) -> List[List[float]]:
    data = []
    pos_per_dict = defaultdict(list)

    #Считываем данные файлов в цикле, обрабатывая ошибки на читаемость файла
    for file in files:
        try:
            with open(file, encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for i in reader:
                        pos_per_dict[i['position']].append(float(i['performance']))
        except Exception as e:
            print(f"Ошибка при чтении файла {file}: {e}")

    for k, v in pos_per_dict.items():
        try:
            avg = sum(v) / len(v)
            data.append([k, round(avg, 2)])
        except ZeroDivisionError:
            print(f"Деление на 0")

    data.sort(reverse=True, key=lambda x: x[1])
    return data


def main():
    args = parse_arguments()
    print(type(args.files))
    table = read_csv(args.files)
    columns = ['position', 'performance']
    print(tabulate(table, headers=columns, showindex=range(1, len(table) + 1)))


if __name__ == "__main__":
    main()
