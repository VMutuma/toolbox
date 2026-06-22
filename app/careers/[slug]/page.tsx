import { urlFor } from '../../../sanity/lib/image';
import { client } from '../../../sanity/lib/client';
import { PortableText } from 'next-sanity';
import Image from 'next/image';

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
type props = {
  params: Promise<{ slug: string }>;
};
async function getCareer(slug: string): Promise<ICareers> {
  const query = `*[_type == "careers" && slug.current == '${slug}']{
    title,
    slug,
    position,
    applicationEndDate,
    shortDescription,
    image,
    body
  }[0]
`;
  const career = await client.fetch(query);
  return career;
}

export async function generateMetadata({ params }: props) {
  const slug = (await params).slug;
  const career = await getCareer(slug);
  if (career === null) return null;
  return {
    title: career.title,
    description: career.shortDescription,
    openGraph: {
      type: 'website',
      title: career.title,
      description: career.shortDescription
        ? career.shortDescription
        : career.title,
      locale: 'en_US',
      url: `https://www.suss.co.ke/careers/${slug}`,
      siteName: 'Suss',
      images: [
        {
          url: urlFor(career.image).width(1200).height(630).url(),
          width: 1200,
          height: 630,
          alt: career.title,
        },
      ],
      metadataBase: new URL('https://www.suss.co.ke/'),
    },
  };
}

export const revalidate = 30;

const page = async ({ params }: props) => {
  const slug = (await params).slug;
  const career = await getCareer(slug);

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
          {career.title}
        </h2>
      </header>
      <Image
        src={urlFor(career.image).url()}
        alt={career.title}
        width={600}
        height={600}
        priority
        className="object-cover h-[500px] w-[600px] rounded-lg"
      />
      <article className="mx-auto text-black prose mb-20 p-5">
        <PortableText value={career.body} components={PortableTextComponent} />
      </article>
    </div>
  );
};

export default page;
