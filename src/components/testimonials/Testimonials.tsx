"use client";

import React from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

interface Testimonial {
  name: string;
  title: string;
  image: string;
  text: string;
}

const testimonials: Testimonial[] = [
  {
    name: "Brian Ondieki",
    title: "Executive Director - Bizin Africa iGaming Consult",
    image: "/Brian_Ondieki.jpg",
    text: "The iGaming Expo Africa Summit is a groundbreaking event that brought together leaders from across the continent. The networking opportunities were unparalleled, and the insights shared have transformed the way we do business in the gaming sector.",
  },
  {
    name: "Job Weku",
    title: "Business Development Manager Africa - Fazi",
    image: "/Job_Weku.jpg",
    text: "Attending the iGaming Expo was the best decision we made for our business. The workshops, panel discussions, and expert sessions were not only enlightening but also actionable. We look forward to next year!",
  },
]; 

export default function Testimonials() {
  return (
    <section id="testimonials" className="relative bg-black py-16">
      {/* Background Design */}
      <motion.div
        className="absolute top-5 left-[-30px] h-full w-[300px]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2 }}
      >
        <Image
          src="/layer_5.png"
          alt="Background Pattern"
          layout="intrinsic"
          width={250}
          height={250}
        />
      </motion.div>

      {/* Section Content */}
      <div className="relative container mx-auto px-6 lg:px-12">
        {/* Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 1 }}
        >
          <h4 className="text-2xl sm:text-3xl lg:text-5xl text-white tracking-wide">
            Don’t take our word for it.
          </h4>
          <p className="text-xl sm:text-2xl lg:text-5xl text-white mt-2 tracking-widest">
            Here’s what our clients have to say.
          </p>
        </motion.div>

        {/* Testimonial Cards */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-6 justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 1.2 }}
        >
          {testimonials.map((testimonial, index) => (
            <TestimonialCard key={index} testimonial={testimonial} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}

const TestimonialCard: React.FC<{ testimonial: Testimonial }> = ({ testimonial }) => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.3,
  });

  return (
    <motion.div
      ref={ref}
      className="relative bg-white rounded-xl shadow-md p-8 sm:p-12 lg:p-16 max-w-xl mx-auto"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: inView ? 1 : 0, y: inView ? 0 : 50 }}
      transition={{ duration: 0.8 }}
    >
      {/* Profile Section */}
      <motion.div
        className="flex flex-col sm:flex-row items-center mb-6"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: inView ? 1 : 0, x: inView ? 0 : -50 }}
        transition={{ duration: 0.8 }}
      >
        <motion.div
          className="w-24 h-24 sm:w-32 sm:h-32 rounded-full overflow-hidden"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: inView ? 1 : 0, scale: inView ? 1 : 0.8 }}
          transition={{ duration: 0.6 }}
        >
          <Image
            src={testimonial.image}
            alt={`${testimonial.name}'s photo`}
            width={128}
            height={128}
            className="object-cover"
          />
        </motion.div>

        <motion.div
          className="ml-5 mt-4 sm:mt-0"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: inView ? 1 : 0, x: inView ? 0 : 50 }}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-2xl sm:text-3xl lg:text-4xl text-black">
            {testimonial.name}
          </h3>
          <p className="text-sm sm:text-lg text-pink-500">
            {testimonial.title}
          </p>
        </motion.div>
      </motion.div>

      {/* Testimonial Text */}
      <motion.p
        className="text-gray-700 leading-normal text-base sm:text-base"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: inView ? 1 : 0, y: inView ? 0 : 20 }}
        transition={{ duration: 0.8 }}
      >
        {testimonial.text}
      </motion.p>

      {/* Quotation Mark */}
      <motion.span
        className="absolute top-4 right-6 text-pink-500 text-6xl font-bold"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: inView ? 1 : 0, scale: inView ? 1 : 0.8 }}
        transition={{ duration: 0.6 }}
      >
        &rdquo;
      </motion.span>
    </motion.div>
  );
};
