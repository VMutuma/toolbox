'use client';
import { useEffect, useState } from 'react';
import { FaFacebook, FaInstagram, FaLinkedin, FaYoutube } from 'react-icons/fa';
import { FaXTwitter } from 'react-icons/fa6';

const navigation = {
  navigate: [
    { name: 'About Us', href: '/about' },
    { name: 'Case Studies', href: '/work' },
    { name: 'Contact Us', href: '/contactus' },
    { name: 'Careers', href: '/careers' },
    { name: 'Blog', href: '/blog' },
  ],
  support: [
    { name: 'Pricing', href: '#' },
    { name: 'Documentation', href: '#' },
    { name: 'Guides', href: '#' },
    { name: 'API Status', href: '#' },
  ],
  products: [
    { name: 'Suss Ads', href: '/products/sussads' },
    { name: 'Suss SMS', href: '/products/susssms' },
    { name: 'Suss Tracker', href: '/products/susstracker' },
    { name: 'Suss Agency', href: '/products/sussagency' },
  ],
  adFormats: [
    { name: 'Push Notifications', href: '/products/sussads' },
    { name: 'Display Ads', href: '/products/sussads' },
    { name: 'Pop Ads', href: '/products/sussads' },
    { name: 'Native Ads', href: '/products/sussads' },
    { name: 'Video Ads', href: '/products/sussads' },
    { name: 'HTML5 Ads', href: '/products/sussads' },
  ],
  legal: [
    { name: 'Claim', href: '#' },
    { name: 'Privacy', href: '#' },
    { name: 'Terms', href: '/terms' },
  ],
  social: [
    {
      name: 'Facebook',
      href: '#',
      icon: FaFacebook,
    },
    {
      name: 'Instagram',
      href: 'https://www.instagram.com/sussads/',
      icon: FaInstagram,
    },
    {
      name: 'Twitter',
      href: 'https://twitter.com/Sussdigital',
      icon: FaXTwitter,
    },
    {
      name: 'LinkedIn',
      href: 'https://www.linkedin.com/products/suss-digital-africa/',
      icon: FaLinkedin,
    },
    {
      name: 'YouTube',
      href: 'https://www.youtube.com/@sussdigitalafrica',
      icon: FaYoutube,
    },
  ],
};

export default function Footer() {
  const [currentYear, setCurrentYear] = useState<number>(
    new Date().getFullYear()
  );

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
  }, []);

  return (
    <footer
      className="bg-[#094C95] xm:text-center"
      aria-labelledby="footer-heading"
    >
      <h2 id="footer-heading" className="sr-only">
        Footer
      </h2>
      <div className="mx-auto max-w-7xl px-4 pb-8 pt-16 sm:px-6 sm:pt-24 lg:px-8 lg:pt-32">
        <div className="xl:grid xl:grid-cols-3 xl:gap-8">
          <div className="mt-16 grid grid-cols-2 gap-5 sm:grid-cols-4 xl:col-span-2 xl:mt-0">
            <div>
              <h3 className="text-lg font-semibold leading-6 text-white">
                Navigate
              </h3>
              <ul role="list" className="mt-6 space-y-4">
                {navigation.navigate.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className="text-base leading-6 text-white hover:text-white"
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold leading-6 text-white">
                Products
              </h3>
              <ul role="list" className="mt-6 space-y-4">
                {navigation.products.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className="text-base leading-6 text-white hover:text-white"
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="mt-10 sm:mt-0">
              <h3 className="text-lg font-semibold leading-6 text-white">
                Ad Formats
              </h3>
              <ul role="list" className="mt-6 space-y-4">
                {navigation.adFormats.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className="text-base leading-6 text-white hover:text-white"
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="mt-10 sm:mt-0">
              <h3 className="text-lg font-semibold leading-6 text-white">
                Legal
              </h3>
              <ul role="list" className="mt-6 space-y-4">
                {navigation.legal.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className="text-base leading-6 text-white hover:text-white"
                    >
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="mt-10 xl:mt-0">
            <h3 className="text-lg font-semibold leading-6 text-white mb-4">
              Contact Us
            </h3>
            <div className="text-white text-base leading-6 space-y-4">
              <div>
                <p className="font-semibold">Nairobi Office:</p>
                <p>The Atrium, Chaka Road</p>
                <p>Nairobi, Kenya</p>
                <p>
                  Email:
                  <a href="mailto:info@suss.co.ke" className="underline">
                    info@suss.co.ke
                  </a>
                </p>
                <p>
                  Phone:
                  <a href="tel:+254727175849" className="underline">
                    +254 727 175 849
                  </a>
                </p>
              </div>

              <div>
                <p className="font-semibold">UAE Office:</p>
                <p>Suss Digital FZ-LLC</p>
                <p>FDBC1756, Compass Building</p>
                <p>Al Shohada Road</p>
                <p>Al Hamra Industrial Zone-FZ</p>
                <p>Ras Al Khaimah, United Arab Emirates</p>
              </div>
            </div>

            <div className="flex space-x-6 xm:justify-center mt-5">
              {navigation.social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-[#094C95] p-2 rounded-xl bg-white hover:text-white"
                >
                  <span className="sr-only">{item.name}</span>
                  <item.icon className="h-6 w-6" aria-hidden="true" />
                </a>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-10 border-t border-gray-900/10 pt-8 sm:mt-20 lg:mt-24">
          <p className="text-base leading-5 text-center text-white">
            &copy; {currentYear} – Suss Digital Africa. <br /> All Rights
            Reserved.
          </p>
          <p className="text-base leading-5 text-center text-white">
            Suss Digital Africa is licensed by CAK (Communications Authority of
            Kenya) under the Content Service Provider ACT. License number:
            TL/CSP/01121
          </p>
        </div>
      </div>
    </footer>
  );
}
