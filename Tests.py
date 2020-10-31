from Input import Input
from Output import Output
from Client import Client
from Server import MyRequestHandler
from http.server import HTTPServer
import http.client
import threading


def test_input_output():
    json_to_test = '{"K":10,"Sums":[1.01,2.02],"Muls":[1,4]}'
    json_input = Input('Json', json_to_test)

    xml_to_test = '<Input><K>10</K><Sums><decimal>1.01</decimal><decimal>2.02</decimal></Sums><Muls><int>1</int><int>4</int></Muls></Input>'
    xml_input = Input('Xml', xml_to_test)

    assert json_input.sums == xml_input.sums == [1.01, 2.02], 'input sums'
    assert json_input.k == xml_input.k == 10, 'input k'
    assert json_input.muls == xml_input.muls == [1, 4], 'input muls'
    print('passed input')

    json_output = Output(json_input)
    xml_output = Output(xml_input)

    assert json_output.mul_result == xml_output.mul_result == 4, 'output mul_result'
    assert json_output.sorted_inputs == xml_output.sorted_inputs == [1.0, 1.01, 2.02, 4.0], 'output sorted_inputs'
    assert json_output.sum_result == xml_output.sum_result == 30.30, 'output sum_result'

    json_output_to_test = '{"SumResult":30.3,"MulResult":4,"SortedInputs":[1,1.01,2.02,4]}'
    xml_output_to_test = '<Output><SumResult>30.3</SumResult><MulResult>4</MulResult><SortedInputs><decimal>1</decimal>' +\
                         '<decimal>1.01</decimal><decimal>2.02</decimal><decimal>4</decimal></SortedInputs></Output>'

    assert json_output.to_json() == json_output_to_test, 'output_json serialization'
    assert xml_output.to_xml() == xml_output_to_test, 'output_xml serialization'
    print('passed output')


def test_client_server():
    server = HTTPServer(("localhost", 3000), MyRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    client = Client(http.client.HTTPConnection('localhost', 3000))
    assert client.send('/Ping') == 200, 'client_server ping'
    assert client.send('/WriteAnswer') == 'input_data is empty!', 'client_server empty input_data'
    assert client.send('/GetInputData') == 'got', 'client_server get_input_data'
    assert client.send('/WriteAnswer') == 'OK', 'client_server answer'
    assert client.send('/WriteAnswer?data={"wrong":format}') == 'Not OK', 'client_server wrong data'
    assert client.send('/WriteAnswer?notadata={"wrong":format}') == 'No data parameter sent!', 'client_server wrong data'
    assert client.send('/SomeMethod') == 'Wrong method!', 'client_server wrong method'
    client.send('/Stop')
    print('client_server passed')


test_input_output()
test_client_server()
