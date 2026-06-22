import Image from 'next/image';

type publisherType = {
  id: number;
  image: string;
};
const localPublishers: publisherType[] = [
  {
    id: 1,
    image: '/publishers/local/business-daily-africa.jpeg',
  },
  {
    id: 2,
    image: '/publishers/local/capital-fm-kenya-logo.png',
  },
  {
    id: 3,
    image: '/publishers/local/Citizen-TV-DIgital.png',
  },
  {
    id: 4,
    image: '/publishers/local/cropped-Nyakundi-LOGO-2.webp',
  },
  {
    id: 6,
    image: '/publishers/local/ghafla.png',
  },
  {
    id: 7,
    image: '/publishers/local/Majira.jpeg',
  },
  {
    id: 8,
    image: '/publishers/local/Mpasho.png',
  },
  {
    id: 9,
    image: '/publishers/local/Nairobi wire.png',
  },
  {
    id: 10,
    image: '/publishers/local/nation.png',
  },
  {
    id: 11,
    image: '/publishers/local/NTV_(Kenya)_logo.png',
  },
  {
    id: 12,
    image: '/publishers/local/Radio Kenya.png',
  },
  {
    id: 13,
    image: '/publishers/local/Standard Media logo.png',
  },
  {
    id: 14,
    image: '/publishers/local/Switch tv.png',
  },
  {
    id: 15,
    image: '/publishers/local/The-Star-Kenya-logo.png',
  },
  {
    id: 17,
    image: '/publishers/local/Tuko.png',
  },
];

const internationalPublishers: publisherType[] = [
  {
    id: 12,
    image: '/publishers/International/mirror-logo.png',
  },
  {
    id: 13,
    image: '/publishers/International/NYP_New_York_Post_logo_.png',
  },
  {
    id: 15,
    image: '/publishers/International/Poki.png',
  },
  {
    id: 2,
    image: '/publishers/International/BBC_Logo.svg',
  },
  {
    id: 17,
    image: '/publishers/International/Sky Sports.png',
  },
  {
    id: 1,
    image: '/publishers/International/9gag.png',
  },
  {
    id: 3,
    image: '/publishers/International/BBC_Sport.png',
  },
  {
    id: 4,
    image: '/publishers/International/BlueStacks_Logo.png',
  },
  {
    id: 6,
    image: '/publishers/International/Britannica-Logo.png',
  },
  {
    id: 8,
    image: '/publishers/International/Dailymotion_logo.svg',
  },
  {
    id: 10,
    image: '/publishers/International/Foxnews.png',
  },
  {
    id: 11,
    image: '/publishers/International/goal.com.svg',
  },
  {
    id: 18,
    image: '/publishers/International/Soccerway_logo.svg.png',
  },
  {
    id: 19,
    image: '/publishers/International/Sofascore_Logo_full.png',
  },
  {
    id: 16,
    image: '/publishers/local/TrueCaller_Logo.png',
  },
  {
    id: 20,
    image: '/publishers/International/Sport logo.png',
  },
  {
    id: 21,
    image: '/publishers/International/Sudoku.png',
  },
  {
    id: 22,
    image: '/publishers/International/Tubidy_Logo.svg.png',
  },
  {
    id: 23,
    image: '/publishers/International/The_Weather_Channel_logo.png',
  },
  {
    id: 17,
    image: '/publishers/International/Yahoo-Mail.png',
  },
  {
    id: 16,
    image: '/publishers/International/Logo-teleloisirs.jpg',
  },
  {
    id: 24,
    image: '/publishers/International/yahoo.png',
  },
  {
    id: 7,
    image: '/publishers/International/CNN.png',
  },
];

const Publishers = () => {
  return (
    <>
      <div className="bg-white py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-center text-[#094C95] sm:text-4xl mb-10">
            Local Publishers
          </h2>
          <div className="mx-auto mt-10 grid max-w-lg grid-cols-4 items-center gap-x-8 gap-y-10 sm:max-w-xl sm:grid-cols-6 sm:gap-x-10 lg:mx-0 lg:max-w-none lg:grid-cols-5">
            {localPublishers?.map((item: publisherType) => (
              <Image
                key={item.id}
                alt="Transistor"
                src={item.image}
                width={100}
                height={100}
                className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
              />
            ))}
          </div>
        </div>
        <div className="mx-auto max-w-7xl px-6 lg:px-8 mt-24">
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-center text-[#094C95] sm:text-4xl mb-10">
            International Publishers
          </h2>
          <div className="mx-auto mt-10 grid max-w-lg grid-cols-4 items-center gap-x-8 gap-y-10 sm:max-w-xl sm:grid-cols-6 sm:gap-x-10 lg:mx-0 lg:max-w-none lg:grid-cols-5">
            {internationalPublishers?.map((item: publisherType) => (
              <Image
                key={item.id}
                alt="Transistor"
                src={item.image}
                width={100}
                height={100}
                className="col-span-2 max-h-12 w-full object-contain lg:col-span-1"
              />
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default Publishers;
