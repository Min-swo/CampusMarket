import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

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


import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


import re
import json

def classify_chat(chat_json: dict) -> dict:
    rules_str = json.dumps(fraud_rules, ensure_ascii=False, indent=2)
    chat_str = json.dumps(chat_json, ensure_ascii=False, indent=2)

    prompt = f"""
        당신은 중고거래 안전 **심사관**입니다.
        아래 '사기 유형 핸드북'을 기준으로 대화를 분석하세요.

        [심사 규칙]
        1. fraud_type은 반드시 fraud_rules["code"] 중 하나 또는 "NORMAL" 하나만 선택한다.
        2. NORMAL은 다음 경우에만 선택한다:
        - 어떤 include_signals도 대화에 등장하지 않는다.
        - 또는 등장했지만 exclude_signals에 의해 무효화된다.
        3. include_signals가 하나라도 등장하면 반드시 해당 fraud_type을 선택한다. 
        (애매하더라도 NORMAL을 선택하지 말라)
        4. rationale은 한두 문장으로 판정 근거를 요약한다.
        5. evidence에는 실제 대화 메시지에서 매칭된 문구만 넣는다.
        6. actions는 fraud_rules의 해당 유형에 정의된 권고 행동만 포함한다.
        7. 출력은 반드시 JSON 한 줄만.

        [출력 형식]
        {{
        "chat_room_id": "{chat_json['chat_room_id']}",
        "fraud_type": "<fraud_code or NORMAL>",
        "rationale": "한두 문장 요약 근거",
        "evidence": ["실제 매칭 문구"],
        "actions": ["권고/경고 문구"]
        }}

        [사기 유형 핸드북]
        {rules_str}

        [입력 대화]
        {chat_str}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "너는 JSON 심사기. 반드시 JSON만 출력해."},
                {"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200,
    )

    result = response.choices[0].message.content.strip()

    # 1차 시도: JSON 파싱
    try:
        return json.loads(result)
    except Exception:
        # 2차 시도: fraud_type만 regex로 뽑아보기
        match = re.search(r'"fraud_type"\s*:\s*"([^"]+)"', result)
        fraud_type = match.group(1) if match else "ERROR"
        return {
            "chat_room_id": chat_json["chat_room_id"],
            "fraud_type": fraud_type,
            "rationale": None,
            "evidence": None,
            "actions": None,
            "raw": result
        }

def evaluate_dataset(base_dir="./ml/chats", num_rules=9, num_samples=5, include_normal=True):
    """
    ./ml/chats/{rule}/chats{i}.txt + ./ml/chats/normal/chats{i}.txt 검증
    규칙별/전체 정확도 평가
    """
    results = {}
    total_correct = 0
    total_count = 0

    # 0~num_rules-1
    rule_folders = [str(i) for i in range(num_rules)]

    # normal도 포함
    if include_normal:
        rule_folders.append("normal")

    for rule_name in rule_folders:
        folder = os.path.join(base_dir, rule_name)
        correct = 0
        count = 0

        if not os.path.exists(folder):
            print(f"⚠️ {folder} 없음, 스킵")
            continue

        for i in range(num_samples):
            file_path = os.path.join(folder, f"chats{i}.txt")
            if not os.path.exists(file_path):
                continue

            # ✅ txt → JSON 파싱
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                try:
                    chat_json = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 파싱 실패: {file_path}, 에러: {e}")
                    continue

            expected = chat_json["fraud_type"]
            chat_json_for_llm = {k: v for k, v in chat_json.items() if k != "fraud_type"}

            predicted = classify_chat(chat_json_for_llm)
            predicted_type = predicted.get("fraud_type", "ERROR")

            print(f"[{file_path}] 예측: {predicted_type} / 정답: {expected}")

            if predicted_type == expected:
                correct += 1
            else:
                print(f"\n❌ Misclassified: {file_path}")
                print(f"   expected: {expected}, got: {predicted_type}")
                print(f"   rationale: {predicted.get('rationale')}")
                print(f"   evidence: {predicted.get('evidence')}")
                print(f"   actions: {predicted.get('actions')}")
                print("📄 대화 내용:")
                for msg in chat_json["messages"]:
                    print(f"  [{msg['sender_id']}] {msg['content']}")

            count += 1

        acc = correct / count if count > 0 else 0
        results[rule_name] = {"accuracy": acc, "correct": correct, "total": count}
        total_correct += correct
        total_count += count

    overall_acc = total_correct / total_count if total_count > 0 else 0
    return results, overall_acc

if __name__ == "__main__":
    results, overall_acc = evaluate_dataset(
        base_dir="./ml/chats", num_rules=9, num_samples=51, include_normal=True
    )

    print("\n=== 규칙별 정확도 ===")
    for rule, stats in results.items():
        print(f"Rule {rule}: {stats['accuracy']:.2%} ({stats['correct']}/{stats['total']})")

    print(f"\n=== 전체 정확도: {overall_acc:.2%} ===")