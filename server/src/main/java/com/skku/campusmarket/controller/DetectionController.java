package com.skku.campusmarket.controller;

import com.skku.campusmarket.dto.request.DetectionRequest;
import com.skku.campusmarket.dto.response.DetectionResponse;
import com.skku.campusmarket.service.DetectionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/detections")
public class DetectionController {
    private final DetectionService detectionService;

    @PostMapping()
    public ResponseEntity<DetectionResponse> postDetection(@RequestBody DetectionRequest request) {
        return detectionService.detectFraud(request);
    }
}
