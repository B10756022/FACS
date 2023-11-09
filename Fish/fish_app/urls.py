from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('video', ArticleViewSet, basename='video')

urlpatterns = [
    # path('', include(router.urls)),
    # path('<int:id>/', include(router.urls)),
    path('videos/', ListVideo.as_view(), name='videos'),
    path('', home.as_view(), name='home'),
    path('about', about.as_view(), name='about'),
    path('upload/', PostVideo.as_view(), name='upload'),
    path('trade/', trade.as_view(), name='trade'),
    path('detail/<int:pk>', VideoDetail.as_view(), name='detail'),
    path('fishAPI', fishAPI.as_view(), name='fishAPI'),

    # account
    path('index/', index, name='index'),
    path('login/', sign_in, name='login'),
    path('register/', sign_up, name='register'),
    path('logout', log_out, name='logout'),
    path('link/', link_ans, name='linkans'),

    # 個人資料
    path('edit/', update_profile, name='update_profile'),
    path('profile/', profile, name='profile'),

    # 訂單
    path('order/', Order_post.as_view(), name='order'),
    path('orderlist/', Order_list.as_view(), name='orderlist'),
    path('orderdetail/<int:id>/', Order_detail, name='orderdetail'),
    path('orderdelete/<int:id>/', Order_delete, name='orderdelete'),
    path('buyerinfo/<int:id>/', Buyerinfo.as_view(), name='buyerinfo'),
    path('orderquantity/<int:quantity>/',Order_quantity.as_view(), name='orderquantity'),

    # 顧客
    path('customerlist/', Customer_list.as_view(), name='Customerlist'),
    path('customerpost/', Customer_post.as_view(), name='Customerpost'),
    path('customerdetail/<int:id>/', Customer_detail, name='Customerdetail'),
    path('Customerdelete/<int:id>/', Customer_delete, name='Customerdelete'),

    #圖表
    path('chart/', chart.as_view(), name='chart'),

]
