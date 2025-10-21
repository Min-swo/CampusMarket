from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from classifier import classify_chat  # 네 파일에서 함수 가져오기
import uvicorn

app = FastAPI(title="Chat Fraud Classifier API")

# ===== 데이터 모델 정의 =====
class ChatMessage(BaseModel):
    id: int
    sender_id: str
    content: str
    timestamp: str

class ChatLog(BaseModel):
    chat_room_id: str = "test_room"
    messages: List[ChatMessage]

# ===== 엔드포인트 =====
@app.post("/classify")
async def classify_chat_log(chat_log: ChatLog):
    # JSON 변환
    chat_json = chat_log.dict()
    result = classify_chat(chat_json)
    return result

# ===== 로컬 실행 =====
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
