# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from urllib import parse
from .models import Lecture
from .spider_main import SpiderMain


def index(request):
    return render(request, 'index.html', {'LectureList': Lecture.objects.all().order_by('-announce_date')})


def craw(request):
    try:
        Lecture.objects.all().delete()
        spider = SpiderMain()
        lecture_list = spider.craw("http://eis.whu.edu.cn/index.shtml", 200)
        for i in lecture_list:
            Lecture.objects.create(url=i['url'], page_title=i['page title'], title=i['title'],
                                   speaker=i['speaker'], announce_date=i['announce date'],
                                   time=i['time'], room=i['room'])
        return render(request, 'list.html', {"LectureList": Lecture.objects.all().order_by('-announce_date')})
    except:
        return HttpResponse("Craw failed. Please update the spider program.")


def search(request):
    input = parse.unquote(request.GET['input'])
    select = request.GET['select']
    if select == 'page_title':
        lecture_list = Lecture.objects.filter(page_title__icontains=input)
    elif select == 'title':
        lecture_list = Lecture.objects.filter(title__icontains=input)
    elif select == 'speaker':
        lecture_list = Lecture.objects.filter(speaker__icontains=input)
    elif select == 'time':
        lecture_list = Lecture.objects.filter(time__icontains=input)
    elif select == 'room':
        lecture_list = Lecture.objects.filter(room__icontains=input)
    elif select == 'announce_date':
        lecture_list = Lecture.objects.filter(
            announce_date__icontains=input)
    else:
        lecture_list = Lecture.objects.all()
    return render(request, 'list.html', {"LectureList": lecture_list.order_by('-announce_date')})
