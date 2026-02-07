#!/usr/bin/env node
/**
 * ML Performance Survey - Multi-Agent Orchestrator
 * Manager agents (Athena, Apollo, Hermes) run periodically.
 * Worker agents are discovered from agent/workers/ folder.
 */

import { spawn, execSync } from 'child_process';
import { existsSync, readFileSync, writeFileSync, readdirSync, watch } from 'fs';
import { dirname, join, basename } from 'path';
import { fileURLToPath } from 'url';
import { createServer } from 'http';
import YAML from 'yaml';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_DIR = join(__dirname, '..');
const MANAGERS_PATH = join(__dirname, 'managers');
const WORKERS_PATH = join(__dirname, 'workers');
const SKILLS_PATH = join(__dirname, 'skills');
const CONFIG_PATH = join(__dirname, 'config.yaml');
const ORCHESTRATOR_PATH = join(__dirname, 'orchestrator.js');
const STATE_PATH = join(__dirname, 'state.json');
const CONTROL_PORT = 3002;

let currentAgentProcess = null;
let currentAgentName = null;
let cycleCount = 0;
let currentAgentIndex = 0;
let managersCompleted = false;
let pendingReload = false;
let isPaused = false;
let startTime = Date.now();

function loadState() {
  try {
    const raw = readFileSync(STATE_PATH, 'utf-8');
    const state = JSON.parse(raw);
    cycleCount = state.cycleCount || 0;
    currentAgentIndex = state.currentAgentIndex || 0;
    managersCompleted = state.managersCompleted || false;
    log(`State loaded: cycle=${cycleCount}, agentIndex=${currentAgentIndex}, managersCompleted=${managersCompleted}`);
    return state;
  } catch (e) {
    log('No saved state, starting fresh');
    return { cycleCount: 0, currentAgentIndex: 0, managersCompleted: false };
  }
}

function saveState() {
  writeFileSync(STATE_PATH, JSON.stringify({ cycleCount, currentAgentIndex, managersCompleted }, null, 2));
}

function log(message) {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  console.log(`[${timestamp}] ${message}`);
}

function loadConfig(silent = false) {
  try {
    const raw = readFileSync(CONFIG_PATH, 'utf-8');
    const config = YAML.parse(raw);
    if (!silent) log(`Config: interval=${config.cycleIntervalMs/1000}s, model=${config.model}`);
    return config;
  } catch (e) {
    log(`Error loading config: ${e.message}, using defaults`);
    return {
      cycleIntervalMs: 600_000,
      agentTimeoutMs: 900_000,
      model: 'claude-opus-4-5',
      athenaCycleInterval: 10,
      apolloCycleInterval: 10,
      trackerIssue: 1
    };
  }
}

function discoverWorkers() {
  try {
    if (!existsSync(WORKERS_PATH)) return [];
    return readdirSync(WORKERS_PATH)
      .filter(f => f.endsWith('.md') && f !== 'everyone.md')
      .map(f => basename(f, '.md'));
  } catch (e) {
    log(`Error discovering workers: ${e.message}`);
    return [];
  }
}

