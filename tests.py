import sys
from tabulate import tabulate
from io import StringIO
from main import parse_arguments, read_csv


def test_parse_arguments_with_files_and_report(monkeypatch):
    # Имитируем запуск скрипта с аргументами
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'file1.csv', 'file2.csv', '--report', 'my_report'])
    args = parse_arguments()
    assert args.files == ['file1.csv', 'file2.csv']
    assert args.report == 'my_report'


def test_parse_arguments_without_report(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'file1.csv'])
    args = parse_arguments()
    assert args.files == ['file1.csv']
    assert args.report == 'report'


def test_read_csv_single_file(tmp_path):
    # Создаем временный CSV файл
    csv_content = """position,performance
Backend Developer, 4.2
DevOps Engineer, 4.0
DevOps Engineer, 4.8
"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding='utf-8')

    data = read_csv([str(file_path)])

    assert data == [['DevOps Engineer', 4.4], ['Backend Developer', 4.2]]


def test_read_csv_multiple_files(tmp_path):
    # Создаем два файла
    csv_content1 = """position,performance
Backend Developer, 4.8
DevOps Engineer, 4.2
"""
    csv_content2 = """position,performance
DevOps Engineer, 4.6
Data Engineer, 4.5
"""

    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    file1.write_text(csv_content1, encoding='utf-8')
    file2.write_text(csv_content2, encoding='utf-8')

    data = read_csv([str(file1), str(file2)])

    expected = [['Backend Developer', 4.8], ['Data Engineer', 4.5], ['DevOps Engineer', 4.4]]
    assert data == expected


def test_read_csv_handles_exceptions(capsys):
    # Передать файл, который нельзя открыть
    data = read_csv(['nonexistent_file.csv'])
    captured = capsys.readouterr()
    assert 'Ошибка при чтении файла' in captured.out
    # Так как файл не существует, data должен быть пустым
    assert data == []


def test_main_prints_table(capsys, tmp_path):
    csv_content = """position,performance
Backend Developer, 80
DevOps Engineer, 90
DevOps Engineer, 85
"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding='utf-8')


    class Args:
        files = [str(file_path)]
        report = 'report'


    table = read_csv(Args.files)

    output = StringIO()
    print(tabulate(table, headers=['position', 'performance'], showindex=range(1, len(table) + 1)), file=output)
    output_value = output.getvalue()
    assert 'Backend Developer' in output_value
    assert 'DevOps Engineer' in output_value
