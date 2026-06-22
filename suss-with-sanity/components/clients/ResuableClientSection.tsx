import Image from 'next/image';

type ClientsType = {
  id?: number;
  name: string;
  image: string;
};

type ClientsProps = {
  clients: ClientsType[];
  title: string;
  header?: string;
};

export default function ResuableClientSection({
  clients,
  title,
  header,
}: ClientsProps) {
  return (
    <div className="bg-sussBg py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <h2 className="mt-2 text-5xl font-bold tracking-tight text-[#094C95] sm:text-5xl mb-7">
          {header}
        </h2>
        <p className="text-center text-3xl font-normal leading-8 text-[#094C95]">
          {title}
        </p>
        <div className="mt-10 inline-flex w-full flex-nowrap overflow-hidden [mask-image:_linear-gradient(to_right,transparent_0,_black_128px,_black_calc(100%-200px),transparent_100%)]">
          <ul className="brands-wrapper">
            {clients.map((client) => (
              <li key={client.name}>
                <Image
                  key={client.name}
                  src={client.image}
                  alt="Transistor"
                  width={100}
                  height={30}
                />
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
