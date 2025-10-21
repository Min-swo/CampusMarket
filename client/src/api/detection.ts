import type { ChatLog } from '@/components/common/ChatScrollArea';
import type { DetectionResponse } from '@/types/detection';
import axios from 'axios';
import { api } from './axios';

export const postDetection = async (
  data: { chat_room_id: string } & { messages: ChatLog }
): Promise<DetectionResponse> => {
  try {
    const response = await api.post('/detections', data);
    return response.data;
  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error('postDetection API 에러 발생:', err.response?.data);
      throw new Error('postDetection API 에러 발생');
    }
    throw err;
  }
};
