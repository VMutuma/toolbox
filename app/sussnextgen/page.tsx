import { type Metadata } from 'next';
import Image from 'next/image';
import { NextGen } from './[slug]/page';
import { urlFor } from '../../sanity/lib/image';
import { client } from '../../sanity/lib/client';

export const metadata: Metadata = {
  title: 'NextGen - Suss',
  description: 'Suss Ads NextGen Program.',
  openGraph: {
    type: 'website',
    title: 'Suss',
    description: 'Suss NextGen',
    locale: 'en_US',
    url: 'https://www.suss.co.ke/sussnextgen',
    siteName: 'Suss',
    images: [
      {
        url: '/suss-logo.png',
        width: 1200,
        height: 630,
        alt: 'Suss',
      },
    ],
  },
  metadataBase: new URL('https://www.suss.co.ke/'),
};
export const revalidate = 30;

const cards = [
  {
    name: 'Empowering Youth with Digital Skills',
    backgroundColor: 'bg-[#D8F1FB]',
    image: '/sussnextgen/EmpoweringYouth.svg',
  },
  {
    name: 'Bridging the Gap Between Academic Learning and Practical Application',
    backgroundColor: 'bg-[#CFE8D9]',
    image: '/images/susstracker/brandstrategy.svg',
  },
  {
    name: 'Supporting Inclusive and Sustainable Economic Growth',
    backgroundColor: 'bg-[#FFF3CF]',
    image: '/images/susstracker/campaignmeasurement.svg',
  },
  {
    name: 'Closing Gaps in Technology Access and Educational Opportunities',
    backgroundColor: 'bg-[#CFE8D9]',
    image: '/sussnextgen/ClosingGap.svg',
  },
  {
    name: 'Encouraging Entrepreneurship and Innovation',
    backgroundColor: 'bg-[#FFF3CF]',
    image: '/images/susstracker/insightsandanalytics.svg',
  },
];

