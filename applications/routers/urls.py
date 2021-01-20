from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from applications.core.orders import views as order_views
from applications.core.heat_check import views as heat_views

urlpatterns = [
    # 处理订单退款API
    path('orders/refund', csrf_exempt(order_views.OrderRefundApiViews.as_view()), name="orders/refund"),


    # 心跳检测
    path('heatCheck', csrf_exempt(heat_views.HeartCheckAPiView.as_view()), name='heat_check')
]
