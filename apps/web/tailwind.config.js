/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef2ff",
          100: "#e0e7ff",
          400: "#818cf8",
          500: "#6366f1",
          600: "#4f46e5",
          700: "#4338ca",
        },
        dark: {
          900: "#090d16",
          850: "#0d1322",
          800: "#131a2e",
          750: "#18223c",
          700: "#1e294b",
          600: "#2d375e"
        },
        radar: {
          cyan: "#06b6d4",
          amber: "#f59e0b",
          rose: "#f43f5e",
          emerald: "#10b981",
          violet: "#8b5cf6"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "SF Mono", "monospace"]
      }
    },
  },
  plugins: [],
}
