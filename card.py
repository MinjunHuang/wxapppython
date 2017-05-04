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
from textwrap import *
import re
import leancloud

class Card(Object):
    pass

def preview(request,id):
    try:
        card = Query(Card).get(id)
        msstream = BytesIO()
        template(card,msstream)
        return HttpResponse(msstream.getvalue(),content_type="image/png") 
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            card = ''
            return HttpResponse(e,content_type="text/plain") 
        else:
            raise e
            return HttpResponse(e,content_type="text/plain") 

def template(card,msstream):
    w = 640
    h = 862
    iw = 600
    ih = 340
    title = card.get('name')
    content = card.get('content')
    spacing = 20
    content = fill(content, 15)
    author = '- 卫斯理 -' 
    copyright = '微信小程序「时光砂砾」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    tw,th = draw.multiline_textsize(title, font=title_fnt)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    cw,ch = draw.multiline_textsize(content, font=content_fnt, spacing=spacing)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)
    h = 635+th+ch+crh+ah;
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)

    

    photo = Image.open("girl.jpg").convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>iw/ih:
        box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
    else:
        box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((iw,ih))
    base.paste(photo,box=(20,20))
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text in the middle of the image, half opacity
    draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,420+th+45+ch+115), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,420+th+45+ch+115+ah+50), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # get BytesIO
    
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png")  


def template2(request):
    w = 640
    h = 1020
    iw = 600
    ih = 340
    title = '标题'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
    spacing = 20
    padding = 2
    author = '- 卫斯理 -' 
    copyright = '微信小程序「时光砂砾」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)


    

    photo = Image.open("girl.jpg").convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>iw/ih:
        box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
    else:
        box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((iw,ih))
    base.paste(photo,box=(20,20))
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # split the title
    tlines = wrap(title, 1)
    # current title height
    tnh = 420
    # get width and height of single title word
    stw,sth = title_fnt.getsize("已")
    for tline in tlines:       
        draw.text((w-115-stw,tnh), tline, fill=(0,0,0,255), font=title_fnt)
        tnh = tnh+sth
    # get width and height of single content word
    scw,sch = content_fnt.getsize("已")    
    clines = wrap(content, 14)
    # current width of content
    cnw = w-115-stw-115-scw
    for cline in clines:
        # current height of content 
        cnh = 420 
        cwords = wrap(cline, 1)
        for cword in cwords:
            pattern = re.compile("[，。、]+") 
            if pattern.search(cword):
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)
                # draw.text((cnw+30-12,cnh-30+12), cword, fill=(0,0,0,255), font=content_fnt)
            else:
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)                           
            cnh = cnh+sch+padding
        cnw = cnw-scw-spacing   

       
    # draw text in the middle of the image, half opacity
    # draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    # draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,h-50-15-crh-ah), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,h-15-crh), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    

def template3(request):
    w = 640
    h = 862
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    title = '标题'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
    spacing = 20
    content = fill(content, 15)
    author = '- 卫斯理 -' 
    copyright = '微信小程序「时光砂砾」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    tw,th = draw.multiline_textsize(title, font=title_fnt)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    cw,ch = draw.multiline_textsize(content, font=content_fnt, spacing=spacing)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)
    h = 695+th+ch+crh+ah;
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)

    

    photo = Image.open("girl.jpg").convert('RGBA')

    pw, ph = photo.size

    if pw > ph:
        box = ((pw-ph*bw/bh)/2,0,(pw+ph*bw/bh)/2,ph)
    else:
        box = (0,(ph-pw*bh/bw)/2,pw,(ph+pw*bh/bw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((bw*4,bh*4))

    circle = Image.new('L', (bw*4, bh*4), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, bw*4, bh*4), fill=255)
    alpha = Image.new('L', (bw*4, bh*4), 255)
    alpha.paste(circle, (0, 0))
    photo.putalpha(alpha)
    photo = photo.resize((bw,bh),Image.ANTIALIAS)

    base.paste(photo,box=(170,120),mask=photo)
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text in the middle of the image, half opacity
    draw.multiline_text((w/2-tw/2,480), title, font=title_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w/2-cw/2,480+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,480+th+45+ch+115), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,480+th+45+ch+115+ah+50), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 


