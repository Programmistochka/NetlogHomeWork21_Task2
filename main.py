import requests

class Yandex:
    
    base_host = "https://cloud-api.yandex.net:443/"
    
    def __init__(self, token: str):
        """Метод инициализации класса Yandex"""
        self.token = token
    
    def get_headers(self):
        """Метод для передачи заголовков"""
        return {
            'Content_Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
    
    def create_new_folder(self, folder_name):
        """Метод для создания новой папки"""
        url = r'v1/disk/resources?path=%2F'
        request_url = self.base_host + url + folder_name
        response = requests.put(request_url, headers = self.get_headers())
        return response.status_code
        
if __name__ == '__main__':
    # Получить токен для Яндекс.полигон от пользователя 
    ya_token = input('Введите токен для Яндекс.Полигон: ')
    uploader = Yandex(ya_token)

    # Создание новой папки на яндекс диске
    folder_name = input('Введите имя новой папки (допустимо использовать: буквы, цифры, пробелы и подчеркивания):')
    if uploader.create_new_folder(folder_name) == 201:
        folder_name = f'/{folder_name}/'
        print('Создана новая папка с имененм: ', folder_name)
    else:
        print('Новую папку создать не удалось')