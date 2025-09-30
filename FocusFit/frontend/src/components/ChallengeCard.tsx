import { Card, CardContent, Typography, Box, Chip, Button } from '@mui/material'

export default function ChallengeCard({ title, subtitle, difficulty='EASY', time, reward, onStart }: { title: string, subtitle: string, difficulty?: 'EASY'|'MEDIUM'|'HARD', time: string, reward: string, onStart: () => void }) {
  const color = difficulty==='EASY' ? 'success' : difficulty==='MEDIUM' ? 'warning' : 'error'
  return (
    <Card elevation={6}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
          <Box>
            <Typography fontWeight={700}>{title}</Typography>
            <Typography variant="body2" color="text.secondary">{subtitle}</Typography>
          </Box>
          <Chip color={color as any} label={difficulty} size="small" variant="outlined" />
        </Box>
        <Box display="flex" gap={2} color="text.secondary" mb={1}>
          <Typography variant="caption">⏱ {time}</Typography>
          <Typography variant="caption">🪙 {reward}</Typography>
        </Box>
        <Button fullWidth variant="contained" onClick={onStart}>Start Challenge</Button>
      </CardContent>
    </Card>
  )
}
