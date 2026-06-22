import Image from 'next/image';
import Link from 'next/link';

const casestudies = [
  {
    id: 1,
    description:
      'Our DIRECT DIGITAL MARKETING SOLUTIONS and PRECISION TARGETING TACTICS will help you achieve this in a cost-efficient way.​',
    href: '/work/nivea',
    image: '/images/casestudies/NiveaCaseStudy.svg',
  },
  {
    id: 2,
    description:
      'We GUARANTEE AD PLACEMENT within safe and suitable environments.​',
    href: '/work/betika',
    image: '/images/casestudies/BetikaCaseStudy.svg',
  },
  {
    id: 3,
    description:
      'We work COLLABORATIVELY with you to adapt content specifically to channel & audience segments.',
    href: '/work/tingatinga',
    image: '/images/casestudies/TingaTingaCaseStudy.svg',
  },
  {
    id: 4,
    description:
      'We utilize the MOST RELEVANT data to personalize & optimize campaign delivery.',
    href: '/work/kra',
    image: '/images/casestudies/KRACaseStudy.svg',
  },
];

export default function CaseStudies() {
  return (
    <div className="bg-white py-16 sm:py-24 xm:text-center">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl md:text-center lg:text-center">
          <h2 className="text-5xl xm:text-5xl font-normal leading-10 text-center tracking-tight text-[#0D4D95] sm:text-6xl">
            Case Studies
          </h2>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-4 gap-y-5 lg:max-w-none lg:grid-cols-2">
            {casestudies.map((item) => (
              <Link key={item.id} href={item.href}>
                <Image
                  className="h-auto max-w-full rounded-lg"
                  src={item.image}
                  width={1000}
                  height={1000}
                  alt="Suss Ads"
                />
              </Link>
            ))}
          </dl>
        </div>
        <div className="mx-auto mt-10 text-center max-w-2xl lg:text-center sm:mt-20 lg:mt-24">
          <Link
            href="/work"
            className="w-32 text-base font-semibold rounded-full bg:white text-sussBlue text-center shadow-sm hover:bg-white border border-sussBlue px-5 py-2.5  items-center hover:border-sussBlue hover:text-sussBlue hover:shadow-xl"
          >
            View More
          </Link>
        </div>
      </div>
    </div>
  );
}
