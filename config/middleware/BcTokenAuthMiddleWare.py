import logging
import json

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponseForbidden
from common.crypto_aes import PyCryptAES
logger = logging.getLogger("default")


class BcTokenAuthMiddleWare(MiddlewareMixin):

    ERR_MSG = "Ops!!! User Agent Forbidden, Please try again later!"

    def process_request(self, request):

        if request.path is not None and request.path == "/docs/":
            return None

        if "HTTP_AUTHENTICATION" not in request.META.keys():
            logger.info("Forbidden user agent")
            return HttpResponseForbidden(BcTokenAuthMiddleWare.ERR_MSG)

        client_id = request.META.get("HTTP_CLIENTID")
        if client_id not in settings.APP_CLIENTS.keys():
            logger.info("Forbidden user agent, client id error")
            return HttpResponseForbidden(BcTokenAuthMiddleWare.ERR_MSG)

        json_data = self.checkout_token(
            token=request.META.get("HTTP_AUTHENTICATION"),
        )
        store_hash = json_data.get("store_hash", None)
        if store_hash != settings.APP_CLIENTS.get(client_id).get("store_hash"):
            logger.info("Forbidden user agent, store hash error")
            return HttpResponseForbidden(BcTokenAuthMiddleWare.ERR_MSG)

        request.META["store_hash"] = store_hash
        request.META["customer_id"] = json_data.get('customer_id')

    @staticmethod
    def checkout_token(token):
        try:
            crypto = PyCryptAES()
            json_data = json.loads(crypto.decrypt(token))
            return json_data
        except Exception as ex:
            logger.exception("jwt decode err: {0}".format(ex))
            return HttpResponseForbidden(BcTokenAuthMiddleWare.ERR_MSG)
