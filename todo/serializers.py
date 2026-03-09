from rest_framework.serializers import ModelSerializer
from .models import Todo


# API 요청 데이터를 모델 객체로 변환하는 변환기
class TodoSerializer(ModelSerializer):
    class Meta:  # 어떤 필드를 JSON으로 변환할지 정하는 설정 공간
        model = Todo
        # 회원가입 폼이 추가됨에 따라 갱신.
        fields = [
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "image",
            "created_at",
            "user",
        ]
        read_only_fields = ["user"]

        # fields = "__all__"  # 모델의 모든 필드를 자동으로 직렬화합니다.
        # read_only_fields = ["created_at", "updated_at"]  # 읽기만 가능

        # fields = [
        #     "name",
        #     "description",
        #     "complete",
        #     "exp",
        #     "completed_at",
        #     "created_at",
        #     "updated_at",
        # ]

        # exclude = ["created_at", "updated_at"]
        # 모든 필드를 기본 포함시키고 → 특정 필드만 제외하고 싶을 때


# read_only_fields or exclude 둘중 한개를 사용합니다.
