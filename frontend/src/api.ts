import type { CoachResponse, ExecuteResponse, Problem, Roadmap } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export async function fetchRoadmap(): Promise<Roadmap> {
  const response = await fetch(`${API_BASE}/api/roadmap`)
  if (!response.ok) throw new Error('Failed to load roadmap')
  return response.json()
}

export async function fetchProblems(): Promise<Problem[]> {
  const response = await fetch(`${API_BASE}/api/problems`)
  if (!response.ok) throw new Error('Failed to load problems')
  const data = await response.json()
  return data.items
}

export async function askCoach(question: string, topic: string): Promise<CoachResponse> {
  const response = await fetch(`${API_BASE}/api/ai/coach`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, topic, student_level: 'Beginner' }),
  })
  if (!response.ok) throw new Error('Coach request failed')
  return response.json()
}

export async function runCode(source_code: string, language_id: number, stdin: string): Promise<ExecuteResponse> {
  const response = await fetch(`${API_BASE}/api/code/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source_code, language_id, stdin }),
  })
  if (!response.ok) throw new Error('Code execution failed')
  return response.json()
}
