'use client';
import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';

const features = [
  {
    id: 1,
    description:
      'Our publishers’ engagement policy ensure that your brand is safe from fake news, crime, hate speech.',
    backgroundColor: '#CFDBEA',
  },
  {
    id: 2,
    description:
      'Exclusion of inappropriate content through page, sound and speech check.​',
    backgroundColor: '#CFE8D9',
  },
  {
    id: 3,
    description:
      'Additional brand safety layer available through segment targeting exclusion – crime, hate speech, drugs, arms, etc.',
    backgroundColor: '#FFF3CF',
  },
  {
    id: 4,
    description:
      'Combination of proprietary and on-demand 3rd party activation.',
    backgroundColor: '#D8F1FB',
  },
];

const tabs = [
  { id: 1, name: 'Push Notifications' },
  { id: 2, name: 'Display Ads' },
  { id: 3, name: 'Interstitial Ads' },
  { id: 4, name: 'Pop  Ads' },
  { id: 5, name: 'Native  Ads' },
  { id: 6, name: 'Video  Ads' },
];

const adFormats = [
  {
    id: 1,
    link: '',
    image: '/animatedassets/Push Notifications.gif',
    body: 'Deliver your brand’s message or offer directly to a user’s device, even when they are not browsing. Get special events, find prospects with user activity targeting, send up to 1M messages in less than a minute – the possibilities are limitless.',
  },
  {
    id: 2,
    link: '',
    image: '/animatedassets/Display ads.gif',
    body: 'We provide multiple types of traditional display banner ads, including skyscraper, rectangle and leader board. These ads are versatile and deliver high engagement.​',
  },
  {
    id: 3,
    link: '',
    image: '/animatedassets/Interstitial Ads.gif',
    body: 'Interstitial ads are an ultimate way to immediately capture attention.Take advantage of the vast creative space, direct contact with a user on both desktop and mobile, and an impressive CTR.​',
  },
  {
    id: 4,
    link: '',
    image: '/animatedassets/Pop Ads.gif',
    body: 'Pop ads provide massive reach at the lowest cost along with access to our exclusive inventory of publishers. Get guaranteed visits and generate fast conversions.​',
  },
  {
    id: 5,
    link: '',
    image: '/animatedassets/Native Ads.gif',
    body: 'Click with your audience with ads that match the look, feel, and function of the media format where they appear.​',
  },
  {
    id: 6,
    link: '',
    image: '/animatedassets/Video ads.gif',
    body: 'Video is definitively one of the most efficient support for digital advertising campaigns. ​​',
  },
];
export default function SussAds() {
  const [selectedTab, setSelectedTab] = useState(tabs[0].id);
  function getAdFormat() {
    const format = adFormats.find((format) => format.id === selectedTab);
    return format ?? adFormats[0];
  }
  return (
    <>
      <div className="container mx-auto px-10 sm:px-6 lg:px-8 mt-20 mb-20 max-w-7xl">
        <div className="grid grid-cols-1 xm:grid-cols-1 md:grid-cols-3 gap-4 text-center md:text-left">
          <div className="col-span-1 xm:col-span-1 md:col-span-2 flex flex-col justify-center">
            <div className="inline-flex space-x-6">
              <span className="inline-flex items-center font-normal space-x-2 text-xl leading-6 text-[#3DB8E9]">
                Suss Ads
              </span>
            </div>
            <h1 className="mt-5 text-3xl xm:text-3xl font-normal tracking-tight text-[#0D4D95] sm:text-5xl">
              Africa`s favourite digital platform for Display Ads, Video Ads,
              Native Ads, Push Notification Ads & Interstitial Ads
            </h1>
          </div>
          <div className="col-span-1 xm:col-span-1 md:ml-20 mt-5 md:mt-0">
            <Image
              src="/animatedassets/Products_Suss Ads.gif"
              alt="App screenshot"
              width={2432}
              height={1442}
              className="w-auto"
            />
          </div>
        </div>
      </div>
      <div className="relative isolate overflow-hidden bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl">
            <div className="hidden sm:block">
              <div className="flex space-x-4 mt-20 -mb-32 justify-center">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    className={`text-[#0D4D95] border border-[#3DB8E9] rounded-full hover:text-white hover:bg-[#3DB8E9]  px-3 py-2 text-sm font-medium ${
                      selectedTab === tab.id ? 'bg-[#3DB8E9] text-white' : ''
                    }`}
                    onClick={() => setSelectedTab(tab.id)}
                  >
                    {tab.name}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div className="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-25 lg:flex lg:px-8 lg:py-32">
          <div className="mx-auto mt-16 flex max-w-2xl ">
            <div className="max-w-4xl flex-none sm:max-w-5xl lg:max-w-none">
              <div className="-m-2">
                <Image
                  src={getAdFormat().image}
                  alt="App screenshot"
                  width={2432}
                  height={1442}
                  className="w-auto xm:w-11/12 h-[38rem]"
                />
              </div>
            </div>
          </div>
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
            <p className="mt-52 text-xl font-normal leading-8 text-black">
              {getAdFormat().body}
            </p>
            <div className="mt-10 flex items-center gap-x-6">
              <Link
                // href={getAdFormat().link}
                href="/bookdemo"
                className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
              >
                Advertise Now
              </Link>
            </div>
          </div>
        </div>
      </div>
      <div className="bg-[#F9FAFB] py-24 sm:py-32 xm:text-center">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl md:text-center lg:text-center">
            <p className="mt-2 text-5xl xm:text-4xl font-bold tracking-tight text-sussBlue sm:text-4xl">
              Run your ads only in BRAND SAFE places
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-4 gap-y-5 lg:max-w-none lg:grid-cols-2">
              {features.map((feature) => (
                <div
                  key={feature.id}
                  className={`flex flex-col border border-gray-300 bg-[${feature.backgroundColor}] px-4 py-8 sm:px-12 rounded-lg shadow-sm hover:shadow-lg`}
                >
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-black">
                    <p className="flex-auto">{feature.description}</p>
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </>
  );
}
