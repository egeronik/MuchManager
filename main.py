import socket
import json

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



# # Примеры
# payload = {"method": "subs", "data": 67580761}
# print(requestAction(payload, 65432))

# payload2 = {"method": "posts", "data": {"channel_id": 67580761, "count": 2}}
# print(requestAction(payload2, 65432))
