// DetectionResponse.java
package com.skku.campusmarket.dto.response;

import lombok.Data;

@Data
public class DetectionResponse {
    private String chat_room_id;
    private String fraud_type;
    private String result;
}
