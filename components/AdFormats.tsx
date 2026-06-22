'use client';
import {
  ArrowPathIcon,
  ChatBubbleLeftRightIcon,
  VideoCameraIcon,
} from '@heroicons/react/20/solid';
const features = [
  {
    title: 'Push Notifications',
    href: '#',
    description:
      'Push Notifications Deliver your brand’s message or offer directly to a user’s device, even when they are not browsing.',
    icon: ArrowPathIcon,
    iconForeground: 'text-teal-700',
    iconBackground: 'bg-teal-50',
  },
  {
    title: 'Pop Ads',
    href: '#',
    description:
      'Boost Your Online Presence with Targeted Pop-Up Ads. Drive Conversions and Engagement with Our Services.',
    icon: ArrowPathIcon,
    iconForeground: 'text-purple-700',
    iconBackground: 'bg-purple-50',
  },
  {
    title: 'Native Ads',
    href: '#',
    description:
      'Click with your audience with ads that match the look, feel, and function of the media format where they appear.',
    icon: ArrowPathIcon,
    iconForeground: 'text-sky-700',
    iconBackground: 'bg-sky-50',
  },
  {
    title: 'Interstitial Ads',
    href: '#',
    description:
      'Elevate Your Advertising with Engaging Interstitial Ads. Drive Engagement, Conversions, and Brand Awareness. Interstitial ads are the ultimate way to immediately capture attention.',
    icon: ArrowPathIcon,
    iconForeground: 'text-yellow-700',
    iconBackground: 'bg-yellow-50',
  },
  {
    title: 'SMS Ads',
    href: '#',
    description:
      'We connect brands with customers through an affordable, faster, secure, and reliable messaging solution.',
    icon: ChatBubbleLeftRightIcon,
    iconForeground: 'text-rose-700',
    iconBackground: 'bg-rose-50',
  },
  {
    title: 'Display Ads',
    href: '#',
    description:
      'Elevate Your Advertising with Engaging Display Ads. Drive Brand Awareness, Conversions, and ROI.',
    icon: ArrowPathIcon,
    iconForeground: 'text-indigo-700',
    iconBackground: 'bg-indigo-50',
  },
  {
    title: 'Video Ads',
    href: '#',
    description:
      'Video Ads served on top websites. For example, the Daily Mail, and CNN. Video is definitively one of the most efficient support for digital advertising campaigns. Browse our selection of video in-stream and out-stream ad formats used to drive ad effectiveness. Our aim is to drive engagement with video formats across the web, mobile web, and mobile apps.​',
    icon: VideoCameraIcon,
    iconForeground: 'text-indigo-700',
    iconBackground: 'bg-indigo-50',
  },
];
function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

const AdFormats = () => {
  const isOddNumberOfFeatures = features.length % 3 === 1;

  return (
    <div className="px-4 py-16 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-xl md:px-24 lg:px-8 lg:py-20">
      <div className="max-w-xl mb-10 md:mx-auto sm:text-center lg:max-w-2xl md:mb-12">
        <div>
          <p className="inline-block px-3 py-px mb-4 text-xs font-semibold tracking-wider text-teal-900 uppercase rounded-full bg-teal-accent-400">
            Ad Formats
          </p>
        </div>
        <h2 className="max-w-lg mb-6 font-sans text-3xl font-bold leading-none tracking-tight text-gray-900 sm:text-4xl md:mx-auto">
          <span className="relative inline-block">
            <svg
              viewBox="0 0 52 24"
              fill="currentColor"
              className="absolute top-0 left-0 z-0 hidden w-32 -mt-8 -ml-20 text-blue-gray-100 lg:w-32 lg:-ml-28 lg:-mt-10 sm:block"
            >
              <defs>
                <pattern
                  id="07690130-d013-42bc-83f4-90de7ac68f76"
                  x="0"
                  y="0"
                  width=".135"
                  height=".30"
                >
                  <circle cx="1" cy="1" r=".7" />
                </pattern>
              </defs>
              <rect
                fill="url(#07690130-d013-42bc-83f4-90de7ac68f76)"
                width="52"
                height="24"
              />
            </svg>
            <span className="relative">The</span>
          </span>{' '}
          Reach more Customers with Top Performing Ads Formats
        </h2>
        <p>20 Billion + Monthly Impressions across Africa</p>
      </div>
      <div className="px-4 py-16 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-xl md:px-24 lg:px-8 lg:py-20">
        <div className="grid gap-8 row-gap-5 lg:grid-cols-3">
          {features.map((feature, featureIdx) => (
            <div
              key={feature.title}
              className={classNames(
                isOddNumberOfFeatures && features.length - 1 === featureIdx
                  ? 'sm:col-span-3'
                  : 'sm:col-span-1',
                featureIdx === 0
                  ? 'rounded-tl-lg rounded-tr-lg sm:rounded-tr-none'
                  : '',
                featureIdx === 1 ? 'sm:rounded-tr-lg' : '',
                featureIdx === features.length - 2 ? 'sm:rounded-bl-lg' : '',
                featureIdx === features.length - 1
                  ? 'rounded-bl-lg rounded-br-lg sm:rounded-bl-none'
                  : '',
                'relative p-px overflow-hidden transition duration-300 transform border rounded shadow-sm hover:scale-105 group hover:shadow-xl'
              )}
            >
              <div className="absolute bottom-0 left-0 w-full h-1 duration-300 origin-left transform scale-x-0 bg-deep-purple-accent-400 group-hover:scale-x-100" />
              <div className="absolute bottom-0 left-0 w-1 h-full duration-300 origin-bottom transform scale-y-0 bg-deep-purple-accent-400 group-hover:scale-y-100" />
              <div className="absolute top-0 left-0 w-full h-1 duration-300 origin-right transform scale-x-0 bg-deep-purple-accent-400 group-hover:scale-x-100" />
              <div className="absolute bottom-0 right-0 w-1 h-full duration-300 origin-top transform scale-y-0 bg-deep-purple-accent-400 group-hover:scale-y-100" />
              <div className="relative p-5 bg-white rounded-sm">
                <div className="flex flex-col mb-2 lg:items-center lg:flex-row">
                  <div className="flex items-center justify-center w-10 h-10 mb-4 mr-2 rounded-full bg-indigo-50 lg:mb-0">
                    <feature.icon
                      className="w-8 h-8 text-deep-purple-accent-400"
                      aria-hidden="true"
                    />
                  </div>
                  <h6 className="font-semibold leading-5">{feature.title}</h6>
                </div>
                <p className="mb-2 text-sm text-gray-900">
                  {feature.description}
                </p>
                {/* <a
                  href="/"
                  aria-label=""
                  className="inline-flex items-center text-sm font-semibold transition-colors duration-200 text-deep-purple-accent-400 hover:text-deep-purple-800"
                >
                  Learn more
                </a> */}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdFormats;
