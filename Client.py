import http.client as client
from urllib.parse import quote
from Input import Input
from Output import Output


class Client:
    def __init__(self, connection: client.HTTPConnection):
        self.connection = connection
        self.input_data = None

    def ping(self):                                                                 # Метод для отправки запроса с методом ping
        self.connection.request('GET', '/Ping')                                     # Возвращает статус ответа
        response = self.connection.getresponse()
        return response.status

    def get_input_data(self):                                                       # Метод для запроса входных данных
        self.connection.request('GET', '/GetInputData')                             # Возвращает объект Input
        response = self.connection.getresponse()
        return Input('Json', str(response.read(), 'UTF-8'))

    def write_answer(self):                                                         # Метод для отправки решения
        output_data = Output(self.input_data).to_json()                             # Отправляет json, полученный из объекта Output
        self.connection.request('GET', f'/WriteAnswer?data={quote(output_data)}')   # Возвращает тело ответа
        response = self.connection.getresponse()
        return str(response.read(), 'UTF-8')

    def stop(self):                                                                 # Метод для остановки сервера и закрытия соединения
        self.connection.request('GET', '/Stop')
        self.connection.close()

    def send(self, request: str):                                                   # Метод для отправки всех запросов
        if request == '/Ping':                                                      # Принимает запрос и запускает соответствующий метод, если он есть
            return self.ping()
        elif request == '/GetInputData':
            self.input_data = self.get_input_data()
            return 'got'
        elif request == '/WriteAnswer':
            if not isinstance(self.input_data, Input):
                return 'input_data is empty!'
            else:
                return self.write_answer()
        elif request == '/Stop':
            self.stop()
        else:                                                                       # Иначе отправляет серверу строку запроса
            self.connection.request('GET', request)
            return str(self.connection.getresponse().read(), 'UTF-8')


# main_connection = client.HTTPConnection('localhost', 3000)
# my_client = Client(main_connection)
# while True:
#     request = input()
#     my_client.send(request)
