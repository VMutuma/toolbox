"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { FaMapMarkerAlt } from "react-icons/fa";
import AddToCalendar from "../calendar/AddToCalendar";

// Define the type for the timeLeft state
interface TimeLeft {
  months: number;
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

export default function Hero() {
  const [timeLeft, setTimeLeft] = useState<TimeLeft>({
    months: 0,
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  const eventDate = new Date("2025-12-01T00:00:00");

  // Calculate the countdown
  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      const difference = eventDate.getTime() - now.getTime();

      const months = Math.floor(difference / (1000 * 60 * 60 * 24 * 30));
      const days = Math.floor((difference / (1000 * 60 * 60 * 24)) % 30);
      const hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((difference / (1000 * 60)) % 60);
      const seconds = Math.floor((difference / 1000) % 60);

      setTimeLeft({ months, days, hours, minutes, seconds });
    }, 1000);

    return () => clearInterval(timer);
  }, [eventDate]);

  // Animation Variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
  };

  const imageVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.8, ease: "easeOut" } },
  };

  return (
    <motion.section
      className="relative bg-gradient-to-br from-black via-gray-800 to-black text-white min-h-screen flex items-center overflow-hidden"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* Decorative Layer */}
      <motion.div
        className="absolute top-0 right-0 w-[300px] md:w-[400px] lg:w-[600px] pointer-events-none z-0 opacity-30" // Reduced visibility with opacity
        variants={imageVariants}
      >
        <Image
          src="/Layer_1.png"
          alt="Decorative Background Image"
          width={900}
          height={900}
          className="object-contain"
          priority
        />
      </motion.div>
      <div id="hero" className="absolute inset-0 bg-gradient-to-b from-black via-gray-900 to-black opacity-30 z-0"></div>
      {/* Main Content */}
      <div className="relative z-10 w-[90%] mx-auto px-6 lg:px-20 grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Left Content */}
        <motion.div
          className="space-y-6 max-w-xl mx-auto lg:mx-0 text-center lg:text-left pt-24 md:pt-17 lg:pt-24"
          variants={containerVariants}
        >
          {/* Event Date */}
          <motion.p
            className="text-3xl sm:text-4xl md:text-5xl font-bold text-white px-4 py-2 rounded-lg inline-block"
            variants={itemVariants}
          >
            1<sup>st</sup> - 3<sup>rd</sup> DEC 2025
          </motion.p>

          {/* Location Section */}
          <motion.div
            className="flex items-center justify-center lg:justify-start space-x-2 text-white px-4 py-2 rounded-lg inline-block"
            variants={itemVariants}
          >
            <FaMapMarkerAlt className="text-xl" />
            <p className="text-lg font-medium">Nairobi, Kenya - Sarit Centre</p>
          </motion.div>

          {/* Title */}
          <motion.h1
            className="text-4xl sm:text-5xl md:text-6xl font-bold leading-snug text-white px-4 py-2 rounded-lg"
            variants={itemVariants}
          >
            iGaming Expo Africa Summit
          </motion.h1>

          {/* Description */}
          <motion.p
            className="text-lg sm:text-xl font-light text-gray-300 px-4 py-2 rounded-lg"
            variants={itemVariants}
          >
            Africa&apos;s Ultimate iGaming Expo
          </motion.p>

          {/* Countdown Timer */}
          <motion.div
            className="flex flex-wrap justify-center lg:justify-start gap-4 mt-6"
            variants={itemVariants}
          >
            {Object.entries(timeLeft).map(([unit, value]) => (
              <div
                key={unit}
                className="flex flex-col items-center bg-gradient-to-r from-pink-500 to-orange-400 rounded-lg px-4 py-2 shadow-lg"
              >
                <span className="font-bold text-3xl">{value}</span>
                <span className="text-sm">{unit.toUpperCase()}</span>
              </div>
            ))}
          </motion.div>

          {/* Add to Calendar Button */}
          <motion.div
            className="flex justify-center lg:justify-start mt-8"
            variants={itemVariants}
          >
            <AddToCalendar />
          </motion.div>
        </motion.div>

        {/* Right-Side Hero Image */}
        <motion.div
          className="relative flex justify-center lg:justify-end"
          variants={imageVariants}
        >
          <Image
            src="/Mask group.png"
            alt="Hero Image"
            width={500}
            height={500}
            className="object-contain w-[250px] md:w-[400px] lg:w-[700px]"
            priority
          />
        </motion.div>
      </div>
    </motion.section>
  );
}
