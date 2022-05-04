from django.http import HttpResponse
from webapp.main_board import MainBoard
from django.shortcuts import render
from webapp.main_board import MainBoard


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'webapp/index.html')


def run_the_code(request):
    MainBoard.run_code()
    return HttpResponse("")
