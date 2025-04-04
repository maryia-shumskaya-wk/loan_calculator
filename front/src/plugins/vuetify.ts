/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { ThemeDefinition, createVuetify } from 'vuetify'

const theme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#E9E9E9',
    surface: '#FFFFFF',
    primary: '#1E4374',
    secondary: '#606060',
    error: '#B00020',
    "button-primary": '#2491EB',
    "button-secondary": '#FFFFFF',
  },
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: theme,
    },
  },
})
