import { defineConfig, fontProviders } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://thissasha.github.io',
  base: '/nata-drem',
  fonts: [
    {
      name: 'Inter',
      cssVariable: '--font-main',
      provider: fontProviders.fontsource(),
      weights: [400, 600, 700],
      styles: ['normal'],
      subsets: ['cyrillic', 'latin'],

    },
    {
      name: 'Amatic SC',
      cssVariable: '--font-decorate',
      provider: fontProviders.fontsource(),
      weights: [400, 700],
      styles: ['normal'],
      subsets: ['cyrillic', 'latin'],

    },
    {
      name: 'Caveat',
      cssVariable: '--font-decorate-2',
      provider: fontProviders.fontsource(),
      weights: [400, 700],
      styles: ['normal'],
      subsets: ['cyrillic', 'latin'],
    }
  ],
  vite: {
    plugins: [
      tailwindcss()
    ]
  },
  devToolbar: {
    enabled: false,
  },
});