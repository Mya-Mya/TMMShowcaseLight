const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  entry: path.join(__dirname, "webapp", "index.js"),
  output: {
    filename: "bundle.js",
    path: path.join(__dirname, "webapp_built"),
  },
  module: {
    rules: [
      {
        test: [/\.js\$/, /\.jsx\$/],
        use: [
          {
            loader: "babel-loader",
            options: {
              presets: ["@babel/preset-env"],
            },
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, "webapp", "index.html"),
    }),
  ],
};
