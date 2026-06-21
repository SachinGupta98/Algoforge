import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { askCoach, fetchProblems, fetchRoadmap, runCode } from './api'
import type { ExecuteResponse, Problem, Roadmap } from './types'

const languageOptions = [
  { label: 'Python', key: 'python', judge0: 71 },
  { label: 'C++', key: 'cpp', judge0: 54 },
  { label: 'Java', key: 'java', judge0: 62 },
  { label: 'C', key: 'c', judge0: 50 },
]

function App() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [problems, setProblems] = useState<Problem[]>([])
  const [problem, setProblem] = useState<Problem | null>(null)
  const [language, setLanguage] = useState(languageOptions[0])
  const [code, setCode] = useState('')
  const [stdin, setStdin] = useState('')
  const [coachQuestion, setCoachQuestion] = useState('I am stuck. What should I think about first?')
  const [coachReply, setCoachReply] = useState('')
  const [execution, setExecution] = useState<ExecuteResponse | null>(null)

  useEffect(() => {
    void Promise.all([fetchRoadmap(), fetchProblems()]).then(([roadmapData, problemsData]) => {
      const initialProblem = problemsData[0] ?? null
      setRoadmap(roadmapData)
      setProblems(problemsData)
      setProblem(initialProblem)
      setCode(initialProblem?.starter_code[languageOptions[0].key] ?? '')
    })
  }, [])

  const dailyGoal = useMemo(() => {
    const total = problems.length
    return `Your goal today: 1 problem + 20 minutes theory (${total} starter problems loaded)`
  }, [problems.length])

  const onAskCoach = async () => {
    if (!problem) return
    const result = await askCoach(coachQuestion, problem.topic)
    setCoachReply(result.reply)
  }

  const onRunCode = async () => {
    const result = await runCode(code, language.judge0, stdin)
    setExecution(result)
  }

  return (
    <div className="app">
      <header className="hero">
        <h1>AlgoForge MVP</h1>
        <p>{dailyGoal}</p>
        <div className="pill">Default theme: amber/orange</div>
      </header>

      <section className="grid">
        <article className="card">
          <h2>Roadmap</h2>
          <h3>Phase 1</h3>
          <ul>{roadmap?.phase_1.map((item) => <li key={item}>{item}</li>)}</ul>
          <h3>Phase 2</h3>
          <ul>{roadmap?.phase_2.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>

        <article className="card">
          <h2>Problem Bank</h2>
          <label>
            Select problem
            <select
              value={problem?.id}
              onChange={(e) => {
                const nextProblem = problems.find((p) => p.id === e.target.value) ?? null
                setProblem(nextProblem)
                setCode(nextProblem?.starter_code[language.key] ?? '')
              }}
            >
              {problems.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.title} • {p.difficulty}
                </option>
              ))}
            </select>
          </label>
          <p className="statement">{problem?.statement}</p>
          <strong>Hint ladder:</strong>
          <ol>{problem?.hints.map((hint) => <li key={hint}>{hint}</li>)}</ol>
        </article>
      </section>

      <section className="workspace">
        <article className="card">
          <h2>Code Workspace</h2>
          <label>
            Language
            <select
              value={language.key}
              onChange={(e) => {
                const selected = languageOptions.find((item) => item.key === e.target.value)
                if (selected && problem) {
                  setLanguage(selected)
                  setCode(problem.starter_code[selected.key] ?? '')
                }
              }}
            >
              {languageOptions.map((item) => (
                <option key={item.key} value={item.key}>
                  {item.label}
                </option>
              ))}
            </select>
          </label>
          <textarea value={code} onChange={(e) => setCode(e.target.value)} rows={12} />
          <label>
            Custom input
            <textarea value={stdin} onChange={(e) => setStdin(e.target.value)} rows={4} />
          </label>
          <button onClick={onRunCode}>Run with Judge0</button>
          {execution && (
            <pre>{`Status: ${execution.status}\nOutput: ${execution.stdout ?? execution.stderr ?? execution.compile_output ?? 'No output'}`}</pre>
          )}
        </article>

        <article className="card">
          <h2>Logic AI Coach</h2>
          <textarea value={coachQuestion} onChange={(e) => setCoachQuestion(e.target.value)} rows={5} />
          <button onClick={onAskCoach}>Ask Socratic Hint</button>
          <pre>{coachReply || 'No response yet.'}</pre>
        </article>
      </section>
    </div>
  )
}

export default App
