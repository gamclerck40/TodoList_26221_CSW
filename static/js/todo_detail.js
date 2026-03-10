document.addEventListener("DOMContentLoaded", () => {
  // ======================================================
  // 0) 기본 설정
  // ======================================================
  const todoId = "{{ todo.id }}";
  const LOGIN_PAGE_URL = "/login/";
  const LIST_PAGE_URL = "/todo/list/";

  // window.api 확인
  if (!window.api) {
    console.error("window.api가 없습니다. base.html에서 static/js/api.js 로드 확인");
    alert("설정 오류: api.js가 로드되지 않았습니다.");
    return;
  }

  // access_token 없으면 로그인으로
  const access = localStorage.getItem("access_token");
  if (!access) {
    console.log("access_token 없음 → 로그인 이동");
    window.location.href = LOGIN_PAGE_URL;
    return;
  }

  // ======================================================
  // 1) 공통 헬퍼
  // ======================================================
  function handleAuthError(err) {
    const status = err.response?.status;
    if (status === 401 || status === 403) {
      alert("로그인이 필요합니다.");

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      window.location.href = LOGIN_PAGE_URL;
    }
    return Promise.reject(err);
  }

  // ======================================================
  // 2) 버튼 이벤트
  // ======================================================
  // 수정 페이지로 이동
  document.querySelector(".todoUpdate").addEventListener("click", () => {
    window.location.href = `/todo/update/${todoId}/`;
  });

  // 삭제 처리
  document.querySelector(".todoDelete").addEventListener("click", async () => {
    const ok = confirm("정말 삭제하시겠습니까?");
    if (!ok) return;

    try {
      await window.api.delete(`/todo/viewsets/view/${todoId}/`);
      window.location.href = LIST_PAGE_URL;
    } catch (err) {
      handleAuthError(err).catch(() => {});
      console.error("삭제 실패:", err.response?.data || err.message);
      alert("삭제 중 오류가 발생했습니다.");
    }
  });

  // 리스트(홈)로 이동
  document.querySelector(".todoHome").addEventListener("click", () => {
    window.location.href = LIST_PAGE_URL;
  });
});
