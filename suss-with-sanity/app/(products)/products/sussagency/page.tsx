import CaseStudies from '@/components/CaseStudies';
import { Metadata } from 'next';
import Image from 'next/image';

const cards = [
  {
    name: 'Programmatic media buying',
    backgroundColor: 'bg-[#D8F1FB]',
    image: '/images/susstracker/programmatic.svg',
  },
  {
    name: 'Brand Strategy',
    backgroundColor: 'bg-[#CFE8D9]',
    image: '/images/susstracker/brandstrategy.svg',
  },
  {
    name: 'Campaign Measurement',
    backgroundColor: 'bg-[#FFF3CF]',
    image: '/images/susstracker/campaignmeasurement.svg',
  },
  {
    name: 'Dynamic Content development',
    backgroundColor: 'bg-[#CFE8D9]',
    image: '/images/susstracker/dynamiccontentdev.svg',
  },
  {
    name: 'Insight & Analytics',
    backgroundColor: 'bg-[#FFF3CF]',
    image: '/images/susstracker/insightsandanalytics.svg',
  },
  {
    name: 'Performance Marketing',
    backgroundColor: 'bg-[#D8F1FB]',
    image: '/images/susstracker/perfomancemarketting.svg',
  },
];
export const metadata: Metadata = {
  title: 'Suss Agency - Suss Digital',
  description:
    'Maximize ROI with Suss Agency: Proven digital tools, years of experience for increased sales and leads. Online/Offline media strategies, programmatic buying, brand strategy, dynamic content, data analysis - your comprehensive solution.',
};
export default function page() {
  return (
    <>
      <div className="container mx-auto px-10 sm:px-6 lg:px-8 mt-20 mb-20 max-w-7xl">
        <div className="grid grid-cols-1 xm:grid-cols-1 md:grid-cols-3 gap-4 text-center md:text-left">
          <div className="col-span-1 xm:col-span-1 md:col-span-2 flex flex-col justify-center">
            <div className="inline-flex space-x-6">
              <span className="inline-flex items-center font-normal space-x-2 text-xl leading-6 text-[#3DB8E9]">
                Suss Agency
              </span>
            </div>
            <h1 className="mt-5 text-3xl xm:text-3xl font-normal tracking-tight text-[#0D4D95] sm:text-5xl">
              Our digital expertise and experience guarantees 100% return on
              investment.
            </h1>
          </div>
          <div className="col-span-1 xm:col-span-1 md:ml-20 mt-5 md:mt-0">
            <Image
              src="/images/sussAgency/sussagencyhero.svg"
              alt="Suss Agency Hero Image"
              width={2432}
              height={1442}
              className="w-auto"
            />
          </div>
        </div>
      </div>
      <div className="relative isolate overflow-hidden bg-white py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto lg:mx-0">
            <h2 className="text-5xl xm:text-5xl font-normal leading-10 text-center tracking-tight text-[#0D4D95] sm:text-6xl">
              What We Do
            </h2>
          </div>
          <div className="mx-auto mt-16 grid grid-cols-1 gap-6 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-8">
            {cards.map((card) => (
              <div
                key={card.name}
                className={`flex flex-col items-center shadow-sm p-10 border border-#094C95 rounded-lg  md:flex-row md:max-w-xl ${card.backgroundColor}`}
              >
                <div className="flex flex-col justify-between p-4 leading-8">
                  <h5 className="mb-2 text-xl font-semibold tracking-tight text-black">
                    {card.name}
                  </h5>
                </div>
                <Image
                  className="h-20 w-20"
                  src={card.image}
                  alt={card.name}
                  width={1000}
                  height={1000}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
      <CaseStudies />
    </>
  );
}
