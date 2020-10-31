const path = require("path");
const url = require("url");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const autoprefixer = require("autoprefixer");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");

const baseStaticPath = process.env.STATIC_URL || "/static/";
const publicPath = url.resolve(baseStaticPath, "/static/");

const resolve = path.resolve.bind(path, __dirname);

const assetsPath = "project/app/static/webpack_sources";

let bundleTrackerPlugin = new BundleTracker({
  filename: "./project/webpack-stats.json",
});

const providePlugin = new webpack.ProvidePlugin({});

let optimization = {};
let plugins = [];

module.exports = (env, argv) => {
  plugins = [
    new webpack.DefinePlugin({
      "process.env.STATIC_URL": JSON.stringify(publicPath),
    }),
    bundleTrackerPlugin,
    providePlugin,
  ];

  if (argv.watch) {
    plugins.push(
      new CleanWebpackPlugin({
        root: resolve("."),
        verbose: false,
        dry: false,
      })
    );
  }

  if (argv.mode === "development") {
    plugins.push(new webpack.SourceMapDevToolPlugin({}));
  }

  if (argv.mode === "production") {
    optimization.minimizer = [
      new UglifyJsPlugin({
        cache: false,
        parallel: false,
        uglifyOptions: {
          ecma: 6,
          // warnings: false,
          compress: {
            drop_console: true,
            // toplevel: true,
          },
          mangle: {
            toplevel: true,
            eval: true,
          },
          ie8: false,
          comments: false,
        },
      }),
    ];
  }

  const _sroucePath = (path) => {
    return resolve(`./${assetsPath}/${path}`);
  };

  return {
    context: __dirname,
    entry: {
      home_page_loader: _sroucePath("js/index.js"),
      // Thêm loader cho page mới ở đưới
    },
    output: {
      path: resolve("./project/static/webpack_bundles/"),
      filename: "[name]-[hash].js",
      chunkFilename: "[name]-[chunkhash].js",
      publicPath,
    },
    optimization,
    performance: {
      hints: "warning",
    },
    plugins,
    resolve: {
      alias: {},
      extensions: [".js", ".jsx"],
    },
    externals: {},
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
            "style-loader",
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
            "style-loader",
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
