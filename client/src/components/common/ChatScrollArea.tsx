import { ScrollArea } from '@/components/ui/scroll-area';
import { chatLogs } from '@/data/chats';
import { Fragment } from 'react/jsx-runtime';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { ChatBox } from './ChatBox';
import { DectectionButton } from './DectectionButton';

type ChatMessage = {
  id: number;
  sender_id: '0' | '1'; // 내가 보낸 건 "me", 상대방은 "other"
  content: string; // 메시지 내용
  timestamp: string; // 보낸 시간
};

export type ChatLog = ChatMessage[];

const chatLog = chatLogs[7];

export function ChatScrollArea() {
  return (
    <div className='flex flex-col bg-gray-50'>
      <section className='flex justify-between items-center p-4 pb-3 px-5  rounded-t-md border-2 bg-gray-100'>
        <h4 className='text-md font-medium  w-full'>채팅</h4>
        <DectectionButton chatLog={chatLog} />
      </section>
      <ScrollArea className='h-156 w-128 border-2 border-y-0'>
        <div className='px-4 py-3 space-y-3'>
          {chatLog.map(({ id, sender_id, content }) => (
            <Fragment key={id}>
              <ChatBox type={sender_id}>
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
