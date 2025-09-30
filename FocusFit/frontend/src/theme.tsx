import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#4c8dff' },
    secondary: { main: '#f9a73b' },
    background: { default: '#0b111b', paper: '#101826' },
  },
  shape: { borderRadius: 12 },
  typography: { fontFamily: 'Inter, system-ui, Segoe UI, Arial' },
  components: {
    MuiCard: { styleOverrides: { root: { backdropFilter: 'blur(6px)', border: '1px solid rgba(255,255,255,0.06)' } } },
    MuiAppBar: { styleOverrides: { root: { background: 'rgba(16,24,38,0.6)', borderBottom: '1px solid rgba(255,255,255,0.08)' } } },
  }
})

export default theme
