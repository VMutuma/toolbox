import Image from 'next/image';

const testimonials = [
  {
    id: 1,
    body: 'As our digital media patner, they have proven to be an insightful and adept digital patner, meeting KPIs set to help achieve the business objective. We have no reservations in recommesning them.',
    logo: '/images/logos/sportpesalogo.svg',
    organization: 'Sportpesa',
    author: {
      name: 'Head Of Advertising',
      handle: 'sportpesa',
      imageUrl:
        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 2,
    body: 'They have helped TIFA research to transform the digital media efforts allowing optimal delivery of communications and campaign. We believe that you will find their level of skill, knowlegde and expertise practical, timely and innovative as they provide comprehensive digital medial solutions.',
    logo: '/images/logos/tifalogo.svg',
    organization: 'TIFA Research',
    author: {
      name: 'Maggie Ireri',
      handle: 'maggieireri',
      imageUrl:
        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 3,
    body: 'They have a clear understanding of our business product and demographics and have effectively deployed digital solutions that are ROI driven. Suss Digital excel in digital strategy and with the help of their programmatic technology, they have set a benchmark in campaign efficiency for our campaigns.',
    logo: '/images/logos/betikalogo.svg',
    organization: 'Betika Kenya',
    author: {
      name: 'Head Of Digital',
      handle: 'betika.com',
      imageUrl:
        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
];

export default function Testimonials() {
  return (
    <div className="bg-white py-16 sm:py-24 xm:text-center">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-xl text-center">
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-[#094C95] sm:text-4xl">
            Client Testimonials
          </h2>
        </div>
        <div className="mx-auto mt-5 flow-root max-w-2xl sm:mt-20 lg:mx-0 lg:max-w-none">
          <div className="grid grid-cols-3 xm:grid-cols-1 gap-4">
            {testimonials.map((testimonial) => (
              <figure
                key={testimonial.id}
                className="max-w-screen-md mx-auto text-center bg-[#E5F2FA] p-5 rounded-xl"
              >
                <div className="flex flex-col h-full">
                  <div className="flex flex-row items-center m-4">
                    <Image
                      src={testimonial.logo}
                      alt={testimonial.organization}
                      width={2432}
                      height={1442}
                      className="w-auto xm:w-11/12 mr-2"
                    />
                    <p className="text-xl font-semibold">
                      {testimonial.organization}
                    </p>
                    <div className="ml-auto mt-2">
                      <svg
                        width="127"
                        height="121"
                        viewBox="0 0 127 121"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="xm:h-20 h-28"
                      >
                        <path
                          d="M74 121L91.5 56H74V0.5H126.5V56L99 121H74ZM0 121L17.5 56H0V0.5H52.5V56L25 121H0Z"
                          fill="white"
                        />
                      </svg>
                    </div>
                  </div>

                  <blockquote className="flex-grow relative">
                    <p className="text-base font-medium">{testimonial.body}</p>
                  </blockquote>

                  <figcaption className="flex items-center justify-center mt-6 space-x-3 rtl:space-x-reverse">
                    <div className="flex items-center divide-x-2 rtl:divide-x-reverse divide-gray-500 dark:divide-gray-700">
                      <cite className="pe-3 font-medium">
                        {testimonial.author.name}
                      </cite>
                      <cite className="ps-3 font-medium	">
                        {testimonial.organization}
                      </cite>
                    </div>
                  </figcaption>
                </div>
              </figure>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
