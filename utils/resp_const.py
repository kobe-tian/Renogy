class RespRET:
    HTTP_OK = 200
    HTTP_FORBIDDEN = 403
    HTTP_ERROR = 500
    HTTP_RET_ORDER_DOES_NOT_EXIST = 1000010
    HTTP_RET_CUSTOMER_ERROR = 1000011

    HTTP_RET_ORDER_QUOTES_FAILED = 1000012
    HTTP_RET_ORDER_REFUND_FAILED = 1000013


RET_MAP = {
    200: "SUCCESS",
    500: "Internal Server Error",
    1000010: "Order Does Not Exist",
    1000011: "User Not Order Owner",
    1000012: "创建退款订单报价失败, 该订单不允许退款，请检查订单是否正常",
    1000013: "创建退款订单失败, 请联系管理处理"
}

