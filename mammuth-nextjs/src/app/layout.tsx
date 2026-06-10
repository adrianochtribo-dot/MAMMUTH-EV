import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
  weight: ['300', '400', '500', '600', '700', '800'],
});

export const metadata: Metadata = {
  title: 'MAMMUTH•EVENTS™ — Where Communities Come Alive',
  description: 'Il primo database certificato degli eventi culturali del territorio italiano. Borgo per borgo.',
  keywords: ['eventi culturali', 'sagre', 'processioni', 'territorio', 'ISTAT', 'Sermoneta', 'Latina'],
  authors: [{ name: 'KREATIO UNIVERSAL SYSTEM™' }],
  openGraph: {
    title: 'MAMMUTH•EVENTS™',
    description: 'Il primo database certificato degli eventi culturali del territorio italiano.',
    type: 'website',
    locale: 'it_IT',
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#F5F5F7',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it" className={inter.variable}>
      <body className="antialiased bg-white text-[#1D1D1F]">
        {children}
      </body>
    </html>
  );
}
