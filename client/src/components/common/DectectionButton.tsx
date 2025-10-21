'use client';

import { postDetection } from '@/api/detection';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { Button } from '@/components/ui/button';
import type { DetectionResponse } from '@/types/detection';
import { useState } from 'react';
import type { ChatLog } from './ChatScrollArea';

type Props = {
  chatLog: ChatLog;
};

export function DectectionButton({ chatLog }: Props) {
  const [res, setRes] = useState<DetectionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const onClickAction = async (chatLog: ChatLog) => {
    try {
      setLoading(true);

      const tmp = await postDetection({
        chat_room_id: 'room1',
        messages: chatLog,
      });
      setRes(tmp);

      console.log('응답 결과:', tmp);
    } catch (err) {
      console.error('요청 실패:', err);
    } finally {
      setLoading(false);
    }
  };

  const onClickClearAction = () => setRes(null);

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button size='sm' variant='skku' onClick={() => onClickAction(chatLog)}>
          AI 검사
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        {loading ? (
          <>
            <AlertDialogHeader>
              <AlertDialogTitle>검사중...</AlertDialogTitle>
            </AlertDialogHeader>
          </>
        ) : (
          <>
            <AlertDialogHeader>
              <AlertDialogTitle>검사 결과</AlertDialogTitle>
              <AlertDialogDescription>
                <p className='text-xl font-extrabold text-red-500'>
                  {res?.fraud_type}
                </p>
              </AlertDialogDescription>
              <AlertDialogDescription>
                <p className='whitespace-pre-wrap'>{res?.result}</p>
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogAction onClick={onClickClearAction}>
                확인
              </AlertDialogAction>
            </AlertDialogFooter>
          </>
        )}
      </AlertDialogContent>
    </AlertDialog>
  );
}
