import Image from 'next/image';
import Link from 'next/link';
import { Button } from '../buttons/Button';

export default function NewHero() {
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 mt-10 mb-10 md:h-[600px] max-w-8xl flex items-center">
      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 gap-4 text-center md:text-left">
        <div className="col-span-1 sm:col-span-1 md:col-span-2 flex flex-col justify-center max-w-[800px] mx-4 sm:mx-0 md:ml-32">
          <h1 className="mt-5 text-4xl sm:text-5xl md:text-6xl font-light tracking-normal text-sussBlue">
            We’re changing the way brands{' '}
            <span className="text-customBlue font-bold italic">
              Boost Their Online
            </span>{' '}
            Presence In Africa.
          </h1>
          <p className="mt-6 text-lg font-normal sm:text-xl md:text-2xl tracking-normal leading-8">
            Unlocking Africa’s Advertising Potential: Your Premier Destination
            for Display, Video, Native, Push, and Interstitial Ads! 🚀
          </p>
          <div className="mt-10 flex flex-col items-center sm:flex-row sm:items-center sm:justify-start">
            <Link
              className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white px-5 py-2.5 text-center mb-4 sm:mb-0 sm:mr-4 sm:inline-flex items-center hover:shadow-lg"
              // href="mailto:info@suss.co.ke?subject=Book%20Demo&body=Hello%20Suss%20Ads%20Team,%0D%0A%0D%0AI%20am%20interested%20in%20booking%20a%20demo%20of%20your%20services.%20Could%20you%20please%20schedule%20a%20demo%20for%20me%20at%20your%20earliest%20convenience?%0D%0A%0D%0AThank%20you.%0D%0A%0D%0AKind%20regards,"
              href="/bookdemo"
            >
              Book Demo
            </Link>
            <Button
              href="https://www.youtube.com/watch?v=SVevoFMPFSI"
              variant="outline"
              className="border border-sussBlue text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
            >
              <svg
                aria-hidden="true"
                className="h-3 w-3 flex-none fill-blue-600 group-active:fill-current"
              >
                <path d="m9.997 6.91-7.583 3.447A1 1 0 0 1 1 9.447V2.553a1 1 0 0 1 1.414-.91L9.997 5.09c.782.355.782 1.465 0 1.82Z" />
              </svg>
              <span className="ml-3">Watch video</span>
            </Button>
          </div>
        </div>
        <div className="col-span-1">
          <Image
            src="/animatedassets/Homepage.gif"
            alt="Suss Hero"
            width={2432}
            height={1442}
            className="w-full h-[20rem] sm:w-auto"
          />
        </div>
      </div>
    </div>
  );
}
