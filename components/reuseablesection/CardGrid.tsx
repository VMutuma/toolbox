type data = {
  name: string;
  description?: string;
  backgroundColor: string;
};
type CardGridProps = {
  headerText: string;
  cards: data[];
};

export default function CardGrid({ headerText, cards }: CardGridProps) {
  return (
    <div className="relative isolate overflow-hidden bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto lg:mx-0">
          <h2 className="text-5xl xm:text-5xl font-normal leading-10 text-center tracking-tight text-[#0D4D95] sm:text-6xl">
            {headerText}
          </h2>
        </div>
        <div className="mx-auto mt-16 grid grid-cols-1 gap-6 sm:mt-20 lg:mx-0 lg:max-w-none lg:grid-cols-3 lg:gap-8">
          {cards.map((card) => (
            <div
              key={card.name}
              className={`flex gap-x-4 rounded-xl p-10  border border-[#094C95] ${card.backgroundColor}`}
            >
              <div className="text-base leading-7">
                <h3 className="font-semibold text-[#0D4D95]">{card.name}</h3>
                <p className="mt-2 text-black">{card.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
