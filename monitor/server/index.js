import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3001;

// Agent directory relative to monitor folder
const AGENT_DIR = path.resolve(__dirname, '../../agent');

app.use(cors());
app.use(express.json());

// GET /api/state - Read orchestrator state
app.get('/api/state', (req, res) => {
  try {
    const statePath = path.join(AGENT_DIR, 'state.json');
    if (!fs.existsSync(statePath)) {
      return res.json({ cycleCount: 0, currentAgentIndex: 0 });
    }
    const data = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /api/logs - Read last N lines of orchestrator.log
app.get('/api/logs', (req, res) => {
  try {
    const logPath = path.join(AGENT_DIR, 'orchestrator.log');
    const lines = parseInt(req.query.lines) || 50;
    
    if (!fs.existsSync(logPath)) {
      return res.json({ logs: [] });
    }
    
    const content = fs.readFileSync(logPath, 'utf-8');
    const allLines = content.split('\n').filter(line => line.trim());
    const lastLines = allLines.slice(-lines);
    
    res.json({ logs: lastLines });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /api/agents - List human and god agents
app.get('/api/agents', (req, res) => {
  try {
    const humansDir = path.join(AGENT_DIR, 'humans');
    const godsDir = path.join(AGENT_DIR, 'gods');
    
    const humans = [];
    const gods = [];
    
    // Read human agents
    if (fs.existsSync(humansDir)) {
      const humanFiles = fs.readdirSync(humansDir).filter(f => f.endsWith('.md'));
      for (const file of humanFiles) {
        const name = file.replace('.md', '');
        const content = fs.readFileSync(path.join(humansDir, file), 'utf-8');
        const firstLine = content.split('\n')[0].replace(/^#\s*/, '');
        humans.push({ name, title: firstLine, file });
      }
    }
    
    // Read god agents
    if (fs.existsSync(godsDir)) {
      const godFiles = fs.readdirSync(godsDir).filter(f => f.endsWith('.md'));
      for (const file of godFiles) {
        const name = file.replace('.md', '');
        const content = fs.readFileSync(path.join(godsDir, file), 'utf-8');
        const firstLine = content.split('\n')[0].replace(/^#\s*/, '');
        gods.push({ name, title: firstLine, file });
      }
    }
    
    res.json({ humans, gods });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /api/config - Read config.yaml
app.get('/api/config', (req, res) => {
  try {
    const configPath = path.join(AGENT_DIR, 'config.yaml');
    if (!fs.existsSync(configPath)) {
      return res.json({ config: null });
    }
    const content = fs.readFileSync(configPath, 'utf-8');
    const config = yaml.load(content);
    res.json({ config, raw: content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Monitor API server running on http://localhost:${PORT}`);
});
