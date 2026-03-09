# Django 인증 관련 함수
# authenticate → 사용자 인증
# login → 세션 로그인 처리
# logout → 세션 로그아웃 처리
from django.contrib.auth import logout

# DRF APIView 사용
from rest_framework.views import APIView

# API 응답 객체
from rest_framework.response import Response

# HTTP 상태 코드
from rest_framework import status

# 모든 사용자 접근 허용
from rest_framework.permissions import AllowAny

# 회원가입 데이터 검증 Serializer
from .serializers import SignupSerializer

from rest_framework.permissions import IsAuthenticated  # 추가


# -----------------------------
# 회원가입 API
# -----------------------------
class SignupAPIView(APIView):
    """
    회원가입은 JWT/세션과 무관하게 그대로 사용
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


# -----------------------------
# 세션 로그인 API -> JWT에서는 더 이상 필요 없음.
# -----------------------------
# class SessionLoginAPIView(APIView):

#     # 로그인하지 않은 사용자도 접근 가능
#     # permission_classes = [AllowAny]
#     """
#     ⚠️ 전환기 임시 로그아웃(세션 정리용)
#     - JWT 환경에서 '로그아웃'은 보통 프론트에서 토큰 삭제로 처리합니다.
#     - 그래도 혹시 남아있을 수 있는 세션을 logout(request)로 정리해줍니다.
#     """
#     permission_classes = [IsAuthenticated]
#     # POST 요청 처리
#     def post(self, request):

#         # 요청 데이터에서 username, password 추출
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")

#         # 사용자 인증
#         # username / password가 맞는지 확인
#         user = authenticate(request, username=username, password=password)

#         # 인증 실패
#         if not user:
#             return Response(
#                 {"detail": "아이디/비밀번호가 올바르지 않습니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # 인증 성공 → 세션 로그인 처리
#         login(request, user)

#         # 로그인 성공 응답
#         return Response({"detail": "로그인 성공"}, status=status.HTTP_200_OK)


# -----------------------------
# 세션 로그아웃 API
# -----------------------------
class SessionLogoutAPIView(APIView):
    """
    ⚠️ 전환기 임시 로그아웃(세션 정리용)
    - JWT 환경에서 '로그아웃'은 보통 프론트에서 토큰 삭제로 처리합니다.
    - 그래도 혹시 남아있을 수 있는 세션을 logout(request)로 정리해줍니다.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃(세션 정리)"}, status=status.HTTP_200_OK)
