const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require("path");
const webpack = require('webpack');
const dotenv = require('dotenv');
const CopyWebpackPlugin = require('copy-webpack-plugin');

dotenv.config();

module.exports = {
  entry: "./src/index.js",
  mode: "development",
  output: {
    path: path.resolve(__dirname, "./dist"),
    filename: "js/[name].[hash].js",
    clean: true,
    publicPath: "/",
  },
  devServer: {
    static: {
      directory: path.join(__dirname, "public"),
    },
    historyApiFallback: true,
    port: 9000,
  },
  module: {
    rules: [
      {
        test: /\.m?js$|jsx/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              ['@babel/preset-env', {
                targets: {
                  firefox: '52',
                },
                useBuiltIns: 'usage',
                corejs: 3,
              }],
              '@babel/preset-react',
            ],
          },
        }
      },
      {
        test: /\.css$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
          }
        ]
      },
      {
        test: /\.(png|jpg|jpeg|gif|webp)$/,
        use: ["file-loader"]
      },
      {
        test: /\.svg$/,
        use: ['@svgr/webpack'],
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, "public", "index.html"),
      inject: "body",
    }),
    new webpack.DefinePlugin({
      'process.env.BACKEND_URL': JSON.stringify(process.env.BACKEND_URL),
      'process.env.AUTH_VAR': JSON.stringify(process.env.AUTH_VAR),
      'process.env.AUTH_USER': JSON.stringify(process.env.AUTH_USER),
      'process.env.AUTH_ROLE': JSON.stringify(process.env.AUTH_ROLE),
    }),
    new CopyWebpackPlugin({
      patterns: [
        { from: path.join(__dirname, "public", "icon.png"), to: path.join(__dirname, "dist") },
        // { from: path.join(__dirname, "public", "README.md"), to: path.join(__dirname, "dist") },
        // { from: path.join(__dirname, "public", "docs"), to: path.join(__dirname, "dist", "docs") },
      ],
    }),
  ]
};