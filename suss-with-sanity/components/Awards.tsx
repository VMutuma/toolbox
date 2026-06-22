import Image from 'next/image';
import Link from 'next/link';

interface Award {
  title: string;
  subtitle: string;
  image: string;
  url?: string;
}

const awards: Award[] = [
  {
    title: 'MSK Awards',
    subtitle: 'Best Agency of the Year Award (Winner)',
    image: '/awards/Trophy 1.png',
    url: '',
  },
  {
    title: 'MSK Awards',
    subtitle: 'Best Media Innovation of the Year (Winner)',
    image: '/awards/Trophy 2.png',
    url: '',
  },
  {
    title: 'SOMA',
    subtitle: 'Top 25 Men in Digital - Dennis Maina, Suss Ads Founder',
    image: '/awards/image 26.png',
    url: 'https://www.soma.co.ke/men/23_men_recognition.php#',
  },
];

const AwardsSection = () => {
  return (
    <div className="bg-white py-16 sm:py-24 text-center">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-xl">
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-[#094C95] sm:text-4xl">
            Awards
          </h2>
        </div>
        <div className="mx-auto mt-10 flow-root max-w-2xl sm:mt-16 lg:mx-0 lg:max-w-none">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {awards.map((award, index) =>
              award.url ? (
                <Link
                  target="_blank"
                  href={award.url}
                  key={index}
                  className="flex flex-col items-center text-center pl-6 pr-6 pt-10 pb-10 border rounded-lg hover:shadow-lg transition-shadow"
                >
                  <AwardContent award={award} />
                </Link>
              ) : (
                <div
                  key={index}
                  className="flex flex-col items-center text-center pl-6 pr-6 pt-10 pb-10 border rounded-lg hover:shadow-lg transition-shadow"
                >
                  <AwardContent award={award} />
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

interface AwardContentProps {
  award: Award;
}

const AwardContent: React.FC<AwardContentProps> = ({ award }) => (
  <>
    <div className="flex items-center justify-center h-40 w-full mb-4 overflow-hidden">
      <Image
        height={1000}
        width={1000}
        src={award.image}
        alt="Trophy Icon"
        className="max-h-full max-w-full object-contain"
      />
    </div>
    <div className="flex flex-col items-center">
      <p className="font-bold text-lg sm:text-xl">{award.title}</p>
      <p className="text-gray-500 text-sm sm:text-base">{award.subtitle}</p>
    </div>
  </>
);

export default AwardsSection;
