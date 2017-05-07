const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const ExtractTextPlugin = require("extract-text-webpack-plugin");

// TODO - this is a really simple version of webpack.config.js that will eventually need to grow

module.exports = {
  //the base directory (absolute path) for resolving the entry option
  context: __dirname,
  //the entry point we created earlier. Note that './' means
  //your current directory. You don't have to specify the extension  now,
  //because you will specify extensions later in the `resolve` section
  entry: "./assets/js/index",

  output: {
    //where you want your compiled bundle to be stored
    path: path.resolve("./assets/bundles/"),
    //naming convention webpack should use for your files
    filename: "[name]-[hash].js",
    publicPath: "/static/bundles/"
  },

  plugins: [
    //tells webpack where to store data about your bundles.
    new BundleTracker({ filename: "./webpack-stats.json" }),
    //makes jQuery available in every module
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),
    new ExtractTextPlugin({
      filename: 'app.css',
      allChunks: true
    })
  ],

  module: {
    loaders: [
      {
        test: /\.jsx?/, // include js and jsx
        exclude: /node_modules/,
        loader: "babel-loader",
        query: {
          // stage-0 is necessary for the crappy import styles that you have
          presets: ["es2015", "react", "stage-0"]
        }
      },
      {
        // file-loader
        test: /\.(jpg|png|svg|jpeg)$/,
        exclude: /node_modules/,
        loader: "file-loader"
        // options: {
        //   name: 'static/bundles/images/[name][hash].[ext]',
        // },
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader?modules,localIdentName="[name]-[local]-[hash:base64:6]"'
        }),
      }
    ]
  },

  resolve: {
    modules: ["node_modules"],
    //extensions that should be used to resolve modules
    extensions: [".js", ".jsx"]
  }
};
