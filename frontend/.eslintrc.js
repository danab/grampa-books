module.exports = {
  root: true,

  parserOptions: {
    parser: 'babel-eslint',
    sourceType: 'module'
  },

  env: {
    browser: true
  },

  // https://github.com/vuejs/eslint-plugin-vue#priority-a-essential-error-prevention
  // consider switching to `plugin:vue/strongly-recommended` or `plugin:vue/recommended` for stricter rules.
  extends: [
    'plugin:vue/recommended',
    '@vue/prettier'
  ],

  // required to lint *.vue files
  plugins: [
    'vue'
  ],

  globals: {
    'cordova': true,
    '__statics': true,
    'process': true
  },

  // add your custom rules here
  rules: {
    'prefer-promise-reject-errors': 'off',

    // warn on console/debugger/unused vars during development only
    // 'no-console': isProd,
    // 'no-debugger': isProd,
    // 'no-unused-vars': isProd
  }
}
