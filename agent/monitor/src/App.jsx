import { useState, useEffect, useRef } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Activity, Users, Sparkles, Settings, ScrollText, RefreshCw, Pause, Play, SkipForward, RotateCcw, Square, Save } from 'lucide-react'

// Proxied through monitor backend to work with Cloudflare tunnel
const ORCHESTRATOR_API = '/api/orchestrator'

function App() {
  const [state, setState] = useState({ cycleCount: 0, currentAgentIndex: 0 })
  const [logs, setLogs] = useState([])
  const [agents, setAgents] = useState({ workers: [], managers: [] })
  const [config, setConfig] = useState({ config: null, raw: '' })
  const [configDraft, setConfigDraft] = useState('')
  const [configDirty, setConfigDirty] = useState(false)
  const [configError, setConfigError] = useState(null)
  const [configSaving, setConfigSaving] = useState(false)
  const [orchestratorStatus, setOrchestratorStatus] = useState(null)
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
      const configData = await configRes.json()
      setConfig(configData)
      // Only update draft if not being edited
      if (!configDirty && configData.raw) {
        setConfigDraft(configData.raw)
      }
      setLastUpdate(new Date())
      setError(null)
      
      // Fetch orchestrator status via proxy
      try {
        const statusRes = await fetch(`${ORCHESTRATOR_API}/status`)
        const statusData = await statusRes.json()
        if (!statusData.offline) {
          setOrchestratorStatus(statusData)
        } else {
          setOrchestratorStatus(null)
        }
      } catch {
        setOrchestratorStatus(null)
      }
    } catch (err) {
      setError(err.message)
    }
  }
  
  const controlAction = async (action) => {
    try {
      const res = await fetch(`${ORCHESTRATOR_API}/${action}`, { method: 'POST' })
      if (res.ok) {
        await fetchData()
      }
    } catch (err) {
      console.error(`Control action ${action} failed:`, err)
    }
  }
  
  const saveConfig = async () => {
    setConfigSaving(true)
    setConfigError(null)
    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: configDraft })
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.error || 'Failed to save')
      }
      setConfigDirty(false)
      await fetchData()
    } catch (err) {
      setConfigError(err.message)
    } finally {
      setConfigSaving(false)
    }
  }
  
  const handleConfigChange = (e) => {
    setConfigDraft(e.target.value)
    setConfigDirty(true)
    setConfigError(null)
  }
  
  const resetConfig = () => {
    setConfigDraft(config.raw || '')
    setConfigDirty(false)
    setConfigError(null)
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
                  <span className="text-neutral-600">Status</span>
                  {orchestratorStatus ? (
                    <Badge variant={orchestratorStatus.paused ? 'warning' : 'success'}>
                      {orchestratorStatus.paused && orchestratorStatus.currentAgent
                        ? '⏳ Pausing...'
                        : orchestratorStatus.paused
                        ? '⏸️ Paused'
                        : '▶️ Running'}
                    </Badge>
                  ) : (
                    <Badge variant="destructive">Offline</Badge>
                  )}
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-neutral-600">Cycle Count</span>
                  <span className="text-2xl font-mono font-bold text-neutral-800">
                    {orchestratorStatus?.cycleCount ?? state.cycleCount}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-neutral-600">Current Agent</span>
                  <Badge variant="secondary">
                    {orchestratorStatus?.currentAgent || 'None'}
                  </Badge>
                </div>
                {orchestratorStatus && (
                  <div className="flex justify-between items-center">
                    <span className="text-neutral-600">Uptime</span>
                    <span className="text-sm font-mono text-neutral-700">
                      {Math.floor(orchestratorStatus.uptime / 3600)}h {Math.floor((orchestratorStatus.uptime % 3600) / 60)}m
                    </span>
                  </div>
                )}
                
                {/* Control Buttons */}
                {orchestratorStatus && (
                  <div className="pt-3 border-t flex flex-wrap gap-2">
                    {orchestratorStatus.paused ? (
                      <Button size="sm" onClick={() => controlAction('resume')} className="flex-1">
                        <Play className="w-3 h-3 mr-1" /> Resume
                      </Button>
                    ) : (
                      <Button size="sm" variant="outline" onClick={() => controlAction('pause')} className="flex-1">
                        <Pause className="w-3 h-3 mr-1" /> Pause
                      </Button>
                    )}
                    <Button size="sm" variant="outline" onClick={() => controlAction('skip')} className="flex-1">
                      <SkipForward className="w-3 h-3 mr-1" /> Skip
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => controlAction('reload')}>
                      <RotateCcw className="w-3 h-3" />
                    </Button>
                    <Button size="sm" variant="destructive" onClick={() => {
                      if (confirm('Stop the orchestrator?')) controlAction('stop')
                    }}>
                      <Square className="w-3 h-3" />
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Worker Agents Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Workers ({agents.workers.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {agents.workers.map((agent, idx) => (
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
                {agents.workers.length === 0 && (
                  <p className="text-sm text-neutral-400">No workers found</p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Manager Agents Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-4 h-4" />
                Managers ({agents.managers.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {agents.managers.map((agent) => (
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
                {agents.managers.length === 0 && (
                  <p className="text-sm text-neutral-400">No managers found</p>
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
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Settings className="w-4 h-4" />
                  Configuration
                </span>
                <div className="flex items-center gap-2">
                  {configDirty && (
                    <Badge variant="warning">Unsaved</Badge>
                  )}
                  {configDirty && (
                    <Button size="sm" variant="ghost" onClick={resetConfig}>
                      Reset
                    </Button>
                  )}
                  <Button 
                    size="sm" 
                    onClick={saveConfig} 
                    disabled={!configDirty || configSaving}
                  >
                    <Save className="w-3 h-3 mr-1" />
                    {configSaving ? 'Saving...' : 'Save'}
                  </Button>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              {configError && (
                <div className="mb-2 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                  {configError}
                </div>
              )}
              <textarea
                className="w-full h-56 bg-neutral-100 rounded-lg p-3 font-mono text-xs text-neutral-700 resize-none focus:outline-none focus:ring-2 focus:ring-blue-200"
                value={configDraft}
                onChange={handleConfigChange}
                placeholder="No config available"
                spellCheck={false}
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default App
