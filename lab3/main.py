import csv
import pickle
from typing import List, Any, Optional, Dict, Union
from datetime import datetime

class Table:
    def __init__(self, columns: List[str], data: List[List[Any]] = None):
        self.columns = columns
        self.data = data if data else []

    def add_row(self, row: List[Any]):
        if len(row) != len(self.columns):
            raise ValueError("Длина строки не соответствует количеству столбцов")
        self.data.append(row)

    def to_dict(self):
        return {"columns": self.columns, "data": self.data}

    @classmethod
    def from_dict(cls, table_dict: Dict[str, Any]):
        return cls(columns=table_dict["columns"], data=table_dict["data"])

    #2
    def get_rows_by_number(self, start: int, stop: Optional[int] = None, copy_table: bool = False):
        if stop is None:
            stop = start
        rows = self.data[start:stop+1]
        return Table(self.columns, [row.copy() for row in rows] if copy_table else rows)

    def get_rows_by_index(self, *values, copy_table: bool = False):
        rows = [row for row in self.data if row[0] in values]
        return Table(self.columns, [row.copy() for row in rows] if copy_table else rows)

    def get_column_types(self, by_number: bool = True) -> Dict[Any, type]:
        types = {}
        for i, col in enumerate(self.columns):
            column = [row[i] for row in self.data if row[i] is not None]
            value_type = set(type(x) for x in column)
            if len(value_type) == 1:
                types[i if by_number else col] = list(value_type)[0]
                #Дополнительное задание 5
                try:
                    datetime_values = [datetime.strptime(str(v), "%Y-%m-%d") if isinstance(v, str) and len(v) == 10 else v for v in column]
                    if all(isinstance(v, datetime) for v in datetime_values):
                        types[i if by_number else col] = datetime
                except ValueError:
                    types[i if by_number else col] = str
            else:
                types[i if by_number else col] = str
        return types

    def set_column_types(self, types_dict: Dict[Any, type], by_number: bool = True):
        for key, col_type in types_dict.items():
            col_idx = key if by_number else self.columns.index(key)
            for row in self.data:
                if row[col_idx] is not None:
                    row[col_idx] = col_type(row[col_idx])

    def get_values(self, column=0) -> List[Any]:
        if isinstance(column, str):
            column = self.columns.index(column)
        return [row[column] for row in self.data]

    def get_value(self, column=0) -> Any:
        if len(self.data) != 1:
            raise ValueError("В таблице больше одной строки")
        if isinstance(column, str):
            column = self.columns.index(column)
        return self.data[0][column]

    def set_values(self, values: List[Any], column=0):
        if len(values) != len(self.data):
            raise ValueError("Количество значений не равно количеству строк таблицы")
        if isinstance(column, str):
            column = self.columns.index(column)
        for i, value in enumerate(values):
            self.data[i][column] = value

    def set_value(self, value: Any, column=0):
        if len(self.data) != 1:
            raise ValueError("В таблице больше одной строки")
        if isinstance(column, str):
            column = self.columns.index(column)
        self.data[0][column] = value

    def print_table(self):
        print("\t".join(self.columns))
        for row in self.data:
            print("\t".join(map(str, row)))

    #Дополнительное задание 3
    @staticmethod
    def concat(table1, table2):
        if table1.columns != table2.columns:
            raise ValueError("Таблицы имеют разную структуру столбцов и не могут быть объединены")
        return Table(columns=table1.columns, data=table1.data + table2.data)

    def split(self, row_number: int):
        table1 = Table(columns=self.columns, data=self.data[:row_number])
        table2 = Table(columns=self.columns, data=self.data[row_number:])
        return table1, table2

    #Дополнительное задание 4
    @staticmethod
    def auto_detect_column_types(data: List[List[Any]]) -> Dict[int, type]:
        column_types = {}
        for col_idx in range(len(data[0])):
            sample_values = [row[col_idx] for row in data if row[col_idx] is not None]
            col_type = str
            
            if sample_values:
                if all(val in ["yes", "no", "True", "False", 1, 0] for val in sample_values):
                    col_type = bool
                elif all(isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit()) for v in sample_values):
                    # Attempt to cast values to integers or floats
                    try:
                        int_values = [int(v) if isinstance(v, str) and v.replace('.', '', 1).isdigit() else v for v in sample_values]
                        if all(isinstance(v, int) for v in int_values):
                            col_type = int
                        else:
                            col_type = float
                    except ValueError:
                        col_type = str
                #Дополнительное задание 5
                try:
                    datetime_values = [datetime.strptime(str(v), "%Y-%m-%d") if isinstance(v, str) and len(v) == 10 else v for v in sample_values]
                    if all(isinstance(v, datetime) for v in datetime_values):
                        col_type = datetime
                except ValueError:
                    col_type = str
            
            column_types[col_idx] = col_type
        return column_types

    
    #Дополнительное задание 7
    def eq(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] == row[col2] for row in self.data]

    def gr(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] > row[col2] for row in self.data]

    def ls(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] < row[col2] for row in self.data]

    def ge(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] >= row[col2] for row in self.data]

    def le(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] <= row[col2] for row in self.data]

    def ne(self, col1: int, col2: int) -> List[bool]:
        
        if len(self.data) == 0:
            return []
        return [row[col1] != row[col2] for row in self.data]

    def filter_rows(self, bool_list: List[bool], copy_table: bool = False) -> 'Table':

        if len(bool_list) != len(self.data):
            raise ValueError("Длина bool_list должна соответствовать количеству строк в таблице")
        
        filtered_data = [row for row, condition in zip(self.data, bool_list) if condition]
        return Table(self.columns, [row.copy() for row in filtered_data] if copy_table else filtered_data)

