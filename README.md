# 🛒 CampusMarket — 중고거래 신뢰 플랫폼

## 🧭 개요  
CampusMarket은 **AI 대화 분석 기반 중고거래 신뢰도 진단 서비스**입니다.  
사용자는 거래 상대방과의 대화 내용을 입력하면, **OpenAI ChatGPT-4o-mini 모델**이 대화 문맥을 분석하여  
사기 가능성을 판단하고, **판단 근거**와 **권장 행동**을 함께 제공합니다.  

단순 키워드 필터링이 아닌 **맥락 기반 분석**을 통해 사용자가 안전하게 거래할 수 있도록 돕습니다.

---

## 🛠 기술 스택  

| 구분 | 기술 |
|------|------|
| **Frontend** | React, TypeScript, TailwindCSS |
| **Backend** | Spring Boot (Java 17) |
| **AI Model** | OpenAI API (ChatGPT-4o-mini) |
| **Infra** | AWS EC2, Nginx, Docker |
| **Database** | MySQL |

---

## 서비스 화면

<img width="558" height="391" alt="image" src="https://github.com/user-attachments/assets/33d95292-df03-4af0-b253-9ae0dcaf915c" />
<img width="558" height="391" alt="image" src="https://github.com/user-attachments/assets/fc0f2054-d5c6-4823-8d0e-75b951036d0a" />

<img width="565" height="406" alt="image" src="https://github.com/user-attachments/assets/0e8b7b04-eae2-42d0-83c8-a0fbecf8297d" />

---

## ✨ 주요 기능  

### 1. AI 사기 탐지  
- OpenAI ChatGPT-4o-mini를 사용해 대화 맥락을 분석  
- “EXT_MESSENGER”, “PREPAYMENT_SCAM” 등 유형별 사기 가능성 판별  

### 2. 판단 근거 및 권장 행동 제공  
- 예측 결과에 따라 자동으로 판단 근거와 사용자 가이드 반환  
- 예시:  
  ```
  판단 근거: 대화에서 오픈채팅으로 이동을 유도하는 발언이 반복됩니다.
  권장 행동: 외부 메신저 이동 자제, 플랫폼 내 안전결제 이용 권고.
  ```

### 3. 대화 분석 API 통신  
- Spring Boot 서버에서 OpenAI API에 직접 POST 요청  
- ObjectMapper를 이용한 JSON 직렬화 및 응답 파싱  

### 4. UI 시각화  
- 위험 유형별 색상 구분 및 경고 메시지 강조 표시  

---

## ⚙️ 시스템 구조  

<img width="493" height="311" alt="image" src="https://github.com/user-attachments/assets/09804f68-d4dd-4ec2-a050-688c2f887523" />

---

## 💡 개발 배경  
중고거래 플랫폼에서는 대화 속 작은 신호로도 사기를 예방할 수 있습니다.  
기존의 키워드 필터링은 단어 중심이라 맥락을 이해하지 못하지만,  
LLM 기반 분석은 **의도와 맥락**을 파악하여 더 정확한 탐지를 가능하게 합니다.  

이에 따라, OpenAI ChatGPT-4o-mini 모델을 사용해 대화의 흐름을 이해하고  
사기 패턴을 **자연어로 설명하는 AI 분석기**를 구축했습니다.

---

## 🚀 실행 방법  

```bash
# Backend (Spring Boot)
cd server
./gradlew bootRun

# Frontend
cd client
npm install
npm run dev
```

---

## 🔐 환경 변수 설정  

```env
# .env or application.properties
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
FASTAPI_URL=http://localhost:8000/classify   # (테스트용)
```

---

## 📈 향후 계획  

- 사용자 평판 시스템 도입 (거래 후 신뢰도 점수)  
- 사기 유형별 위험도 시각화 및 신고 기능 추가  
- LLM 프롬프트 엔지니어링 고도화로 판단 정확도 향상  

---

## 📄 라이선스  
이 프로젝트는 개인 학습 및 포트폴리오 목적의 공개용으로 제작되었습니다.
