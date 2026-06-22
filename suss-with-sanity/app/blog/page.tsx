import { PageIntro } from '@/components/PageIntro';
import { type Metadata } from 'next';
import Image from 'next/image';
import { client } from '../../sanity/lib/client';
import { urlFor } from '../../sanity/lib/image';

export const revalidate = 30;

export const metadata: Metadata = {
  title: 'Blog - Suss',
  description: 'Stay up-to-date with the latest news from the Suss Team',
  openGraph: {
    type: 'website',
    title: 'Suss',
    description: 'Suss Blogs',
    locale: 'en_US',
    url: 'https://www.suss.co.ke/blog',
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

const fetchAllBlogs = async (): Promise<Blog[]> => {
  const query = `*[_type == "blog"] | order(publishedAt desc){
    title,
    slug,
    shortDescription,
    mainImage,
    publishedAt,
  }`;

  const blogs = await client.fetch(query);
  return blogs;
};

const page = async () => {
  const articles = await fetchAllBlogs();
  return (
    <>
      <PageIntro eyebrow="Blog" title="The latest articles and news">
        <p>Stay up-to-date with the latest news from our team</p>
      </PageIntro>
      <div className="bg-white py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:max-w-4xl">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              From the blog
            </h2>
            <p className="mt-2 text-lg leading-8 text-gray-600">
              Learn how to grow your business with our expert advice.
            </p>
            <div className="mt-16 space-y-20 lg:mt-20 lg:space-y-20">
              {articles.map((post) => (
                <article
                  key={post.slug.current}
                  className="relative isolate flex flex-col gap-8 lg:flex-row"
                >
                  <div className="relative aspect-[16/9] sm:aspect-[2/1] lg:aspect-square lg:w-64 lg:shrink-0">
                    <Image
                      width={1000}
                      height={1000}
                      src={
                        post.mainImage?.asset?._ref
                          ? urlFor(post.mainImage).url()
                          : '/placeholder.png'
                      }
                      alt={post.title}
                      className="absolute inset-0 h-full w-full rounded-2xl bg-gray-50 object-cover"
                    />
                    <div className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-gray-900/10" />
                  </div>
                  <div>
                    <div className="flex items-center gap-x-4 text-xs">
                      <time
                        dateTime={post.publishedAt}
                        className="text-gray-500"
                      >
                        {post.publishedAt.split('T')[0]}
                      </time>
                    </div>
                    <div className="group relative max-w-xl">
                      <h3 className="mt-3 text-lg font-semibold leading-6 text-gray-900 group-hover:text-gray-600">
                        <a href={`/blog/${post.slug.current}`}>
                          <span className="absolute inset-0" />
                          {post.title}
                        </a>
                      </h3>
                      <p className="mt-5 text-sm leading-6 text-gray-600">
                        {post.shortDescription}
                      </p>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default page;
