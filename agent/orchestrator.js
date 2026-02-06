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
import YAML from 'yaml';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_DIR = join(__dirname, '..');
const MANAGERS_PATH = join(__dirname, 'managers');
const WORKERS_PATH = join(__dirname, 'workers');
const SKILLS_PATH = join(__dirname, 'skills');
const CONFIG_PATH = join(__dirname, 'config.yaml');
const ORCHESTRATOR_PATH = join(__dirname, 'orchestrator.js');
const STATE_PATH = join(__dirname, 'state.json');

let currentAgentProcess = null;
let currentAgentName = null;
let cycleCount = 0;
let currentAgentIndex = 0;
let pendingReload = false;

function loadState() {
  try {
    const raw = readFileSync(STATE_PATH, 'utf-8');
    const state = JSON.parse(raw);
    cycleCount = state.cycleCount || 0;
    currentAgentIndex = state.currentAgentIndex || 0;
    log(`State loaded: cycle=${cycleCount}, agentIndex=${currentAgentIndex}`);
    return state;
  } catch (e) {
    log('No saved state, starting fresh');
    return { cycleCount: 0, currentAgentIndex: 0 };
  }
}

function saveState() {
  writeFileSync(STATE_PATH, JSON.stringify({ cycleCount, currentAgentIndex }, null, 2));
}

function log(message) {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  console.log(`[${timestamp}] ${message}`);
}

function loadConfig() {
  try {
    const raw = readFileSync(CONFIG_PATH, 'utf-8');
    const config = YAML.parse(raw);
    log(`Config: interval=${config.cycleIntervalMs/1000}s, model=${config.model}`);
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

async function runAgent(agent, config, isManager = false) {
  log(`Running: ${agent}${isManager ? ' (manager)' : ''}`);
  
  exec('git pull --rebase --quiet');
  
  const skillPath = isManager ? join(MANAGERS_PATH, `${agent}.md`) : join(WORKERS_PATH, `${agent}.md`);
  const everyoneSkill = loadSkill(join(__dirname, 'everyone.md'));
  const agentSkill = loadSkill(skillPath);
  
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

  return new Promise((resolve) => {
    const proc = spawn('claude', [
      '--model', config.model,
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
  const config = loadConfig();
  const workers = discoverWorkers();
  
  if (currentAgentIndex === 0) {
    cycleCount++;
    log(`===== CYCLE ${cycleCount} (${workers.length} workers) =====`);
    
    // Athena (strategist) at cycle 1, 11, 21...
    if (cycleCount % (config.athenaCycleInterval || 10) === 1) {
      await runAgent('athena', config, true);
      saveState();
      if (pendingReload) return config;
    }
    
    // Apollo (HR) at cycle 1, 11, 21...
    if (cycleCount % (config.apolloCycleInterval || 10) === 1) {
      await runAgent('apollo', config, true);
      saveState();
      if (pendingReload) return config;
    }
    
    // Hermes (PM) every cycle
    await runAgent('hermes', config, true);
    saveState();
    if (pendingReload) return config;
  } else {
    log(`===== CYCLE ${cycleCount} (resuming ${currentAgentIndex}/${workers.length}) =====`);
  }
  
  // Run worker agents
  while (currentAgentIndex < workers.length) {
    const agent = workers[currentAgentIndex];
    await runAgent(agent, config, false);
    currentAgentIndex++;
    saveState();
    if (pendingReload) return config;
  }
  
  currentAgentIndex = 0;
  saveState();
  
  return config;
}

async function main() {
  log('Orchestrator started');
  loadState();
  
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
    const config = await runCycle();
    
    if (pendingReload) {
      log('⚡ Reloading...');
      process.exit(75);
    }
    
    log(`Sleeping ${config.cycleIntervalMs / 1000}s...`);
    await sleep(config.cycleIntervalMs);
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
