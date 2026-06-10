/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['-apple-system','BlinkMacSystemFont','Inter','Segoe UI','Helvetica Neue','sans-serif'],
        mono: ['ui-monospace','SF Mono','Fira Code','monospace'],
      },
      letterSpacing: {
        tightest: '-0.045em',
        tighter:  '-0.030em',
        tight:    '-0.018em',
        snug:     '-0.011em',
        normal:    '0em',
        wide:      '0.06em',
        wider:     '0.10em',
      },
      colors: {
        titanium: { 200: '#F5F5F7', 300: '#EBEBED', 400: '#D2D2D4' },
        ink: { DEFAULT: '#1D1D1F', 70: 'rgba(29,29,31,.70)', 45: 'rgba(29,29,31,.45)', 20: 'rgba(29,29,31,.18)', 8: 'rgba(29,29,31,.07)' },
        iri: { violet: '#8B7CF6', rose: '#E879A0', sky: '#38BDF8', mint: '#34D399', amber: '#FBBF24' },
      },
      borderRadius: { apple: '18px', 'apple-lg': '24px', 'apple-xl': '28px', bento: '28px', pill: '999px' },
      boxShadow: {
        apple: '0 2px 4px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06), 0 0 0 .5px rgba(0,0,0,.05)',
        'apple-lg': '0 4px 8px rgba(0,0,0,.06), 0 20px 56px rgba(0,0,0,.10), 0 0 0 .5px rgba(0,0,0,.05)',
      },
      transitionTimingFunction: {
        'apple-out': 'cubic-bezier(.16,1,.3,1)',
        'apple-spring': 'cubic-bezier(.34,1.56,.64,1)',
      },
    },
  },
  plugins: [
    function ({ addUtilities }) {
      addUtilities({
        '.text-balance': { 'text-wrap': 'balance' },
        '.text-eyebrow': { 'font-size': '11px', 'font-weight': '700', 'letter-spacing': '0.10em', 'text-transform': 'uppercase' },
        '.text-iri': { 'background': 'linear-gradient(135deg, #8B7CF6 0%, #E879A0 45%, #38BDF8 90%)', '-webkit-background-clip': 'text', 'background-clip': 'text', '-webkit-text-fill-color': 'transparent' },
      });
    },
  ],
};
