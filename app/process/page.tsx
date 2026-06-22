import { type Metadata } from 'next';
import Image from 'next/image';
import { Blockquote } from '@/components/Blockquote';
import { Container } from '@/components/Container';
import { FadeIn } from '@/components/FadeIn';
import { GridList, GridListItem } from '@/components/GridList';
import { List, ListItem } from '@/components/List';
import { PageIntro } from '@/components/PageIntro';
import { SectionIntro } from '@/components/SectionIntro';
import { StylizedImage } from '@/components/StylizedImage';
import { TagList, TagListItem } from '@/components/TagList';
import imageReporting from '@/public/images/brenda-reporting.jpg';
import imageObjectives from '@/public/images/deniss-sportsbet.jpg';
import imageStrategy from '@/public/images/suss-4.jpg';
import imageImplementation from '@/public/images/suss-2.jpg';
import imageAnalysis from '@/public/images/suss-1.jpg';

function Section({
  title,
  image,
  children,
}: {
  title: string;
  image: React.ComponentPropsWithoutRef<typeof StylizedImage>;
  children: React.ReactNode;
}) {
  return (
    <Container className="group/section [counter-increment:section]">
      <div className="lg:flex lg:items-center lg:justify-end lg:gap-x-8 lg:group-even/section:justify-start xl:gap-x-20">
        <div className="flex justify-center">
          <FadeIn className="w-full flex-none lg:w-[45rem]">
            <Image
              {...image}
              sizes="(min-width: 1216px) 76rem, 100vw"
              priority
              className="justify-center lg:justify-end lg:group-even/section:justify-start rounded-2xl mx-auto lg:mx-0"
              alt="process"
            />
          </FadeIn>
        </div>
        <div className="mt-12 lg:mt-0 lg:w-[37rem] lg:flex-none lg:group-even/section:order-first">
          <FadeIn>
            <div
              className="font-display text-base font-semibold before:text-neutral-300 before:content-['/_'] after:text-neutral-950 after:content-[counter(section,decimal-leading-zero)]"
              aria-hidden="true"
            />
            <h2 className="mt-2 font-display text-3xl font-medium tracking-tight text-neutral-950 sm:text-4xl">
              {title}
            </h2>
            <div className="mt-6">{children}</div>
          </FadeIn>
        </div>
      </div>
    </Container>
  );
}

function Discover() {
  return (
    <Section title="Discover" image={{ src: imageObjectives }}>
      <div className="space-y-6 text-base text-neutral-600">
        <p>
          The first and fundamental step that Suss Ads takes to achieve
          measurable results is understanding the{' '}
          <strong className="font-semibold text-neutral-950">
            clients objectives.
          </strong>
          This step sets the foundation of our strategies and involves in-depth
          discussions, comprehensive research, and thorough analysis of the
          clients needs.
        </p>
        <p>
          At this stage, the agency collaborates with the client to set{' '}
          <strong className="font-semibold text-neutral-950">
            specific, measurable, achievable, relevant, and time-bound SMART
            goals.
          </strong>
          These goals serve as the benchmark against which success will be
          measured.
        </p>
      </div>
    </Section>
  );
}

function Strategy() {
  return (
    <Section title="Strategy" image={{ src: imageStrategy, shape: 1 }}>
      <div className="space-y-6 text-base text-neutral-600">
        <p>
          Once the clients objectives are established, we then proceed to work
          on tailored strategies. Our strategies highlight the value
          proposition, audience attributes, market trends, PESTEL & SWOT
          analysis, specific actions, tactics, channels and tools that will be
          utilized to meet the clients goals.
        </p>
        <h3 className="mt-12 font-display text-base font-semibold text-neutral-950">
          Fundamentally, our strategies are guided by the 5Ws and 2Hs approach{' '}
        </h3>
        <List className="mt-8">
          <ListItem title="What (Measurable Objectives)">
            Our projects always have 100% test coverage, which would be
            impressive if our tests weren’t as porous as a sieve.
          </ListItem>
          <ListItem title="Who (Target Audience)">
            We define our target audience; their demographics, personas,
            preferences, and pain points to tailor our marketing strategy.
          </ListItem>
          <ListItem title="When (Campaign Duration)">
            We establish the timeline for our marketing strategy and deadlines
            for key milestones and marketing initiatives to stay on track.
          </ListItem>
        </List>
      </div>
      <h3 className="mt-12 font-display text-base font-semibold text-neutral-950">
        Included in this phase
      </h3>
      <TagList className="mt-4">
        <TagListItem>Budget</TagListItem>
        <TagListItem>Rationale/Justification</TagListItem>
        <TagListItem>Tactics/Execution</TagListItem>
        <TagListItem>Channels/Connection Point</TagListItem>
      </TagList>
      <Blockquote
        author={{ name: 'Betika Kenya', role: 'Head Of Digital' }}
        className="mt-12"
      >
        Suss Digital excel in digital strategy and with the help of their
        programmatic technology, they have set a benchmark in campaign
        efficiency for our campaigns.
      </Blockquote>
    </Section>
  );
}

