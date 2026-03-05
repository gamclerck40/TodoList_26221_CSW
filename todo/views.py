# Create your views here.
from django.shortcuts import render
from .models import Todo


def todo_list(request):  #  함수형
    todos = Todo.objects.all()
    return render(request, "todo/todo.html", {"todos": todos})
