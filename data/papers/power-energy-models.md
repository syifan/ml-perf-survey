# Power and Energy Prediction Models

Papers on ML-based power modeling, GPU energy optimization, and alternatives to analytical power models (2017-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Target | Notes |
|-------|---------|------|-------|--------|-------|
| Zeus | You et al. | 2023 | NSDI | GPU | 15-76% energy reduction, open-source |
| Perseus | You et al. | 2024 | arXiv | GPU | Large model training energy |
| Accelergy | Wu et al. | 2019 | ICCAD | NPU | Component-level energy estimation |
| PRIME | various | 2023 | DAC | NPU | ML power model, 5% error |
| NeuroSim | Chen et al. | 2018 | TCAD | NPU | Circuit-level PPA modeling |
| CarbonTracker | Anthony et al. | 2020 | ICML-WS | Multi | Real-time carbon footprint |
| CodeCarbon | Courty et al. | 2022 | arXiv | Multi | Open-source carbon tracking |
| HADAS | Siddiqui et al. | 2023 | DATE | Edge | NAS + DVFS, 57% energy gains |
| BUTTER-E | various | 2024 | arXiv | Multi | 30K+ config benchmark |

---

## Key Categories

### GPU Energy Optimization
- **Zeus (2023)**: Automatic energy optimization
  - Batch size + power limit search
  - 15.3-75.8% energy reduction
  - Open-source PyTorch integration
  - Michigan team

- **Perseus (2024)**: Large model training
  - Extends Zeus to distributed training
  - Addresses energy bloat

- **GPU Energy Empirical (2024)**: BUTTER-E dataset
  - 63,527 experimental runs
  - 30,582 distinct configurations
  - Enables ML model training

### Accelerator Power Modeling
- **Accelergy (2019)**: Component-level estimation
  - Companion to Timeloop
  - Library-based approach
  - MIT

- **PRIME (2023)**: ML-based power model
  - Trained on RTL simulation
  - 5% error vs RTL, 1000x faster

- **NeuroSim (2018)**: Circuit-level modeling
  - Various memory technologies
  - Georgia Tech

### Carbon and Sustainability
- **CarbonTracker (2020)**: Real-time tracking
  - Predictive modeling for jobs
  - Copenhagen

- **CodeCarbon (2022)**: Open-source library
  - Major ML framework integration

- **Chasing Low-Carbon (2023)**: Carbon-aware scheduling
  - Geographic and temporal optimization

### Energy-Aware NAS
- **Energy Estimation for NAS (2017)**: Layer-wise model
  - Enables energy-aware architecture search
  - MIT

- **HADAS (2023)**: Dynamic optimization
  - Joint NAS + DVFS
  - Up to 57% energy gains on edge

---

## Key Insights

1. **GPU Energy Is Underexplored**: Zeus is pioneering work
2. **Analytical + ML Hybrid Works Best**: Accelergy + ML refinement
3. **Carbon Awareness Emerging**: Multiple tools now available
4. **Energy and Latency Often Trade Off**: Need multi-objective models
5. **Edge Devices Have Unique Constraints**: HADAS addresses this

---

## Gap Analysis

### Well-Covered
- GPU training energy (Zeus, Perseus)
- Accelerator energy estimation (Accelergy)
- Carbon tracking (CarbonTracker, CodeCarbon)

### Underexplored
- LLM inference energy prediction
- Real-time power control
- Multi-accelerator energy balancing
- Embodied carbon in hardware

---

## Coverage for Survey

This file addresses reviewer W1 gap: "Power/energy prediction models (McPAT alternatives)"

Papers added: 15+
Key venues: NSDI, ICCAD, DAC, DATE, TCAD
