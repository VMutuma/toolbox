import type { Metadata } from "next";
import {Inter} from "next/font/google";
import "./globals.css";
import Header from '@/components/navbar/Header';
import Footer from '@/components/footer/Footer';

const inter = Inter({subsets: ['latin']});

export const metadata: Metadata = {
  title: " iGaming Expo Africa",
  description: "The premier gaming expo in Africa",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} antialiased`}
      >
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
