const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  pages: {
    index: {
      entry: "src/index.js",
      template: "public/index.html",
      //filename: "vue_index.html"
      filename: "index.html",
    },
  },
  devServer: {
    clientLogLevel: "warning",
    hot: true,
    contentBase: "dist",
    compress: true,
    open: true,
    overlay: { warnings: false, errors: true },
    //publicPath: "/velox/vue_index.html/",
    publicPath: "/",
    quiet: true,
    watchOptions: {
      poll: false,
      ignored: /node_modules/,
    },
  },

  chainWebpack: (config) => {
    config.plugins.delete("prefetch-index"),
      config.module
        .rule("vue")
        .use("vue-loader")
        .tap((args) => {
          args.compilerOptions.whitespace = "preserve";
        });
  },
  productionSourceMap: false,
  assetsDir: "./static/velox/", // local

  // cloud
  //assetsDir: "./velox/",
  //publicPath: "https://storage.googleapis.com/velox-webapp-static-dev/",

  configureWebpack: {
    plugins: [
      new CopyPlugin({
        patterns: [
          { from: "src/assets/img", to: "static/velox/img" },
          { from: "src/assets/logos", to: "static/velox/logos" },
          { from: "src/assets/fonts", to: "static/velox/fonts" },
          {
            from: "node_modules/onnxruntime-web/dist/*.wasm",
            to: "static/velox/js/[name].[ext]",
          },
        ],
      }),
    ],
  },
};
