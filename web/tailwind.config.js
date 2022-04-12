module.exports = {
  purge: {
    enabled: true,
    content: ["src/*.html"],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend:{
      fontFamily: {
        body:['Poppins', 'sans-serif'],
       },
       colors:{
         purple: {
            050:'#F1F0FE',
            100:'#E3E1FD',
            200:'#C7C4FB',
            300:'#A39EF9',
            400:'#847DF7',
            500:'#655CF5',
            600:'#514AC4',
            700:'#3C3792',
         },
          yellow:{
            200:'#FFF2AB',
            300:'#FEE974',
            400:'#FEE145',
            500:'#FEDA16',
            600:'#CBAE12',
            700:'#97820D',
          },
          gray:{
            300:'#F8FBFE',
            400:'#E9F0F6',
            500:'#AAC2DB',
            600:'#556987',
            700:'#333F51',
          },
          white: '#FFFFFF',
       }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