function Implementation() {
  return (
    <Section title="Implementation" image={{ src: imageImplementation }}>
      <div className="space-y-6 text-base text-neutral-600">
        <p>
          With a well-defined strategy in place, the agency proceeds with the
          execution of the plan. This phase can involve various activities, from
          creating and running advertising campaigns, optimizing website
          content, developing social media content, or any other actions aligned
          with the client&apos;s unique strategy.
        </p>
      </div>
    </Section>
  );
}

function Analysis() {
  return (
    <Section title="Analysis" image={{ src: imageAnalysis }}>
      <div className="space-y-6 text-base text-neutral-600">
        <p>
          Suss Ads continuously monitors, optimizes and analyses campaigns using
          a suite of analytical tools keeping a close eye on key performance
          indicators (KPIs) such as website traffic, engagement metrics,
          conversion rates, and more. This data provides crucial insights into
          making prompt recommendations on what&apos;s working and what needs
          adjustment.
        </p>
      </div>
    </Section>
  );
}

function Report() {
  return (
    <Section title="Report" image={{ src: imageReporting, shape: 2 }}>
      <div className="space-y-6 text-base text-neutral-600">
        <p>
          At Suss Ads, we believe in consistent communication. We keep our
          clients informed about progress and allow for input and feedback,
          through regular reporting. Clear and concise, we ensure that our
          reports demonstrate the{' '}
          <strong className="font-semibold text-neutral-950">
            return on investment
          </strong>{' '}
          (ROI) for the client and how the agency&apos;s efforts directly
          contribute to the client&apos;s measurable goals.
        </p>
        <p>
          In July 2023, our esteemed customer SportPesa reached out to us with a
          clear objective: to revolutionize the consumer experience within the
          betting and gaming industry. This marked the commencement of an
          innovative journey, with a primary focus on enhancing customer
          journeys and elevating customer engagement.
        </p>
      </div>

      {/* <h3 className="mt-12 font-display text-base font-semibold text-neutral-950">
        Included in this phase
      </h3>
      <List className="mt-8">
        <ListItem title="Testing">
          Our projects always have 100% test coverage, which would be impressive
          if our tests weren’t as porous as a sieve.
        </ListItem>
        <ListItem title="Infrastructure">
          To ensure reliability we only use the best Digital Ocean droplets that
          $4 a month can buy.
        </ListItem>
        <ListItem title="Support">
          Because we hold the API keys for every critical service your business
          uses, you can expect a lifetime of support, and invoices, from us.
        </ListItem>
      </List> */}
    </Section>
  );
}

function Values() {
  return (
    <div className="relative my-24 pt-24 sm:my-32 sm:pt-32 lg:my-40 lg:pt-40">
      <SectionIntro
        eyebrow="Our values"
        title="Balancing reliability and innovation"
      >
        <p>
          We strive to stay at the forefront of emerging trends and
          technologies, while completely ignoring them and forking that old
          Rails project we feel comfortable using. We stand by our core values
          to justify that decision.
        </p>
      </SectionIntro>

      <Container className="mt-24">
        <GridList>
          <GridListItem title="AdTech Solutions">
            Leverage the power of data-driven advertising with our cutting-edge
            AdTech solutions. We provide comprehensive tools to optimize your ad
            campaigns, target the right audience, and maximize your return on
            investment. Suss ensures that your brand stands out in the
            competitive digital landscape.
          </GridListItem>
          <GridListItem title="MarTech Innovations">
            Transform your marketing strategies with our MarTech innovations. We
            offer a suite of tools and platforms to streamline your marketing
            efforts, from customer acquisition to retention. Our solutions
            enable you to create personalized, targeted campaigns that resonate
            with your audience and drive meaningful engagement.
          </GridListItem>
          <GridListItem title="DevTech Excellence">
            Unlock the true potential of your digital infrastructure with
            Suss&apos;s DevTech excellence. Our team of skilled developers and
            technologists are dedicated to crafting custom solutions tailored to
            your unique business needs. From web and app development to API
            integrations, we ensure your digital ecosystem is robust, scalable,
            and future-ready.
          </GridListItem>
        </GridList>
      </Container>
    </div>
  );
}

export const metadata: Metadata = {
  title: 'Our Process',
  description:
    'We believe that content should be bold, well-crafted, and leave a lasting impression',
};

export default function Process() {
  return (
    <>
      <PageIntro eyebrow="Our process" title="How we work">
        <p>
          In today&apos;s competitive business landscape, Suss Ads has adopted a
          systematic and meticulous approach to help clients achieve measurable
          results, as demonstrated in the steps below
        </p>
      </PageIntro>

      <div className="mt-24 space-y-24 [counter-reset:section] sm:mt-32 sm:space-y-32 lg:mt-40 lg:space-y-40">
        <Discover />
        <Strategy />
        <Implementation />
        <Analysis />
        <Report />
      </div>

      <Values />
    </>
  );
}
