import Awards from '@/components/Awards';
import CaseStudies from '@/components/CaseStudies';
import OurProducts from '@/components/OurProducts';
import Publishers from '@/components/Publishers';
import About from '@/components/about/Aboutsection';
import ResuableClientSection from '@/components/clients/ResuableClientSection';
import NewHero from '@/components/hero/NewHero';
import Testimonials from '@/components/testimonials/Testimonials';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Home - Suss Digital',
  description:
    "Africa's preferred digital hub: Display, Video, Native, Push, Interstitial Ads. Stay ahead with us. Optimize for guaranteed visits, fast conversions. Trusted by thousands. Launch your campaign and create effective ads today.",
};

export default function Home() {
  const clients = [
    {
      name: 'KCB',
      image: '/images/logos2/kcblogo.svg',
    },
    {
      name: 'Bio',
      image: '/images/logos2/Bio logo.png',
    },
    {
      name: 'Cardbury',
      image: '/images/logos2/Cardbury logo.png',
    },
    {
      name: 'dentsu',
      image: '/images/logos2/dentsu logo.png',
    },
    {
      name: 'eighty eight',
      image: '/images/logos2/eighty eight logo.png',
    },
    {
      name: 'gamepawa',
      image: '/images/logos2/gamepawa logo.png',
    },
    {
      name: 'gift pesa',
      image: '/images/logos2/gift pesa logo.png',
    },
    {
      name: 'How low',
      image: '/images/logos2/How low logo.png',
    },
    {
      name: 'Nivea',
      image: '/images/logos2/Nivea logo.png',
    },
    {
      name: 'Sarit',
      image: '/images/logos2/Sarit.png',
    },
    {
      name: 'sportpesa',
      image: '/images/logos2/sportpesa logo.png',
    },
    {
      name: 'sportsbet.io',
      image: '/images/logos2/sportsbet.io.png',
    },
    {
      name: 'Bethipo',
      image: '/images/logos2/Bethipo logo.png',
    },
    {
      name: 'Betika',
      image: '/images/logos2/Betika logo.png',
    },
    {
      name: 'Betkwiff',
      image: '/images/logos2/Betkwiff logo.png',
    },
    {
      name: 'ALX',
      image: '/images/logos2/alx logo.png',
    },
    {
      name: 'ABSA',
      image: '/images/logos2/absa logo.png',
    },
    {
      name: '1xbet',
      image: '/images/logos2/1xbet logo.png',
    },
    {
      name: 'Ultrabet',
      image: '/images/logos2/Ultrabet logo.png',
    },
    {
      name: 'udemy',
      image: '/images/logos2/udemy logo.png',
    },

    {
      name: 'BetKing',
      image: '/images/logos2/Betking logo.png',
    },
    {
      name: 'Omo',
      image: '/images/logos2/Omo logo.png',
    },
    {
      name: 'Agakhan',
      image: '/images/logos2/Agakhan logo.png',
    },
    {
      name: 'Vaal',
      image: '/images/logos2/Vaal logo.png',
    },
    {
      name: 'KRA',
      image: '/images/logos2/KRA logo.png',
    },
    {
      name: 'Liason',
      image: '/images/logos2/Liason logo.png',
    },
    {
      name: 'Saracen',
      image: '/images/logos2/Saracen logo.png',
    },
    {
      name: 'Firefox',
      image: '/images/logos2/Firefox logo.png',
    },
    {
      name: 'Unilever',
      image: '/images/logos2/Unilever-Logo.png',
    },
    {
      name: 'Mondelez',
      image: '/images/logos2/Mondelez logo.png',
    },
    {
      name: 'Mozilla',
      image: '/images/logos2/Mozilla_logo.svg.png',
    },
    {
      name: 'Pocket_App_Logo',
      image: '/images/logos2/Pocket_App_Logo.png',
    },
    {
      name: 'Hanan',
      image: '/images/logos2/Hanan logo.png',
    },

    {
      name: 'GOK',
      image: '/images/logos2/GOK logo.png',
    },
    {
      name: 'National_Olympic_Committee_of_Kenya_logo',
      image: '/images/logos2/National_Olympic_Committee_of_Kenya_logo.png',
    },

    {
      name: 'Kepsa',
      image: '/images/logos2/Kepsa logo.png',
    },
    {
      name: 'oxygene_logo',
      image: '/images/logos2/oxygene_logo1.png',
    },
    {
      name: 'LG',
      image: '/images/logos2/LG-Logo.png',
    },
    {
      name: 'Betsafe-logo',
      image: '/images/logos2/Betsafe-logo.png',
    },
    {
      name: 'sangare_logo',
      image: '/images/logos2/sangare_logo.png',
    },
    {
      name: 'Royco-logo',
      image: '/images/logos2/Royco-logo-website.png',
    },

    {
      name: 'Telkom',
      image: '/images/logos2/Telkom logo.png',
    },
    {
      name: 'betafriq',
      image: '/images/logos2/BETAFRIQ-Kenya-dark-logo.png',
    },
    {
      name: 'E Citizen',
      image: '/images/logos2/E citizen logo.png',
    },
    {
      name: 'Brookside',
      image: '/images/logos2/Brookside-logo.svg',
    },
    {
      name: 'AFFTI',
      image: '/images/logos2/AFFTI-logo.svg',
    },
    {
      name: 'Betkumi',
      image: '/images/logos2/Betkumi-Logo.svg',
    },
    {
      name: 'Bola-Bet',
      image: '/images/logos2/Bola-Bet Logo.svg',
    },
    {
      name: 'Cadbury',
      image: '/images/logos2/Cadbury-logo.svg',
    },
    {
      name: 'Delamere',
      image: '/images/logos2/Delamere-logo.svg',
    },
    {
      name: 'Illara',
      image: '/images/logos2/Illara-logo.svg',
    },
    {
      name: 'IndigoHomes',
      image: '/images/logos2/IndigoHomes-Logo.svg',
    },
    {
      name: 'Mastercard',
      image: '/images/logos2/Mastercard-logo.svg',
    },
    {
      name: 'Pakakumi',
      image: '/images/logos2/Pakakumi-logo.svg',
    },
    {
      name: 'Sokabet',
      image: '/images/logos2/Sokabet-logo.svg',
    },
    {
      name: 'Visa',
      image: '/images/logos2/Visa-logo.svg',
    },
  ];
  return (
    <>
      <NewHero />
      <CaseStudies />
      <About />
      <OurProducts />
      <ResuableClientSection
        clients={clients}
        title="Trusted by the world’s most innovative brands"
      />
      <Publishers />
      <Testimonials />
      <Awards />
    </>
  );
}
