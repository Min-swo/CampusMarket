import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

OUTPUT_DIR = "./ml/chats"

def generate_responses(index):
    prompt = f"""
        당신은 중고거래 채팅 데이터를 생성하는 역할을 맡았습니다.
        사람이 실제로 대화하는 것처럼 자연스럽게 이어지는 1:1 채팅을 만들어주세요.

        [조건]
        - JSON 형식으로만 출력해야 합니다.  JSON 형태로 다른 곳에 바로 입력가능하도록 해야합니다.
        - 코드블록(````json`) 같은 마크다운 문법은 절대 포함하지 마세요.
        - chat_room_id는 "{index}"로 고정합니다.
        - fraud_type은 "NORMAL"로 설정합니다.
        - sender_id는 0(구매자), 1(판매자) 두 가지입니다.
        - id는 1부터 시작하는 AUTO_INCREMENT 정수입니다.
        - timestamp는 "2025-09-20T18:45:00" 같은 ISO 형식을 사용합니다.
        - 대화는 최소 6턴 이상 (왕복 3회 이상)으로 구성하세요.

        [정상 거래 기준]
        - 선입금/보증금/외부 메신저 유도는 절대 포함하지 마세요.
        - 합리적인 가격, 상품 설명, 거래 일정 협의, 안전결제/대면거래 안내를 포함하세요.
        - 택배 거래 시 운송장 번호 제공 등 신뢰할 수 있는 요소를 포함하세요.
        - 서로 존중하는 말투를 사용하세요.

        [출력 형식]
        {{
        "chat_room_id": "{index}",
        "fraud_type": "NORMAL",
        "messages": [
            {{
            "id": 1,
            "sender_id": "0",
            "content": "안녕하세요, 자전거 아직 판매 중이신가요?",
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

def save_responses(index, responses):
    # 개별 파일 저장
    os.makedirs(f"{OUTPUT_DIR}/normal", exist_ok=True)
    output_path = os.path.join(f"{OUTPUT_DIR}/normal", f"chats{index}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(responses)

    # # ✅ 통합 파일에 덧붙이기
    # all_path = os.path.join(OUTPUT_DIR, "all_chats.txt")
    # with open(all_path, "a", encoding="utf-8") as f:
    #     f.write(responses.strip() + "\n")  # 줄바꿈 보장

def process_files(start: int, end: int):
    for i in range(start, end + 1):
        print(f"✅ Processing Responses for rule #{i}...")
        responses = generate_responses(i)
        save_responses(i, responses)
        print(f"📁 저장 완료: {OUTPUT_DIR}/chats{i}.txt\n")

if __name__ == "__main__":
    # 👇 여기에서 시작~끝 파일 번호 지정 (예: 22~23)
    start_file = 5
    end_file = 50

    process_files(start=start_file, end=end_file)