import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

OUTPUT_DIR = "./ml/chats"

fraud_rules = [
    {
        "code": "EXT_MESSENGER",
        "title": "외부 메신저 유도",
        "description": "플랫폼 밖(텔레그램/카톡 오픈채팅/DM 등)으로 대화를 옮기도록 유도해 안전장치를 회피.",
        "include_signals": ["카톡오픈채팅", "오픈채팅 링크", "톡아이디", "텔레", "t.me", "디엠", "라인으로 얘기", "kakao.com/o 링크", "옾챗"],
        "exclude_signals": ["플랫폼 내 결제·채팅 고수", "공식 고객센터 안내(화이트리스트 링크)"],
        "rule": "외부 메신저 이동 요구가 1회 이상이면 매칭. 화이트리스트 도메인 안내 목적은 제외.",
        "severity": "중간",
        "actions": ["외부 메신저 이동 자제 경고", "플랫폼 내 안전결제 권고"],
    },
    {
        "code": "PREPAY",
        "title": "선입금/보증금 요구",
        "description": "물건 확인 전 선입금/예약금/보증금 요구 또는 입금 먼저 강요.",
        "include_signals": ["선입금", "예약금", "보증금", "입금 먼저", "선결제", "계좌부터", "계좌번호 제시"],
        "exclude_signals": ["플랫폼 에스크로 결제", "대면 후 이체"],
        "rule": "선입금 표현 + 계좌 제시가 함께 있으면 강 매칭. 계좌 없이 예약 문의는 보류.",
        "severity": "높음",
        "actions": ["선입금 금지 안내", "계좌 공유 금지", "신고/차단 버튼 노출"],
    },
    {
        "code": "FAKE_ESCROW",
        "title": "가짜 안전결제/피싱",
        "description": "공식 안전결제를 사칭한 유사 도메인/가짜 UI 링크로 결제 유도.",
        "include_signals": ["안전결제 링크", "에스크로 결제창", "송장 확인 링크", "단축 URL", "의심 도메인"],
        "exclude_signals": ["공식 도메인(예: pay.naver.com, order.coupang.com, 공식 택배사)"],
        "rule": "‘안전결제/에스크로’ 언급 + 비화이트리스트 도메인 URL 동시 존재 시 매칭.",
        "severity": "높음",
        "actions": ["링크 미리보기 차단", "피싱 경고 배너", "신고 유도"],
    },
    {
        "code": "FAKE_ITEM_OR_NO_SHIP",
        "title": "허위매물/미발송",
        "description": "실재하지 않는 물건 또는 선입금 후 지연·잠적. 혹은 발송 약속만 반복.",
        "include_signals": ["시세 대비 과도한 저가", "오늘만 이 가격/급처", "입금하면 바로 발송", "입금 후 지속 지연"],
        "exclude_signals": ["정상 운송장 공유 + 실제 수령 확인"],
        "rule": "시세 괴리 + 선입금/지연·잠적 맥락 반복 시 매칭.",
        "severity": "높음",
        "actions": ["선입금 금지 재안내", "거래 중지 권고"],
    },
    {
        "code": "WRONG_ITEM_OR_QUALITY",
        "title": "다른 물품/불량 발송",
        "description": "설명/사진과 다른 물건 또는 불량품 발송 후 환불 회피.",
        "include_signals": ["설명이랑 다름", "다른 모델 도착", "하자 숨김", "상태 상이"],
        "exclude_signals": ["하자 사전 고지 + 합의된 가격"],
        "rule": "상태/모델 상이 지적 + 환불 회피 표현이 결합되면 매칭.",
        "severity": "중간",
        "actions": ["환불·분쟁 가이드 제공", "증빙 업로드 유도"],
    },
    {
        "code": "COUNTERFEIT",
        "title": "가품(위조) 판매",
        "description": "위조품을 정품으로 속여 판매.",
        "include_signals": ["과도히 저렴한 가격", "정품 강변", "저화질 감정서/보증서 사진"],
        "exclude_signals": ["공식 감정/영수증 확인으로 진위 일치"],
        "rule": "정품 강변 + 시세 괴리 + 증빙 신뢰도 낮음이면 매칭.",
        "severity": "높음",
        "actions": ["정품 인증 방법 안내", "거래 보류 권고"],
    },
    {
        "code": "THIRD_PARTY_MEDIATION",
        "title": "3자 사기(중개형)",
        "description": "사기꾼이 구매자/판매자 사이에 끼어 양쪽을 속여 돈·물건 편취.",
        "include_signals": ["대리 거래", "지인 대신 수령", "입금 계좌/수령인/대화 상대 불일치", "모호한 중개 설명"],
        "exclude_signals": ["공식 대행/탁송 서비스"],
        "rule": "계좌·수령인·연락처 중 2개 이상 불일치 + 중개 모호 시 매칭.",
        "severity": "높음",
        "actions": ["한 채널·한 당사자 원칙 안내", "입금·수령 정보 일치 확인"],
    },
    {
        "code": "ID_OR_ACCOUNT_FRAUD",
        "title": "신분/계좌 도용",
        "description": "도용 신분증·대포통장 사용 정황.",
        "include_signals": ["신분증 사진 전달(이상한 모자이크/각도)", "명의자와 입금주 불일치", "계좌 변경 요구"],
        "exclude_signals": ["명의 일치 확인"],
        "rule": "입금주/연락처/수령인/신분증 이름 중 2개 이상 불일치 시 매칭.",
        "severity": "높음",
        "actions": ["본인확인 경고", "거래 중단 권고", "신고 안내"],
    },
    {
        "code": "PRESSURE_OR_URGENCY",
        "title": "과도한 압박/긴급성 조성",
        "description": "짧은 시간 내 결정을 강요하여 정상 검증 방해.",
        "include_signals": ["지금 바로", "5분 안에", "다른 분도 대기", "오늘만"],
        "exclude_signals": ["상식적 예약·대기 안내"],
        "rule": "시간 압박 표현 반복 + 결제/선입금 요구와 결합 시 다른 유형 가중.",
        "severity": "중간",
        "actions": ["충분한 검토 권고", "안전결제/직거래 유도"],
    },
]

