# Register your models here.
from django.contrib import admin
from .models import Todo


@admin.register(Todo)  # 둘중 택1 둘다 있으면 오류가 발생합니다.
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
