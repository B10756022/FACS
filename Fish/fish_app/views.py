# django models
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Video, Order, Profile, Customer
from .forms import RegisterForm, LoginForm, OrderForm, UserForm, ProfileForm, CustomerForm
from django.contrib import messages
from django.db.models import Sum
from .core.utils import vid_detect ,load_model

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view

# models
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# tensorflow
import tensorflow as tf
from statistics import mean
from tensorflow.python.saved_model import tag_constants

# serializer
from .serializers import VideoSerializer, PostSerializer, UserSerializer, OrderSerializer, CustomerSerializer

import secrets
#分頁
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#影片處理
import cv2 as cv
import numpy as np
import os
import glob
# from google.colab.patches import cv2_imshow
from matplotlib import pyplot as plt
from skimage import exposure,img_as_ubyte
# 辨識模型
pb_path = r"fish_app/checkpoints/yolov4-416"
saved_model_loaded = tf.saved_model.load(pb_path, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

# 地區資料
area_data = {
    '臺北市': [
        '臺北','台北','中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區', '士林區', '文山區'
    ],
    '新北市': [
        '新北','板橋區', '新莊區', '泰山區', '林口區', '淡水區', '金山區', '八里區', '萬里區', '石門區', '三芝區', '瑞芳區', '汐止區', '平溪區', '貢寮區', '雙溪區', '深坑區', '石碇區', '新店區', '坪林區', '烏來區', '中和區', '永和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '蘆洲區', '五股區'
    ],
    '基隆市': [
        '基隆','仁愛區', '中正區', '信義區', '中山區', '安樂區', '暖暖區', '七堵區'
    ],
    '桃園市': [
        '桃園','桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '龜山區', '龍潭區', '大溪區', '大園區', '觀音區', '新屋區', '復興區'
    ],
    '新竹縣': [
        '新竹','新竹縣','竹北市', '竹東鎮', '新埔鎮', '關西鎮', '峨眉鄉', '寶山鄉', '北埔鄉', '橫山鄉', '芎林鄉', '湖口鄉', '新豐鄉', '尖石鄉', '五峰鄉'
    ],
    '新竹市': [
        '新竹市','東區', '北區', '香山區'
    ],
    '苗栗縣': [
        '苗栗''苗栗市', '通霄鎮', '苑裡鎮', '竹南鎮', '頭份鎮', '後龍鎮', '卓蘭鎮', '西湖鄉', '頭屋鄉', '公館鄉', '銅鑼鄉', '三義鄉', '造橋鄉', '三灣鄉', '南庄鄉', '大湖鄉', '獅潭鄉', '泰安鄉'
    ],
    '臺中市': [
        '台中','中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '東勢區', '石岡區', '新社區', '和平區', '神岡區', '潭子區', '大雅區', '大肚區', '龍井區', '沙鹿區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'
    ],
    '南投縣': [
        '南投','南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉', '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'
    ],
    '彰化縣': [
        '彰化','彰化市', '員林鎮', '和美鎮', '鹿港鎮', '溪湖鎮', '二林鎮', '田中鎮', '北斗鎮', '花壇鄉', '芬園鄉', '大村鄉', '永靖鄉', '伸港鄉', '線西鄉', '福興鄉', '秀水鄉', '埔心鄉', '埔鹽鄉', '大城鄉', '芳苑鄉', '竹塘鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '溪州鄉'
    ],
    '雲林縣': [
        '雲林','斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '莿桐鄉', '林內鄉', '古坑鄉', '大埤鄉', '崙背鄉', '二崙鄉', '麥寮鄉', '臺西鄉', '東勢鄉', '褒忠鄉', '四湖鄉', '口湖鄉', '水林鄉', '元長鄉'
    ],
    '嘉義縣': [
        '嘉義','太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'
    ],
    '嘉義市': [
        '東區', '西區'
    ],
    '臺南市': [
        '臺南','台南','中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'
    ],
    '高雄市': [
        '高雄','楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區', '小港區', '旗津區', '鳳山區', '大寮區', '鳥松區', '林園區', '仁武區', '大樹區', '大社區', '岡山區', '路竹區', '橋頭區', '梓官區', '彌陀區', '永安區', '燕巢區', '田寮區', '阿蓮區', '茄萣區', '湖內區', '旗山區', '美濃區', '內門區', '杉林區', '甲仙區', '六龜區', '茂林區', '桃源區', '那瑪夏區'
    ],
    '屏東縣': [
        '屏東','屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉', '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉', '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '霧台鄉', '瑪家鄉', '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉', '三地門鄉'
    ],
    '宜蘭縣': [
        '宜蘭','宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉', '三星鄉', '大同鄉', '南澳鄉'
    ],
    '花蓮縣': [
        '花蓮','花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '秀林鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '富里鄉', '卓溪鄉'
    ],
    '臺東縣': [
        '臺東','台東','臺東市', '成功鎮', '關山鎮', '長濱鄉', '海端鄉', '池上鄉', '東河鄉', '鹿野鄉', '延平鄉', '卑南鄉', '金峰鄉', '大武鄉', '達仁鄉', '綠島鄉', '蘭嶼鄉', '太麻里鄉'
    ],
    '澎湖縣': [
        '澎湖','馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'
    ],
    '金門縣': [
        '金門','金城鎮', '金湖鎮', '金沙鎮', '金寧鄉', '烈嶼鄉', '烏坵鄉'
    ],
    '連江縣': [
        '連江','南竿鄉', '北竿鄉', '莒光鄉', '東引鄉'
    ]
}

# 圖表
class chart(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "chart.html"

    def get(self, request):

        if request.user.id != None:
            u = request.user
            all = Order.objects.all()
            queryset = all.filter(user=u)
            total = []
            quantity_total = []
            town = []
            t_price = []
            for i in range(1,13):# 價錢
                queryset = all.filter(user=u, date__year='2021',date__month=i)
                price = queryset.aggregate(Sum('price'))
                for k,v in price.items():
                    total.append(v)

            for i in range(1,13): # 數量
                queryset = all.filter(user=u, date__year='2021',date__month=i)
                quantity = queryset.aggregate(Sum('quantity'))
                for k,v in quantity.items():
                    quantity_total.append(v)

            for k,v in area_data.items():
                for i in v :
                    queryset = all.filter(user=u,place__contains=i[0:2])
                    if  queryset :
                        town.append(i)
                        price = queryset.aggregate(Sum('price'))
                        for a,b in price.items():
                            t_price.append(b)




            return Response({'quantity': quantity_total,'price':total,'town':town,'t_price':t_price})
        else:
            return redirect('/login/')

# 個人檔案
def profile(request):
    if request.user.id != None:
        return render(request, 'profile.html')
    else:
        return redirect('/login/')


def update_profile(request):
    if request.user.id != None:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(
                request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, ('個人檔案成功更新！'))
                return redirect('/edit')
            else:
                messages.error(request, ('請注意錯誤！'))
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            return render(request, 'update_profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
    else:
        return redirect('/login/')

#----------------------------------------------------------------------------#

# 首頁

def index(request):
    return render(request, 'index_new.html')

# 註冊

def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            messages.error(request, '帳號已存在或資料輸入錯誤，請再試一次')
            return redirect('/register')
    context = {

        'form': form

    }

    return render(request, 'User/register.html', context)
#綁定
def link_ans(request):
    if request.user.id != None:
        if request.method == 'GET':
            link_Token = request.GET['linkToken']
            nonce = request.GET['nonce']
            request.user.nonce = "nonce";





# 登入

def sign_in(request):

    form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        #link_Token=request.get_header('linkToken')
        #print(link_Token)
        if user is not None:
            login(request, user)
            #if link_Token:
            #    nonce = secrets.token_urlsafe()
            #    request.session['linkToken'] = link_Token
            #    request.session['nonce'] = nonce
            #    return redirect('/link')
            #else:
            #    return redirect('/')  # 重新導向到首頁
            return redirect('/')  # 重新導向到首頁
        else:
            messages.error(request, '帳號或密碼錯誤！')
            return redirect('/login')

    context = {
        'form': form
    }
    return render(request, 'User/login.html', context)

# 登出

def log_out(request):
    logout(request)
    return redirect('/login')  # 重新導向到登入畫面

#----------------------------------------------------------------------------#

# 影片列表


class ListVideo(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_list.html"

    def get(self, request):

        if request.user.id != None:
            u = request.user
            all = Video.objects.all()
            queryset = all.filter(user=u)
            return Response({'videos': queryset})
        else:
            return redirect('/login/')

# 上傳影片

class PostVideo(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_upload.html"

    def get(self, request):
        if request.user.id != None:

            queryset = Video.objects.last()
            return Response({'video': queryset})
        else:
            return redirect('/login/')

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(id=request.user.id))
            last = Video.objects.last()

            count = vid_detect(
                r'../upload_media/{}'.format(last.video.name),
                r'../upload_media/predict_video/{}'.format(last.video.name),
                infer
            )
            print(count)
            c = mean(count)
            video_path = r'predict_video/{}'.format(last.video.name)
            #print(video_path)
            last.after_predict = video_path
            last.quantity = int(c)
            last.save()

            return redirect('/upload/', status=201)
        else:
            messages.error(request, '未選檔案或輸入錯誤，請再確認一次！')
            return redirect('/upload/')

# 暫時沒用

class VideoDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'video_detail.html'

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video)
        return Response({'serializer': serializer, 'video': video})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'video': video})
        serializer.save()
        return redirect('/videos/')

#----------------------------------------------------------------------------#

# 時間模組


class home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        now = datetime.now()  # 時間模組
        return Response({'profiles': now})


class about(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'about.html'

    def get(self, request):
        now = datetime.now()  # 時間模組
        return Response({'profiles': now})


class trade(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'trade.html'

    def get(self, request):
        now = datetime.now()  # 時間模組
        return Response({'profiles': now})


class fishAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'fishAPI.html'

    def get(self, request):
        now = datetime.now()  # 時間模組
        return Response({'profiles': now})

#----------------------------------------------------------------------------#

# 訂單列表


class Order_list(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Order/order_list.html"

    def get(self, request):

        if request.user.id != None:
            buyer = request.GET
            print(buyer.get("name"))
            if buyer.get("name") != "" and buyer.get("name") != None:
                query = buyer.get("name")
                u = request.user
                try:
                    query = Customer.objects.get(name=query).id
                    all = Order.objects.filter(user=u).filter(buyer=query)
                    if not all:
                        messages.error(request, ('找不到您搜尋的內容！'))

                except Customer.DoesNotExist:
                    query = None
                    all = Order.objects.filter(user=u).filter(buyer=query)
                    # messages.error(request, ('找不到您搜尋的內容！'))
                    try:

                        all = Order.objects.filter(user=u).filter(
                                    fish_species=buyer.get("name"))
                        print(all)
                        print(all==None)
                        if not all:
                            messages.error(request, ('找不到您搜尋的內容！'))
                    except Order.DoesNotExist :
                        all = Order.objects.filter(user=u)
                        messages.error(request, ('找不到您搜尋的內容！'))




                #queryset = all
                page = request.GET.get('page', 1)
                paginator = Paginator(all, 8)
                try:
                    queryset = paginator.page(page)
                except PageNotAnInteger:
                    queryset = paginator.page(1)
                except EmptyPage:
                    queryset = paginator.page(paginator.num_pages)
                return render(request, 'order/order_list.html', {'orders': queryset})
                #return Response({'orders': queryset})

            u = request.user
            all = Order.objects.filter(user=u)
            # queryset = all
            page = request.GET.get('page', 1)
            paginator = Paginator(all, 8)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)
            return render(request, 'order/order_list.html', {'orders': queryset})
            #return Response({'orders': queryset})
        else:
            return redirect('/login/')

# 新增訂單


class Order_post(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Order/order.html"

    def get(self, request):

        if request.user.id != None:
            u = request.user
            all = Customer.objects.all()
            queryset = all.filter(user=u)

            return Response({'customers': queryset})
        else:
            return redirect('/')

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(id=request.user.id))
            messages.success(request, ('訂單資料成功新增！'))

            return redirect('/order/', status=201)
        return redirect('/order/', status=400)

# 訂單編輯


def Order_detail(request, id):
    if request.user.id != None:

        if request.method == 'POST':
            order = Order.objects.get(id=id)
            order_form = OrderForm(request.POST, instance=order)
            if order_form.is_valid():
                order_form.save()
                messages.success(request, ('訂單資料成功更新！'))
                return redirect('/orderdetail/'+str(id))

            else:
                messages.error(request, ('請注意錯誤！'))
        else:
            u = request.user
            order = Order.objects.get(id=id)
            customer = Customer.objects.all()
            customer = customer.filter(user=u)
            order_form = OrderForm(instance=order)
            return render(request, 'Order/order_detail.html', {'order_form': order_form, 'order': order, 'customers': customer})

    else:
        return redirect('/login/')

# 訂單刪除


def Order_delete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('/orderlist/')

#數字帶入
class Order_quantity(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Order/order.html"
    def get(self, request, quantity):

        if request.user.id != None:

            u = request.user
            all = Customer.objects.all()
            queryset = all.filter(user=u)

            return Response({'customers': queryset,'quantity': quantity})
        else:
            return redirect('/login/')

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(id=request.user.id))
            messages.success(request, ('訂單資料成功新增'))

            return redirect('/order/', status=201)
        return redirect('/order/', status=400)
    # return render(request, 'Order/order.html', {'quantity': quantity})


# 購買人資訊


class Buyerinfo(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Order/buyerlnfo.html"

    def get(self, request, id):

        if request.user.id != None:
            customer = Customer.objects.get(id=id)

            return Response({'customer': customer})
        else:
            return redirect('/login/')

#----------------------------------------------------------------------------#

# 顧客列表


class Customer_list(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Customer/customer_list.html"

    def get(self, request):

        if request.user.id != None:
            u = request.user
            all = Customer.objects.all()
            queryset = all.filter(user=u)
            page = request.GET.get('page', 1)
            paginator = Paginator(queryset, 8)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)
            return render(request, 'Customer/customer_list.html', {'customers': queryset})
            # return Response({'orders': queryset})
            #return Response({'customers': queryset})
        else:
            return redirect('/login/')

# 新增顧客


class Customer_post(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Customer/customer_post.html"

    def get(self, request):
        if request.user.id != None:
            queryset = Customer.objects.last()
            return Response({'customers': queryset})
        else:
            return redirect('/login/')

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=User.objects.get(id=request.user.id))
            messages.success(request, ('顧客資料成功新增！'))
            return redirect('/customerpost/', status=201)
        return redirect('/customerpost/', status=400)

# 顧客編輯


def Customer_detail(request, id):
    if request.user.id != None:

        if request.method == 'POST':
            customer = Customer.objects.get(id=id)
            customer_form = CustomerForm(request.POST, instance=customer)
            if customer_form.is_valid():
                customer_form.save()
                messages.success(request, ('顧客資料成功更新！'))
                return redirect('/customerdetail/'+str(id))

            else:
                messages.error(request, ('請注意錯誤！'))
        else:
            customer_form = CustomerForm(instance=request.user)
            customer = Customer.objects.get(id=id)
            return render(request, 'Customer/customer_detail.html', {'customer_form': customer_form, 'customer': customer})

    else:
        return redirect('/')

# 刪除顧客


def Customer_delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('/customerlist/')

#----------------------------------------------------------------------------#
