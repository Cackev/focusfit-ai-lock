import { useEffect, useMemo, useState } from 'react'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Container from '@mui/material/Container'
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import IconButton from '@mui/material/IconButton'
import Tooltip from '@mui/material/Tooltip'
import LightModeIcon from '@mui/icons-material/LightMode'
import DarkModeIcon from '@mui/icons-material/DarkMode'
import TokenIcon from '@mui/icons-material/Token'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import MetricCard from './components/MetricCard'
import ChallengeCard from './components/ChallengeCard'
import Ring from './components/Ring'
import Sparkline from './components/Sparkline'
import { getHealth, getMode, getTimes, setTimes, setMode, getGoals, getHistory, startChallenge, type GoalsInfo } from './api'
import { Toaster, toast } from 'react-hot-toast'
import Modal from '@mui/material/Modal'
import Paper from '@mui/material/Paper'

export default function App() {
  const [health, setHealth] = useState<'ok' | 'down'>('down')
  const [mode, setModeState] = useState<'strict' | 'normal'>('strict')
  const [times, setTimesState] = useState<string[]>([])
  const [goals, setGoals] = useState<GoalsInfo | null>(null)
  const [history, setHistory] = useState<string[]>([])
  const [challenge, setChallenge] = useState<'Push-ups' | 'Squats' | 'Jumping Jacks'>('Push-ups')
  const [reps, setReps] = useState<number>(5)
  const [busy, setBusy] = useState<boolean>(false)
  const [themeMode, setThemeMode] = useState<'light'|'dark'>(() => ((localStorage.getItem('ff_theme') as 'light'|'dark') || 'dark'))
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [difficulty, setDifficulty] = useState<'ALL'|'EASY'|'MEDIUM'|'HARD'>('ALL')

  useEffect(() => {
    (async () => {
      try {
        const h = await getHealth(); setHealth(h.status === 'ok' ? 'ok' : 'down')
        setModeState(await getMode())
        setTimesState(await getTimes())
        setGoals(await getGoals())
        setHistory(await getHistory())
      } catch { toast.error('Failed to load') }
    })()
  }, [])

  useEffect(() => {
    const id = setInterval(async () => {
      try { setGoals(await getGoals()); setHistory(await getHistory()) } catch {}
    }, 5000)
    return () => clearInterval(id)
  }, [])

  useEffect(() => { document.documentElement.dataset.theme = themeMode; localStorage.setItem('ff_theme', themeMode) }, [themeMode])

  const dailyLabel = useMemo(() => goals ? `${Math.min(goals.daily_reps, goals.daily_goal)}/${goals.daily_goal}` : '-', [goals])
  const last7 = useMemo(() => [4,6,3,8,7,10,9], [])

  const handleStart = async () => {
    if (reps <= 0) { toast.error('Reps must be positive'); return }
    setBusy(true)
    try { await startChallenge(challenge, reps); toast.success('Challenge started') } catch { toast.error('Failed to start challenge') } finally { setBusy(false) }
  }

  const saveTimes = async (text: string) => {
    const list = text.split(',').map(s => s.trim()).filter(Boolean)
    try { await setTimes(list); setTimesState(list); toast.success('Times saved') } catch { toast.error('Failed to save times') }
  }

  const toggleAppMode = async () => {
    const next = mode === 'strict' ? 'normal' : 'strict'
    try { await setMode(next); setModeState(next); toast.success(`Mode: ${next}`) } catch { toast.error('Failed to set mode') }
  }

  const filtered = (tag: 'EASY'|'MEDIUM'|'HARD') => difficulty === 'ALL' || difficulty === tag

  return (
    <>
      <Toaster position="top-right" />
      <AppBar position="sticky" color="transparent" elevation={0} sx={{ backdropFilter:'blur(8px)', borderBottom:'1px solid rgba(255,255,255,0.08)' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flex: 1, fontWeight: 700 }}>FocusFit</Typography>
          <Chip size="small" label={`API: ${health}`} color={health==='ok' ? 'success' : 'default'} variant="outlined" sx={{ mr: 1 }} />
          <Chip size="small" label={`Mode: ${mode}`} variant="outlined" onClick={toggleAppMode} sx={{ mr: 1, cursor:'pointer' }} />
          <Tooltip title="Toggle theme">
            <IconButton color="inherit" onClick={() => setThemeMode(themeMode==='dark'?'light':'dark')}>
              {themeMode==='dark' ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      <Box sx={{ height: 260, position:'relative', overflow:'hidden', borderBottom:'1px solid rgba(255,255,255,0.08)', background:'linear-gradient(180deg, rgba(0,0,0,0.25), rgba(0,0,0,0.6)), url(/vite.svg) center/cover no-repeat' }}>
        <Container sx={{ position:'relative', zIndex:1, py: 4 }}>
          <Typography variant="h3" fontWeight={800} gutterBottom>Unlock with Movement</Typography>
          <Typography variant="subtitle1" color="text.secondary" gutterBottom>Complete challenges to unlock your session and earn $FIT.</Typography>
          <Box display="flex" gap={1}>
            <Button variant="contained" onClick={() => { setChallenge('Push-ups'); setReps(10); handleStart() }}>Start Challenge</Button>
            <Button variant="outlined" onClick={() => setSettingsOpen(true)}>Set Times</Button>
          </Box>
        </Container>
      </Box>

      <Container sx={{ py: 3 }}>
        <Box sx={{ display:'grid', gap:2, gridTemplateColumns: { xs:'1fr', md:'repeat(3,1fr)' } }}>
          <MetricCard title="Daily Progress" action={<Typography variant="caption" color="success.main">{goals ? Math.round(goals.daily_percent) + '%' : '0%'}</Typography>}>
            <Box display="flex" alignItems="center" gap={2}>
              <Ring percent={goals?.daily_percent ?? 0} />
              <Box>
                <Typography variant="h5" fontWeight={700}>{dailyLabel}</Typography>
                <Typography variant="body2" color="text.secondary">Challenges completed today</Typography>
              </Box>
            </Box>
          </MetricCard>
          <MetricCard title="$FIT Balance" action={<TokenIcon color="secondary" /> }>
            <Typography variant="h5" fontWeight={700}>127</Typography>
            <Typography variant="body2" color="text.secondary">Tokens earned</Typography>
            <Box mt={1}><Button size="small" variant="outlined">View Wallet</Button></Box>
          </MetricCard>
          <MetricCard title="7‑Day Activity" action={<TrendingUpIcon color="primary" />}>
            <Sparkline data={last7} />
            <Typography variant="body2" color="text.secondary">Workouts this week</Typography>
          </MetricCard>
        </Box>

        <Box display="flex" alignItems="center" justifyContent="space-between" mt={3} mb={1}>
          <Typography variant="h6">Available Challenges</Typography>
          <Box display="flex" gap={1}>
            <Chip label="All" variant={difficulty==='ALL'?'filled':'outlined'} onClick={() => setDifficulty('ALL')} />
            <Chip label="Easy" variant={difficulty==='EASY'?'filled':'outlined'} onClick={() => setDifficulty('EASY')} />
            <Chip label="Medium" variant={difficulty==='MEDIUM'?'filled':'outlined'} onClick={() => setDifficulty('MEDIUM')} />
            <Chip label="Hard" variant={difficulty==='HARD'?'filled':'outlined'} onClick={() => setDifficulty('HARD')} />
          </Box>
        </Box>
        <Divider sx={{ mb: 2 }} />

        <Box sx={{ display:'grid', gap:2, gridTemplateColumns: { xs:'1fr', md:'repeat(3,1fr)' } }}>
          {filtered('EASY') && (
            <ChallengeCard title="Morning Push-ups" subtitle="Complete 20 push-ups with proper form" difficulty="EASY" time="3 min" reward="5 $FIT" onStart={() => { setChallenge('Push-ups'); setReps(20); handleStart() }} />
          )}
          {filtered('EASY') && (
            <ChallengeCard title="Focus Session" subtitle="2-minute breathing meditation" difficulty="EASY" time="2 min" reward="3 $FIT" onStart={() => { setChallenge('Jumping Jacks'); setReps(1); handleStart() }} />
          )}
          {filtered('MEDIUM') && (
            <ChallengeCard title="Squat Challenge" subtitle="Complete 30 squats in perfect form" difficulty="MEDIUM" time="5 min" reward="8 $FIT" onStart={() => { setChallenge('Squats'); setReps(30); handleStart() }} />
          )}
        </Box>

        <Box mt={3}>
          <Typography variant="h6" gutterBottom>Recent Activity</Typography>
          {history.length === 0 ? (
            <Typography variant="body2" color="text.secondary">No entries yet.</Typography>
          ) : (
            <Box component="ul" sx={{ pl: 3, m: 0 }}>
              {history.slice().reverse().map((h, i) => (
                <Box component="li" key={i} sx={{ mb: 1 }}>{decorateActivity(h)}</Box>
              ))}
            </Box>
          )}
        </Box>

        <Box mt={3}>
          <Typography variant="subtitle2" color="text.secondary">Challenge Editor</Typography>
          <Box display="flex" gap={1} alignItems="center" sx={{ '& > *': { transition:'transform 0.15s ease' }, '& button:hover': { transform:'translateY(-1px)' } }}>
            <Chip label={challenge} />
            <Button variant="outlined" onClick={() => setChallenge('Push-ups')}>Push-ups</Button>
            <Button variant="outlined" onClick={() => setChallenge('Squats')}>Squats</Button>
            <Button variant="outlined" onClick={() => setChallenge('Jumping Jacks')}>Jumping Jacks</Button>
            <input type="number" value={reps} min={1} onChange={e => setReps(parseInt(e.target.value || '0', 10))} style={{ width: 100, background:'transparent', color:'inherit', border:'1px solid rgba(255,255,255,0.12)', borderRadius:8, padding:'8px 10px' }} />
            <Button variant="contained" onClick={handleStart} disabled={busy || health !== 'ok'}>Start</Button>
          </Box>
        </Box>
      </Container>

      <SettingsModal open={settingsOpen} onClose={() => setSettingsOpen(false)} mode={mode} setMode={async (m) => { await setMode(m); setModeState(m) }} times={times} onSave={saveTimes} />
    </>
  )
}

function SettingsModal({ open, onClose, mode, setMode, times, onSave }: { open: boolean, onClose: () => void, mode: 'strict'|'normal', setMode: (m: 'strict'|'normal') => void, times: string[], onSave: (val: string) => void }) {
  const [text, setText] = useState(times.join(', '))
  const [localMode, setLocalMode] = useState<'strict'|'normal'>(mode)
  useEffect(() => { setText(times.join(', ')); setLocalMode(mode) }, [times, mode])
  return (
    <Modal open={open} onClose={onClose}>
      <Paper sx={{ width: 520, mx: 'auto', mt: 10, p: 2 }}>
        <Typography variant="h6" gutterBottom>Settings</Typography>
        <Box display="grid" gap={2}>
          <Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>App Mode</Typography>
            <Box display="flex" gap={1}>
              <Chip label="Strict" color={localMode==='strict'?'primary':'default'} onClick={() => setLocalMode('strict')} />
              <Chip label="Normal" color={localMode==='normal'?'primary':'default'} onClick={() => setLocalMode('normal')} />
            </Box>
          </Box>
          <Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>Allowed Times (HH:MM, comma-separated)</Typography>
            <input value={text} onChange={e => setText(e.target.value)} placeholder="e.g. 08:00, 13:30, 19:00" style={{ width:'100%', background: 'transparent', color: 'inherit', border: '1px solid rgba(255,255,255,0.12)', borderRadius: 8, padding: '8px 10px' }} />
          </Box>
          <Box display="flex" justifyContent="flex-end" gap={1}>
            <Button variant="text" onClick={onClose}>Cancel</Button>
            <Button variant="outlined" onClick={() => { setMode(localMode) }}>Set Mode</Button>
            <Button variant="contained" onClick={() => { onSave(text); onClose() }}>Save</Button>
          </Box>
        </Box>
      </Paper>
    </Modal>
  )
}

function decorateActivity(entry: string) {
  try {
    const [, name, reps] = entry.split('|').map(s => s.trim())
    const emoji = name.includes('Push') ? '🏋️' : name.includes('Squat') ? '🦵' : '🤸'
    const ago = 'just now'
    return `${emoji} ${name}: ${reps} • ${ago}`
  } catch { return entry }
}
