import Footer from '@/components/footer/Footer';
import Navbar from '@/components/navbar/Navbar';
import clsx from 'clsx';
import type { Metadata } from 'next';
import { Poppins } from 'next/font/google';
import './globals.css';
import { GoogleTagManager } from '@next/third-parties/google';
import { Analytics } from '@vercel/analytics/react';
import Script from 'next/script';
const poppins = Poppins({
  weight: '400',
  subsets: ['latin'],
});
export const metadata: Metadata = {
  title: 'Home - Suss Digital',
  description:
    "Africa's preferred digital hub: Display, Video, Native, Push, Interstitial Ads. Stay ahead with us. Optimize for guaranteed visits, fast conversions. Trusted by thousands. Launch your campaign and create effective ads today.",
  openGraph: {
    images: './opengraph-image.png',
  },
  metadataBase: new URL('https://www.suss.co.ke/'),
  twitter: {
    card: 'summary_large_image',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={clsx('h-full bg-gray-50 antialiased')}>
      <Script
        async
        src="https://www.googletagmanager.com/gtag/js?id=G-E1ZJGQBHYR"
      ></Script>
      <Script id="google-analytics">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
         gtag('config', 'G-E1ZJGQBHYR');
        `}
      </Script>
      <body className={poppins.className}>
        <Navbar />
        {children}
        <Footer />
        <GoogleTagManager gtmId="GTM-TLDLD35" />
        <Analytics />
      </body>
    </html>
  );
}
