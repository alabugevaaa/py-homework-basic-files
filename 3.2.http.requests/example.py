import os
import requests
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = os.getenv('API_KEY')
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
URL_YANDEX = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

def translate_it(file_input, file_output, from_lang, to_lang='ru'):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    if file_input == '':
        return 'Не указан путь к файлу с текcтом'
    if file_output == '':
        return 'Не указан путь к файлу с результатом'
    if from_lang != '':
        from_lang += '-'
    if to_lang == '':
        to_lang = 'ru'

    try:
        with open(file_input, 'r', encoding='utf-8-sig') as f:
            text = f.read()
    except FileNotFoundError:
        return f'Файл {file_input} не существует'

    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}{}'.format(from_lang,to_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    if response.status_code == 200:
        with open(file_output, 'w', encoding='utf-8') as f:
            f.write(''.join(json_['text']))
        print(''.join(json_['text']))
    else:
        return json_


    # Загрузка на Яндекс.Диск
    params_yandex = {
        'path': f'app:/{file_output}',
        'overwrite': True,
    }

    resp_yandex_url = requests.get(URL_YANDEX, headers={'Authorization': 'OAuth ' + OAUTH_TOKEN}, params=params_yandex)
    resp_yandex_json = resp_yandex_url.json()
    if resp_yandex_url.status_code == 200:
        response_yandex = requests.put(resp_yandex_json['href'], file_output)

        return f'Статус загрузки на Яндекс.Диск: {response_yandex.reason}'
    else:
        return f'Не удалось получить url для загрузки: {resp_yandex_json}'


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    file_input = input('Путь к файлу с текcтом: ')
    file_output = input('Путь к файлу с результатом: ')
    from_lang = input('Язык с которого перевести: ')
    to_lang = input('Язык на который перевести (по-умолчанию русский): ')
    print(translate_it(file_input, file_output, from_lang, to_lang))