/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2b8a3e", // Dark green for the footer background
        secondary: "#a9e63d", // Vibrant green for icons
        "primary-foreground": "#ffffff", // Text color in the footer
      },
    },
  },
  plugins: [],
};
