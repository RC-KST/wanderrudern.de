/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./content/*.md",
    "./themes/**/*.html",
  ],
  theme: {
    fontFamily: {
      sans: ["Noto Sans", "sans-serif"],
      serif: ["serif"],
    },
    extend: {},
  },
  plugins: [],
}

