# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from ..models import Todo  # 경로변경
from ..serializers import TodoSerializer  # 경로변경
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# 인증된 사용자만 접근 가능하도록 하는 권한 클래스
from rest_framework.permissions import IsAuthenticated

# ---------------------------------------------------------
# models에서 좋아요 / 북마크 / 댓글 모델 import
# ---------------------------------------------------------
# .. 는 상위 디렉토리를 의미합니다.
# 즉 todo 앱의 models.py 에서 정의된 모델을 가져옵니다.
from interaction.models import TodoLike, TodoBookmark, TodoComment
from django.db.models import Q

# ---------------------------------------------------------
# DRF action / permission import
# ---------------------------------------------------------
# action
# → ViewSet 안에서 "추가 API"를 만들 때 사용하는 데코레이터
# → 기본 CRUD 외에 커스텀 API를 만들 수 있음
#
# permission
# → API 접근 권한을 제어
# → 로그인 필요 / 누구나 가능 등을 설정
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


# ---------------------------------------------------------
# Todo 목록 페이지네이션 설정
# ---------------------------------------------------------
class TodoListPagination(PageNumberPagination):

    page_size = 3
    # 한 페이지에 기본적으로 보여줄 데이터 개수

    page_size_query_param = "page_size"
    # URL 쿼리 파라미터로 페이지 크기 변경 가능
    # 예: /todo/viewsets/view/?page_size=5

    max_page_size = 50
    # 사용자가 설정할 수 있는 최대 페이지 크기 제한
    # 예: page_size=100 요청 시 최대 50까지만 허용


# ModelViewSet을 사용하면 아래 기능이 자동 생성됩니다
# - list()      : 전체 목록 조회 (GET)
# - retrieve()  : 단일 데이터 조회 (GET)
# - create()    : 데이터 생성 (POST)
# - update()    : 전체 수정 (PUT)
# - partial_update() : 부분 수정 (PATCH)
# - destroy()   : 삭제 (DELETE)


