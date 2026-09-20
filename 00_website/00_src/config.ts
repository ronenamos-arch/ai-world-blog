export const SITE = {
  website: "https://ai-world-blog.vercel.app/", // current production domain
  author: "עולם ה AI",
  profile: "",
  desc: "בלוג על כלי AI חדשים והסברים נגישים בעברית",
  title: "עולם ה AI",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 6,
  postPerPage: 9,
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
