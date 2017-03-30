const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

// TODO - this is a really simple version of webpack.config.js that will eventually need to grow

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    //the entry point we created earlier. Note that './' means
    //your current directory. You don't have to specify the extension  now,
    //because you will specify extensions later in the `resolve` section
    entry: './assets/js/index',

    output: {
        //where you want your compiled bundle to be stored
        path: path.resolve('./assets/bundles/'),
        //naming convention webpack should use for your files
        filename: '[name]-[hash].js',
    },

    plugins: [
        //tells webpack where to store data about your bundles.
        new BundleTracker({filename: './webpack-stats.json'}),
        //makes jQuery available in every module
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        })
    ],

    module: {
        loaders: [
            //a regexp that tells webpack use the following loaders on all
            //.js and .jsx files
            {
              test: /\.jsx?/,
              exclude: /node_modules/,
              loader: 'babel-loader',
              query:
                {
                  // stage-0 is necessary for the crappy import styles that you have
                  presets: ['es2015','react','stage-0']
                }
            }
        ]
    },

    resolve: {
        modules: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: ['.js', '.jsx']
    }
}
