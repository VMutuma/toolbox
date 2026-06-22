import { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';

const data = [
  {
    id: 1,
    description:
      'We enable effective communication between individuals and organizations (B2B, B2C, and C2C).',
  },
  {
    id: 1,
    description:
      ' We power your marketing with alerts, reminders, and personalized messages for your brand.',
  },
  {
    id: 1,
    description:
      'We offer instant message deliveries to all networks through a customized sender-id.',
  },
];

export const metadata: Metadata = {
  title: 'Suss SMS - Suss Digital',
  description:
    'Empower connections: Suss SMS, your affordable, fast, secure messaging solution. Enhance B2B, B2C, C2C communication. Drive marketing success with instant alerts, reminders, personalized messages, and swift network delivery.',
};

export default function Page() {
  return (
    <>
      <div className="container mx-auto px-10 sm:px-6 lg:px-8 mt-20 mb-20 max-w-7xl">
        <div className="grid grid-cols-1 xm:grid-cols-1 md:grid-cols-3 gap-4 text-center md:text-left">
          <div className="col-span-1 xm:col-span-1 md:col-span-2 flex flex-col justify-center">
            <div className="inline-flex space-x-6">
              <span className="inline-flex items-center font-normal space-x-2 text-xl leading-6 text-[#3DB8E9]">
                Suss Sms
              </span>
            </div>
            <h1 className="mt-5 text-3xl xm:text-3xl font-normal tracking-tight text-[#0D4D95] sm:text-5xl">
              We connect brands with customers through an affordable, faster,
              secure, and reliable messaging solution.
            </h1>
          </div>
          <div className="col-span-1 xm:col-span-1 md:ml-20 mt-5 md:mt-0">
            <Image
              src="/animatedassets/Product_Suss SMS.gif"
              alt="Suss SMS"
              width={1000}
              height={1000}
              className="w-auto"
            />
          </div>
        </div>
      </div>

      <div className="bg-white">
        <div className="container pt-20 mx-auto m-24 max-w-7xl">
          <Image
            src="/images/sms/suss-sms-dashboard.svg"
            alt="Suss SMS Dashboard"
            width={2432}
            height={1442}
          />
          <div className="grid grid-cols-2 md:grid-cols-2 xm:grid-cols-1 gap-4 ml-10 mr-10 mt-14">
            <div className=" aspect-video ">
              <iframe
                className=" h-full w-full rounded-lg"
                src="https://www.youtube.com/embed/cdVW8lyNIoU?si=-HFyuu6pfkkM9x1D"
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              ></iframe>
            </div>

            <div className="justify-center">
              <dl className="max-w-xl space-y-8 text-base leading-7 text-gray-600 lg:max-w-none">
                {data.map((item) => (
                  <div
                    key={item.id}
                    className="relative pl-9 font-normal text-xl text-[#094C95] leading-9"
                  >
                    <dd className="inline"> - {item.description}</dd>
                  </div>
                ))}
              </dl>
              <div className="ml-10 mt-10 xm:text-center">
                <Link
                  className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
                  href="mailto:info@suss.co.ke?subject=Book%20Demo&body=Hello%20Suss%20Ads%20Team,%0D%0A%0D%0AI%20am%20interested%20in%20booking%20a%20demo%20of%20your%20services.%20Could%20you%20please%20schedule%20a%20demo%20for%20me%20at%20your%20earliest%20convenience?%0D%0A%0D%0AThank%20you.%0D%0A%0D%0AKind%20regards,"
                >
                  Book Demo
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
