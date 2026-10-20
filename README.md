# 우유의 도구함 · 배포용

나눠 쓰는 Claude 플러그인의 **설치 파일과 안내**만 두는 곳입니다.

## edufine — 에듀파인 품의 도우미

견적서 사진(또는 PDF·캡처)을 주면 K-에듀파인 품의의 **제목·개요·품목내역**을 학교 양식에 맞춰 만들어 줍니다.
금액과 한글 금액(금일○○원정)은 프로그램이 계산하고, 견적서 합계와 맞는지도 검산합니다.

### 설치

Claude Code에서 아래 두 줄을 차례로 입력하세요.

```
/plugin marketplace add onggyu32/uyu-releases
/plugin install edufine@uyu
```

### 쓰는 법

견적서를 올리고 **"이 견적서로 품의 써 줘"** 라고 말하면 됩니다.

- **품의 도우미 페이지** `plugins/edufine/skills/edufine-pumui/helper.html` — 브라우저로 열어 칸별로 복사할 수 있습니다.
- **자동입력 북마크** `plugins/edufine/skills/edufine-pumui/bookmarklet.txt` — 에듀파인 제목·개요 칸을 채워 줍니다.

### 알아 두실 점

- 만든 내용은 반드시 직접 확인한 뒤 에듀파인에 입력하세요.
- 예산(세부사업·원가통계비목), 요구일자, 견적서 첨부는 직접 선택하고 올려야 합니다.
- 자동입력 북마크는 실제 에듀파인 화면에서 아직 충분히 시험하지 않았습니다.

---

edufine 0.1.0
