import React from "react";
import Faqs from '@/components/faqs/Faqs';
import { faqs } from '@/components/faqs/faqsData';

export default function Event() {
  return (
          <section
          id="getToEvent"
          className="pt-40 md:pt-56 pb-12 px-6 md:px-20 bg-gradient-to-r from-pink-500 to-orange-500"
        >
  

      {/* Heading Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white drop-shadow-md">
          Venue
        </h1>
        <p className="text-lg md:text-xl text-gray-100 mt-4 max-w-3xl mx-auto">
          Discover the perfect destination for the iGaming Expo Africa 2025, where innovation and collaboration meet.
        </p>
      </div>

      {/* Venue Details Section */}
      <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
        {/* Image */}
        <img
          src="/venueNight.jpg"
          alt="Sarit Centre"
          className="rounded-xl shadow-lg w-full lg:w-1/2 object-cover"
        />

        {/* Description */}
        <div className="text-white text-base lg:text-lg lg:w-1/2 space-y-6 leading-relaxed">
          <p>
            The <strong>Sarit Centre</strong> is a premier exhibition and conference venue located in the heart of Nairobi, Kenya. Renowned for its modern facilities and strategic location, the Sarit Centre offers over{" "}
            <strong>5,000 square meters</strong> of versatile exhibition space, complete with state-of-the-art audiovisual technology and amenities.
          </p>
          <p>
            With its vibrant atmosphere and easy accessibility, the venue is perfectly suited to foster engagement and collaboration among industry leaders, enhancing the overall experience for exhibitors and attendees alike.
          </p>
          <p>
            Surrounded by Nairobi&apos;s rich cultural diversity and bustling business environment, the Sarit Centre is an ideal backdrop for this landmark event, promising an unforgettable networking and learning experience.
          </p>
        </div>
      </div>

      {/* Map Section */}
      <div className="mt-16">
        <h2 className="text-3xl md:text-4xl font-extrabold text-white text-center mb-8">
          Location
        </h2>
        <div className="relative rounded-xl overflow-hidden shadow-lg">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15955.236899231968!2d36.81215362100398!3d-1.2635803999999964!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x182f19a46ad0b1ff%3A0xab7193f4f4035bc6!2sSarit%20Centre!5e0!3m2!1sen!2ske!4v1639131424787!5m2!1sen!2ske"
            width="100%"
            height="450"
            allowFullScreen
            loading="lazy"
            className="border-none rounded-lg shadow-xl"
            aria-label="Google Map showing Sarit Centre location in Nairobi, Kenya"
          ></iframe>
        </div>
      </div>

      {/* FAQ Section */}
      <div className="mt-20">
        <h2 className="text-3xl md:text-4xl font-extrabold text-center text-white mb-8">
          Frequently Asked Questions
        </h2>
        <Faqs faqs={faqs} />
      </div>
    </section>
  );
}
