import { UsersIcon } from '@heroicons/react/24/outline';
import { FcAdvertising } from 'react-icons/fc';
import { MdOutlineSms } from 'react-icons/md';
import { TbBrandGoogleAnalytics } from 'react-icons/tb';

const products = [
  {
    title: 'Suss Ads',
    href: '/products/sussads',
    icon: FcAdvertising,
    backgroundColor: 'bg-[#CFDBEA]',
    iconForeground: 'text-teal-700',
    iconBackground: 'bg-teal-50',
    description:
      'Africas favourite digital platform for Display Ads, Video Ads, Native Ads, Push Notification Ads & Interstitial Ads',
  },
  {
    title: 'Suss SMS',
    href: '/products/susssms',
    icon: MdOutlineSms,
    backgroundColor: 'bg-[#CFE8D9]',
    iconForeground: 'text-purple-700',
    iconBackground: 'bg-purple-50',
    description:
      'We connect brands with customers through an affordable, faster, secure, and reliable messaging solution.',
  },
  {
    title: 'Suss Agency',
    href: '',
    // href: '/products/sussagency',
    icon: UsersIcon,
    backgroundColor: 'bg-[#FFF3CF]',
    iconForeground: 'text-sky-700',
    iconBackground: 'bg-sky-50',
    description:
      'Increases your sales and leads ultimately giving you not less than 100% return on investment on your digital marketing investment.',
  },
  {
    title: 'Suss Tracker',
    href: '',
    // href: '/products/susstracker',
    icon: TbBrandGoogleAnalytics,
    backgroundColor: 'bg-[#D8F1FB]',
    iconForeground: 'text-yellow-700',
    iconBackground: 'bg-yellow-50',
    description: 'Connect with third-party tools',
  },
];
export default function OurProducts() {
  return (
    <div className="bg-white py-16 sm:py-24 xm:text-center">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl mb-6 lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">
            Our Products
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Our Products
          </p>
          <p className="mt-3 text-lg leading-8 text-gray-600">
            Innovative smart marketing
          </p>
        </div>
        <div className="divide-y divide-gray-200 overflow-hidden rounded-lg sm:grid sm:grid-cols-4 sm:gap-px sm:divide-y-0">
          {products.map((product) => (
            <a
              href={product.href}
              key={product.title}
              className={`group w-[270px] xm:w-auto relative ${product.backgroundColor} rounded-3xl	 m-3 p-6 focus-within:ring-2 shadow hover:shadow-lg`}
              style={{ display: 'flex', flexDirection: 'column' }}
            >
              <div className="mt-8 mb-5">
                <h3 className="text-2xl font-semibold leading-6 text-[#094C95] flex flex-row xm:justify-center">
                  <span className="absolute inset-0" aria-hidden="true" />
                  <product.icon className="h-6 w-6 mr-2" aria-hidden="true" />
                  {product.title}
                </h3>
                <p className="mt-3 text-base text-black">
                  {product.description}
                </p>
              </div>
              <div className="mt-auto text-center">
                <button className="text-sm font-semibold border border-sussBlue rounded-full text-sussBlue hover:bg-white px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg">
                  Learn More
                </button>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
