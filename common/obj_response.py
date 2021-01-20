from utils.resp_const import RespRET, RET_MAP


class ObjectResp:

    @staticmethod
    def value_of(code=None, message=None, **response):
        if code is None:
            code = RespRET.HTTP_OK
        if message is None:
            message = RET_MAP[RespRET.HTTP_OK]
        return ObjectResp.response(code, message, **response)

    @staticmethod
    def response(code=None, message=None, **response):
        result = {
            'code': code,
            'message': message,
            'data': response
        }
        return result