function exec(cmd, options = {}) {
  try {
    return execSync(cmd, { 
      cwd: REPO_DIR, 
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      ...options 
    }).trim();
  } catch (e) {
    return e.stdout?.trim() || '';
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function loadSkill(path) {
  try {
    return readFileSync(path, 'utf-8');
  } catch (e) {
    log(`Warning: Could not load skill ${path}: ${e.message}`);
    return '';
  }
}

function extractModel(skillContent) {
  // Parse YAML frontmatter for model field
  const match = skillContent.match(/^---\n([\s\S]*?)\n---/);
  if (match) {
    const frontmatter = match[1];
    const modelMatch = frontmatter.match(/^model:\s*(.+)$/m);
    if (modelMatch) {
      return modelMatch[1].trim();
    }
  }
  return null;
}

async function runAgent(agent, config, isManager = false) {
  log(`Running: ${agent}${isManager ? ' (manager)' : ''}`);
  
  exec('git pull --rebase --quiet');
  
  const skillPath = isManager ? join(MANAGERS_PATH, `${agent}.md`) : join(WORKERS_PATH, `${agent}.md`);
  const everyoneSkill = loadSkill(join(__dirname, 'everyone.md'));
  const agentSkill = loadSkill(skillPath);
  const agentModel = extractModel(agentSkill) || config.model;
  
  const prompt = `You are ${agent} working on the ML Performance Survey project.

**Config:**
- GitHub Repo: syifan/ml-perf-survey
- Local Path: ${REPO_DIR}
- Tracker Issue: #${config.trackerIssue}

**Shared Rules:**
${everyoneSkill}

**Your Role:**
${agentSkill}

**Instructions:**
Execute your full cycle as described above. Work autonomously. Complete your tasks, then exit.`;

  log(`Using model: ${agentModel}`);
  
  return new Promise((resolve) => {
    const proc = spawn('claude', [
      '--model', agentModel,
      '--dangerously-skip-permissions',
      '--print',
      prompt
    ], {
      cwd: REPO_DIR,
      stdio: ['ignore', 'ignore', 'ignore']
    });

    currentAgentProcess = proc;
    currentAgentName = agent;

    const timeout = setTimeout(() => {
      log(`${agent} timed out, killing...`);
      proc.kill('SIGTERM');
    }, config.agentTimeoutMs);

    proc.on('close', (code) => {
      clearTimeout(timeout);
      currentAgentProcess = null;
      currentAgentName = null;
      log(`${agent} done (code ${code})`);
      resolve(code);
    });

    proc.on('error', (err) => {
      clearTimeout(timeout);
      currentAgentProcess = null;
      currentAgentName = null;
      log(`${agent} error: ${err.message}`);
      resolve(1);
    });
  });
}

async function runCycle() {
  // Check for STOP file
  const stopFile = join(__dirname, 'STOP');
  if (existsSync(stopFile)) {
    log('🛑 STOP file found - halting orchestrator');
    const reason = readFileSync(stopFile, 'utf-8');
    log(reason);
    process.exit(0);
  }
  
  const config = loadConfig();
  const workers = discoverWorkers();
  
  // New cycle: run managers first
  if (!managersCompleted) {
    cycleCount++;
    log(`===== CYCLE ${cycleCount} (${workers.length} workers) =====`);
    
    // Athena (strategist) - runs on cycle 1, 1+interval, 1+2*interval, etc.
    if ((cycleCount - 1) % (config.athenaCycleInterval || 10) === 0) {
      await runAgent('athena', config, true);
      saveState();
      if (pendingReload) return config;
    }
    
    // Apollo (HR) - runs on cycle 1, 1+interval, 1+2*interval, etc.
    if ((cycleCount - 1) % (config.apolloCycleInterval || 10) === 0) {
      await runAgent('apollo', config, true);
      saveState();
      if (pendingReload) return config;
    }
    
    // Hermes (PM) every cycle
    await runAgent('hermes', config, true);
    managersCompleted = true;
    saveState();
    if (pendingReload) return config;
  } else {
    log(`===== CYCLE ${cycleCount} (resuming workers ${currentAgentIndex}/${workers.length}) =====`);
  }
  
  // Run worker agents
  while (currentAgentIndex < workers.length) {
    const agent = workers[currentAgentIndex];
    await runAgent(agent, config, false);
    currentAgentIndex++;
    saveState();
    if (pendingReload) return config;
  }
  
  // Cycle complete - reset for next cycle
  currentAgentIndex = 0;
  managersCompleted = false;
  saveState();
  
  return config;
}

// ============ Control API Server ============

function startControlServer() {
  const server = createServer((req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }
    
    const url = new URL(req.url, `http://localhost:${CONTROL_PORT}`);
    const path = url.pathname;
    
    // GET /status
    if (req.method === 'GET' && path === '/status') {
      const config = loadConfig(true);  // silent
      const workers = discoverWorkers();
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        running: !isPaused,
        paused: isPaused,
        currentAgent: currentAgentName,
        currentAgentIndex,
        cycleCount,
        managersCompleted,
        totalWorkers: workers.length,
        pid: process.pid,
        uptime: Math.floor((Date.now() - startTime) / 1000),
        cycleIntervalMs: config.cycleIntervalMs,
        pendingReload
      }));
      return;
    }
    
    // GET /queue
    if (req.method === 'GET' && path === '/queue') {
      const workers = discoverWorkers();
      const config = loadConfig(true);  // silent
      const queue = [];
      
      // Add remaining workers in current cycle
      for (let i = currentAgentIndex; i < workers.length; i++) {
        queue.push({ name: workers[i], type: 'worker' });
      }
      
      // Add managers for next cycle
      const nextCycle = cycleCount + 1;
      if ((nextCycle - 1) % (config.athenaCycleInterval || 10) === 0) {
        queue.push({ name: 'athena', type: 'manager', nextCycle: true });
      }
      if ((nextCycle - 1) % (config.apolloCycleInterval || 10) === 0) {
        queue.push({ name: 'apollo', type: 'manager', nextCycle: true });
      }
      queue.push({ name: 'hermes', type: 'manager', nextCycle: true });
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ queue, workers }));
      return;
    }
    
    // POST /pause
    if (req.method === 'POST' && path === '/pause') {
      isPaused = true;
      log('⏸️  Paused via API');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, paused: true }));
      return;
    }
    
    // POST /resume
    if (req.method === 'POST' && path === '/resume') {
      isPaused = false;
      log('▶️  Resumed via API');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, paused: false }));
      return;
    }
    
    // POST /skip
    if (req.method === 'POST' && path === '/skip') {
      if (currentAgentProcess) {
        log(`⏭️  Skipping ${currentAgentName} via API`);
        currentAgentProcess.kill('SIGTERM');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, skipped: currentAgentName }));
      } else {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, message: 'No agent running' }));
      }
      return;
    }
    
    // POST /reload
    if (req.method === 'POST' && path === '/reload') {
      log('🔄 Reload requested via API');
      pendingReload = true;
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, pendingReload: true }));
      return;
    }
    
    // POST /stop
    if (req.method === 'POST' && path === '/stop') {
      log('🛑 Stop requested via API');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, stopping: true }));
      if (currentAgentProcess) currentAgentProcess.kill('SIGTERM');
      setTimeout(() => process.exit(0), 500);
      return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  });
  
  server.listen(CONTROL_PORT, () => {
    log(`Control API listening on http://localhost:${CONTROL_PORT}`);
  });
  
  return server;
}

