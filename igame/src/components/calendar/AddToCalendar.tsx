"use client";

import React, { useState } from "react";
import { generateGoogleCalendarLink,
  //  generateOutlookCalendarLink, generateICSFileLink 
  } from "./calendarUtils";
import { motion } from "framer-motion";

export default function AddToCalendar() {
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  return (
    <div className="relative">
      {/* Main Add to Calendar Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setDropdownOpen((prev) => !prev)}
        className="px-4 py-2 bg-gradient-to-r from-pink-500 to-orange-500 text-white rounded-lg font-semibold"
      >
        Add to Calendar
      </motion.button>

      {/* Dropdown for Calendar Options */}
      {isDropdownOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="absolute mt-2 bg-white rounded-lg shadow-lg w-48 z-10"
        >
          <ul className="text-gray-800">
            <li>
              <a
                href={generateGoogleCalendarLink()}
                target="_blank"
                rel="noopener noreferrer"
                className="block px-4 py-2 hover:bg-gray-100"
              >
                Google Calendar
              </a>
            </li>
            {/* <li>
              <a
                href={generateOutlookCalendarLink()}
                target="_blank"
                rel="noopener noreferrer"
                className="block px-4 py-2 hover:bg-gray-100"
              >
                Outlook
              </a>
            </li>
            <li>
              <a
                href={generateICSFileLink()}
                download
                className="block px-4 py-2 hover:bg-gray-100"
              >
                iOS Calendar (ICS)
              </a>
            </li> */}
          </ul>
        </motion.div>
      )}
    </div>
  );
}
