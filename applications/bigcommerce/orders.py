"""
    orders
"""
import json

from applications.bigcommerce.base import BigCommerceModel
from tenacity import retry, stop_after_attempt, wait_exponential


class OrdersBCRequests(BigCommerceModel):
    """
        OrdersBCRequests
    """

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_by_order_id(self, store_hash, order_id, version="v2"):
        """
            @get_order_by_order_id
        :param store_hash: code
        :param order_id: id
        :param version: v2
        :return:
        """
        url = f"/orders/{order_id}"

        resp = self.get_method(
            store_hash=store_hash,
            uri=url,
            version=version
        )
        return resp

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_images_by_order_id(self, params):
        """
            @get_order_images_by_order_id
        :param params: store_hash, order_id
        :return: order image
        """
        store_hash, order_id = params.get("store_hash"), params.get("order_id")

        resp = self.get_order_product_by_order_id(
            store_hash=store_hash, order_id=order_id, result=[])

        if resp is False or resp == []:
            return {
                "orderId": order_id,
                "imageUrl": None
            }

        url = "/catalog/products/{product_id}/images".format(
            product_id=resp[0]["product_id"])

        resp = self.get_method(
            store_hash=store_hash,
            uri=url,
            version="v3"
        )
        if resp is False:
            return {
                "orderId": order_id,
                "imageUrl": None
            }
        return {
            "orderId": order_id,
            "imageUrl": resp["data"][0]["url_standard"] if any(resp["data"]) else ""
        }

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def update_order_comments_by_customer_id(self, store_hash, order_id, comments, version="v2"):
        """
            @update_order_comments_by_customer_id
        :param store_hash: store code
        :param order_id: id
        :param comments:
        :param version: v2
        :return: resp
        """
        url = "/orders/{order_id}".format(order_id=order_id)

        params = {
            "customer_message": comments
        }
        resp = self.put_method(
            store_hash=store_hash,
            uri=url,
            version=version,
            data=json.dumps(params)
        )
        return resp

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_product_by_order_id(self, store_hash, order_id, result: list, page=1, limit=250):
        """
            @get_order_product_by_order_id
        :param store_hash: code
        :param order_id: id
        :param page: 1
        :param result: []
        :param limit: 250
        :return: resp
        """
        url = "/orders/{order_id}/products".format(order_id=order_id)

        resp = self.get_method(
            store_hash=store_hash,
            uri=url,
            version="v2",
            params={"page": page, "limit": limit}
        )
        if resp is False:
            return []

        result.extend(resp)
        if len(resp) == limit:
            return self.get_order_product_by_order_id(
                store_hash=store_hash,
                order_id=order_id,
                result=result,
                page=page+1,
                limit=limit
            )
        return result

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_shipping_address(self, store_hash, order_id, version='v2'):
        """
            @get_order_shipping_address
        :param store_hash: store code
        :param order_id: id
        :param version: v2
        :return: address
        """
        url = "/orders/{order_id}/shipping_addresses".format(order_id=order_id)
        resp = self.get_method(
            store_hash=store_hash,
            uri=url,
            version=version
        )
        return resp

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_shipments(self, store_hash, order_id, version='v2'):
        """
            @get_order_shipments
        :param store_hash: store code
        :param order_id: id
        :param version: v2
        :return: shipments
        """
        url = "/orders/{order_id}/shipments".format(order_id=order_id)

        resp = self.get_method(
            store_hash=store_hash,
            uri=url,
            version=version
        )
        return resp

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_order_by_customer_id(self, store_hash: str, customer_id: str, page: int, result: list):
        url = "/orders"
        params = {
            "customer_id": customer_id,
            "page": page,
            "limit": 250
        }
        resp = self.get_method(
            uri=url,
            store_hash=store_hash,
            params=params,
            version="v2"
        )

        if resp is False:
            return result

        result.extend(resp)

        if len(resp) < 250:
            return result

        return self.get_order_by_customer_id(store_hash, customer_id, page+1, result)

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def create_order_refund_quotes(self, store_hash: str, order_id: str, quotes: dict):
        uri = f"/orders/{order_id}/payment_actions/refund_quotes"

        request_params = json.dumps(quotes)

        resp = self.post_method(
            uri=uri,
            store_hash=store_hash,
            data=request_params,
            version="v3"
        )

        if resp is False:
            return resp

        return resp.get("data")

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def create_order_refund(self, store_hash: str, order_id: str, quotes: dict):

        uri = f"/orders/{order_id}/payment_actions/refunds"

        request_params = json.dumps(quotes)

        resp = self.post_method(
            uri=uri,
            store_hash=store_hash,
            data=request_params,
            version="v3"
        )

        return resp
