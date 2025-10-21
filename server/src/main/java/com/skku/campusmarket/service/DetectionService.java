package com.skku.campusmarket.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.skku.campusmarket.dto.request.DetectionRequest;
import com.skku.campusmarket.dto.response.DetectionResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class DetectionService {

    private final RestTemplate restTemplate;
    private static final String FASTAPI_URL = "http://localhost:8000/classify";

    private String translateFraudType(String code) {
        return switch (code) {
            case "EXT_MESSENGER" -> "외부 메신저 유도";
            case "PREPAY" -> "선입금 유도";
            case "FAKE_ESCROW" -> "가짜 에스크로 유도";
            case "FAKE_ITEM_OR_NO_SHIP" -> "허위 상품 또는 미발송";
            case "WRONG_ITEM_OR_QUALITY" -> "상품 불일치 또는 불량";
            case "COUNTERFEIT" -> "위조품 판매";
            case "THIRD_PARTY_MEDIATION" -> "제3자 중개 사기";
            case "ID_OR_ACCOUNT_FRAUD" -> "계정 또는 신분 도용";
            case "PRESSURE_OR_URGENCY" -> "압박·긴급성 유도";
            case "NORMAL" -> "정상 거래";
            default -> "기타";
        };
    }

    public ResponseEntity<DetectionResponse> detectFraud(DetectionRequest detectionRequest) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<DetectionRequest> entity = new HttpEntity<>(detectionRequest, headers);

            System.out.println("==== Sending to FastAPI ====");
            System.out.println(new ObjectMapper().writeValueAsString(detectionRequest));

            ResponseEntity<String> response =
                    restTemplate.postForEntity(FASTAPI_URL, entity, String.class);

            System.out.println("==== FastAPI Response ====");
            System.out.println(response.getBody());

            ObjectMapper mapper = new ObjectMapper();
            JsonNode jsonNode = mapper.readTree(response.getBody());

            String chatRoomId = jsonNode.get("chat_room_id").asText();
            String fraudType = jsonNode.get("fraud_type").asText();
            String fraudTypeKor = translateFraudType(fraudType);
            String rationale = jsonNode.get("rationale").asText();

            // evidence + actions 병합
            StringBuilder resultBuilder = new StringBuilder();

            resultBuilder.append("판단 근거:\n")
                    .append("- ").append(rationale).append("\n");

            JsonNode evidenceArray = jsonNode.withArray("evidence");
            if (evidenceArray.isArray() && evidenceArray.size() > 0) {
                resultBuilder.append("\n증거:\n");
                for (JsonNode e : evidenceArray) {
                    resultBuilder.append("- ").append(e.asText()).append("\n");
                }
            }

            JsonNode actionsArray = jsonNode.withArray("actions");
            if (actionsArray.isArray() && actionsArray.size() > 0) {
                resultBuilder.append("\n권장 행동:\n");
                for (JsonNode a : actionsArray) {
                    resultBuilder.append("- ").append(a.asText()).append("\n");
                }
            }

            DetectionResponse detectionResponse = new DetectionResponse();
            detectionResponse.setChat_room_id(chatRoomId);
            detectionResponse.setFraud_type(fraudTypeKor);
            detectionResponse.setResult(resultBuilder.toString());

            return ResponseEntity.ok(detectionResponse);

        } catch (Exception e) {
            e.printStackTrace();
            DetectionResponse error = new DetectionResponse();
            error.setChat_room_id("unknown");
            error.setFraud_type("ERROR");
            error.setResult("FastAPI 서버 호출 실패: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}

