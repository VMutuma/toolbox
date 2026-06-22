import Link from 'next/link';
import { BsClipboard2DataFill } from 'react-icons/bs';
import { FaPeopleCarry } from 'react-icons/fa';
import { GiOnTarget } from 'react-icons/gi';
import { MdCampaign } from 'react-icons/md';

const features = [
  {
    name: 'Precision Targeting Tactics',
    description:
      'Our DIRECT DIGITAL MARKETING SOLUTIONS and PRECISION TARGETING TACTICS will help you achieve this in a cost-efficient way.​',
    href: '#',
    icon: GiOnTarget,
  },
  {
    name: 'Guaranteed Ad Placement',
    description:
      'We GUARANTEE AD PLACEMENT within safe and suitable environments.​',
    href: '#',
    icon: MdCampaign,
  },
  {
    name: 'Collaboration',
    description:
      'We work COLLABORATIVELY with you to adapt content specifically to channel & audience segments.',
    href: '#',
    icon: FaPeopleCarry,
  },
  {
    name: 'Relevant Data',
    description:
      'We utilize the MOST RELEVANT data to personalize & optimize campaign delivery.',
    href: '#',
    icon: BsClipboard2DataFill,
  },
];

export default function AboutSection() {
  return (
    <div className="bg-sussBg py-16 sm:py-24 xm:text-center">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl md:text-center lg:text-center">
          <p className="mt-2 text-5xl xm:text-4xl font-bold tracking-tight text-sussBlue sm:text-4xl">
            Perfect Solution For Your Business
          </p>
          <p className="mt-6 text-xl xm:text-xl leading-8 text-sussBlue">
            We are an integrated DIGITAL MARKETING and COMMUNICATION platform
            with a vast reach in the African region. We enable you to ENGAGE
            with your audience at the RIGHT TIME and on the RIGHT AD PLACEMENTS.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-4 gap-y-5 lg:max-w-none lg:grid-cols-2">
            {features.map((feature) => (
              <div
                key={feature.name}
                className="flex flex-col border border-gray-300 bg-white px-4 py-12 sm:px-12 rounded-lg shadow-sm hover:shadow-lg"
              >
                <dt className="flex items-center gap-x-3 text-xl font-semibold leading-7 text-customBlue">
                  <feature.icon
                    className="h-7 w-7 flex-none text-customBlue"
                    aria-hidden="true"
                  />
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-black">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </div>
            ))}
          </dl>
        </div>
        <div className="mx-auto mt-10 text-center max-w-2xl lg:text-center sm:mt-20 lg:mt-24">
          <Link
            href="/bookdemo"
            className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
          >
            Advertise Now
            <MdCampaign className="h-6 w-6 ml-2" />
          </Link>
        </div>
      </div>
    </div>
  );
}
