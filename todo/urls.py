from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("list/", views.todo_list, name="list"),  # 첫 테스트용
]
