import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from applications.bigcommerce.orders import OrdersBCRequests

from utils.resp_const import RespRET, RET_MAP
from common.obj_response import ObjectResp

logger = logging.getLogger("default")

order_request = OrdersBCRequests(logger)


class OrderRefundApiViews(APIView):
    """
    @ 创建订单退款
    1、判断当前订单是否存在
    2、判断当前订单状态是否为已付款订单
    3、获取当前订单的支付方式
    4、创建退货订单价目表
    5、创建退货订单
    6、返回
    """

    def post(self, request):

        json_data = json.loads(request.body)
        order_id = json_data.get("orderId")
        reason = json_data.get("reason", "")
        store_hash = request.META.get("store_hash")
        customer_id = request.META.get("customer_id")

        order = order_request.get_order_by_order_id(
            store_hash=store_hash,
            order_id=order_id
        )

        # 订单不存在，则直接返回
        if order is False:
            result = ObjectResp.response(
                code=RespRET.HTTP_RET_ORDER_DOES_NOT_EXIST,
                message=RET_MAP[RespRET.HTTP_RET_ORDER_DOES_NOT_EXIST],
                **{}
            )
            return Response(result)

        if int(customer_id) != order.get("customer_id"):
            result = ObjectResp.response(
                code=RespRET.HTTP_RET_CUSTOMER_ERROR,
                message=RET_MAP[RespRET.HTTP_RET_CUSTOMER_ERROR],
                **{}
            )
            return Response(result)

        if order.get("status") != "Awaiting Fulfillment":
            result = ObjectResp.response(
                code=RespRET.HTTP_RET_ORDER_STATUS_ERROR,
                message=RET_MAP[RespRET.HTTP_RET_ORDER_STATUS_ERROR],
                **{}
            )
            return Response(result)

        payment_method = order.get("payment_method")

        order_products = order_request.get_order_product_by_order_id(
            order_id=order_id,
            store_hash=store_hash,
            result=[]
        )

        items = []
        for product in order_products:
            # 该产品已经在该订单中退款过了
            if product.get("is_refunded") is True:
                continue
            item = {
                "item_id": product.get("id"),
                "item_type": "PRODUCT",
                "quantity": product.get("quantity"),
                "reason": reason
            }
            items.append(item)

        quote = order_request.create_order_refund_quotes(
            store_hash=store_hash,
            order_id=order_id,
            quotes={"items": items}
        )

        if quote is False:
            result = ObjectResp.response(
                code=RespRET.HTTP_RET_ORDER_QUOTES_FAILED,
                message=RET_MAP[RespRET.HTTP_RET_ORDER_QUOTES_FAILED],
                **{}
            )
            return Response(result)

        tax_adjustment_amount = quote.get("adjustment")
        refund_methods = quote.get("refund_methods")

        resp = order_request.create_order_refund(
            store_hash=store_hash,
            order_id=order_id,
            quotes={
                "tax_adjustment_amount": tax_adjustment_amount,
                "items": items,
                "payments": self.calculate_order_refund(refund_methods, payment_method)
            }
        )

        if resp is False:
            result = ObjectResp.response(
                code=RespRET.HTTP_RET_ORDER_REFUND_FAILED,
                message=RET_MAP[RespRET.HTTP_RET_ORDER_REFUND_FAILED],
                **{}
            )
            return Response(result)

        return Response(ObjectResp.value_of(**{}))

    @staticmethod
    def calculate_order_refund(refund_methods: list, payment_method: str):
        """
        @计算正确的退款方式
        :param refund_methods:  退款方式
        :param payment_method:  订单的支付方式
        :return:
        """
        refund_method = list(filter(lambda x: len(x) > 1, refund_methods))

        if any(refund_method) is True:

            return refund_method[0]

        refund_method = list(filter(lambda x: x[0].get("provider_description") == payment_method, refund_methods))

        if any(refund_method) is True:

            return refund_method[0]

        refund_method = list(filter(lambda x: x[0].get("provider_id") == "storecredit", refund_methods))

        if any(refund_method) is True:

            return refund_method

        refund_method = list(filter(lambda x: x[0].get("provider_id") == "custom", refund_methods))

        if any(refund_method) is True:

            return refund_method
