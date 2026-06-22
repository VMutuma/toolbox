/* eslint-disable @next/next/no-img-element */
"use client";

import React, { useState } from "react";
import { FiMenu, FiX } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";

// Type for navigation items
interface NavItem {
  label: string;
  link: string;
  dropdown?: NavItem[];
  subDropdown?: NavItem[];
}

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [hoveredSubDropdown, setHoveredSubDropdown] = useState<string | null>(null);

  // Navigation Items with dropdowns
  const navItems: NavItem[] = [
    {
      label: "About",
      link: "#about",
      dropdown: [
        { label: "About us", link: "#about-expo" },
        { label: "Venue", link: "#venue" },
        { label: "FAQs", link: "#faqs" },
      ],
    },
    {
      label: "Exhibit/Sponsor",
      link: "#floorplan",
      dropdown: [
        { label: "Floor Plan", link: "#floor-plan" },
        { label: "Exhibitors", link: "#exhibitors" },
        { label: "Sponsors", link: "#sponsors" },
        {
          label: "Partners",
          subDropdown: [
            { label: "Strategic", link: "#strategic-partners" },
            { label: "Media", link: "#media-partners" },
            { label: "Other", link: "#other-partners" },
          ],
          link: "",
        },
      ],
    },
    {
      label: "Conference",
      link: "#speakers",
      dropdown: [
        { label: "Agenda", link: "#agenda" },
        { label: "Speakers", link: "#speakers" },
        { label: "Become a Speaker", link: "#become-speaker" },
        { label: "Safari Experience", link: "#safari-experience" },
      ],
    },
    {
      label: "Awards",
      link: "#footer",
      dropdown: [
        { label: "Awards Dinner", link: "#awards-dinner" },
        { label: "Nominees", link: "#nominees" },
        { label: "Sponsors/Partners", link: "#sponsors-partners" },
        { label: "Winners", link: "#winners" },
      ],
    },
  ];

  // Animation Variants
  const navItemVariants = {
    hidden: { opacity: 0, y: -10 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: { delay: i * 0.1, duration: 0.5 },
    }),
  };

  const dropdownVariants = {
    hidden: { opacity: 0, y: -10, scale: 0.95 },
    visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.3 } },
  };

  const subDropdownVariants = {
    hidden: { opacity: 0, x: -10, scale: 0.95 },
    visible: { opacity: 1, x: 0, scale: 1, transition: { duration: 0.3 } },
  };

  return (
    <header className="absolute top-0 left-0 w-full z-20">
      {/* Top Header */}
      <motion.div
        className="flex items-center justify-between px-8 py-4 bg-transparent"
        initial="hidden"
        animate="visible"
      >
        <motion.div
          className="flex items-center space-x-2"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0, transition: { duration: 0.5 } }}
        >
          <img src="logo.png" alt="iGaming Logo" className="h-8 w-8" />
          <span className="text-xl font-bold text-white">
            IGaming <br /> Expo Africa
          </span>
        </motion.div>

        {/* Buttons */}
        <motion.div
          className="hidden md:flex items-center space-x-4"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0, transition: { duration: 0.5 } }}
        >
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="px-4 py-2 border border-white rounded-full text-white"
          >
            Sponsor/Exhibit
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="px-4 py-2 text-white rounded-full"
            style={{
              background: "linear-gradient(rgba(227, 5, 140, 1), rgba(255, 129, 114, 1))",
            }}
          >
            Get Tickets
          </motion.button>
        </motion.div>

        {/* Hamburger Icon */}
        <motion.button
          whileHover={{ scale: 1.2 }}
          className="md:hidden text-white text-2xl"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle Menu"
        >
          {isMenuOpen ? <FiX /> : <FiMenu />}
        </motion.button>
      </motion.div>

      {/* Desktop Navigation */}
      <nav className="hidden md:flex justify-around items-center py-4 bg-gradient-to-r from-pink-500 to-orange-500 shadow-lg">
        {navItems.map((item, index) => (
          <motion.div
            key={item.label}
            className="relative group"
            onMouseEnter={() => setActiveDropdown(item.label)}
            onMouseLeave={() => {
              setActiveDropdown(null);
              setHoveredSubDropdown(null);
            }}
            custom={index}
            initial="hidden"
            animate="visible"
            variants={navItemVariants}
          >
            <a
              href={item.link}
              className="text-white text-lg font-semibold hover:text-gray-300"
            >
              {item.label}
            </a>
            {item.dropdown && activeDropdown === item.label && (
              <motion.div
                className="absolute left-0 top-8 flex flex-col bg-pink-600 text-white rounded-md shadow-lg p-4"
                initial="hidden"
                animate="visible"
                exit="hidden"
                variants={dropdownVariants}
              >
                {item.dropdown.map((dropdownItem) =>
                  dropdownItem.subDropdown ? (
                    <div
                      key={dropdownItem.label}
                      className="relative group"
                      onMouseEnter={() => setHoveredSubDropdown(dropdownItem.label)}
                      onMouseLeave={() => setHoveredSubDropdown(null)}
                    >
                      <span className="block px-4 py-2 hover:bg-pink-700 cursor-pointer">
                        {dropdownItem.label}
                      </span>
                      {hoveredSubDropdown === dropdownItem.label && (
                        <motion.div
                          className="absolute left-full top-0 flex flex-col bg-orange-600 text-white rounded-md shadow-lg p-4"
                          initial="hidden"
                          animate="visible"
                          exit="hidden"
                          variants={subDropdownVariants}
                        >
                          {dropdownItem.subDropdown.map((subItem) => (
                            <a
                              key={subItem.label}
                              href={subItem.link}
                              className="block px-4 py-2 hover:bg-pink-600"
                            >
                              {subItem.label}
                            </a>
                          ))}
                        </motion.div>
                      )}
                    </div>
                  ) : (
                    <a
                      key={dropdownItem.label}
                      href={dropdownItem.link}
                      className="block px-4 py-2 hover:bg-pink-700"
                    >
                      {dropdownItem.label}
                    </a>
                  )
                )}
              </motion.div>
            )}
          </motion.div>
        ))}
      </nav>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            className="md:hidden flex flex-col space-y-4 px-6 py-4 bg-gradient-to-r from-pink-500 to-orange-500 text-white"
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
          >
            {navItems.map((item) => (
              <div key={item.label} className="flex flex-col">
                <button
                  onClick={() =>
                    setActiveDropdown(activeDropdown === item.label ? null : item.label)
                  }
                  className="text-lg font-semibold flex justify-between items-center w-full"
                >
                  {item.label}
                  {item.dropdown && (
                    <span>{activeDropdown === item.label ? "▲" : "▼"}</span>
                  )}
                </button>
                {item.dropdown && activeDropdown === item.label && (
                  <motion.div
                    className="ml-4 mt-2 flex flex-col space-y-2"
                    initial="hidden"
                    animate="visible"
                    exit="hidden"
                    variants={dropdownVariants}
                  >
                    {item.dropdown.map((dropdownItem) =>
                      dropdownItem.subDropdown ? (
                        <div key={dropdownItem.label}>
                          <button
                            onClick={() =>
                              setHoveredSubDropdown(
                                hoveredSubDropdown === dropdownItem.label
                                  ? null
                                  : dropdownItem.label
                              )
                            }
                            className="flex justify-between items-center w-full"
                          >
                            {dropdownItem.label}
                            <span>
                              {hoveredSubDropdown === dropdownItem.label ? "▲" : "▼"}
                            </span>
                          </button>
                          {hoveredSubDropdown === dropdownItem.label && (
                            <motion.div
                              className="ml-4 mt-2 flex flex-col space-y-2"
                              initial="hidden"
                              animate="visible"
                              exit="hidden"
                              variants={subDropdownVariants}
                            >
                              {dropdownItem.subDropdown.map((subItem) => (
                                <a
                                  key={subItem.label}
                                  href={subItem.link}
                                  className="hover:text-gray-300"
                                >
                                  {subItem.label}
                                </a>
                              ))}
                            </motion.div>
                          )}
                        </div>
                      ) : (
                        <a
                          key={dropdownItem.label}
                          href={dropdownItem.link}
                          className="hover:text-gray-300"
                        >
                          {dropdownItem.label}
                        </a>
                      )
                    )}
                  </motion.div>
                )}
              </div>
            ))}

            {/* Add Buttons */}
            <div className="flex flex-col space-y-4 mt-4">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="px-4 py-2 border border-white rounded-full text-white"
              >
                Sponsor/Exhibit
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="px-4 py-2 text-white rounded-full"
                style={{
                  background: "linear-gradient(rgba(227, 5, 140, 1), rgba(255, 129, 114, 1))",
                }}
              >
                Get Tickets
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
