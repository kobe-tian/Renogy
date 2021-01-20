from rest_framework.views import APIView
from rest_framework.response import Response
from common.obj_response import ObjectResp
import logging

logger = logging.getLogger('default')


class HeartCheckAPiView(APIView):

    """
    @心跳检测
    """

    def get(self, request):
        return Response(ObjectResp.value_of())
