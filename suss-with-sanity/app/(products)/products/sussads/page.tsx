import SussAds from '@/components/sussads/SussAds';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Suss Ads - Suss Digital',
  description:
    'Boost Engagement with Suss Ads: Push Notifications for direct messages, user-targeted events, and rapid delivery of 1M messages. Diverse Display Ads – Skyscraper, Rectangle, and more. Limitless Possibilities.',
};

export default function Page() {
  return <SussAds />;
}
