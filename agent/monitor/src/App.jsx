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
  const [configForm, setConfigForm] = useState({
    cycleIntervalMs: 1800000,
    agentTimeoutMs: 900000,
    model: 'claude-opus-4-5',
    trackerIssue: 1,
    athenaCycleInterval: 1,
    apolloCycleInterval: 1
  })
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
      // Only update form if not being edited
      if (!configDirty && configData.config) {
        setConfigForm({
          cycleIntervalMs: configData.config.cycleIntervalMs || 1800000,
          agentTimeoutMs: configData.config.agentTimeoutMs || 900000,
          model: configData.config.model || 'claude-opus-4-5',
          trackerIssue: configData.config.trackerIssue || 1,
          athenaCycleInterval: configData.config.athenaCycleInterval || 1,
          apolloCycleInterval: configData.config.apolloCycleInterval || 1
        })
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
      // Generate YAML from form
      const yaml = `# ML Performance Survey - Orchestrator Configuration
# Reloaded at the start of each cycle

cycleIntervalMs: ${configForm.cycleIntervalMs}
agentTimeoutMs: ${configForm.agentTimeoutMs}
model: ${configForm.model}
trackerIssue: ${configForm.trackerIssue}

# Manager agents (run periodically, manage the system)
athenaCycleInterval: ${configForm.athenaCycleInterval}
apolloCycleInterval: ${configForm.apolloCycleInterval}

# Worker agents are discovered from agent/workers/ folder
`
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: yaml })
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
  
  const updateConfigField = (field, value) => {
    setConfigForm(prev => ({ ...prev, [field]: value }))
    setConfigDirty(true)
    setConfigError(null)
  }
  
  const resetConfig = () => {
    if (config.config) {
      setConfigForm({
        cycleIntervalMs: config.config.cycleIntervalMs || 1800000,
        agentTimeoutMs: config.config.agentTimeoutMs || 900000,
        model: config.config.model || 'claude-opus-4-5',
        trackerIssue: config.config.trackerIssue || 1,
        athenaCycleInterval: config.config.athenaCycleInterval || 1,
        apolloCycleInterval: config.config.apolloCycleInterval || 1
      })
    }
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
                {agents.workers.map((agent) => {
                  const isActive = orchestratorStatus?.currentAgent === agent.name
                  return (
                    <div
                      key={agent.name}
                      className={`flex items-center justify-between p-2 rounded ${
                        isActive
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
                      {isActive && (
                        <Badge variant="success">Active</Badge>
                      )}
                    </div>
                  )
                })}
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
                {agents.managers.map((agent) => {
                  const isActive = orchestratorStatus?.currentAgent === agent.name
                  return (
                    <div
                      key={agent.name}
                      className={`flex items-center justify-between p-2 rounded ${
                        isActive
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
                      {isActive && (
                        <Badge variant="success">Active</Badge>
                      )}
                    </div>
                  )
                })}
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
              <div className="space-y-3 text-sm">
                {/* Cycle Interval */}
                <div className="flex items-center justify-between">
                  <label className="text-neutral-600">Cycle Interval</label>
                  <select 
                    className="px-2 py-1 bg-neutral-100 border rounded text-sm"
                    value={configForm.cycleIntervalMs}
                    onChange={(e) => updateConfigField('cycleIntervalMs', Number(e.target.value))}
                  >
                    <option value={0}>No delay</option>
                    <option value={300000}>5 minutes</option>
                    <option value={600000}>10 minutes</option>
                    <option value={1200000}>20 minutes</option>
                    <option value={1800000}>30 minutes</option>
                    <option value={3600000}>1 hour</option>
                  </select>
                </div>
                
                {/* Agent Timeout */}
                <div className="flex items-center justify-between">
                  <label className="text-neutral-600">Agent Timeout</label>
                  <select 
                    className="px-2 py-1 bg-neutral-100 border rounded text-sm"
                    value={configForm.agentTimeoutMs}
                    onChange={(e) => updateConfigField('agentTimeoutMs', Number(e.target.value))}
                  >
                    <option value={300000}>5 minutes</option>
                    <option value={600000}>10 minutes</option>
                    <option value={900000}>15 minutes</option>
                    <option value={1800000}>30 minutes</option>
                  </select>
                </div>
                
                {/* Model */}
                <div className="flex items-center justify-between">
                  <label className="text-neutral-600">Default Model</label>
                  <select 
                    className="px-2 py-1 bg-neutral-100 border rounded text-sm"
                    value={configForm.model}
                    onChange={(e) => updateConfigField('model', e.target.value)}
                  >
                    <option value="claude-sonnet-4-20250514">Sonnet 4</option>
                    <option value="claude-opus-4-5">Opus 4.5</option>
                    <option value="claude-opus-4-6">Opus 4.6</option>
                  </select>
                </div>
                
                {/* Athena Cycle Interval */}
                <div className="flex items-center justify-between">
                  <label className="text-neutral-600">Athena runs every</label>
                  <div className="flex items-center gap-1">
                    <input 
                      type="number"
                      className="w-16 px-2 py-1 bg-neutral-100 border rounded text-sm text-right"
                      value={configForm.athenaCycleInterval}
                      onChange={(e) => updateConfigField('athenaCycleInterval', Number(e.target.value))}
                      min={1}
                    />
                    <span className="text-neutral-500 text-xs">cycles</span>
                  </div>
                </div>
                
                {/* Apollo Cycle Interval */}
                <div className="flex items-center justify-between">
                  <label className="text-neutral-600">Apollo runs every</label>
                  <div className="flex items-center gap-1">
                    <input 
                      type="number"
                      className="w-16 px-2 py-1 bg-neutral-100 border rounded text-sm text-right"
                      value={configForm.apolloCycleInterval}
                      onChange={(e) => updateConfigField('apolloCycleInterval', Number(e.target.value))}
                      min={1}
                    />
                    <span className="text-neutral-500 text-xs">cycles</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default App
