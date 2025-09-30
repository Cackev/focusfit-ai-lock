import { Card, CardContent, Typography, Box } from '@mui/material'
import type { ReactNode } from 'react'

export default function MetricCard({ title, action, children }: { title: string, action?: ReactNode, children: ReactNode }) {
  return (
    <Card elevation={6}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
          <Typography variant="subtitle2" color="text.secondary">{title}</Typography>
          {action}
        </Box>
        {children}
      </CardContent>
    </Card>
  )
}
