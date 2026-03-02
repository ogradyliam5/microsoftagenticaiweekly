/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './archive.html',
    './sources.html',
    './corrections.html',
    './about.html',
    './posts/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        ink: '#0b1220',
        slate: '#334155'
      }
    }
  },
  plugins: []
};
