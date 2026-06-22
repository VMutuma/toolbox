import { urlFor } from '../../../sanity/lib/image';
import { client } from '../../../sanity/lib/client';
import { PortableText } from 'next-sanity';
import Image from 'next/image';

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

export const revalidate = 30;

async function getCaseStudy(slug: string): Promise<CaseStudy> {
  const query = `*[_type == "casestudy" && slug.current == '${slug}']{
    title,
    slug,
    shortDescription,
    image,
    body
  }[0]
`;
  const nextgen = await client.fetch(query);
  return nextgen;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const caseStudy = await getCaseStudy(slug);
  if (caseStudy === null) return null;
  return {
    title: caseStudy.title,
    description: caseStudy.shortDescription,
    openGraph: {
      type: 'website',
      title: caseStudy.title,
      description: caseStudy.shortDescription
        ? caseStudy.shortDescription
        : caseStudy.title,
      locale: 'en_US',
      url: `https://www.suss.co.ke/work/${slug}`,
      siteName: 'Suss',
      images: [
        {
          url: urlFor(caseStudy.image).width(1200).height(630).url(),
          width: 1200,
          height: 630,
          alt: caseStudy.title,
        },
      ],
      metadataBase: new URL('https://www.suss.co.ke/'),
    },
  };
}

const page = async ({ params }: { params: Promise<{ slug: string }> }) => {
  const slug = (await params).slug;
  const casestudy = await getCaseStudy(slug);

  const PortableTextComponent = {
    types: {
      image: ({ value }: { value: any }) => {
        if (!value?.asset?._ref) {
          return null;
        }
        return (
          <Image
            src={urlFor(value).url()}
            alt="Image"
            width={800}
            height={800}
            className="object-cover h-auto w-full rounded-lg"
          />
        );
      },
    },
  };
  return (
    <div className="flex flex-col items-center bg-gray-100 px-4 py-8">
      <header className="text-center my-10">
        <h2 className="text-lg text-[#094C95] font-bold uppercase tracking-wider">
          {casestudy.title}
        </h2>
      </header>
      <article className="mx-auto text-black prose mb-20 p-5">
        <PortableText
          value={casestudy.body}
          components={PortableTextComponent}
        />
      </article>
    </div>
  );
};

export default page;
