export const SITE = {
  website: "https://olam-ha-ai.vercel.app/", // replace after Vercel deploy
  author: "עולם ה AI",
  profile: "",
  desc: "בלוג על כלי AI חדשים והסברים נגישים בעברית",
  title: "עולם ה AI",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: false,
    text: "ערוך דף",
    url: "",
  },
  dynamicOgImage: true,
  dir: "rtl", // "rtl" | "auto"
  lang: "he", // html lang code. Set this empty and default will be "en"
  timezone: "Asia/Jerusalem", // Default global timezone (IANA format)
} as const;
