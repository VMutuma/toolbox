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
          Tech Lab Upgrade
        </h2>
        <h1 className="text-3xl font-semibold text-[#094C95] mt-2">
          Githumu Boys High School
        </h1>
      </header>
      <div className="mt-6">
        <Image
          height={500}
          width={1000}
          src="/sussnextgen/2024_0622_12551900.jpg"
          alt="Githumu Boys High School event"
          className="rounded-lg max-w-full"
        />
      </div>
      <div className="max-w-4xl text-left my-14">
        <p className="text-[#1B1A3C]">
          As part of the Suss NextGen Program, Githumu Boys High School was the
          first beneficiary through a project aimed at upgrading the Tech Lab to
          modern standards. In June 2024, the school received a commitment of
          Ksh. 500,000 from Suss Ads to revamp its tech lab, with an initial
          donation of Ksh. 100,000 already provided.
        </p>
      </div>
      <div className="grid grid-cols-1 xs:grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
        <div className="h-[400px] md:h-[600px] w-full rounded-lg overflow-hidden">
          <Image
            height={500}
            width={1000}
            src="/sussnextgen/2024_0622_12511200.jpg"
            alt="Image description 1"
            className="w-full h-full object-cover"
          />
        </div>

        <div className="h-[400px] md:h-[600px] w-full rounded-lg overflow-hidden">
          <Image
            height={500}
            width={1000}
            src="/sussnextgen/2024_0622_13093400.jpg"
            alt="Image description 2"
            className="w-full h-full object-cover"
          />
        </div>
      </div>

      <div className="max-w-4xl  text-left my-14">
        <p className="text-[#1B1A3C]">
          The initiative aims to bridge the gap in technology access and improve
          educational opportunities for students. The school previously faced
          challenges due to limited access to computers, but the new resources
          are expected to significantly enhance student learning while equipping
          them with the digital skills necessary to excel in todays world,
          starting with his former school.
        </p>
      </div>

      <div className="container mx-auto max-w-5xl mb-14">
        <div className="relative w-full h-[500px] rounded-lg overflow-hidden">
          <iframe
            className="absolute inset-0 w-full h-full"
            src="https://www.youtube.com/embed/AIzuUBLGmRU"
            title="Githumu Boys High School Tech Lab Upgrade"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </div>
    </div>
  );
};

export default page;
