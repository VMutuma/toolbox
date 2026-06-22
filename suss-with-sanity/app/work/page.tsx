import Image from 'next/image';
import Link from 'next/link';
import { urlFor } from '../../sanity/lib/image';
import { client } from '../../sanity/lib/client';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Case studies - Suss',
  description: 'Suss Ads Case studies',
  openGraph: {
    type: 'website',
    title: 'Suss',
    description: 'Suss Case studies',
    locale: 'en_US',
    url: 'https://www.suss.co.ke/work',
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

interface CaseStudy {
  title: string;
  slug: {
    current: string;
  };
  shortDescription: string;
  image: {
    asset: {
      _ref: string;
    };
    alt: string;
  };
  body: any;
}

async function getCaseStudies(): Promise<CaseStudy[]> {
  const query = `*[_type == "casestudy"] | order(_createdAt desc){
    title,
    slug,
    shortDescription,
    image,
    body
  }
`;
  const caseStudies = await client.fetch(query);
  return caseStudies;
}
export default async function page() {
  const caseStudies = await getCaseStudies();

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
            {caseStudies.map((casestudy) => (
              <Link
                key={casestudy.slug.current}
                href={`/work/${casestudy.slug.current}`}
              >
                <Image
                  className="h-auto max-w-full rounded-lg"
                  src={urlFor(casestudy.image).url()}
                  width={1000}
                  height={1000}
                  alt={casestudy.title}
                />
              </Link>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
}
