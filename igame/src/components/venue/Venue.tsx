"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link"; // For routing
import { motion } from "framer-motion";

export default function Venue() {
  return (
    <section id="venue" className="bg-black pt-12">
      <div className="flex justify-center items-center py-12 bg-white rounded-t-3xl border-t-8 border-white">
        <div className="flex flex-col md:flex-row items-center max-w-5xl mx-auto gap-8 px-6">
          {/* Left Side (Text) */}
          <motion.div
            className="text-center md:text-left md:w-1/2"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl font-light text-pink-500 mb-4">
              About <span className="text-pink-500 font-medium">Venue</span>
            </h2>
            <p className="text-gray-600 mb-4">
              The iGaming Expo Africa will be held at the Sarit Centre, a premier exhibition and conference venue located in the heart of Nairobi, Kenya.
            </p>
            <Link href="/event" passHref>
              <motion.a
                className="bg-gradient-to-r from-pink-500 to-orange-500 text-white py-3 px-8 rounded-full font-bold transition-transform transform inline-block text-center hover:scale-105"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3 }}
              > 
                GET TO EVENT <span className="ml-2">&rarr;</span>
              </motion.a>
            </Link>
          </motion.div>

          {/* Right Side (Image) */}
          <motion.div
            className="w-full md:w-1/2"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
          >
            <Image
              src="/venueNight.jpg"
              alt="Venue"
              width={800}
              height={650}
              className="rounded-xl shadow-lg"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
