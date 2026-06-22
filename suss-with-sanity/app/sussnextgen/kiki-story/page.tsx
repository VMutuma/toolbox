import Image from 'next/image';

import { type Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Suss NextGen - Suss Digital',
  description: 'Suss Ads NextGen Program.',
};

const page = () => {
  return (
    <div className="flex flex-col items-center bg-gray-100 px-4 py-8">
      <header className="text-center my-10">
        <h2 className="text-lg text-[#094C95] font-bold uppercase tracking-wider">
          Student Apprenticeship Program
        </h2>
        <h1 className="text-3xl font-semibold text-[#094C95] mt-2">
          15-Year-Old Kiki in Grade 11: Learning Beyond the Books Through
          Apprenticeships
        </h1>
      </header>
      <div className="mt-6">
        <Image
          height={500}
          width={1000}
          src="/sussnextgen/Kiki.png"
          alt="15-Year-Old Kiki in Grade 11: Learning Beyond the Books Through
          Apprenticeships"
          className="rounded-lg max-w-full"
        />
      </div>
      <div className="max-w-4xl text-left my-14">
        <p className="text-[#1B1A3C]">
          We invest in student apprenticeships to bridge the gap between
          academics and professional skills, empowering young people with
          hands-on experience and mentorship.
        </p>
        <p>
          This initiative nurtures future leaders, fosters innovation, and
          reflects Suss NextGen’s program commitment to giving back to the
          community.
        </p>
      </div>

      <div className="container mx-auto max-w-5xl mb-14">
        <div className="relative w-full h-[500px] rounded-lg overflow-hidden">
          <iframe
            className="absolute inset-0 w-full h-full"
            src="https://www.youtube.com/embed/Y-TmDJJE3xk?si=UQk12seC8xN2MNe-"
            title="Wanjiku Mukuria “Kiki” - Suss NextGen Program Apprentice"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </div>
    </div>
  );
};

export default page;
