import { ScrollArea } from '@/components/ui/scroll-area';
import { Fragment } from 'react/jsx-runtime';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { ChatBox } from './ChatBox';

type ChatMessage = {
  id: string;
  sender: 'me' | 'other'; // 내가 보낸 건 "me", 상대방은 "other"
  content: string; // 메시지 내용
  timestamp: Date; // 보낸 시간
};

type ChatLog = ChatMessage[];

const chatLog: ChatLog = [
  {
    id: '1',
    sender: 'me',
    content: '안녕? 오늘 저녁에 뭐해?',
    timestamp: new Date('2025-09-20T18:45:00'),
  },
  {
    id: '2',
    sender: 'other',
    content: '오 안녕! 저녁에 영화 보러 갈래?',
    timestamp: new Date('2025-09-20T18:46:00'),
  },
  {
    id: '3',
    sender: 'me',
    content: '좋지! 무슨 영화 볼까?',
    timestamp: new Date('2025-09-20T18:47:00'),
  },
  {
    id: '4',
    sender: 'other',
    content: '코미디 어때? 요즘 스트레스 많잖아 ㅋㅋ',
    timestamp: new Date('2025-09-20T18:48:00'),
  },
  {
    id: '5',
    sender: 'me',
    content: '완전 좋아 😂 예매는 내가 할게!',
    timestamp: new Date('2025-09-20T18:49:00'),
  },
];

export function ChatScrollArea() {
  return (
    <div className='flex flex-col bg-gray-50'>
      <section className='flex justify-between items-center p-4 pb-3 px-5  rounded-t-md border-2 bg-gray-100'>
        <h4 className='text-md font-medium  w-full'>채팅</h4>
        <Button size='sm' variant='skku'>
          AI 검사
        </Button>
      </section>
      <ScrollArea className='h-156 w-128 border-2 border-y-0'>
        <div className='px-4 py-3 space-y-3'>
          {chatLog.map(({ id, sender, content }) => (
            <Fragment key={id}>
              <ChatBox type={sender}>
                <div className='text-sm'>{content}</div>
              </ChatBox>
            </Fragment>
          ))}
        </div>
      </ScrollArea>
      <section className='flex gap-3 px-3 py-1 pb-4 rounded-b-md border-2 border-t-0'>
        <Input className='w-full self-center border-2 bg-white'></Input>
        <Button variant='skku'>전송</Button>
      </section>
    </div>
  );
}
