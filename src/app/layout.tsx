import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#9333ea' },
    { media: '(prefers-color-scheme: dark)', color: '#1e1b4b' },
  ],
};

export const metadata: Metadata = {
  title: "ШаржМастер PRO - AI Шаржи",
  description: "Создавайте уникальные шаржи с помощью AI и делитесь ими в ВКонтакте и Telegram. 12 стилей, геймификация, готовые подписи для постов.",
  keywords: ["шарж", "карикатура", "AI", "AI искусство", "ВКонтакте", "Telegram", "фото", "портрет", "юмор"],
  authors: [{ name: "ШаржМастер Team" }],
  manifest: "/manifest.json",
  icons: {
    icon: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
    ],
  },
  openGraph: {
    title: "ШаржМастер PRO - Создавайте AI шаржи",
    description: "Создавайте уникальные шаржи и делитесь ими в соцсетях",
    type: "website",
    locale: "ru_RU",
    images: [
      {
        url: "/icon-512.png",
        width: 512,
        height: 512,
        alt: "ШаржМастер PRO",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "ШаржМастер PRO",
    description: "Создавайте уникальные шаржи с помощью AI",
    images: ["/icon-512.png"],
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "ШаржМастер",
  },
  formatDetection: {
    telephone: false,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <head>
        <link rel="apple-touch-icon" href="/icon-192.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