# ---------------------------------------------------------
# 핵심 ViewSet
# ---------------------------------------------------------
# ModelViewSet
#
# 아래 CRUD가 자동 생성됩니다.
#
# GET    /todos/          → list
# POST   /todos/          → create
# GET    /todos/{id}/     → retrieve
# PUT    /todos/{id}/     → update
# DELETE /todos/{id}/     → destroy
#
# 즉 CRUD API를 자동으로 만들어주는 클래스입니다.
# ---------------------------------------------------------
class TodoViewSet(viewsets.ModelViewSet):

    # -----------------------------------------------------
    # 기본 queryset
    # -----------------------------------------------------
    # Todo 테이블 전체 데이터를 가져옵니다.
    # created_at 기준으로 최신순 정렬
    # queryset = Todo.objects.all().order_by("-created_at")

    # -----------------------------------------------------
    # serializer 지정
    # -----------------------------------------------------
    # 데이터 → JSON 변환
    # JSON → 데이터 검증 및 저장
    serializer_class = TodoSerializer

    # -----------------------------------------------------
    # 기본 permission
    # -----------------------------------------------------
    # AllowAny
    # → 로그인하지 않아도 조회 가능
    #
    # 즉
    # list / retrieve 는 누구나 가능
    permission_classes = [AllowAny]

    # -----------------------------------------------------
    # list API 커스터마이징
    # -----------------------------------------------------
    # 기본 list 응답
    #
    # [
    #   {...},
    #   {...}
    # ]
    #
    # 하지만 JS에서 사용하기 편하도록
    # 아래처럼 응답 구조를 변경했습니다.
    #
    # {
    #   data: [...],
    #   current_page: 1,
    #   page_count: 5,
    #   next: true,
    #   previous: false
    # }
    # -----------------------------------------------------
    pagination_class = TodoListPagination  # 리스트 조회 시 페이지네이션 적용

    # ======================================================
    # 생성 / 수정 / 삭제는 로그인 필요
    # ======================================================
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    # ======================================================
    # 공개글 + 내 글 조회 로직
    # ======================================================
    def get_queryset(self):
        user = self.request.user  # 현재 로그인한 사용자

        # 비로그인 사용자는 공개글만 조회
        if not user.is_authenticated:
            return Todo.objects.filter(Q(is_public=True)).order_by("-created_at")

        return Todo.objects.filter(
            # Q 객체를 사용하여 OR 조건을 생성
            # ---------------------------------------------
            # Q(is_public=True)
            #   → 다른 사용자가 작성한 Todo라도
            #     "공개글(is_public=True)"이면 조회 가능
            #
            # Q(user=user)
            #   → 현재 로그인한 사용자가 작성한 Todo는
            #     공개 여부와 상관없이 모두 조회 가능
            #
            # 즉,
            # "공개글이거나 OR 내가 작성한 글" 을 조회
            Q(is_public=True)
            | Q(user=user)
        ).order_by(
            "-created_at"
        )  # 최신 글이 먼저 보이도록 정렬

    # ======================================================
    # Todo 생성 시 작성자 자동 설정
    # ======================================================
    def perform_create(self, serializer):
        # 프론트에서 user를 보내지 않아도
        # 현재 로그인한 사용자를 작성자로 자동 저장
        # 또한 기본적으로 글을 공개 상태(is_public=True)로 생성
        serializer.save(user=self.request.user, is_public=True)

    def list(self, request, *args, **kwargs):

        # queryset 필터링
        qs = self.filter_queryset(self.get_queryset())

        # pagination 처리
        page = self.paginate_queryset(qs)

        # ---------------------------------------------
        # pagination이 적용된 경우
        # ---------------------------------------------
        if page is not None:

            # serializer 실행
            serializer = self.get_serializer(
                page,
                many=True,
                context={"request": request},
            )

            return Response(
                {
                    "data": serializer.data,
                    # 현재 페이지
                    "current_page": int(request.query_params.get("page", 1)),
                    # 전체 페이지 수
                    "page_count": self.paginator.page.paginator.num_pages,
                    # 다음 페이지 존재 여부
                    "next": self.paginator.get_next_link() is not None,
                    # 이전 페이지 존재 여부
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )

        # ---------------------------------------------
        # pagination이 없는 경우
        # ---------------------------------------------
        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )

    # -----------------------------------------------------
    # 좋아요 토글 API
    # -----------------------------------------------------
    # URL
    #
    # POST /todo/viewsets/view/<id>/like/
    #
    # detail=True
    # → 특정 Todo 대상 API
    #
    # permission_classes=[IsAuthenticated]
    # → 로그인한 사용자만 가능
    #
    # get_or_create 패턴
    # → 없으면 생성
    # → 있으면 삭제
    #
    # 즉
    # 좋아요 ON / OFF 토글 기능
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):

        # 현재 Todo 가져오기
        todo = self.get_object()

        # 로그인한 사용자
        user = request.user

        # 좋아요 존재 확인
        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        # 새로 생성된 경우 → 좋아요 ON
        if created:
            liked = True

        # 이미 존재 → 삭제 → 좋아요 OFF
        else:
            obj.delete()
            liked = False

        # 전체 좋아요 개수 계산
        like_count = TodoLike.objects.filter(todo=todo).count()

        # 응답
        return Response({"liked": liked, "like_count": like_count})

    # -----------------------------------------------------
    # 북마크 토글 API
    # -----------------------------------------------------
    # URL
    #
    # POST /todo/viewsets/view/<id>/bookmark/
    #
    # 좋아요와 동일한 구조
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):

        # 현재 Todo
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 북마크 생성 또는 조회
        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        # 북마크 ON
        if created:
            bookmarked = True

        # 북마크 OFF
        else:
            obj.delete()
            bookmarked = False

        # 전체 북마크 수
        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()

        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    # -----------------------------------------------------
    # 댓글 등록 API
    # -----------------------------------------------------
    # URL
    #
    # POST /todo/viewsets/view/<id>/comments/
    #
    # request.data
    # → 클라이언트에서 보낸 JSON 데이터
    #
    # {
    #   "content": "댓글 내용"
    # }
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):

        # Todo 가져오기
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 댓글 내용 가져오기
        content = (request.data.get("content") or "").strip()

        # 댓글 내용 검증
        if not content:
            return Response({"detail": "content is required"}, status=400)

        # 댓글 생성
        TodoComment.objects.create(todo=todo, user=user, content=content)

        # 댓글 개수 계산
        comment_count = TodoComment.objects.filter(todo=todo).count()

        return Response({"comment_count": comment_count})
