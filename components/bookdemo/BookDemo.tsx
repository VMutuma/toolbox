'use client';

import { useEffect } from 'react';

export default function BookDemo() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://js-eu1.hsforms.net/forms/embed/v2.js';
    document.body.appendChild(script);

    script.addEventListener('load', () => {
      if (window.hbspt) {
        window.hbspt.forms.create({
          region: process.env.NEXT_PUBLIC_HUBSPOT_REGION,
          portalId: process.env.NEXT_PUBLIC_HUBSPOT_PORTAL_ID,
          formId: process.env.NEXT_PUBLIC_HUBSPOT_FORM_ID,
          target: '#hubspotForm',
        });
      }
    });
  }, []);

  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8 border border-gray-200 rounded-lg pt-10 pb-10">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-sussBlue">
            Suss Ads
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Book Demo
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            We Got Everything You Need To Move Your Brand To The Next Level
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <div id="hubspotForm" className="hubspotForm"></div>
        </div>
      </div>
    </div>
  );
}
