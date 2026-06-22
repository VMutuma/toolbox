"use client";

import React from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

export default function FloorPlan() {
  const { ref: headerRef, inView: headerInView } = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  const { ref: sponsorsRef, inView: sponsorsInView } = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  // Sponsors array with image and website URL
  const sponsors = [
    { name: "suss", image: "/suss.png", website: "https://suss.co.ke/?utm_source=igaming&utm_medium=sponsorlogo" },
    { name: "igaming", image: "/igaming.png", website: "#" },
    // Add more sponsors here
  ];

  return (
    <section id="floorplan" className="relative bg-black text-white py-16 overflow-hidden">
      {/* Decorative Layer */}
      <motion.div
        className="absolute top-[720px] right-[-20%] z-0 w-[900px] h-[900px] overflow-hidden pointer-events-none"
        style={{
          transform: "translateX(-12%)",
        }}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: headerInView ? 1 : 0 }}
        transition={{ duration: 1 }}
      >
        <Image
          src="/Layer_3.png"
          alt="Decorative Layer"
          layout="intrinsic"
          width={700}
          height={700}
          objectFit="cover"
        />
      </motion.div>

      {/* Content Section */}
      <div className="relative z-10 w-[90%] mx-auto">
        {/* Header Section */}
        <motion.div
          className="flex flex-wrap md:flex-nowrap items-start gap-8 p-8 rounded-lg"
          style={{
            background: "linear-gradient(135deg, rgba(227,5,140,1) 0%, rgba(255,129,114,1) 100%)",
          }}
          ref={headerRef}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: headerInView ? 1 : 0, y: headerInView ? 0 : 50 }}
          transition={{ duration: 1 }}
        >
          {/* Text Section */}
          <div className="w-full md:w-1/3 flex flex-col justify-center">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4 text-white">Floor Plan</h2>
            <p className="text-white text-opacity-90 leading-relaxed font-light mb-6">
              Explore the detailed layout of the event floor, including exhibitor booths, networking lounges,
              and more. Click below to download the complete floor plan.
            </p>
            <motion.ul
              className="space-y-4 text-white"
              initial="hidden"
              animate={headerInView ? "visible" : "hidden"}
              variants={{
                hidden: { opacity: 0, y: 50 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: {
                    staggerChildren: 0.2,
                    duration: 0.8,
                  },
                },
              }}
            >
              {[...Array(10)].map((_, index) => (
                <motion.li
                  key={index}
                  className="flex justify-between items-center py-2 px-4 border-b border-white pb-1"
                  variants={{
                    hidden: { opacity: 0 },
                    visible: { opacity: 1 },
                  }}
                >
                  <span className="flex-1 tracking-wide font-light">YOUR HEADER GOES HERE</span>
                  <span>&rarr;</span>
                </motion.li>
              ))}
            </motion.ul>

            {/* Download Button */}
            <div className="mt-8 flex justify-center">
              <motion.a
                href="/floorplan.pdf"
                target="_blank"
                className="px-8 py-3 bg-gradient-to-r from-pink-500 to-orange-400 text-white font-bold text-lg rounded-full shadow-lg hover:opacity-90"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3 }}
              >
                VIEW FLOOR PLAN
              </motion.a>
            </div>
          </div>

          {/* Floor Plan Image Section */}
          <motion.div
            className="relative w-full md:w-2/3 flex justify-center items-center"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: headerInView ? 1 : 0.8, opacity: headerInView ? 1 : 0 }}
            transition={{ duration: 1 }}
          >
            <Image
              src="/Floor Plan.png"
              alt="Floor Plan"
              width={900}
              height={600}
              layout="intrinsic"
              objectFit="cover"
            />
          </motion.div>
        </motion.div>

        {/* Sponsors Section */}
        <motion.div
          className="relative mt-10 text-left"
          ref={sponsorsRef}
          initial={{ opacity: 0 }}
          animate={{ opacity: sponsorsInView ? 1 : 0 }}
          transition={{ duration: 1 }}
        >
          {/* Sponsors Container */}
          <div className="bg-white p-8 rounded-3xl shadow-lg">
            {/* Title */}
            <h3 className="text-3xl font-light text-pink-500 mb-8">Our Sponsors & Partners</h3>

            {/* Sponsors Grid */}
            <motion.div
              className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: sponsorsInView ? 1 : 0 }}
              transition={{ duration: 1 }}
            >
              {sponsors.map((sponsor, index) => (
                <motion.div
                  key={index}
                  className="flex justify-center items-center p-0 hover:scale-105 transition-transform"
                  whileHover={{ scale: 1.1 }}
                  transition={{ duration: 0.3 }}
                >
                  {/* Wrap Image with Anchor Tag */}
                  <a href={sponsor.website} target="_blank" rel="noopener noreferrer">
                    <Image
                      src={sponsor.image}
                      alt={`${sponsor.name} logo`}
                      width={75}
                      height={75}
                    />
                  </a>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
