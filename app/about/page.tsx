import { type Metadata } from 'next';
import Image from 'next/image';

export const metadata: Metadata = {
  title: 'About Us - Suss Digital',
  description:
    "Africa's Top Digital Ads Platform: Display, Video, Native, Push Notification, Interstitial Ads. Propel your brand ahead. Optimize with us for guaranteed visits, fast conversions. Trusted by thousands. Start your successful campaign today.",
};

import Link from 'next/link';
import { MdCampaign } from 'react-icons/md';

const products = [
  {
    title: 'Passion',
    href: '/products/sussads',
    icon: '/images/about/passion.svg',
    backgroundColor: 'bg-[#CFDBEA]',
    iconForeground: 'text-teal-700',
    iconBackground: 'bg-teal-50',
    description:
      'We are committed to providing the best digital marketing solutions for clients, continuously learning and integrating new ideas into our culture.',
  },
  {
    title: 'Commitment',
    href: '/products/susssms',
    icon: '/images/about/commitment.svg',
    backgroundColor: 'bg-[#CFE8D9]',
    iconForeground: 'text-purple-700',
    iconBackground: 'bg-purple-50',
    description:
      'We partner with reputable agencies and parties to increase brand credibility and ensure clients are associated with legitimate data dealers.',
  },
  {
    title: 'Compassion',
    href: '/products/sussagency',
    icon: '/images/about/compassion.svg',
    backgroundColor: 'bg-[#FFF3CF]',
    iconForeground: 'text-sky-700',
    iconBackground: 'bg-sky-50',
    description:
      'For businesses seeking to gain a foothold in the market, partnering with us offers a unique opportunity to achieve outstanding results.',
  },
];
const niches = [
  { name: 'Billion Monthly Impressions', value: '40+' },
  { name: 'Countries', value: '50+' },
  { name: 'Years of Experience', value: '10+' },
  { name: 'Partners', value: '100+' },
];
export default function page() {
  return (
    <>
      <div className="relative bg-[#F9FAFB] max-h-[600px] xm:text-center mb-10">
        <div className="mx-auto max-w-7xl lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">
          <div className="px-6 pb-24 pt-10 sm:pb-32 lg:col-span-7 xm:mb-5 lg:px-0 lg:pb-56 lg:pt-48 xl:col-span-6">
            <div className="mx-auto max-w-2xl lg:mx-0">
              <h1 className="mt-24 text-4xl font-bold tracking-tight text-[#0D4D95] sm:mt-10 sm:text-6xl leading-10">
                We are a <span className="text-[#09A8E1]">tech enabled</span>{' '}
                limitless center of innovation, we serve the world`s best loved
                brands.
              </h1>
            </div>
          </div>
          <div className="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0">
            <Image
              width={2432}
              height={1442}
              className="aspect-[3/2] xm:h-[370px] xm:-mt-28 xm:w-full w-[804px] h-full bg-gray-50 object-fit lg:absolute lg:inset-0 lg:aspect-auto lg:h-full"
              src="/animatedassets/About us V1.gif"
              alt="Suss About Page Hero Image"
            />
          </div>
        </div>
      </div>
      <div className="relative isolate overflow-hidden bg-white py-24 sm:py-32 text-center">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto lg:mx-0 max-w-1xl">
            <h2 className="text-4xl text-[#0D4D95] font-bold tracking-tight sm:text-6xl">
              Empowering Ads Through
              <br /> Innovative Excellence
            </h2>
            <p className="mt-6 text-[#0D4D95] text-lg leading-8">
              We use advanced tools, tech, and a skilled team to collaborate
              closely with <br /> clients for seamless integration, empowering
              businesses to achieve goals.
            </p>
          </div>
          <div className="mx-auto mt-10 lg:mx-0 lg:max-w-none">
            <dl className="mt-16 grid grid-cols-1 gap-8 sm:mt-20 sm:grid-cols-2 lg:grid-cols-4">
              {niches.map((niche) => (
                <div key={niche.name} className="flex flex-col-reverse">
                  <dt className="text-base leading-7 text-[#3DB8E9]">
                    {niche.name}
                  </dt>
                  <dd className="text-2xl font-bold leading-9 tracking-tight text-[#3DB8E9]">
                    {niche.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
      <div className="bg-[#F9FAFB] py-24 sm:py-32 xm:text-center">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 text-center">
          <div className="mx-auto max-w-2xl mb-6 lg:text-center">
            <h2 className="leading-7 mt-2 text-3xl font-bold tracking-tight leading-10  text-sussBlue sm:text-4xl">
              We Offer a Niche Clientele
              <br /> With 360° Services
            </h2>
          </div>
          <div className="divide-y divide-gray-200 overflow-hidden rounded-lg sm:grid sm:grid-cols-1 text-center">
            {products.map((product) => (
              <div
                key={product.title}
                className={`group  xm:w-auto relative ${product.backgroundColor} rounded-3xl justify-start items-start	m-3 p-6 focus-within:ring-2 shadow hover:shadow-lg`}
                style={{ display: 'flex', flexDirection: 'column' }}
              >
                <div className="mt-8 mb-5">
                  <h3 className="text-2xl font-semibold leading-6 text-sussBlue flex flex-row xm:justify-center">
                    <Image
                      src={product.icon}
                      width={200}
                      height={200}
                      className="h-7 w-7 text-center mr-2"
                      aria-hidden="true"
                      alt={product.title}
                    />
                    {product.title}
                  </h3>
                  <p className="mt-3 ml-10 text text-base text-black">
                    {product.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="mx-auto mt-10 mb-20 text-center max-w-2xl lg:text-center sm:mt-20 lg:mt-24">
            <Link
              href="/bookdemo"
              className="bg-sussYellow border text-sm font-light rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
            >
              Advertise Now
              <MdCampaign className="h-6 w-6 ml-2" />
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
