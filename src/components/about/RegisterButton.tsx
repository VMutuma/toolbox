"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { FiChevronDown } from "react-icons/fi";

interface RegisterButtonProps {
    aboutInView: boolean;
  }
  
  export default function RegisterButton({ aboutInView }: RegisterButtonProps) {
    const [showOptions, setShowOptions] = useState(false);
  
    const toggleOptions = () => setShowOptions(!showOptions);
  
    return (
      <div className="relative">
        {/* Main Button */}
        <motion.button
          className="flex items-center px-8 py-4 rounded-full text-lg font-medium relative z-10"
          style={{
            background: "linear-gradient(rgba(227, 5, 140, 1), rgba(255, 129, 114, 1))",
          }}
          onClick={toggleOptions}
          initial={{ opacity: 0 }}
          animate={{ opacity: aboutInView ? 1 : 0 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          REGISTER NOW
          <FiChevronDown className="text-xl ml-2" />
        </motion.button>
  
        {/* Dropdown Menu */}
        {showOptions && (
          <motion.div
            className="absolute top-14 left-0 bg-white text-black rounded-lg shadow-lg w-60"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <ul className="p-2 space-y-2">
              <li>
                <a
                  href="https://mail.google.com/mail/?view=cm&fs=1&to=info@igamingexpo.africa&su=Registration%20for%20iGaming%20Expo%202025&body=Register%20me%20now!"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block px-4 py-2 hover:bg-gray-100 rounded-lg"
                >
                  Gmail
                </a>
              </li>
              <li>
                <a
                  href="https://outlook.office.com/mail/deeplink/compose?to=info@igamingexpo.africa&subject=Registration%20for%20iGaming%20Expo%202025&body=Register%20me%20now!"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block px-4 py-2 hover:bg-gray-100 rounded-lg"
                >
                  Outlook
                </a>
              </li>
              <li>
                <a
                  href="mailto:info@igamingexpo.africa?subject=Registration%20for%20iGaming%20Expo%202025&body=Register%20me%20now!"
                  className="block px-4 py-2 hover:bg-gray-100 rounded-lg"
                >
                  Apple Mail
                </a>
              </li>
            </ul>
          </motion.div>
        )}
      </div>
    );
  }
  
