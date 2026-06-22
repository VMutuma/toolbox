function page() {
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Our offices
          </h2>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Give us a call or drop by anytime, we endeavour to answer all
            enquiries within 24 hours on business days. We will be happy to
            answer your questions.
          </p>
        </div>
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 text-base leading-7 sm:grid-cols-2 sm:gap-y-16 lg:mx-0 lg:max-w-none lg:grid-cols-4">
          <div>
            <h3 className="border-l border-indigo-600 pl-6 font-semibold text-gray-900">
              Nairobi
            </h3>
            <address className="border-l border-gray-200 pl-6 pt-2 not-italic text-gray-600">
              <p>The Atrium, Chaka Road. Nairobi.</p>
              <p> +254 727 175 849</p>
              <p>info@suss.co.ke</p>
            </address>
          </div>
          <div>
            <h3 className="border-l border-indigo-600 pl-6 font-semibold text-gray-900">
              Ras Al Khaima, United Arabs Emirates.
            </h3>
            <address className="border-l border-gray-200 pl-6 pt-2 not-italic text-gray-600">
              <p>Suss Digital FZ-LLC, FDBC1756,</p>
              <p>Compass Building, Al Shohada Road,</p>
              <p>Al Hamra Industrial Zone-FZ,</p>
            </address>
          </div>
        </div>
      </div>
    </div>
  );
}

export default page;
