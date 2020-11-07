const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const autoprefixer = require("autoprefixer");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const publicPath = process.env.STATIC_URL || "/static/";

const resolve = path.resolve.bind(path, __dirname);

module.exports = (env, argv) => {
  return {
    context: __dirname,
    entry: {
      home_page_loader: path.resolve(
        __dirname,
        "project/app/static/webpack_sources/js/index.js"
      ),
    },
    output: {
      path: path.resolve(__dirname, "project/app/static/webpack_bundles"),
      filename: "[name]-[hash].js",
      chunkFilename: "[name]-[chunkhash].js",
      publicPath,
    },
    optimization: {
      minimizer:
        argv.mode === "production"
          ? [
              // TODO: Use another repo, because:
              // > This repository has been archived by the owner. It is now read-only.
              //
              // Recommendation: https://webpack.js.org/plugins/terser-webpack-plugin/
              new UglifyJsPlugin({
                cache: false,
                parallel: false,
                uglifyOptions: {
                  ecma: 6,
                  compress: {
                    drop_console: true,
                  },
                  mangle: {
                    toplevel: true,
                    eval: true,
                  },
                },
              }),
            ]
          : [],
    },
    performance: {
      hints: "warning",
    },
    plugins: [
      new webpack.DefinePlugin({
        "process.env.STATIC_URL": JSON.stringify(publicPath),
      }),
      new BundleTracker({
        path: path.join(__dirname, "project"),
        filename: "webpack-stats.json",
      }),
      new MiniCssExtractPlugin({
    		filename: "[name]-[hash].css",
    	}),
      ...(argv.watch ? [new CleanWebpackPlugin()] : []),
      ...(argv.mode === "development" ? [new webpack.SourceMapDevToolPlugin()] : []),
      ...(argv.mode === "development" ? [new webpack.SourceMapDevToolPlugin({
        filename: '[file].map[query]',
        exclude: ['vendor.js'],
        publicPath: publicPath,
      })] : []),
    ],
    resolve: {
      extensions: [".js", ".jsx"],
    },
    mode: argv.mode,
    devtool: false,
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: [
            {
              loader: "babel-loader",
              options: {
                presets: ["@babel/preset-env"],
              },
            },
          ],
        },
        {
          test: /\.s[ac]ss$/i,
          use: [
            {
							loader: MiniCssExtractPlugin.loader,
							options: {
								publicPath
							},
						},
            "css-loader",
            {
              loader: "sass-loader",
              options: {
                // Prefer `dart-sass`
                implementation: require("sass"),
              },
            },
          ],
        },
        {
          test: /\.css$/,
          use: [
            "css-loader",
            {
              loader: "resolve-url-loader",
              options: {
                root: resolve("./assets/static/"),
                absolute: true,
              },
            },
            {
              loader: "postcss-loader",
              options: {
                plugins: [autoprefixer],
              },
            },
          ],
        },
        {
          test: /\.(gif|cur|eot|otf|png|svg|jpg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
          loader: "file-loader",
          options: {
            name: "[path][name]-[hash].[ext]",
            publicPath,
          },
        },
      ],
    },
  };
};
