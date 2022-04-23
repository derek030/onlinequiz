const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/**/*.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      sans: ['Poppins', 'sans-serif'],
      body: ['Poppins', 'sans-serif'],
    },
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
    },
    backgroundImage: {
      'quiz-pattern': "url('../media/bkg-pattern.png')",
    },
    extend: {
      colors: {
        'purple': {
          050:'#F1F0FE',
          100:'#E3E1FD',
          200:'#C7C4FB',
          300:'#A39EF9',
          400:'#847DF7',
          500:'#655CF5',
          600:'#514AC4',
          700:'#3C3792',
       },
        'yellow':{
          200:'#FFF2AB',
          300:'#FEE974',
          400:'#FEE145',
          500:'#FEDA16',
          600:'#CBAE12',
          700:'#97820D',
        },
        'gray':{
          200:'#D5DAE1',
          300:'#F8FBFE',
          400:'#E9F0F6',
          500:'#AAC2DB',
          600:'#556987',
          700:'#333F51',
        },
        white:'#FFFFFF',
        red:'#FF8080',
        orange:'#FDAE5E',
        green:{
          500:'#75E209',
          600:'#5eb507',
        },
        cyan:'#1FE8FF',
        blue:'#6791F5',
        pink:'#E498FF',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('tailwindcss'),
    require('autoprefixer'),
  ],
}
