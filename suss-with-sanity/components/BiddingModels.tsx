import {
  BanknotesIcon,
  CheckBadgeIcon,
  ClockIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';

const actions = [
  {
    title: 'CPM',
    href: '#',
    icon: ClockIcon,
    iconForeground: 'text-teal-700',
    iconBackground: 'bg-teal-50',
    description:
      'Generate sustainable volumes of traffic or target placements that deliver high conversion rates for you via whitelisting.',
  },
  {
    title: 'CPC',
    href: '#',
    icon: CheckBadgeIcon,
    iconForeground: 'text-purple-700',
    iconBackground: 'bg-purple-50',
    description:
      'Pay only for the users that have already expressed some interest in your product by clicking on the ad.',
  },
  {
    title: 'CPA',
    href: '#',
    icon: UsersIcon,
    iconForeground: 'text-sky-700',
    iconBackground: 'bg-sky-50',
    description:
      'Built atop of CPM/CPC bidding, while the system is finding converting traffic according to the desired CPA and targeting.',
  },
  {
    title: 'SMART CPM',
    href: '#',
    icon: BanknotesIcon,
    iconForeground: 'text-yellow-700',
    iconBackground: 'bg-yellow-50',
    description:
      'We bid for you based on an algorithm that automatically finds the best possible prices (CPM) for each ad placement.',
  },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export default function BiddingModels() {
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">
            Bidding Models
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Smart Bidding Models
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Innovative bidding models
          </p>
        </div>
        <div className="divide-y divide-gray-200 overflow-hidden rounded-lg sm:grid sm:grid-cols-4 sm:gap-px sm:divide-y-0">
          {actions.map((action, actionIdx) => (
            <div
              key={action.title}
              className={classNames(
                actionIdx === 0
                  ? 'rounded-tl-lg rounded-tr-lg sm:rounded-tr-none'
                  : '',
                actionIdx === 1 ? 'sm:rounded-tr-lg' : '',
                actionIdx === actions.length - 2 ? 'sm:rounded-bl-lg' : '',
                actionIdx === actions.length - 1
                  ? 'rounded-bl-lg rounded-br-lg sm:rounded-bl-none'
                  : '',
                'group relative bg-white m-3 p-6 focus-within:ring-2 shadow hover:shadow-lg focus-within:ring-inset focus-within:ring-indigo-500'
              )}
            >
              <div>
                <span
                  className={classNames(
                    action.iconBackground,
                    action.iconForeground,
                    'inline-flex rounded-lg p-3 ring-4 ring-white'
                  )}
                >
                  <action.icon className="h-6 w-6" aria-hidden="true" />
                </span>
              </div>
              <div className="mt-8">
                <h3 className="text-base font-semibold leading-6 text-gray-900">
                  <span className="absolute inset-0" aria-hidden="true" />
                  {action.title}
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  {action.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
