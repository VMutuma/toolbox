import CardGrid from '@/components/reuseablesection/CardGrid';
import { Metadata } from 'next';
import Image from 'next/image';
const cards = [
  {
    name: 'Digital Listening',
    description:
      'We track online conversations to understand your brand, product, campaign, and team impact.',
    backgroundColor: 'bg-[#D8F1FB]',
  },
  {
    name: 'Hashtag Tracking',
    description:
      'Our method provides detailed insights to compare campaign and hashtag effectiveness.',
    backgroundColor: 'bg-[#CFE8D9]',
  },
  {
    name: 'Crisis Tracking',
    description:
      'We track crises and instantly share relevant info with your team or clients, creating post-crisis reports.',
    backgroundColor: 'bg-[#FFF3CF]',
  },
  {
    name: 'Social Channels Analytics',
    description:
      'We analyze the performance of your own social channels and benchmark with the competition.',
    backgroundColor: 'bg-[#CFE8D9]',
  },
  {
    name: 'Competitive Intelligence',
    description:
      'Our deep dive approach helps you learn from competitors for optimizing your own strategy.',
    backgroundColor: 'bg-[#FFF3CF]',
  },
  {
    name: 'Campaign Monitoring',
    description:
      'We identify consumer insights to optimize keyword strategy and measure ad campaign performance in real time.',
    backgroundColor: 'bg-[#D8F1FB]',
  },
];
export const metadata: Metadata = {
  title: 'Suss Tracker - Suss Digital',
  description:
    'Stay Ahead with Suss Tracker: Digital Monitoring Solutions for proactive insights. Act in real-time with a smart social media strategy. Navigate the evolving landscape with precision.',
};
export default function page() {
  return (
    <>
      <div className="container mx-auto px-10 sm:px-6 lg:px-8 mt-20 mb-20 max-w-7xl">
        <div className="grid grid-cols-1 xm:grid-cols-1 md:grid-cols-3 gap-4 text-center md:text-left">
          <div className="col-span-1 xm:col-span-1 md:col-span-2 flex flex-col justify-center">
            <div className="inline-flex space-x-6">
              <span className="inline-flex items-center font-normal space-x-2 text-xl leading-6 text-[#3DB8E9]">
                Suss Tracker
              </span>
            </div>
            <h1 className="mt-5 text-3xl xm:text-3xl font-normal tracking-tight text-[#0D4D95] sm:text-5xl">
              Be ahead of the competition and act while the iron is still hot.
            </h1>
          </div>
          <div className="col-span-1 xm:col-span-1 md:ml-20 mt-5 md:mt-0">
            <Image
              src="/images/susstracker/susstrackerhero.svg"
              alt="Suss Tracker Hero"
              width={2432}
              height={1442}
              className="w-auto"
            />
          </div>
        </div>
      </div>
      <CardGrid headerText="Digital Monitoring Solutions" cards={cards} />
    </>
  );
}
