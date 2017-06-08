# coding: utf-8

from datetime import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from leancloud import Object
from leancloud import Query
from leancloud.errors import LeanCloudError
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
import os


class Todo(Object):
    pass

class Card(Object):
    pass
class _User(Object):
    pass    
    


def index(request):
    return render(request, 'index.html', {})


def current_time(request):
    return HttpResponse(datetime.now())

def os_info(request):
    environ = os.environ
    return HttpResponse(environ.keys(),content_type="application/json") 


def image(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.GaussianBlur)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  

def imageNew(request):  
    image_data = Image.new('RGBA',(400,100),ImageColor.getrgb('#fff')) 
    fnt = ImageFont.truetype('font/zhanghaishan.ttf',40)
    text = 'Pillow文字示例'
    (width,height) = fnt.getsize(text)
    print(width)
    d = ImageDraw.Draw(image_data)
    d.text(((400-width)/2,(100-height)/2), text, font=fnt, fill=(0,0,0))
    msstream=BytesIO()
    image_data.save(msstream,"jpeg")
    image_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg") 
class CardView(View):
    def get(self, request):
        try:
            cards = Query(Card).descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'cards.html',{'cards':cards})

class UserView(View):
    def get(self, request):
        try:
            users = Query(_User).descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'users.html',{'users':users})              

class TodoView(View):
    def get(self, request):
        try:
            todos = Query(Todo).descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                todos = []
            else:
                raise e
        return render(request, 'todos.html', {
            'todos': [x.get('content') for x in todos],
        })

    def post(self, request):
        content = request.POST.get('content')
        todo = Todo(content=content)
        try:
            todo.save()
        except LeanCloudError as e:
            return HttpResponseServerError(e.error)
        return HttpResponseRedirect(reverse('todo_list'))