async function getNextGens(): Promise<NextGen[]> {
  const query = `*[_type == "nextgen"] | order(_createdAt desc){
    title,
    slug,
    subtitle,
    image,
  }
`;
  const nextgens = await client.fetch(query);
  return nextgens;
}
const Page = async () => {
  const nextgens = await getNextGens();
  return (
    <>
      <div className="relative bg-[#D3EDF6]">
        <div className="mx-auto max-w-7xl lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">
          <div className="px-6 pb-24 pt-10 sm:pb-32 lg:col-span-7 lg:px-0 lg:pb-56 lg:pt-48 xl:col-span-6">
            <div className="mx-auto max-w-2xl lg:mx-0 text-center">
              <h1 className="mt-24 text-4xl font-bold tracking-tight text-sussBlue sm:mt-10 sm:text-6xl">
                Empowering Generations
              </h1>
            </div>
          </div>
          <div className="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0 my-10">
            <Image
              width={50}
              height={80}
              alt="Suss Next Gen"
              src="/sussnextgen/SussNextGenHero.svg"
              className="aspect-[3/2] w-auto bg-[#D3EDF6] object-cover lg:absolute lg:inset-0 lg:aspect-auto lg:h-full"
            />
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="flex flex-col items-center justify-center p-8">
        <div className="container max-w-7xl">
          <div className="flex flex-col sm:flex-col md:flex-row items-center md:space-x-8 my-10 sm:my-20">
            <div className="w-full md:w-1/2 flex justify-center min-h-[300px] sm:min-h-[400px] lg:min-h-[500px]">
              <Image
                width={500}
                height={500}
                src="/sussnextgen/AboutSussNextGen.svg"
                alt="Laptop Typing"
                className="rounded-lg max-w-full bg-[#D3EDF6] h-auto object-cover"
              />
            </div>
            <div className="w-full md:w-1/2 text-center md:text-left mt-6 sm:mt-0">
              <h2 className="text-3xl md:text-4xl font-bold text-sussBlue mb-4">
                About The Program
              </h2>
              <p className="text-black text-base">
                Suss NextGen Program is a transformative, tech-led program
                designed to empower high school and university students with
                advanced tech and digital skills, critical thinking abilities,
                and innovative mindsets.
              </p>
              <p className="text-black text-base">
                This initiative aims to bridge the gap between academic learning
                and practical application, preparing students for the dynamic
                demands of the modern workforce, nationally and internationally.
              </p>
            </div>
          </div>

          {/* Mission Section */}
          <div className="flex flex-col-reverse sm:flex-col-reverse md:flex-row-reverse items-center md:space-x-8 my-10 sm:my-20">
            <div className="w-full md:w-1/2 flex justify-center min-h-[300px] sm:min-h-[400px] lg:min-h-[500px]">
              <Image
                width={500}
                height={500}
                src="/sussnextgen/SussNextgenPersonWithLaptop.svg"
                alt="Person with tablet"
                className="rounded-lg max-w-full bg-[#D3EDF6] h-auto object-cover"
              />
            </div>
            <div className="w-full md:w-1/2 text-center md:text-left mt-6 sm:mt-0">
              <h2 className="text-3xl md:text-4xl font-bold text-sussBlue mb-4">
                Our Mission
              </h2>
              <p className="text-black text-base">
                To empower students across high schools and tertiary
                institutions with essential tech-led platforms, knowledge,
                resources, and opportunities, enabling them to thrive in
                today&apos;s digital world.
              </p>
            </div>
          </div>

          {/* Vision Section */}
          <div className="flex flex-col sm:flex-col md:flex-row items-center md:space-x-8 my-10 sm:my-20">
            <div className="w-full md:w-1/2 flex justify-center min-h-[300px] sm:min-h-[400px] lg:min-h-[500px]">
              <Image
                width={500}
                height={500}
                src="/sussnextgen/PersonWithDesktop.svg"
                alt="Person with desktop"
                className="rounded-lg max-w-full bg-[#D3EDF6] h-auto object-cover"
              />
            </div>
            <div className="w-full md:w-1/2 text-center md:text-left mt-6 sm:mt-0">
              <h2 className="text-3xl md:text-4xl font-bold text-sussBlue mb-4">
                Vision
              </h2>
              <p className="text-black text-base">
                To be a global transformation leader by impacting generations
                through education and career readiness by bridging the gap
                between academic learning and practical application through
                innovative, technology-driven programs.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Alignment with SDG 8 Section */}
      <div className="relative isolate overflow-hidden bg-white py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto lg:mx-0">
            <h2 className="text-3xl xm:text-5xl font-normal leading-10 text-center tracking-tight text-[#0D4D95] sm:text-6xl">
              Suss NextGen&apos;s Alignment with SDG 8
            </h2>
          </div>

          {/* Cards Section */}
          <div className="mx-auto mt-16 grid grid-cols-1 gap-6 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-8">
            {cards.map((card) => (
              <div
                key={card.name}
                className={`flex flex-col items-center shadow-sm p-10 border rounded-lg md:flex-row md:max-w-xl ${card.backgroundColor}`}
              >
                <div className="flex flex-col justify-between p-4 leading-8">
                  <h5 className="mb-2 text-xl font-semibold tracking-tight text-black">
                    {card.name}
                  </h5>
                </div>
                <Image
                  className="h-20 w-20"
                  src={card.image}
                  alt={card.name}
                  width={1000}
                  height={1000}
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Stories Section */}
      <div className="bg-white pb-20">
        <div className="container mx-auto text-center sm:px-6 lg:px-8 max-w-7xl">
          <h2 className="text-2xl xm:text-lg sm:text-5xl font-normal leading-10 tracking-tight text-[#0D4D95] mb-20">
            Suss NextGen&apos;s Alignment with SDG 8
          </h2>
          <div className="grid grid-cols-1 xm:grid-cols-1 xm:px-10 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {nextgens.map((story, index) => (
              <div
                key={index}
                className="bg-white rounded-lg overflow-hidden border"
              >
                <Image
                  width={1000}
                  height={1000}
                  src={urlFor(story.image).url()}
                  alt={story.title}
                  className="w-full h-[300px] sm:h-[400px] object-cover"
                />
                <div className="p-4 text-left">
                  <h3 className="text-xl font-bold text-gray-800">
                    {story.title}
                  </h3>
                  <a
                    href={`/sussnextgen/${story.slug.current}`}
                    className="inline-block mt-4 px-4 py-2 text-sussBlue border border-sussBlue rounded-full hover:bg-sussBlue hover:text-white transition duration-300"
                  >
                    Read More &rarr;
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default Page;
