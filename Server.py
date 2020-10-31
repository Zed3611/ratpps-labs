from http.server import BaseHTTPRequestHandler
from Input import Input
from Output import Output
from urllib.parse import parse_qs

input_data = '{"K":10,"Sums":[1.01,2.02],"Muls":[1,4]}'             # Входные данные задачи для клиента
answer = Output(Input('Json', input_data)).to_json()                # Ответ, который ожидается от клиента


class MyRequestHandler(BaseHTTPRequestHandler):                     # Обработчик запросов
    def do_GET(self):                                               # Метод для обработки get запросов
        switch = {'/Ping': self.send_ok,
                  '/GetInputData': self.send_input_data,
                  '/WriteAnswer': self.send_answer,
                  '/Stop': self.stop
                  }
        if '?' in self.path:                                        # Проверка на наличие параметров в запросе
            index = self.path.index('?')                            # В path записываем метод
            path = self.path[:index]                                # В self.path записываем параметры, если они есть
            self.path = self.path[index+1:]
        else:
            path = self.path

        if path not in switch:
            self.send_err('Wrong method!')
        else:
            switch[path]()

    def send_ok(self):                                              # Метод для отправки статуса 200
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def send_input_data(self):                                      # Метод для отправки входных данных
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(input_data, 'UTF-8'))

    def send_answer(self):                                          # Метод для проверки ответа
        params = parse_qs(self.path)                                # в self.path должен лежать параметр data
        if 'data' in params:
            self.send_ok()
            if params['data'][0] == answer:
                self.wfile.write(bytes('OK', 'UTF-8'))
            else:
                self.wfile.write(bytes('Not OK', 'UTF-8'))
        else:
            self.send_err('No data parameter sent!')

    def send_err(self, message):                                    # Метод для отправки ошибки со статусом 400
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, 'UTF-8'))

    def stop(self):                                                 # Метод для остановки сервера
        self.server._BaseServer__shutdown_request = True


# server = HTTPServer(("localhost", 3000), MyRequestHandler)
# server.serve_forever()
