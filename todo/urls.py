from django.urls import path
from .views.templates_views import (
    TodoListView,
    TodoCreateView,
    TodoDetailView,
    TodoUpdateView,
)
from .views.api_views import (
    TodoListAPI,
    TodoCreateAPI,
    TodoRetrieveAPI,
    TodoUpdateAPI,
    TodoDeleteAPI,
)

app_name = "todo"

urlpatterns = [
    # path("list/", views.todo_list, name="todo_List"), # 첫 테스트용
    # api DRF / JSON 응답 뷰
    path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    path("api/update/<int:pk>/", TodoUpdateAPI.as_view(), name="todo_api_update"),
    path("api/delete/<int:pk>/", TodoDeleteAPI.as_view(), name="todo_api_delete"),
    # 탬플릿View
    path("list/", TodoListView.as_view(), name="list"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_Update"),
    # APIView
    path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
]
