"use client";

import { FaTwitter, FaYoutube, FaInstagram, FaGithub } from "react-icons/fa";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";

export default function Footer() {
  const footerRef = useRef<HTMLDivElement | null>(null); // Ensure it's typed correctly
  const isInView = useInView(footerRef, { margin: "-50px" });

  return (
    <footer
      ref={footerRef}
      id="footer"
      className="bg-gradient-to-r from-pink-500 to-orange-600 text-white py-12 relative"
    >
      <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-start gap-8">
        <motion.div
          className="w-full md:w-auto mb-8 md:mb-0"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-2xl font-bold mb-2">iGaming</h3>
          <p className="text-sm"></p>
        </motion.div>

        <motion.div
          className="grid grid-cols-2 gap-8 w-full md:grid-cols-5 md:gap-16 mt-8 md:mt-0"
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : {}}
          transition={{ duration: 1 }}
        >
          <FooterSection
            title="About"
            links={[
              { name: "About iGaming Expo", href: "#" },
              { name: "Venue", href: "#" },
              { name: "FAQs", href: "#" },
            ]}
            isInView={isInView}
            delay={0.2}
          />

          <FooterSection
            title="Exhibit/Sponsor"
            links={[
              { name: "Floor Plan", href: "#" },
              { name: "Exhibitors", href: "#" },
              { name: "Sponsors", href: "#" },
              { name: "Partners", href: "#" },
            ]}
            isInView={isInView}
            delay={0.4}
          />

          <FooterSection
            title="Conference"
            links={[
              { name: "Agenda", href: "#" },
              { name: "About Us", href: "#" },
              { name: "Team", href: "#" },
              { name: "Privacy", href: "#" },
            ]}
            isInView={isInView}
            delay={0.6}
          />

          <FooterSection
            title="Awards"
            links={[
              { name: "Awards Dinner", href: "#" },
              { name: "Nominees", href: "#" },
              { name: "Sponsor/Partners", href: "#" },
              { name: "Winners", href: "#" },
            ]}
            isInView={isInView}
            delay={0.8}
          />

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6, delay: 1 }}
          >
            <h4 className="text-lg font-semibold mb-4">Contact Us</h4>
            <p className="text-sm mb-4">
              <a href="mailto:info@igamingexpo.africa">info@igamingexpo.africa</a>
            </p>
            <div className="flex gap-4">
              <FooterIcon href="#" Icon={FaTwitter} />
              <FooterIcon href="#" Icon={FaYoutube} />
              <FooterIcon href="#" Icon={FaInstagram} />
              <FooterIcon href="#" Icon={FaGithub} />
            </div>
          </motion.div>
        </motion.div>
      </div>

      <motion.div
        className="border-t border-white/20 mt-8 pt-6 items-center text-sm px-6"
        initial={{ opacity: 0, y: 20 }}
        animate={isInView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.8 }}
      >
        <p className="text-center">
          All rights reserved. Copyright © 2024 iGaming Expo
        </p>
      </motion.div>

      {/* New section for Designed and Built by */}
      <motion.div
        className="mt-4 text-center text-sm"
        initial={{ opacity: 0, y: 20 }}
        animate={isInView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.6, delay: 1 }}
      >
        <p>
          Designed and Built by{" "}
          <a href="https://suss.co.ke/?utm_source=igaming&utm_medium=footer" target="_blank" rel="noopener noreferrer" className="text-white hover:underline">
            Suss Digital Africa Ltd (Suss Ads)
          </a>
        </p>
      </motion.div>
    </footer>
  );
}

// FooterSection component with type annotations for props
interface FooterSectionProps {
  title: string;
  links: { name: string; href: string }[];
  isInView: boolean;
  delay: number;
}

function FooterSection({ title, links, isInView, delay }: FooterSectionProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay }}
    >
      <h4 className="text-lg font-semibold mb-4">{title}</h4>
      <ul className="space-y-2 text-sm">
        {links.map((link, index) => (
          <li key={index}>
            <a href={link.href} className="hover:underline">
              {link.name}
            </a>
          </li>
        ))}
      </ul>
    </motion.div>
  );
}

// FooterIcon component with type annotations
interface FooterIconProps {
  href: string;
  Icon: React.ElementType; 
}

function FooterIcon({ href, Icon }: FooterIconProps) {
  return (
    <motion.a
      href={href}
      className="hover:text-gray-300"
      whileHover={{ scale: 1.1 }}
      transition={{ duration: 0.2 }}
    >
      <Icon />
    </motion.a>
  );
}
