const themeDir = __dirname + '/../../';

module.exports = {
  plugins: {
    'postcss-import': {},
    tailwindcss: { config: themeDir + "assets/css/tailwind.config.js" },
    autoprefixer: { path: [themeDir] },
    //require("postcss-import")({}),
    //require("tailwindcss")("../../assets/tailwind/tailwind.config.js"),
    //require("autoprefixer")({
    //  path: ["../../"]
    //})
  }
}
