module.exports = {
	root: true,
	parser: "@typescript-eslint/parser",
	parserOptions: {
		ecmaVersion: 2022,
		sourceType: "module",
		ecmaFeatures: { jsx: true },
	},
	env: { browser: true, es2022: true, node: true },
	extends: [
		"eslint:recommended",
		"plugin:react/recommended",
		"plugin:@typescript-eslint/recommended",
		"plugin:jsx-a11y/recommended",
		"prettier"
	],
	plugins: ["react", "@typescript-eslint", "jsx-a11y", "import"],
	settings: { react: { version: "detect" }, "import/resolver": { typescript: {} } },
	rules: {
		"react/react-in-jsx-scope": "off",
		"@typescript-eslint/explicit-module-boundary-types": "off",
		"@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }]
	}
};