#1 + дополнительное задание 1
def load_table(*filenames: str, auto_detect_types: bool = False) -> Table:

    table = None

    for filename in filenames:
        if filename.endswith('.csv'):
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                if table is None:
                    table = Table(columns=header)
                elif table.columns != header:
                    raise ValueError(f"Несоответствие структуры столбцов в файле {filename}")

                for row in reader:
                    table.add_row(row)

        elif filename.endswith('.pkl') or filename.endswith('.pickle'):
            with open(filename, 'rb') as f:
                partial_table = pickle.load(f)
                partial_table_obj = Table.from_dict(partial_table)
                if table is None:
                    table = partial_table_obj
                elif table.columns != partial_table_obj.columns:
                    raise ValueError(f"Несоответствие структуры столбцов в файле {filename}")

                table.data.extend(partial_table_obj.data)

        else:
            raise ValueError("Неподдерживаемый формат файла. Используйте '.csv' или '.pickle'")

    if table is None:
        raise ValueError("Загружена недопустимая таблица")
        
    if auto_detect_types:
        column_types = Table.auto_detect_column_types(table.data)
        table.set_column_types(column_types, by_number=True)
        
    return table


def save_table(table: Table, filename: str, max_rows: Optional[int] = None):

    if filename.endswith('.csv'):
        file_format = 'csv'
    elif filename.endswith('.pkl') or filename.endswith('.pickle'):
        file_format = 'pickle'
    elif filename.endswith('.txt'):
        file_format = 'txt'
    else:
        raise ValueError("Неподдерживаемый формат файла. Используйте '.csv' или '.pickle'")

    if max_rows is None:
        if file_format == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(table.columns)
                writer.writerows(table.data)
        elif file_format == 'pickle':
            with open(filename, 'wb') as f:
                pickle.dump(table.to_dict(), f)
        elif file_format == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("\t".join(table.columns) + "\n")
                for row in table.data:
                    f.write("\t".join(map(str, row)) + "\n")
    #Дополнительное задание 2
    else:
        num_files = (len(table.data) + max_rows - 1) // max_rows
        for i in range(num_files):
            split_data = table.data[i * max_rows:(i + 1) * max_rows]
            split_filename = f"{filename}_part{i + 1}.{file_format}"
            if file_format == 'csv':
                with open(split_filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(table.columns)
                    writer.writerows(split_data)
            elif file_format == 'pickle':
                with open(split_filename, 'wb') as f:
                    pickle.dump({"columns": table.columns, "data": split_data}, f)
            elif file_format == 'txt':
                with open(split_filename, 'w', encoding='utf-8') as f:
                    f.write("\t".join(table.columns) + "\n")
                    for row in split_data:
                        f.write("\t".join(map(str, row)) + "\n")


if __name__ == '__main__':
    #Пример вызова функций
    table = load_table('house-price.csv', 'house-price.pkl', auto_detect_types=True)
    print('Вывод таблицы')
    table.print_table()
    print()

    print('Функция get_rows_by_number(1, 4)')
    table.get_rows_by_number(1, 4).print_table()
    print('Функция get_rows_by_number(10)')
    table.get_rows_by_number(10).print_table()
    print()

    print('Функция get_rows_by_index(13300000,12250000)')
    table.get_rows_by_index(13300000,12250000).print_table()
    print()

    print('Функция get_column_types(False)')
    print(table.get_column_types(False))
    print()

    print('Функция set_column_types({5: int}')
    table.set_column_types({5: int})
    table.print_table()
    print()

    print('Функция get_values(4)')
    print(table.get_values(4))
    print()

    print('Функция set_values([1, 2, 3, 4, 5]*4, 6)')
    table.set_values([1, 2, 3, 4, 5]*4, 6)
    table.print_table()
    print()

    #Функция save_table
    save_table(table, 'new_file.csv', 15)

    table1 = load_table('new_file.csv_part1.csv', auto_detect_types=True)
    table2 = load_table('new_file.csv_part2.csv', auto_detect_types=True)

    print('Функция concat(table1, table2)')
    Table.concat(table1, table2).print_table()
    print()

    print('Функция split(7)[0]')
    table.split(7)[0].print_table()
    print('Функция split(7)[1]')
    table.split(7)[1].print_table()
    print()

    print('Функция eq(2, 3)')
    print(table.eq(2, 3))
    print()

    print('Функция gr(2, 3)')
    print(table.gr(2, 3))
    print()

    print('Функция ls(2, 3)')
    print(table.ls(2, 3))
    print()

    print('Функция ge(2, 3)')
    print(table.ge(2, 3))
    print()

    print('Функция le(2, 3)')
    print(table.le(2, 3))
    print()

    print('Функция ge(2, 3)')
    print(table.ne(2, 3))
    print()

    print('Функция filter_rows(table.le(2, 3))')
    table.filter_rows(table.le(2, 3)).print_table()
