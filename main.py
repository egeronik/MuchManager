import socket
import json
from flask import Flask, request

VK_PORT = 65432
YouTube_PORT = 65433
HOST = "127.0.0.1"  # IP машины с парсерами, у нас лупбек

# Кастомная функция чтения даты из сокета
def recvall(sock):
    """Функция для получения всего сообщения целиком из сокета

    Args:
        sock (_type_): сокет

    Returns:
        _type_: Цельное сообщение из сокета
    """
    BUFF_SIZE = 4096  # 4 KiB
    data = b""
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data



def requestAction(payload: dict, port: int) -> dict:
    """ Функция подготовки/отправки запроса к парсеру

    Args:
        payload (dict): состав сообщения
        port (int): порт на котором запущен парсер

    Returns:
        dict: резульат обработки парсера
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        s.sendall(str.encode(json.dumps(payload)))
        data = recvall(s)
        res = json.loads(data)
    return res

api = Flask(__name__)

# Для каждого парсера пишем одну функцию, все запросы идут через метод GET
@api.route('/VK/<method>', methods=['GET'])
def get_vk(method):
    """Функция отвечающая за направление запросов на VK парсер

    Args:
        method (str): Вызываемый метод. subs|posts

    Returns:
        _type_: Текст ответа
    """
    # Перечисляем список разрешенных методов
    allowed_methods = {"subs","posts","group"}
    
    if not method in allowed_methods:
        return "Bad method"
    
    payload = dict(request.args)
    payload["method"]=method
    
    try:
        # Кидаем запрос на парсер
        return requestAction(payload, VK_PORT)
    # Если парсер не пашет ловим ошибку
    except ConnectionRefusedError:
        return  {"type": "error", "data":{"error":"Parser not started"}}

    
@api.route('/YouTube/<method>', methods=['GET'])
def get_yt(method):
    """Функция отвечающая за направление запросов на YiuTube парсер
    Args:
        method (str): Вызываемый метод. channel|subs|videos
    Returns:
        _type_: Текст ответа
    """
    # Перечисляем список разрешенных методов
    allowed_methods = {"channel", "subs", "videos"}

    if not method in allowed_methods:
        return "Bad method"

    payload = dict(request.args)
    payload["method"] = method

    try:
        # Кидаем запрос на парсер
        return requestAction(payload, YouTube_PORT)
    # Если парсер не пашет ловим ошибку
    except ConnectionRefusedError:
        return {"type": "error", "data": {"error": "Parser not started"}}


@api.route('/')
def hello():
    return 'А что это мы тут смотрим???'


api.run()

# # Примеры
# payload = {"method": "subs", "data": 67580761}
# print(requestAction(payload, 65432))

# payload2 = {"method": "posts", "data": {"channel_id": 67580761, "count": 2}}
# print(requestAction(payload2, 65432))

# payload3 = {"method": "videos", "data": {"channel_id": "UCfcc8OORrouV1lO_qeIZVNQ", "count": 3}}
# print(requestAction(payload3, 65433))
