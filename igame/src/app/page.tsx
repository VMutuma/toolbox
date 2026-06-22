import Header from '@/components/navbar/Header';
import Hero from '@/components/hero/Hero';
import About from '@/components/about/About';
import FloorPlan from '@/components/floor/FloorPlan';
import Speakers from '@/components/speakers/Speakers';
import Testimonials from '@/components/testimonials/Testimonials';
import Venue from '@/components/venue/Venue';
import Faqs from '@/components/faqs/Faqs'; 
import { faqs } from '@/components/faqs/faqsData';

export default function Home() {
  const limitedFaqs = faqs.slice(0, 5);

  return (
    <>
      <Header />
      <main>
        <Hero />
        <About />
        <FloorPlan />
        <Speakers />
        <Testimonials />
        <Venue />
        <Faqs faqs={limitedFaqs} />
      </main>
    </>
  );
}
