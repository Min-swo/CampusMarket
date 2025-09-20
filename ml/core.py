import os
import numpy as np
import torch

from openai import OpenAI

OPEN_API_KEY = ""

llm_model = "gpt-4o-mini"


def make_prompt(chat, ref_docs):
    prompt = f"""
            [시스템]
            - 너는 중고거래 안전 심사관이다. 아래 '사기유형 핸드북'를 기준으로 대화를 평가하라.

            [규칙]
            - 다중 라벨 허용. exclude 신호에 해당하면 제외.
            - 출력은 반드시 JSON 한 줄만:

            [출력]
            {{
                "risk": "low | medium | high",
                "labels": ["EXT_MESSENGER", "PREPAY"],
                "rationale": "한두 문장 요약 근거",
                "evidence": ["매칭 문구 또는 URL/계좌 등"],
                "actions": ["사용자에게 보여줄 권고/경고"]
            }}
            
            
            [사기 유형 핸드북]
            {ref_docs}

            [입력 대화]
            {chat}
    """
    
    return prompt.strip()

def llm_request(model_name, prompt, max_tokens=150):
    try:
        client = OpenAI(
            api_key=OPEN_API_KEY,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling model {model_name}: {e}")
        return ""