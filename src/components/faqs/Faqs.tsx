"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

  

  export default function Faqs({ faqs }: { faqs: { question: string; answer: string }[] }) {
    const [openIndex, setOpenIndex] = useState<number | null>(null);
  
    const toggleFAQ = (index: number) => {
      setOpenIndex(openIndex === index ? null : index);
    };
  
    return (
      <section className="bg-gray-100 py-10 px-6 md:px-20" id="faqs">
        {/* <h2 className="text-3xl md:text-4xl font-bold text-center text-">
          Frequently Asked Questions
        </h2> */}
        <br/>
        <div className="max-w-4xl mx-auto space-y-6">
          {faqs.map((faq, index) => (
            <div key={index} className="border-b border-gray-300 pb-4">
              <button
                className="w-full text-left flex justify-between items-center text-lg md:text-xl font-medium text-gray-700 hover:text-pink-600 transition"
                onClick={() => toggleFAQ(index)}
              >
                {faq.question}
                <motion.span
                  animate={{ rotate: openIndex === index ? 180 : 0 }}
                  className="text-pink-600"
                >
                  ▼
                </motion.span>
              </button>
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden mt-2"
                  >
                    <p className="text-gray-600 text-base md:text-lg">{faq.answer}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </section>
    );
  }
  