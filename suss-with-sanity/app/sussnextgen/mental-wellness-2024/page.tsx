import Image from 'next/image';
import { type Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Suss NextGen - Suss Digital',
  description: 'Suss Ads NextGen Program.',
};

const Page = () => {
  return (
    <div className="flex flex-col items-center bg-gray-100 px-4 py-12">
      <header className="text-center mb-12">
        <h2 className="text-sm text-[#094C95] font-bold uppercase tracking-widest">
          Suss NextGen Mental Wellness Outreach
        </h2>
        <h1 className="text-4xl font-semibold text-[#094C95] mt-3">
          World Mental Health Day 2024: Thika High School
        </h1>
      </header>

      {/* Image Section */}
      <div className="w-full max-w-4xl rounded-lg overflow-hidden shadow-md mb-12">
        <Image
          src="/sussnextgen/mentalAwareness.jpg"
          alt="World Mental Health Day 2024: Thika High School"
          width={1000}
          height={500}
          layout="responsive"
          objectFit="cover"
          className="rounded-lg"
        />
      </div>

      {/* Text Section */}
      <div className="max-w-4xl text-left my-10 px-4 sm:px-0">
        <p className="text-[#1B1A3C] leading-relaxed text-lg mb-8">
          We recognize the vital role mental health plays in shaping future
          generations. In 2024, we aim to connect with 3,000 students, and in
          2025, we’re intent on reaching over 12,000 students across Kenya
          through partnerships with high schools and universities.
        </p>

        {/* Video Section */}
        <div className="relative w-full h-[300px] sm:h-[500px] rounded-lg overflow-hidden shadow-lg mb-10">
          <iframe
            src="https://www.youtube.com/embed/vuV9U-0qKoE?si=ySSKFMfnQIEO2k8n"
            title="Suss NextGen Mental Wellness Outreach | Thika High School - 12th October"
            className="absolute inset-0 w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerPolicy="strict-origin-when-cross-origin"
            allowFullScreen
          ></iframe>
        </div>

        <p className="text-[#1B1A3C] leading-relaxed text-lg">
          Collaborating with inspiring leaders and impact-focused organizations
          across diverse sectors, we aim to nurture and empower students.
          Through these partnerships, we provide platforms, opportunities, and
          resources that not only support students’ career aspirations but also
          foster positive mindsets and holistic mental well-being.
        </p>
      </div>
    </div>
  );
};

export default Page;
