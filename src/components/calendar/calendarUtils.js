// components/calendar/calendarUtils.js

export const getBaseUrl = () => {
    return process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000";
  };
  
  // Generate Google Calendar URL
  export const generateGoogleCalendarLink = () => {
    const baseURL = "https://calendar.google.com/calendar/render";
    const params = new URLSearchParams({
      action: "TEMPLATE",
      text: "iGaming Expo Africa",
      details: "Join the premier iGaming Expo in Africa at Sarit Centre, Nairobi, Kenya.",
      location: "Sarit Centre, Nairobi, Kenya",
      dates: "20251201T090000Z/20251203T180000Z",
    });
  
    return `${baseURL}?${params.toString()}`;
  };
  
  // Generate Outlook Calendar URL
  export const generateOutlookCalendarLink = () => {
    const baseURL = "https://outlook.live.com/calendar/0/deeplink/compose";
    const params = new URLSearchParams({
      path: "/calendar/action/compose",
      subject: "iGaming Expo Africa",
      body: "Join the premier iGaming Expo in Africa at Sarit Centre, Nairobi, Kenya.",
      location: "Sarit Centre, Nairobi, Kenya",
      startdt: "2025-12-01T09:00:00",
      enddt: "2025-12-03T18:00:00",
    });
  
    return `${baseURL}?${params.toString()}`;
  };
  
  // Generate iOS Calendar ICS file URL
  export const generateICSFileLink = () => {
    return `${getBaseUrl()}/igaming-expo.ics`; 
  };
  