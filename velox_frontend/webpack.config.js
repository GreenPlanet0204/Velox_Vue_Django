var path = require('path');
var webpack = require('webpack');
// var vueLoader = require('vue-loader');
const { VueLoaderPlugin } = require('vue-loader');
// const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

let config = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: 'eval-cheap-source-map',
  plugins: [new VueLoaderPlugin()]
};

let mainConfig = Object.assign({}, config, {
  name: "mainConfig",
    entry: {
    'main': './src/main.js',
  },
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/static/cmmc/js/',
    // publicPath: 'https://storage.googleapis.com/cmmc_static/cmmc/vue-datagrid/',
    // publicPath: 'https://storage.googleapis.com/cmmc_static_test/cmmc/js/',

    // filename: 'build.js'
    filename: "[name].js",
    chunkFilename: "[name].js",
  },
});

// let auditConfig = Object.assign({}, config, {
//     name: "auditConfig",
//     entry: "./src/audits.js",
//     output: {
//         path: path.resolve(__dirname, './dist'),
//         publicPath: '/static/cmmc/js/',
//         filename: "audits.js",
//         chunkFilename: "audits.js",
//         libraryTarget: 'umd',
//         libraryExport: 'default',
//         library: 'AuditDetail',
//         umdNamedDefine: true
//     }
// });

// module.exports = [auditConfig, mainConfig];
// module.exports = [auditConfig];
module.exports = [mainConfig];

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map';
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      // 'process.env': {
      //   NODE_ENV: '"production"'
      // }
    }),
    // new UglifyJsPlugin({
    //         "uglifyOptions":
    //             {
    //                 compress: {
    //                     warnings: false
    //                 },
    //                 sourceMap: true
    //             }
    //     }
    // ),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    }),

  ])
}
