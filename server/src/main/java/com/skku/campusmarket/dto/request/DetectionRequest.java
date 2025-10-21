package com.skku.campusmarket.dto.request;

import com.skku.campusmarket.dto.ChatMessageDto;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class  DetectionRequest {
    private String chat_room_id;
    private List<ChatMessageDto> messages;
}
