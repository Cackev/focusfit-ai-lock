import axios from 'axios'

const api = axios.create({ baseURL: '/' })

export type Mode = 'strict' | 'normal'

export async function getHealth() { return (await api.get('/health')).data }
export async function getMode(): Promise<Mode> { return (await api.get('/mode')).data.mode }
export async function setMode(mode: Mode) { return (await api.post('/mode', { mode })).data }
export async function getTimes(): Promise<string[]> { return (await api.get('/times')).data.times }
export async function setTimes(times: string[]) { return (await api.post('/times', { times })).data }

export type GoalsInfo = {
  daily_reps: number
  weekly_challenges: number
  daily_percent: number
  weekly_percent: number
  daily_goal: number
  weekly_goal: number
  daily_goal_achieved: boolean
  weekly_goal_achieved: boolean
}
export async function getGoals(): Promise<GoalsInfo> { return (await api.get('/goals')).data }
export async function getHistory(): Promise<string[]> { return (await api.get('/history')).data.history }
export async function startChallenge(challenge: 'Push-ups'|'Squats'|'Jumping Jacks', reps: number) { return (await api.post('/challenge/start', { challenge, reps })).data }
