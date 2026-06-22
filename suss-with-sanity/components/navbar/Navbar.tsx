'use client';
import { Dialog, Disclosure, Popover, Transition } from '@headlessui/react';
import {
  ChevronDownIcon,
  FingerPrintIcon,
  PhoneIcon,
  SquaresPlusIcon,
} from '@heroicons/react/20/solid';
import {
  Bars3Icon,
  ChartPieIcon,
  CursorArrowRaysIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import Image from 'next/image';
import Link from 'next/link';
import { Fragment, useState } from 'react';

const products = [
  {
    name: 'Suss Ads',
    description:
      'Connect with your audience with the world’s leading customer engagement platforms.',
    href: '/products/sussads',
    icon: ChartPieIcon,
  },
  {
    name: 'Suss SMS',
    description:
      'We connect brands with customers through an affordable, faster, secure, and reliable messaging solution.',
    href: '/products/susssms',
    icon: CursorArrowRaysIcon,
  },
  {
    name: 'Suss Agency',
    description:
      'Increases your sales and leads ultimately giving you not less than 100% return on investment on your digital marketing investment.',
    href: '/products/sussagency',
    icon: FingerPrintIcon,
  },
  {
    name: 'Suss Tracker',
    description: 'Connect with third-party tools',
    href: '/products/susstracker',
    icon: SquaresPlusIcon,
  },
];
const callsToAction = [{ name: 'Contact sales', href: '#', icon: PhoneIcon }];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);

  return (
    <header className="bg-white">
      <nav
        className="mx-auto flex max-w-8xl items-center justify-between p-6 lg:px-8"
        aria-label="Global"
      >
        <div className="flex lg:flex-1">
          <Link href="/" className="-m-1.5 p-1.5">
            <span className="sr-only">Suss Ads</span>
            <Image
              className="h-10 w-auto"
              src="/images/suss-logo.png"
              height={200}
              width={200}
              alt="Suss Ads"
            />
          </Link>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <Popover.Group className="hidden lg:flex lg:gap-x-12">
          <Link
            href="/"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Home
          </Link>
          <Link
            href="/about"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            About Us
          </Link>
          <Popover className="relative">
            <Popover.Button
              onClick={() => setIsPopoverOpen(!isPopoverOpen)}
              className="flex items-center gap-x-1 text-sm font-semibold leading-6 text-gray-900"
            >
              Product
              <ChevronDownIcon
                className="h-5 w-5 flex-none text-gray-400"
                aria-hidden="true"
              />
            </Popover.Button>

            <Transition
              as={Fragment}
              show={isPopoverOpen}
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <Popover.Panel className="absolute -left-8 top-full z-10 mt-3 w-screen max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
                <div className="p-4">
                  {products.map((item) => (
                    <div
                      key={item.name}
                      onClick={() => setIsPopoverOpen(false)}
                      className="group relative flex items-center gap-x-6 rounded-lg p-4 text-sm leading-6 hover:bg-gray-50"
                    >
                      <div className="flex h-11 w-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white">
                        <item.icon
                          className="h-6 w-6 text-gray-600 group-hover:text-indigo-600"
                          aria-hidden="true"
                        />
                      </div>
                      <div className="flex-auto">
                        <Link
                          href={item.href}
                          className="block font-semibold text-gray-900"
                        >
                          {item.name}
                          <span className="absolute inset-0" />
                        </Link>
                        <p className="mt-1 text-gray-600">{item.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="grid grid-cols-2 divide-x divide-gray-900/5 bg-gray-50">
                  {callsToAction.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="flex items-center justify-center gap-x-2.5 p-3 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-100"
                    >
                      <item.icon
                        className="h-5 w-5 flex-none text-gray-400"
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  ))}
                </div>
              </Popover.Panel>
            </Transition>
          </Popover>
          <Link
            href="/process"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Our Process
          </Link>
          <Link
            href="/work"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Case Studies
          </Link>
          <Link
            href="/sussnextgen"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Suss NextGen
          </Link>
          <Link
            href="/blog"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Blogs
          </Link>
          <Link
            href="/contactus"
            className="text-sm font-semibold leading-6 text-gray-900"
          >
            Contact Us
          </Link>
        </Popover.Group>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end">
          <Link
            // href="mailto:info@suss.co.ke?subject=Book%20Demo&body=Hello%20Suss%20Ads%20Team,%0D%0A%0D%0AI%20am%20interested%20in%20booking%20a%20demo%20of%20your%20services.%20Could%20you%20please%20schedule%20a%20demo%20for%20me%20at%20your%20earliest%20convenience?%0D%0A%0D%0AThank%20you.%0D%0A%0D%0AKind%20regards,"
            href="/bookdemo"
            className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
          >
            Book Demo
          </Link>
          <Link
            href="https://ads.suss.co.ke/api/auth/login"
            target="_blank"
            className="bg-white ml-3 border border-sussBlue text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
          >
            Login
          </Link>
        </div>
      </nav>
      <Dialog
        as="div"
        className="lg:hidden"
        open={mobileMenuOpen}
        onClose={setMobileMenuOpen}
      >
        <div className="fixed inset-0 z-10" />
        <Dialog.Panel className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
          <div className="flex items-center justify-between">
            <Link href="/" className="-m-1.5 p-1.5">
              <span className="sr-only">Suss Ads</span>
              <Image
                className="h-10 w-auto"
                src="/images/suss-logo.png"
                height={200}
                width={200}
                alt="Suss Ads"
              />
            </Link>
            <button
              type="button"
              className="-m-2.5 rounded-md p-2.5 text-gray-700"
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="sr-only">Close menu</span>
              <XMarkIcon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div className="mt-6 flow-root">
            <div className="-my-6 divide-y divide-gray-500/10">
              <div className="space-y-2 py-6">
                <Link
                  href="/"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Home
                </Link>
                <Link
                  href="/about"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  About Us
                </Link>
                <Disclosure as="div" className="-mx-3">
                  {({ open }) => (
                    <>
                      <Disclosure.Button className="flex w-full items-center justify-between rounded-lg py-2 pl-3 pr-3.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                        Product
                        <ChevronDownIcon
                          className={classNames(
                            open ? 'rotate-180' : '',
                            'h-5 w-5 flex-none'
                          )}
                          aria-hidden="true"
                        />
                      </Disclosure.Button>
                      <Disclosure.Panel className="mt-2 space-y-2">
                        {[...products, ...callsToAction].map((item) => (
                          <Disclosure.Button
                            key={item.name}
                            as="a"
                            href={item.href}
                            className="block rounded-lg py-2 pl-6 pr-3 text-sm font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                          >
                            {item.name}
                          </Disclosure.Button>
                        ))}
                      </Disclosure.Panel>
                    </>
                  )}
                </Disclosure>
                <Link
                  href="/process"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Our Process
                </Link>
                <Link
                  href="/work"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Case Studies
                </Link>
                <Link
                  href="/sussnextgen"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Suss NextGen
                </Link>
                <Link
                  href="/blog"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Blogs
                </Link>
                <Link
                  href="/contactus"
                  onClick={() => {
                    setMobileMenuOpen(false);
                  }}
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                >
                  Contact Us
                </Link>
              </div>
              <div className="py-6">
                <Link
                  // href="mailto:info@suss.co.ke?subject=Book%20Demo&body=Hello%20Suss%20Ads%20Team,%0D%0A%0D%0AI%20am%20interested%20in%20booking%20a%20demo%20of%20your%20services.%20Could%20you%20please%20schedule%20a%20demo%20for%20me%20at%20your%20earliest%20convenience?%0D%0A%0D%0AThank%20you.%0D%0A%0D%0AKind%20regards,"
                  href="/bookdemo"
                  className="bg-sussYellow border text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
                >
                  Book Demo
                </Link>
                <Link
                  href="https://ads.suss.co.ke/api/auth/login"
                  target="_blank"
                  className="bg-white ml-3 border border-sussBlue text-sm font-semibold rounded-full text-sussBlue hover:border hover:border-sussBlue hover:bg-white  px-5 py-2.5 text-center inline-flex items-center hover:shadow-lg"
                >
                  Login
                </Link>
              </div>
            </div>
          </div>
        </Dialog.Panel>
      </Dialog>
    </header>
  );
}
