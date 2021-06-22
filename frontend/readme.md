# 1.Initialize frontend
# Paths are relative to frontend folder:
1. create folders src, src/components, static, static/scripts, static/css, static/images, templates
2. run npm init -y

# 2.Install dependencies
# Install webpack (files bundler)
1. run npm i webpack wepack-cli --save-dev
2. add configuration to package.json to "scripts"
  "scripts": {
    #webpack dev script (in development mode and watch mode(means will track for changes and update))
    "dev": "webpack --mode development --watch",
    #webpack build script
    "build": "webpack --mode production"
  },
3. add configuration file "webpack.config.js"
# Install babel
1. run npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
2. add configuration file "babel.config.json"

# Install react 
1. run npm i react react-dom
# for routing pages
2. run npm install react-rounter-dom

# Install UI packages (similar to bootstrap)
1. run npm install @materials-ui/core
2. npm install material-ui/icons

# Install js packages (to use async and await in js)
run npm install @babel/plugin-proposal-class-properties
