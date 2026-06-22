import { urlFor } from '../../../sanity/lib/image';
import { client } from '../../../sanity/lib/client';
import { PortableText } from 'next-sanity';
import Image from 'next/image';

export const revalidate = 30;

interface Blog {
  title: string;
  slug: {
    current: string;
  };
  shortDescription: string;
  mainImage: {
    asset: {
      _ref: string;
    };
    alt: string;
  };
  publishedAt: string;
  body: any;
}

async function getBlogBySlug(slug: string): Promise<Blog> {
  const query = `*[_type == "blog" && slug.current == '${slug}']{
    title,
    slug,
    shortDescription,
    mainImage,
    publishedAt,
    body
  }[0]
`;
  const blog = await client.fetch(query);
  return blog;
}
type props = {
  params: Promise<{ slug: string }>;
};
export async function generateMetadata({ params }: props) {
  const slug = (await params).slug;
  const blog = await getBlogBySlug(slug);
  if (blog === null) return null;
  return {
    title: blog.title,
    description: blog.shortDescription,
    openGraph: {
      type: 'website',
      title: blog.title,
      description: blog.shortDescription ? blog.shortDescription : blog.title,
      locale: 'en_US',
      url: `https://www.suss.co.ke/blog/${slug}`,
      siteName: 'Suss',
      images: [
        {
          url: urlFor(blog.mainImage).width(1200).height(630).url(),
          width: 1200,
          height: 630,
          alt: blog.title,
        },
      ],
      metadataBase: new URL('https://www.suss.co.ke/'),
    },
  };
}

export default async function page({ params }: props) {
  const slug = (await params).slug;
  const blog = await getBlogBySlug(slug);

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
          {blog.title}
        </h2>
      </header>
      <Image
        src={urlFor(blog.mainImage).url()}
        alt={blog.title}
        width={600}
        height={600}
        priority
        className="object-cover h-[500px] w-[600px] rounded-lg"
      />
      <article className="mx-auto text-black prose mb-20 p-5">
        <PortableText value={blog.body} components={PortableTextComponent} />
      </article>
    </div>
  );
}
