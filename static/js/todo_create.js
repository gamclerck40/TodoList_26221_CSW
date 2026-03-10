document.addEventListener("DOMContentLoaded", () => {
  // ======================================================
  // 0) 기본 설정
  // ======================================================
  const LOGIN_PAGE_URL = "/login/";
  const CREATE_API_URL = "/todo/viewsets/view/";

  // axios 인스턴스(window.api) 확인
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
  // 인증 실패(401/403) → 토큰 삭제 후 로그인 이동
  function handleAuthError(err) {
    const status = err.response?.status;
    if (status === 401 || status === 403) {
      console.log("인증 실패(401/403) → 토큰 삭제 후 로그인 이동");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = LOGIN_PAGE_URL;
    }
    return Promise.reject(err);
  }

  // FormData 생성
  function buildFormData() {
    const formData = new FormData();

    formData.append("name", document.getElementById("name").value.trim());
    formData.append("description", document.getElementById("description").value.trim());
    formData.append("complete", document.getElementById("complete").checked ? "true" : "false");
    formData.append("exp", document.getElementById("exp").value || "0");

    const fileInput = document.getElementById("image");
    if (fileInput.files && fileInput.files.length > 0) {
      formData.append("image", fileInput.files[0]);
    }

    return formData;
  }

  // ======================================================
  // 2) 이벤트 처리
  // ======================================================
  document.getElementById("todoCreate").addEventListener("click", async (e) => {
    e.preventDefault();

    try {
      const formData = buildFormData();

      // FormData일 때 Content-Type은 axios가 자동 설정하므로 헤더를 따로 건드리지 않음
      const res = await window.api.post(CREATE_API_URL, formData);

      console.log("생성 성공:", res.data);
      window.location.href = "/todo/list/";
    } catch (err) {
      handleAuthError(err).catch(() => {});
      console.error("생성 실패:", err.response?.data || err.message);
      alert("생성 실패: 콘솔/네트워크 확인");
    }
  });

  // ======================================================
  // 3) 초기화(선택)
  // ======================================================
  // 필요하면 여기서 기본값 세팅/포커스 처리 가능
  // document.getElementById("name").focus();
});
