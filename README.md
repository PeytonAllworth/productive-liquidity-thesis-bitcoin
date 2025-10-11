# Reimagining Keynesian Economics: Bitcoin as a Productive, Liquid Asset in Economic Crises

**Author:** Peyton Allworth  
**Status:** Pre-publication (preparing for Ledger journal submission)

---

## Overview

This research challenges a core assumption of Keynesian economics: that the most liquid asset in an economy (money) is inherently unproductive and thus requires expansion during crises to prevent hoarding and support aggregate demand.

**Core Thesis:**  
Bitcoin, due to its lack of capital controls at the base layer, is the most liquid asset available globally. However, unlike traditional fiat money, Bitcoin is *not* unproductive. Through its proof-of-work mechanism, transaction fees flow directly to miners who invest in energy and infrastructure. During economic crises, increased on-chain liquidity preference behavior (urgency, fee-market activity) creates a counter-cyclical economic force—miner revenue increases precisely when economic activity spikes—*without requiring monetary expansion*.

This finding is critical because Bitcoin's adoption threatens the very mechanism (monetary expansion) that Keynesian policy relies upon. Understanding Bitcoin's productive liquidity may offer an alternative framework for crisis response in a post-fiat world.

---

## Research Question

**Do economic crises trigger measurable liquidity-preference behavior on Bitcoin's base layer, and does this behavior increase miner revenue in ways that could create counter-cyclical economic effects?**

---

## Core Metrics (BTC-Native Only)

This study uses **four categories of on-chain indicators**, all measured in Bitcoin-native units:

### 1. Fee Rate & Urgency
- **Median fee rate** (sat/vB) — baseline willingness to pay
- **Urgency spread** (p90 - p50) — willingness to "cut the mempool line"

### 2. Fees & Fee-to-Subsidy
- **Fees per block** (BTC) — direct miner revenue from fees
- **Fee-to-Subsidy ratio** — proportion of block reward from fees vs. subsidy

### 3. Dormancy Proxy (CDD/BDD)
- **Bitcoin/Coin Days Destroyed** — old coins moving (liquidity preference)
- Indicates HODLers breaking dormancy during crises

### 4. Activity Pressure
- **Mempool backlog** (vbytes) — unconfirmed transaction pressure
- **Transactions per day** — base-layer usage intensity

---

## Data Sources (Free & Open)

1. **Blockchain.com API** — Total fees/day, transactions/day, BDD
2. **Mempool.space API** — Mempool backlog, fee estimates (limited historical data)
3. **Bitcoin Core RPC** (optional) — Full node for per-block/per-tx granularity (requires `txindex=1`)
4. **Community mirrors/CSVs** — For historical data gaps

**Note:** We avoid USD-denominated metrics entirely. All analysis is in BTC, sats, sat/vB, or ratios.

---

## Event Windows

We analyze three crisis periods using **±90-day windows** (default) around anchor dates:

1. **Cyprus Banking Crisis** (March 2013) — Capital controls, bank runs
2. **Venezuela Hyperinflation** (2017-2018) — Currency collapse, LocalBitcoins surge
3. **COVID/CPI Peak** (June 2022) — Inflation peak, macro uncertainty

Each event compares:
- **Pre-period:** Days before the anchor
- **Crisis period:** Days after (and including) the anchor

---

## Methodology

### Reproducibility Pipeline

```
1. Raw data collection    → data/raw/
2. Metric computation      → data/processed/
3. Event window analysis   → Sliced CSVs + summary tables
4. Visualization           → data/figures/ (PNG charts)
```

### Statistical Approach

- **Descriptive statistics:** Mean, median, p90 for pre vs. crisis periods
- **Percent change:** `(crisis_mean - pre_mean) / pre_mean * 100`
- **Percentage point change:** For ratios (e.g., fee-to-subsidy)
- **Rolling averages:** 30-day MA for smoothing

**Limitation:** This is a descriptive study. We do not claim causal inference. Confounds include Bitcoin price movements, halving cycles, Layer 2 adoption, inscriptions/ordinals, and other technological/market factors.

---

## Repository Structure

```
reimagining-keynes-bitcoin-liquidity-crises/
├─ README.md                    ← You are here
├─ LICENSE                      ← MIT
├─ .gitignore                   ← Python + data exclusions
├─ requirements.txt             ← Python dependencies
├─ config/
│  ├─ settings.example.yaml     ← Copy to settings.yaml and edit
│  └─ __init__.py
├─ data/
│  ├─ raw/                      ← Downloaded JSON/CSV snapshots
│  ├─ processed/                ← Tidy, metric-ready CSVs
│  └─ figures/                  ← Saved PNG/SVG charts
├─ src/
│  ├─ __init__.py
│  ├─ config.py                 ← Load settings.yaml
│  ├─ utils/
│  │  ├─ date_windows.py        ← Event window logic
│  │  ├─ io.py                  ← CSV save/load helpers
│  │  └─ math_stats.py          ← Percentiles, % change, etc.
│  ├─ data_sources/             ← API adapters
│  │  ├─ node_rpc.py            ← Bitcoin Core RPC (optional)
│  │  ├─ mempool_space.py       ← Mempool.space API
│  │  ├─ blockchain_com.py      ← Blockchain.com API
│  │  ├─ input_new_data_source_1.py  ← Placeholder for custom data
│  │  ├─ input_new_data_source_2.py
│  │  └─ input_new_data_source_3.py
│  ├─ metrics/                  ← Metric calculators
│  │  ├─ fee_rate_urgency.py
│  │  ├─ fees_and_fee_to_subsidy.py
│  │  ├─ dormancy_cdd.py
│  │  └─ mempool_and_tx_activity.py
│  ├─ plotting/                 ← Chart generation
│  │  ├─ styles.py
│  │  └─ plot_event_windows.py
│  └─ pipelines/                ← End-to-end workflows
│     ├─ build_event_dataset.py
│     └─ compute_summary_tables.py
├─ scripts/                     ← CLI entry points
│  ├─ 01_fetch_data.py
│  ├─ 02_compute_metrics.py
│  └─ 03_make_figures.py
└─ paper/                       ← Manuscript drafts
   ├─ paper_outline.md
   └─ references.bib
```

