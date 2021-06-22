### How to use webpack
Assuming you are in the desired directory to have webpack
### Install webpack and save as development dependency
npm install webpack webpack-cli --save-dev
### init npm project
npm init -y
### install lodash and include javascript file with bundled codes
npm install --save lodash
### create html file and load javascript file with bundled codes
### update package.json
add "private":true
modify "scripts" so that "npm run build" command bundles the required files
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "webpack"
  },

### add config file (to setup terminal environment) "webpack.config.js (run npm webpack --config <config file>) to use the conif file
In webpack.config.js:
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
};