def template4(request):
    w = 640
    h = 1080
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    padding = 2
    title = '标题'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
    spacing = 20
    content = fill(content, 15)
    author = '- 卫斯理 -' 
    copyright = '微信小程序「时光砂砾」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)

    

    photo = Image.open("girl.jpg").convert('RGBA')

    pw, ph = photo.size

    if pw > ph:
        box = ((pw-ph*bw/bh)/2,0,(pw+ph*bw/bh)/2,ph)
    else:
        box = (0,(ph-pw*bh/bw)/2,pw,(ph+pw*bh/bw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((bw*4,bh*4))

    circle = Image.new('L', (bw*4, bh*4), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, bw*4, bh*4), fill=255)
    alpha = Image.new('L', (bw*4, bh*4), 255)
    alpha.paste(circle, (0, 0))
    photo.putalpha(alpha)
    photo = photo.resize((bw,bh),Image.ANTIALIAS)

    base.paste(photo,box=(170,120),mask=photo)
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # split the title
    tlines = wrap(title, 1)
    # current title height
    tnh = 480
    # get width and height of single title word
    stw,sth = title_fnt.getsize("已")
    for tline in tlines:       
        draw.text((w-115-stw,tnh), tline, fill=(0,0,0,255), font=title_fnt)
        tnh = tnh+sth
    # get width and height of single content word
    scw,sch = content_fnt.getsize("已")    
    clines = wrap(content, 14)
    # current width of content
    cnw = w-115-stw-115-scw
    for cline in clines:
        # current height of content 
        cnh = 480 
        cwords = wrap(cline, 1)
        for cword in cwords:
            pattern = re.compile("[，。、]+") 
            if pattern.search(cword):
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)
                # draw.text((cnw+30-12,cnh-30+12), cword, fill=(0,0,0,255), font=content_fnt)
            else:
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)                           
            cnh = cnh+sch+padding
        cnw = cnw-scw-spacing   

       
    # draw text in the middle of the image, half opacity
    # draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    # draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,h-50-15-crh-ah), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,h-15-crh), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 
def image_text(request): 
    fontSize = 40
    w = 640
    h = 640
    text = '当一艘船沉入海底\n当一个人成了谜\n你不知道\n他们为何离去\n那声再见竟是他最后一句' 
    meta = '后会无期·G.E.M.邓紫棋'
    copyright = '— 微信小程序 : 时光砂砾 —'
    # 按长度（字数）换行
    # text = fill(text,11)
    # make a blank image as the background
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    # get an image
    photo = Image.open("girl.jpg").convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>w/h:
        box = ((pw-ph)/2,0,(pw+ph)/2,ph)
    else:
        box = (0,(ph-pw)/2,pw,(pw+ph)/2)  

    photo = photo.crop(box)
    photo = photo.resize((w,h))
   
    # blur filter
    photo = photo.filter(ImageFilter.GaussianBlur())

    base.paste(photo)


    # make a blank image for text, initailized to half-transparent text color
    txt = Image.new('RGBA', (w, h), (0,0,0,100))
    # get a font
    fnt = ImageFont.truetype('font/zh/LiJin.ttf',fontSize)
    meta_fnt = ImageFont.truetype('font/zh/PingFang.ttf',20)
    copyright_fnt = ImageFont.truetype('font/zh/TongXin.ttf',14)
    # get size of the text
    # (tw, th) = fnt.getsize(text)
    # get a drawing context
    draw = ImageDraw.Draw(txt)
    tw,th = draw.multiline_textsize(text, fnt)
    mw,mh = draw.multiline_textsize(meta, meta_fnt)
    cpw,cph =draw.multiline_textsize(copyright, copyright_fnt)
    # draw text in the middle of the image, half opacity
    draw.multiline_text(((w-tw)/2,(h-th)/2), text, font=fnt, fill=(255,255,255,255), align='center',spacing=15)
    draw.multiline_text(((w-mw)/2,h-mh-30), meta, font=meta_fnt, fill=(255,255,255,150), align='center')
    draw.multiline_text(((w-cpw)/2,h-cph-10), copyright, font=copyright_fnt, fill=(255,255,255,150), align='center')

    # composite base image and text image
    out = Image.alpha_composite(base, txt)
    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    out.save(msstream,"png")
    # release memory
    out.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png")  

