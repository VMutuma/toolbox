"use client";

import React from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import RegisterButton from "./RegisterButton";

export default function About() {
  const { ref: aboutRef, inView: aboutInView } = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  const { ref: statsRef, inView: statsInView } = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  return (
    <motion.section
      className="relative bg-black text-white py-16"
      initial={{ opacity: 0 }}
      animate={{ opacity: aboutInView ? 1 : 0 }}
      transition={{ duration: 0.8 }}
      ref={aboutRef}
    >
      {/* About Menu */}
      <div id="about" className="relative bg-white rounded-t-lg py-4 w-[85%] mx-auto">
        <div className="absolute top-[80px] left-1/1 transform -translate-x-1/2 z-[2] hidden sm:block">
          <Image
            src="/Layer_2.png"
            alt="Layer Decorative Image"
            width={60}
            height={60}
            className="object-contain"
          />
        </div>

        {/* Menu Items */}
        <div className="container mx-auto flex flex-col sm:flex-row flex-wrap justify-around items-center space-y-4 sm:space-y-0 sm:space-x-4">
          {["SCHEDULE", "CONFERENCE AGENDA", "FLOOR PLAN", "ATTENDEES DOWNLOAD", "NEWS"].map(
            (item, index) => (
              <a
                key={index}
                href={`#${item.toLowerCase().replace(/ /g, "-")}`}
                className="text-pink-500  text-lg hover:underline text-center sm:text-left"
              >
                {item.split(" ").map((word, i) => (
                  <span
                    key={i}
                    className={word.toLowerCase() === "download" ? "text-sm block" : "block"}
                  >
                    {word}
                  </span>
                ))}
              </a>
            )
          )}
        </div>
      </div>

      {/* About Section */}
      <motion.div
        className="w-[85%] mx-auto flex flex-wrap md:flex-nowrap items-center mt-8 gap-8"
        initial={{ opacity: 0, x: -100 }}
        animate={{ opacity: aboutInView ? 1 : 0, x: aboutInView ? 0 : -100 }}
        transition={{ duration: 1 }}
      >
        <div className="w-full md:w-1/2 px-4 sm:px-8 md:px-20 space-y-8">
          <motion.h2
            className="text-3xl sm:text-4xl lg:text-5xl font-light leading-tight"
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: aboutInView ? 1 : 0, x: aboutInView ? 0 : -100 }}
            transition={{ delay: 0.3, duration: 1 }}
          >
            About <span className="font-extrabold">iGaming</span>
          </motion.h2>
          <motion.p
            className="text-lg text-gray-300 leading-8 max-w-[85%] md:max-w-[90%]"
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: aboutInView ? 1 : 0, x: aboutInView ? 0 : -100 }}
            transition={{ delay: 0.4, duration: 1 }}
          >
            The iGaming Expo Africa (IEA) 2025 is scheduled to take place from December 1<sup>st</sup> - 3<sup>rd</sup> in Nairobi, Kenya.
            IEA connects igaming operators, affiliates, tech vendors, and game providers in a networking environment to foster & create strong, trust-based partnerships that will drive business growth and secure competitive advantage.
            Bringing together solution providers and gaming professionals across all key verticals, suffice to say that IEA has something for everyone.
            More than 100 well-known companies from around the world will be on display, showcasing cutting-edge technology, cutting-edge games, and services that will change the game.
          </motion.p>

          {/* Register Button */}
          <RegisterButton aboutInView={aboutInView} />
        </div>

        <motion.div
          className="relative w-full md:w-1/2 flex justify-center md:justify-end"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: aboutInView ? 1 : 0, y: aboutInView ? 0 : 50 }}
          transition={{ duration: 1 }}
        >
          <div className="relative w-[600px]">
            <Image
              src="/Mask group 2.png"
              alt="Mask Decorative Image"
              width={600}
              height={600}
              className="object-contain"
            />
            <div className="absolute bottom-0 right-[-50px] z-[1]">
              <Image
                src="/logo.png"
                alt="Logo"
                width={90}
                height={90}
                className="object-contain opacity-90"
                style={{
                  transform: "translateY(25%)",
                }}
              />
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Stats Section */}
      <motion.div
        className="mt-16"
        ref={statsRef}
        initial={{ opacity: 0 }}
        animate={{ opacity: statsInView ? 1 : 0 }}
        transition={{ duration: 1 }}
      >
        <div
          className="mx-auto bg-gradient-to-r from-pink-500 to-orange-500 rounded-3xl p-8"
          style={{ width: "75%" }}
        >
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 gap-8 text-center text-white">
            {[{ number: "5.5K", description: " DELEGATES" }, { number: "550", description: " OPERATORS" }, { number: "110+", description: "SPEAKERS" }, { number: "100+", description: "EXHIBITORS & SPONSORS" }, { number: "150", description: "AFFILIATES" }, { number: "62%", description: "C-LEVELS" }].map(
              (stat, index) => (
                <motion.div
                  key={index}
                  className="flex flex-col items-center justify-center space-y-2"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: statsInView ? 1 : 0 }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                >
                  <p className="text-4xl sm:text-3xl md:text-4xl font-bold">{stat.number}</p>
                  <p className="text-sm sm:text-base">{stat.description}</p>
                </motion.div>
              )
            )}
          </div>
        </div>
      </motion.div>
    </motion.section>
  );
}
