const js = require("@eslint/js");
const globals = require("globals");

module.exports = [
    js.configs.recommended,

    // Browser source files
    {
        files: ["proziceri.js"],
        languageOptions: {
            ecmaVersion: 2015,
            sourceType: "script",
            globals: {
                ...globals.browser,
                $: "readonly",
                jQuery: "readonly",
                Papa: "readonly",
                ga: "readonly",
                constructDadaSaying: "readonly",
            },
        },
    },

    // Shared logic file (browser global + CommonJS guard for Node tests)
    {
        files: ["proziceri.logic.js"],
        languageOptions: {
            ecmaVersion: 2015,
            sourceType: "script",
            globals: {
                ...globals.browser,
                module: "readonly",
            },
        },
    },

    // Jest test files
    {
        files: ["tests/**/*.js"],
        languageOptions: {
            ecmaVersion: 2020,
            sourceType: "commonjs",
            globals: {
                ...globals.node,
                ...globals.jest,
            },
        },
    },

    // Node config files (jest.config.js, eslint.config.js)
    {
        files: ["*.config.js"],
        languageOptions: {
            ecmaVersion: 2020,
            sourceType: "commonjs",
            globals: globals.node,
        },
    },

    // Ignore vendored and generated files
    {
        ignores: ["papaparse.min.js", "node_modules/"],
    },
];
