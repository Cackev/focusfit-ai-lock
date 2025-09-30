import { LineChart, Line, ResponsiveContainer } from 'recharts'

export default function Sparkline({ data }: { data: number[] }) {
  const points = data.map((v, i) => ({ x: i, y: v }))
  return (
    <div style={{ width:'100%', height:40 }}>
      <ResponsiveContainer>
        <LineChart data={points} margin={{ left: 0, right: 0, top: 8, bottom: 0 }}>
          <Line type="monotone" dataKey="y" stroke="#4c8dff" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