def generate_responses(index, rule):
    prompt = f"""
        당신은 중고거래 채팅 데이터를 생성하는 역할을 맡았습니다.
        사람이 실제로 대화하는 것처럼 자연스럽게 이어지는 1:1 채팅을 만들어주세요.

        [조건]
        - 완전한 JSON 형식으로만 출력해야 합니다.
        - 코드블록(````json`) 같은 마크다운 문법은 절대 포함하지 마세요.
        - chat_room_id는 "{index}"로 고정합니다.
        - fraud_type은 "{fraud_rules[rule]['code']}"로 설정합니다.
        - sender_id는 0(피해자), 1(사기꾼) 두 가지입니다.
        - id는 1부터 시작하는 AUTO_INCREMENT 정수입니다.
        - timestamp는 "2025-09-20T18:45:00" 같은 ISO 형식을 사용합니다.
        - 대화는 최소 6턴 이상 (왕복 3회 이상)으로 구성하세요.

        [사기 유형 기준]
        - 이번 대화는 "{fraud_rules[rule]['title']}" 유형({fraud_rules[rule]['code']})에 해당해야 합니다.
        - {fraud_rules[rule]['include_signals']}를 참고해서 유사하게 대화를 유도해주세요.
        - {fraud_rules[rule]['exclude_signals']}는 절대 포함하지 마세요.
        - 피해자는 의심하거나 망설이는 표현도 포함하여 현실감을 살리세요.

        [출력 형식]
        {{
            "chat_room_id": "{index}",
            "fraud_type": "{fraud_rules[rule]['code']}",
            "messages": [
                {{
                "id": 1,
                "sender_id": "0",
                "content": "안녕하세요, 물건 아직 있나요?",
                "timestamp": "2025-09-20T18:45:00"
                }},
                ...
            ]
        }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=1000
    )

    return response.choices[0].message.content

def save_responses(index, responses, rule):
    # 개별 파일 저장
    os.makedirs(f"{OUTPUT_DIR}/{rule}", exist_ok=True)
    output_path = os.path.join(f"{OUTPUT_DIR}/{rule}", f"chats{index}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(responses)

    # # ✅ 통합 파일에 덧붙이기
    # all_path = os.path.join(OUTPUT_DIR, "all_chats.txt")
    # with open(all_path, "a", encoding="utf-8") as f:
    #     f.write(responses.strip() + "\n")  # 줄바꿈 보장

def process_files(start: int, end: int, rule):
    for r in rule :
        for i in range(start, end + 1):
            print(f"✅ Processing Responses for rule #{r} #{i}...")
            responses = generate_responses(i, r)
            save_responses(i, responses, r)
            print(f"📁 저장 완료: {OUTPUT_DIR}/chats{i}.txt\n")

if __name__ == "__main__":
    # 👇 여기에서 시작~끝 파일 번호 지정 (예: 22~23)
    start_file = 5
    end_file = 50
    rule = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    process_files(start=start_file, end=end_file, rule=rule)