async function main() {
  log('Orchestrator started');
  loadState();
  startControlServer();
  
  let debounce = null;
  watch(ORCHESTRATOR_PATH, (eventType) => {
    if (eventType === 'change') {
      clearTimeout(debounce);
      debounce = setTimeout(() => {
        log('⚡ Code changed — reloading after current agent');
        pendingReload = true;
      }, 500);
    }
  });
  
  while (true) {
    // Check pause state
    while (isPaused) {
      await sleep(1000);
    }
    
    await runCycle();
    
    if (pendingReload) {
      log('⚡ Reloading...');
      process.exit(75);
    }
    
    // Reload config right before sleep to get latest interval
    const sleepConfig = loadConfig();
    log(`Sleeping ${sleepConfig.cycleIntervalMs / 1000}s...`);
    await sleep(sleepConfig.cycleIntervalMs);
  }
}

process.on('SIGINT', () => {
  log('Shutting down...');
  if (currentAgentProcess) currentAgentProcess.kill('SIGTERM');
  process.exit(0);
});

process.on('SIGTERM', () => {
  log('Shutting down...');
  if (currentAgentProcess) currentAgentProcess.kill('SIGTERM');
  process.exit(0);
});

process.on('SIGHUP', () => {
  log('⚡ SIGHUP — reloading after current agent');
  pendingReload = true;
});

main().catch(console.error);
