import json


class TCPXMessage(object):
    id = None
    header = None
    body = None


class TCPXProtocol(object):

    def __init__(self, serializer):
        self.serializer = serializer

    def pack(self, message):
        id = message.id
        header = message.header
        body = message.body

        if self.serializer == 'json':
            _body = bytes(json.dumps(body), 'utf-8')
        else:
            _body = body.SerializeToString()

        _id = id.to_bytes(4, 'big')
        _header = bytes(json.dumps(header), 'utf-8')
        _header_length = len(_header).to_bytes(4, 'big')
        _body_length = len(_body).to_bytes(4, 'big')

        _packet = _id + _header_length + _body_length + _header + _body

        _data = len(_packet).to_bytes(4, 'big') + _packet

        return _data

    def unpack(self, data, response=None):
        message = TCPXMessage()

        _packet = data[4:]
        _header_length = int.from_bytes(_packet[4:8], 'big')
        _body_length = int.from_bytes(_packet[8:12], 'big')

        message.id = int.from_bytes(_packet[0:4], 'big')
        message.header = data[16:16+_header_length]

        _body = data[16+_header_length:16+_header_length+_body_length]
        if self.serializer == 'json':
            message.body = json.loads(_body.decode('utf-8'))
        else:
            response.ParseFromString(_body)
            message.body = response

        return message
