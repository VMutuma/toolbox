import { urlFor } from '../../../sanity/lib/image';
import { client } from '../../../sanity/lib/client';
import { PortableText } from 'next-sanity';
import Image from 'next/image';

export interface NextGen {
  title: string;
  slug: {
    _type: string;
    current: string;
  };
  subtitle: string;
  image: {
    _type: string;
    asset: {
      _ref: string;
      _type: string;
    };
  };
  shortDescription: string;
  body: any;
  _createdAt: string;
}

export const revalidate = 30;

async function getNextGenBySlug(slug: string): Promise<NextGen> {
  const query = `*[_type == "nextgen" && slug.current == '${slug}']{
    title,
    slug,
    subtitle,
    image,
    shortDescription,
    body,
    _createdAt
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
  const highlight = await getNextGenBySlug(slug);
  if (highlight === null) return null;
  return {
    title: highlight.title,
    description: highlight.shortDescription,
    openGraph: {
      type: 'website',
      title: highlight.title,
      description: highlight.shortDescription
        ? highlight.shortDescription
        : highlight.title,
      locale: 'en_US',
      url: `https://www.suss.co.ke/sussnextgen/${slug}`,
      siteName: 'Suss',
      images: [
        {
          url: urlFor(highlight.image).width(1200).height(630).url(),
          width: 1200,
          height: 630,
          alt: highlight.title,
        },
      ],
      metadataBase: new URL('https://www.suss.co.ke/'),
    },
  };
}

const page = async ({ params }: { params: Promise<{ slug: string }> }) => {
  const { slug } = await params;
  const casestudy = await getNextGenBySlug(slug);

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
        <h1 className="text-3xl font-semibold text-[#094C95] mt-2">
          {casestudy.subtitle}
        </h1>
      </header>
      <Image
        src={urlFor(casestudy.image).url()}
        alt={casestudy.title}
        width={600}
        height={600}
        priority
        className="object-cover h-[500px] w-[600px] rounded-lg"
      />
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
