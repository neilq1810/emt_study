/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        accent: '#0e7490',
      },
      maxWidth: {
        prose: '72ch',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
