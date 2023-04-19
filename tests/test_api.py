import pytest
import requests
from main import Yandex

@pytest.fixture(scope='module')
def create_Yandex_connection():
    """Фикстура, которая создает связь с Yandex.диском"""
    ya_token = input('Введите токен для Яндекс.Полигон: ')
    creater = Yandex(ya_token)
    return creater

@pytest.fixture(scope='module') 
def get_headers(create_Yandex_connection):
    """Фикстура, которая создает заголовки для запросов к Yndex.диску"""
    return {
        'Content_Type': 'application/json',
        'Authorization': f'OAuth {create_Yandex_connection.token}'
        }

@pytest.fixture(scope='module')
def input_folder_name():
    """Фикстура, которая запрашивает у пользователя имя создаваемой папки"""
    folder_name = input('Введите имя новой папки (допустимо использовать: буквы, цифры, пробелы и подчеркивания):')
    return folder_name
    
@pytest.fixture(scope='module')
def test_Yandex_create_new_folder(create_Yandex_connection, input_folder_name):
    """Тест(фикстура) полученния результата о создании папки на Yandex.диске"""
    rez = create_Yandex_connection.create_new_folder(input_folder_name)
    assert rez != 400, 'Код 400. Отрицательный результат. Некорректные данные'
    assert rez != 401, 'Код 401. Отрицательный результат. Пользователь не авторизован'
    assert rez != 404, 'Код 404. Отрицательный результат. Не удалось найти запрашиваемый ресурс'
    assert rez != 409, f'Код 409. Отрицательный результат. Ресурс {input_folder_name} уже существует.'
    assert rez == 201
    return rez


def test_list_of_files_in_Yndex_disk(create_Yandex_connection,get_headers, input_folder_name, test_Yandex_create_new_folder):
    """Тест на наличие созданной папки с списке ресурсов (папок) на Yandex.диске"""
    if test_Yandex_create_new_folder == 201:
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        params = {'path': 'disk:/', 'limit': '500'}
        response = requests.get(url, headers = get_headers, params = params )
        exist_dirs=[el['name'] for el in response.json()['_embedded']['items'] if el['type']=='dir']
        print('Список папок на Yandex.диске: ', exist_dirs)
        assert input_folder_name in exist_dirs