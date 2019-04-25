var path = require('path');

module.exports = {
  entry: "./src/static/scripts/master.js",
  output: {
    path: path.resolve(__dirname, "./src/static/temp"),
    filename: "master.js"
  },

  module: {
    loaders: [
      {
        loader: 'babel-loader',
        query: {
          presets: ['es2015']
        },
        test: /\.js$/,
        exclude: /node_modules/
      }
    ]
  }
}
