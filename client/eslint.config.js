// eslint.config.js

import js from '@eslint/js';
import globals from 'globals';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import prettier from 'eslint-plugin-prettier';
import eslintConfigPrettier from 'eslint-config-prettier';
import tseslint from 'typescript-eslint';
import { defineConfig, globalIgnores } from 'eslint/config';

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [js.configs.recommended, tseslint.configs.recommended],
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
      prettier,
    },
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    settings: {
      react: {
        version: '18.3', // React 버전 지정 (자동 감지도 되지만 명시적으로 쓰면 안전)
      },
    },
    rules: {
      // React plugin 기본 룰
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,

      // React hooks 룰
      ...reactHooks.configs.recommended.rules,

      // React Refresh (Vite fast refresh 관련)
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],

      // Prettier 룰
      'prettier/prettier': 'error',
    },
  },
  eslintConfigPrettier, // prettier와 충돌하는 룰 비활성화
]);