---

## Quickstart

### 1. Install Dependencies

```bash
cd /Users/peytonallworth/projects/reimagining-keynes-bitcoin-liquidity-crises
pip install -r requirements.txt
```

### 2. Configure Settings

```bash
cp config/settings.example.yaml config/settings.yaml
# Edit settings.yaml with your RPC credentials (if using node) or leave defaults for APIs
```

### 3. Fetch Data

```bash
python scripts/01_fetch_data.py --sources blockchain_com mempool_space --start-date 2012-01-01 --end-date 2024-01-01
```

### 4. Compute Metrics

```bash
python scripts/02_compute_metrics.py
```

### 5. Generate Figures

```bash
python scripts/03_make_figures.py --event cyprus_2013 --days-before 90 --days-after 90
python scripts/03_make_figures.py --event venezuela_2017
python scripts/03_make_figures.py --event covid_cpi_peak_2022
```

Charts will be saved to `data/figures/`.

---

## Bitcoin Core Node Setup (Optional but Recommended)

For full historical data, consider running a Bitcoin Core node:

### On Raspberry Pi or Desktop:

1. **Install Bitcoin Core:** https://bitcoin.org/en/download
2. **Edit `bitcoin.conf`:**
   ```
   txindex=1
   server=1
   rpcuser=bitcoinrpc
   rpcpassword=YOUR_SECURE_PASSWORD
   ```
3. **Sync the blockchain** (this takes days/weeks)
4. **Update `config/settings.yaml`** with your RPC credentials

**Why?** APIs often lack deep historical data or per-transaction granularity. A full node gives you complete control.

---

## Publishing to GitHub

This repo is ready to be pushed to GitHub:

```bash
# (Assuming git is already initialized locally)
gh repo create reimagining-keynes-bitcoin-liquidity-crises --public --source=. --remote=origin
git push -u origin main
```

Or manually:
1. Create repo on GitHub: https://github.com/new (name: `reimagining-keynes-bitcoin-liquidity-crises`, public)
2. Add remote: `git remote add origin https://github.com/YOUR_USERNAME/reimagining-keynes-bitcoin-liquidity-crises.git`
3. Push: `git push -u origin main`

---

## Limitations

1. **Descriptive, not causal** — We observe correlations, not mechanisms
2. **Confounds:**
   - Bitcoin price volatility (though we avoid USD units)
   - Halving events (subsidy reductions)
   - Layer 2 adoption (Lightning reduces base-layer pressure)
   - Inscriptions/Ordinals (non-monetary fee activity)
   - Regulatory events unrelated to macroeconomic crises
3. **Data availability** — Some APIs lack deep historical data; manual CSV snapshots may be needed
4. **Sample size** — Only three crisis events (more research needed)

---

## Future Work

- Expand crisis catalog (SVB 2023, Greek crisis 2015, etc.)
- Segment fee activity (monetary vs. non-monetary/inscriptions)
- Layer 2 adoption modeling (how Lightning affects base-layer urgency)
- Comparative analysis with gold flows during crises
- Causal inference methods (difference-in-differences, synthetic controls)

---

## Citation

If you use this research or code, please cite:

```bibtex
@article{allworth2025keynes,
  title={Reimagining Keynesian Economics: Bitcoin as a Productive, Liquid Asset in Economic Crises},
  author={Allworth, Peyton},
  journal={Ledger},
  year={2025},
  note={Preprint},
  url={https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin}
}
```

**For the code specifically:**
```
Allworth, P. (2025). Bitcoin Liquidity Crisis Research [Software]. 
Available at: https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin
Licensed under MIT License.
```

---

## Contact

For questions, collaboration, or data sharing:  
**Email:** peytonallworth0001@gmail.com  
**LinkedIn:** https://www.linkedin.com/in/peytonallworth/  
**GitHub:** https://github.com/PeytonAllworth  
**Issues:** https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin/issues

---

## License & Copyright

### Code & Software
The **code, scripts, and software** in this repository are released under the **MIT License** (see [LICENSE](LICENSE)).  
You are free to use, modify, and distribute the code with attribution.

### Research Paper & Ideas
The **research paper, theoretical contributions, and written content** in the `paper/` directory are **© 2025 Peyton Allworth. All Rights Reserved.**

The ideas, analysis, and theoretical framework (the "productive liquid asset" thesis) are original intellectual contributions by Peyton Allworth. 

**To use or reference this research:**
- **Cite the published paper** (once published in Ledger)
- **Pre-publication citation:**
  ```
  Allworth, P. (2025). Reimagining Keynesian Economics: Bitcoin as a Productive, 
  Liquid Asset in Economic Crises. Preprint. https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin
  ```

**Why separate licenses?**
- **Code = MIT License:** Encourages reproducibility and scientific transparency
- **Paper = Copyright:** Protects intellectual contribution and ensures proper academic attribution
- **Ledger publication:** Timestamped on Bitcoin blockchain for permanent proof of authorship

This follows standard academic practice: Open-source code + copyrighted research content.

