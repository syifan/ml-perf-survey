import { useState, useEffect, useRef } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Activity, Users, Sparkles, Settings, ScrollText, RefreshCw } from 'lucide-react'

function App() {
  const [state, setState] = useState({ cycleCount: 0, currentAgentIndex: 0 })
  const [logs, setLogs] = useState([])
  const [agents, setAgents] = useState({ humans: [], gods: [] })
  const [config, setConfig] = useState({ config: null, raw: '' })
  const [lastUpdate, setLastUpdate] = useState(null)
  const [error, setError] = useState(null)
  const logsEndRef = useRef(null)

  const fetchData = async () => {
    try {
      const [stateRes, logsRes, agentsRes, configRes] = await Promise.all([
        fetch('/api/state'),
        fetch('/api/logs?lines=100'),
        fetch('/api/agents'),
        fetch('/api/config'),
      ])

      if (!stateRes.ok || !logsRes.ok || !agentsRes.ok || !configRes.ok) {
        throw new Error('Failed to fetch data')
      }

      setState(await stateRes.json())
      setLogs((await logsRes.json()).logs)
      setAgents(await agentsRes.json())
      setConfig(await configRes.json())
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const formatTime = (date) => {
    return date ? date.toLocaleTimeString() : '--:--:--'
  }

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-800">ML Perf Survey Monitor</h1>
            <p className="text-sm text-neutral-500">Orchestrator Dashboard</p>
          </div>
          <div className="flex items-center gap-3 text-sm text-neutral-500">
            <RefreshCw className="w-4 h-4" />
            <span>Last update: {formatTime(lastUpdate)}</span>
            {error && <Badge variant="warning">Error: {error}</Badge>}
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* State Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Orchestrator State
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-neutral-600">Cycle Count</span>
                  <span className="text-2xl font-mono font-bold text-neutral-800">
                    {state.cycleCount}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-neutral-600">Current Agent Index</span>
                  <span className="text-2xl font-mono font-bold text-neutral-800">
                    {state.currentAgentIndex}
                  </span>
                </div>
                {agents.humans.length > 0 && (
                  <div className="pt-2 border-t">
                    <span className="text-sm text-neutral-500">Current Agent: </span>
                    <Badge variant="secondary">
                      {agents.humans[state.currentAgentIndex]?.name || 'N/A'}
                    </Badge>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Human Agents Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Human Agents ({agents.humans.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {agents.humans.map((agent, idx) => (
                  <div
                    key={agent.name}
                    className={`flex items-center justify-between p-2 rounded ${
                      idx === state.currentAgentIndex
                        ? 'bg-blue-50 border border-blue-200'
                        : 'bg-neutral-50'
                    }`}
                  >
                    <div>
                      <span className="font-medium text-neutral-800 capitalize">
                        {agent.name}
                      </span>
                      <p className="text-xs text-neutral-500 truncate max-w-[180px]">
                        {agent.title}
                      </p>
                    </div>
                    {idx === state.currentAgentIndex && (
                      <Badge variant="success">Active</Badge>
                    )}
                  </div>
                ))}
                {agents.humans.length === 0 && (
                  <p className="text-sm text-neutral-400">No human agents found</p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* God Agents Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-4 h-4" />
                God Agents ({agents.gods.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {agents.gods.map((agent) => (
                  <div
                    key={agent.name}
                    className="flex items-center justify-between p-2 rounded bg-neutral-50"
                  >
                    <div>
                      <span className="font-medium text-neutral-800 capitalize">
                        {agent.name}
                      </span>
                      <p className="text-xs text-neutral-500 truncate max-w-[180px]">
                        {agent.title}
                      </p>
                    </div>
                  </div>
                ))}
                {agents.gods.length === 0 && (
                  <p className="text-sm text-neutral-400">No god agents found</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
          {/* Logs Card */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ScrollText className="w-4 h-4" />
                Orchestrator Logs
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-neutral-900 rounded-lg p-3 h-64 overflow-y-auto font-mono text-xs">
                {logs.length === 0 ? (
                  <p className="text-neutral-500">No logs available</p>
                ) : (
                  logs.map((line, idx) => (
                    <div key={idx} className="text-neutral-300 whitespace-pre-wrap break-all">
                      {line}
                    </div>
                  ))
                )}
                <div ref={logsEndRef} />
              </div>
            </CardContent>
          </Card>

          {/* Config Card */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Configuration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-neutral-100 rounded-lg p-3 h-64 overflow-y-auto font-mono text-xs">
                {config.raw ? (
                  <pre className="text-neutral-700 whitespace-pre-wrap">{config.raw}</pre>
                ) : (
                  <p className="text-neutral-500">No config available</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default App
