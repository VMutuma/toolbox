import { type Metadata } from 'next';
import Image from 'next/image';
import { urlFor } from '../../sanity/lib/image';
import { client } from '../../sanity/lib/client';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Careers  - Suss Digital',
  description: 'Suss Digital careers.',
  openGraph: {
    type: 'website',
    title: 'Suss',
    description: 'Suss Careers',
    locale: 'en_US',
    url: 'https://www.suss.co.ke/careers',
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

interface ICareers {
  title: string;
  slug: {
    current: string;
  };
  position: string;
  image: {
    asset: {
      _ref: string;
    };
    alt: string;
  };
  shortDescription: string;
  applicationEndDate: string;
  body: any;
}
async function getCareers(): Promise<ICareers[]> {
  const query = `*[_type == "careers"] | order(applicationEndDate desc){
    title,
    slug,
    position,
    applicationEndDate,
    shortDescription,
    image,
  }
`;
  const careers = await client.fetch(query);
  console.log(careers);
  return careers;
}
export default async function page() {
  const careers = await getCareers();
  return (
    <>
      {/* Wrapper div with background and spacing */}
      <div className="relative bg-[#F9FAFB] max-h-[600px] xm:text-center mb-10 lg:pb-24 z-10">
        <div className="mx-auto max-w-7xl lg:grid lg:grid-cols-12 lg:gap-x-8 px-4 sm:px-6 lg:px-8">
          <div className="px-6 pb-24 pt-10 sm:pb-32 lg:col-span-7 xm:mb-5 lg:px-0 lg:pb-56 lg:pt-48 xl:col-span-6">
            <div className="mx-auto max-w-2xl lg:mx-0">
              <h1 className="mt-24 text-4xl font-bold tracking-tight text-[#0D4D95] sm:mt-10 sm:text-6xl leading-10">
                Innovation. Passion. Limitless Opportunities.
              </h1>
            </div>
          </div>

          {/* Ensure image container is only absolutely positioned on very large screens */}
          <div className="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0">
            <Image
              width={2432}
              height={1442}
              className="aspect-[3/2] xm:h-[370px] xm:-mt-28 xm:w-full w-[804px] h-full bg-gray-50 object-cover lg:aspect-auto lg:h-full"
              src="/hero/CareersHero.svg"
              alt="Suss About Page Hero Image"
            />
          </div>
        </div>
      </div>

      {/* Bottom section with additional margin and clear-both to prevent overlap */}
      <section className="py-5 mt-12 sm:mt-64 md:mt-96 lg:mt-10 relative z-20 clear-both">
        <div className="mx-auto max-w-2xl mb-6 text-center lg:text-center">
          <h2 className="leading-7 mt-2 text-3xl xm:text-center font-bold tracking-tight text-sussBlue sm:text-4xl">
            Current Openings
          </h2>
        </div>
        {careers.map((career) => (
          <SussCareers
            image={urlFor(career.image).url()}
            key={career.slug.current}
            url={career.slug.current}
            description={career.shortDescription}
            title={career.title}
          />
        ))}
      </section>
    </>
  );
}

interface SussCareersProps {
  title: string;
  description: string;
  image: string;
  url: string;
}

const SussCareers = ({ title, description, image, url }: SussCareersProps) => {
  return (
    <div className="bg-[#D8F1FB] text-[#094C95] p-8 lg:p-12 flex flex-col lg:flex-row lg:container lg:mx-auto items-center rounded-xl lg:gap-20 gap-10 my-10">
      <div className="flex flex-col lg:flex-row items-center">
        <div className="ml-6 mt-6 lg:mt-0">
          <Image
            src={image}
            alt={title}
            className="rounded-md lg:w-[419px] lg:h-[419px] w-[300px] h-[300px] object-cover"
            width={300}
            height={300}
          />
        </div>
      </div>

      <div className="mt-6 lg:mt-0 lg:ml-12 text-center lg:text-left">
        <div className="flex flex-row items-center">
          <h2 className="text-lg flex-start font-bold mb-2">Role</h2>
        </div>

        <h1 className=" text-2xl lg:text-4xl font-bold mb-4 py-2">{title}</h1>
        <p className="text-[#1B1A3C] mb-6 lg:text-2xl max-w-[500px] py-2">
          {description}
        </p>
        <div className="flex items-center lg:justify-between justify-center">
          <Link
            href={`/careers/${url}`}
            className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
          >
            Apply
          </Link>
        </div>
      </div>
    </div>
  );
};
