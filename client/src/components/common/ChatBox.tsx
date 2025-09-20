import { Card, CardContent } from '@/components/ui/card';
import type { PropsWithChildren } from 'react';

type Props = {
  type: 'me' | 'other';
};

export function ChatBox({ type, children }: PropsWithChildren<Props>) {
  return (
    <Card
      className={`w-fit max-w-2/3 bg-gray-800 text-white text-center ${type == 'me' && ' ml-auto bg-green-600'}`}
    >
      <CardContent>{children}</CardContent>
    </Card>
  );
}
