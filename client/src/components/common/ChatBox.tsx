import { Card, CardContent } from '@/components/ui/card';
import type { PropsWithChildren } from 'react';

type Props = {
  type: '0' | '1';
};

export function ChatBox({ type, children }: PropsWithChildren<Props>) {
  return (
    <Card
      className={`w-fit max-w-2/3 bg-gray-800 text-white text-left ${type == '0' && ' ml-auto bg-green-600'}`}
    >
      <CardContent>{children}</CardContent>
    </Card>
  );
}
