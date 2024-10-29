import csv
import os
import json


class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path='files'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        keys = {
            'название': ['название', 'продукт', 'товар', 'наименование'],
            'цена': ['цена', 'розница'],
            'вес': ['фасовка', 'масса', 'вес']
        }
        datas = os.listdir(file_path)
        for file in datas:
            if file.endswith('.csv') and file.startswith('price'):
                with open(os.path.join(file_path, file), 'r', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=',')
                    for row in reader:
                        info = {'файл': file}
                        for key, possible_keys in keys.items():
                            for possible_key in possible_keys:
                                if possible_key in row:
                                    info[key] = row[possible_key]
                                    break
                        self.data.append(info)
                print(f'Файл {file} прочитан')
            else:
                print(f'Файл {file} не является CSV')

    def export_to_console(self):
        for id, element in enumerate(self.data, 1):
            print(
                f"{id}. Название: {element.get('название')}, Цена: {element.get('цена')},"
                f" Вес: {element.get('вес')}, Файл: {element.get('файл')}")


    def _search_product_price_weight(self, headers):
        res = []

        for element in self.data:
            if headers.lower() in element.get('название', '').lower():
                res.append(element)

        sort_res = sorted(res, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sort_res




    def export_to_html(self, fname='output.html'):
        if self.data:
            sort = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            with open(fname, 'w', encoding='utf-8') as file:
                file.write('''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset='UTF-8'>
                            <title>Позиции продуктов</title>
                        </head>
                        <body>
                            <table>
                                <tr>
                                    <th>Номер</th>
                                    <th>Название</th>
                                    <th>Цена</th>
                                    <th>Фасовка</th>
                                    <th>Файл</th>
                                    <th>Цена за кг.</th>
                                </tr>
                        ''')
                for id, row in enumerate(sort, start=1):
                    name = row.get('название', '')
                    weight = row.get('вес', '')
                    cost = row.get('цена', '')
                    try:
                        price = float(row.get('цена', 0)) / float(row.get('вес', 1))
                    except ValueError:
                        price = 0
                    file.write(
                        f"<tr><td>{id}</td><td>{name}</td><td>{cost}</td><td>{weight}"
                        f"</td><td>{row.get('файл', '')}</td><td>{price:.1f}</td></tr>"
                    )
                file.write('''
                            </table>
                        </body>
                        </html>
                        ''')
            print(f"HTML файл успешно создан: {fname}")
        else:
            print("Нет данных для экспорта в HTML файл.")
    
    def find_text(self, text):
        res = []
        for row in self.data:
            if 'название' in row and text.lower() in row['название'].lower():
                res.append(row)

        sort_res = sorted(res, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))

        if sort_res:

            for id, result in enumerate(sort_res, 1):
                print(
                    f"{id}. Название: {result.get('название')}, Цена: {result.get('цена')}, Вес: {result.get('вес')},"
                    f" Файл: {result.get('файл')}, Цена за кг: {float(result.get('цена', 0)) / float(result.get('вес', 1))}")
        else:
            print("По вашему результату ничего не найдено")

        return sort_res

    
pm = PriceMachine()
print(pm.load_prices())

'''
    Логика работы программы
'''
while True:
    search_res = input("Введите наименование товара (для завершения работы 'exit'): ")
    if search_res.lower() == "exit":
        print("Работа завершена.")
        break
    results = pm.find_text(search_res)

print('the end')
print(pm.export_to_html())

