export type Problem = {
  id: string
  title: string
  difficulty: string
  forge_difficulty: number
  topic: string
  statement: string
  hints: string[]
  starter_code: Record<string, string>
}

export type Roadmap = {
  phase_1: string[]
  phase_2: string[]
  theme: string
}

export type CoachResponse = {
  reply: string
  provider: string
}

export type ExecuteResponse = {
  stdout?: string | null
  stderr?: string | null
  compile_output?: string | null
  status: string
  time?: string | null
  memory?: number | null
}
