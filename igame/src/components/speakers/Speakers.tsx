"use client";

import React from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

interface Speaker {
  name: string;
  title: string;
  image: string;
  company: string;
}

export default function Speakers() {
  const speakers: Speaker[] = [
    {
      name: "Jeremiah Maangi",
      title: "Founder/CEO",
      company: "iGaming AFRIKA",
      image: "/Jeremiah_Maangi.jpg",
    },
    {
      name: "Geoffrey Muindi",
      title: "CEO",
      company: "Dive Marketing",
      image: "/Geoffrey_Muindi.jpg",
    },
    {
      name: "Dennis Maina",
      title: "Managing Partner",
      company: "Suss Digital Africa",
      image: "/Dennis_Maina.jpg",
    },
  ];

  return (
    <motion.section
      className="relative py-16 bg-white"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      {/* Decorative Pattern Top */}
      <div className="absolute top-0 w-full h-12 bg-[url('/layer_4.png')] bg-repeat"></div>

      {/* Section Content */}
      <div className="relative container mx-auto px-6 lg:px-12">
        {/* Section Title */}
        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-light text-pink-500 text-left mb-12">
          Featured <span className="font-extrabold">Speakers</span>
        </h2>

        {/* Speakers Grid */}
        <motion.div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: { opacity: 0 },
            visible: {
              opacity: 1,
              transition: {
                staggerChildren: 0.3,
                duration: 0.8,
              },
            },
          }}
        >
          {speakers.map((speaker, index) => (
            <SpeakerCard key={index} speaker={speaker} />
          ))}
        </motion.div>

        {/* See More Speakers Button */}
        <div id="speakers" className="flex justify-center mt-20">
          <motion.button
            className="flex items-center justify-center gap-2 px-8 py-3 bg-gradient-to-r from-pink-500 to-orange-400 text-white text-lg font-bold rounded-full shadow-md hover:opacity-90"
            whileHover={{ scale: 1.05 }} // Button hover effect
            transition={{ duration: 0.3 }}
          >
            See More Speakers <span>&rarr;</span>
          </motion.button>
        </div>
      </div>

      {/* Decorative Pattern Bottom */}
      <div className="absolute bottom-0 w-full h-12 bg-[url('/layer_4.png')] bg-repeat"></div>
    </motion.section>
  );
}

interface SpeakerCardProps {
  speaker: Speaker;
}

const SpeakerCard: React.FC<SpeakerCardProps> = ({ speaker }) => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.3,
  });

  return (
    <motion.div
      ref={ref}
      className="relative bg-white border border-gray-200 rounded-xl p-6 text-center shadow-sm hover:shadow-lg transition-shadow z-10"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: inView ? 1 : 0, scale: inView ? 1 : 0.95 }}
      transition={{ duration: 0.8 }}
      whileHover={{ scale: 1.05 }}
    >
      {/* Profile Image */}
      <div className="relative mx-auto w-24 h-24 sm:w-32 sm:h-32 rounded-full overflow-hidden mb-4">
        <Image
          src={speaker.image}
          alt={`${speaker.name}'s Image`}
          layout="fill"
          objectFit="cover"
        />
      </div>

      {/* Speaker Info */}
      <p className="text-sm sm:text-base font-medium text-gray-500 uppercase mb-2">
      </p>
      <h3 className="text-xl sm:text-2xl font-semibold text-gray-800 mb-2">
        {speaker.name}
      </h3>
      <p className="text-gray-600 text-sm sm:text-base font-light">{speaker.title}</p>
      <p className="text-gray-600 text-sm sm:text-base font-light">{speaker.company}</p>

      {/* Read More */}
      {/* <div className="flex items-center justify-center mt-4">
        <a
          href="#"
          className="text-pink-500 font-medium text-sm sm:text-base hover:underline"
        >
          Read More
        </a>
        <span
          className="ml-2 flex items-center justify-center w-8 h-8 rounded-full text-pink-500 text-lg font-bold bg-gradient-to-r from-pink-500 to-orange-400 p-[2px]"
        >
          <span className="flex items-center justify-center w-full h-full rounded-full bg-white">
            +
          </span>
        </span>
      </div> */}

      {/* Logo beneath first speaker */}
      {speaker.name === "John Doe" && (
        <div className="absolute -bottom-6 left-1 transform -translate-x-1/2 z-0">
          <Image
            src="/logo.png"
            alt="Event Logo"
            width={40}
            height={40}
            className="max-w-full"
          />
        </div>
      )}
    </motion.div>
  );
};
