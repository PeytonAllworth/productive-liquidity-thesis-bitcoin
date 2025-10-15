# Reimagining Keynesian Economics: Bitcoin as a Productive, Liquid Asset in Economic Crises

**Author:** Peyton Allworth  
**Target Journal:** Ledger  
**Target Length:** 8,000–12,000 words  
**Status:** Draft outline

---

**Copyright Notice:**  
© 2025 Peyton Allworth. All Rights Reserved.

This research paper, including all theoretical contributions, analysis, and written content, is the original intellectual property of Peyton Allworth. The "productive liquid asset" thesis and associated framework are original contributions to Bitcoin economics and monetary theory.

This work is intended for publication in Ledger journal, which timestamps publications on the Bitcoin blockchain for permanent proof of authorship.

---

## Abstract (250 words max)

**Summary of key argument:**
- Keynesian economics posits that money, as the most liquid asset, must be expanded during crises to prevent hoarding and support aggregate demand
- Central assumption: money is inherently unproductive
- Bitcoin challenges this framework: it is the most liquid asset (no capital controls at base layer) BUT is productive (PoW → miner revenue → energy/infrastructure investment)
- Research question: Do economic crises trigger measurable liquidity-preference behavior on Bitcoin's base layer, and does this behavior increase miner revenue?
- Method: Event study analysis of three crises (Cyprus 2013, Venezuela 2016-17, COVID lockdown 2020) using BTC-native metrics (fee rates, fee-to-subsidy ratio, dormancy, activity)
- Findings: [TO BE COMPLETED AFTER ANALYSIS]
- Implications: Bitcoin's fee market creates counter-cyclical economic forces during crises without monetary expansion—critical because Bitcoin adoption threatens nations' ability to expand money supply

**Keywords:** Bitcoin, Keynesian economics, liquidity preference, proof-of-work, fee markets, economic crises, monetary policy

---

## 1. Introduction

### 1.1 The Keynesian Framework
- Keynes's theory of liquidity preference
- Money as the most liquid but unproductive asset
- Crisis response: Monetary expansion to prevent hoarding, stimulate demand
- Historical context: Gold standard → fiat → current monetary system

### 1.2 Bitcoin's Challenge to Monetary Orthodoxy
- Bitcoin as "hardest" money (fixed supply, predictable issuance)
- Adoption threatens governments' monetary expansion capabilities
- Key question: If monetary expansion becomes impossible, how can economies respond to crises?

### 1.3 The Productive Liquidity Paradox
- Bitcoin = most liquid (no capital controls, global, 24/7, permissionless)
- Bitcoin ≠ unproductive (PoW mining requires energy, creates infrastructure investment)
- Transaction fees → miner revenue → real-world productive investment
- Hypothesis: Crisis → increased on-chain activity → fee spike → increased miner revenue (counter-cyclical)

### 1.4 Research Contribution
- First empirical analysis of Bitcoin's base-layer behavior during major economic crises
- BTC-native methodology (no USD metrics)
- Event study framework with ±90-day windows
- Policy implications for post-fiat monetary systems

### 1.5 Paper Structure
[Brief roadmap of sections]

---

## 2. Literature Review

### 2.1 Keynesian Monetary Theory
- General Theory (1936) — liquidity preference, effective demand
- Money as store of value vs. medium of exchange tension
- Critiques and extensions (Post-Keynesian, New Keynesian)

### 2.2 Austrian Economics & Hard Money
- Mises, Hayek: Money as information system
- Critique of monetary expansion (malinvestment, business cycles)
- Bitcoin as digital gold standard?

### 2.3 Bitcoin Economics Literature
- Security budget debates (Carlsten et al. 2016, Budish 2022)
- Fee market analysis (Rizun 2015, Kasahara & Kawahara 2019)
- Layer 2 adoption effects on base layer
- Ordinals/Inscriptions and non-monetary use (2023+)

### 2.4 Crisis Behavior & Capital Controls
- Cyprus 2013: Bank runs, capital controls, Bitcoin price surge
- Venezuela hyperinflation: LocalBitcoins volume, dollarization
- COVID-19 & inflation: Macro uncertainty, institutional adoption

### 2.5 Gaps in Existing Research
- No systematic event study of on-chain crisis behavior
- Lack of BTC-native analysis (most studies use USD/price)
- Missing: Connection between liquidity preference theory and Bitcoin's productive layer

---

## 3. Theoretical Framework

### 3.1 Keynesian Liquidity Preference Revisited
- Why people hold liquid assets in crises
- Trade-off: Liquidity vs. productivity
- Traditional model: Cash is barren, no yield

### 3.2 Bitcoin as a Monetary Technology
- Base layer properties: Settlement finality, censorship resistance
- Proof-of-Work as productive mechanism
- Fee market as price discovery for urgency/liquidity

### 3.3 The Productive Liquid Asset Model
**Proposition 1:** Bitcoin is maximally liquid (no capital controls)  
**Proposition 2:** Bitcoin is productive (fees → mining → capital investment)  
**Proposition 3:** Crisis → liquidity preference → on-chain activity ↑ → fees ↑ → miner revenue ↑

### 3.4 Testable Predictions
1. **Fee urgency:** Median & p90 fee rates increase during crises
2. **Urgency spread:** p90 - p50 widens (users pay premium for speed)
3. **Miner revenue:** Fee-to-subsidy ratio increases (fees become larger share of block reward)
4. **Dormancy break:** Bitcoin Days Destroyed (BDD) spikes (HODLers move coins for liquidity)
5. **Activity surge:** Transactions/day increase (base-layer demand)

### 3.5 Alternative Hypotheses & Confounds
- Price effects (crisis → BTC price ↑ → fee USD value ↑, but we use BTC-native metrics)
- Inscriptions/Ordinals (non-monetary demand, primarily 2023+)
- Halving effects (subsidy reduction affects fee-to-subsidy mechanically)
- Lightning Network adoption (moves activity off-chain, reduces base-layer pressure)

---

## 4. Data & Methodology

### 4.1 Data Sources
- **Blockchain.com API:** Total fees/day, tx/day, blocks/day, BDD
- **Mempool.space:** Current mempool backlog (limited historical)
- **Bitcoin Core RPC:** Per-transaction fee rates (optional, if implemented)
- **Date range:** 2009–2024 (full Bitcoin history)

### 4.2 BTC-Native Metrics
**Why BTC-native?**
- Avoids USD volatility confounding results
- Measures on-chain behavior directly
- Tests Bitcoin's internal dynamics, not price speculation

**Metrics:**
1. **Median fee rate** (sat/vB): Baseline willingness to pay
2. **p90 fee rate** (sat/vB): High-priority transaction fees
3. **Urgency spread** (p90 - p50): Premium for fast confirmation
4. **Fees per block** (BTC): Direct miner revenue from fees
5. **Fee-to-subsidy ratio:** Fees / (fees + subsidy) — proportion of block reward from fees
6. **Bitcoin Days Destroyed (BDD):** Dormancy proxy (old coins moving)
7. **Transactions per day:** Base-layer usage intensity

### 4.3 Event Selection & Windows
**Selected Crises:**
1. **Cyprus Banking Crisis (March 2013)**
   - Anchor date: 2013-03-16 (bank run, capital controls imposed)
   - Window 1: ±90 days (Dec 16, 2012 – Jun 14, 2013)
   - Window 2: 180/45 days (Sep 18, 2012 – May 1, 2013)
   
2. **Venezuela Hyperinflation (2016-2017)**
   - Anchor date: 2016-11-13 (Hanke's daily-IMF methodology: first breach of 50%-per-month hyperinflation threshold)
   - Window 1: ±90 days (Aug 15, 2016 – Feb 10, 2017)
   - Window 2: 180/45 days (May 17, 2016 – Dec 28, 2016)
   
3. **COVID Lockdown (March 2020)**
   - Anchor date: 2020-03-19 (California stay-at-home order, US lockdown begins)
   - Window 1: ±90 days (Dec 20, 2019 – Jun 17, 2020)
   - Window 2: 180/45 days (Sep 21, 2019 – May 3, 2020)

**Window Rationale:**
- **90/90 days:** Standard event study window, captures immediate response + sustained effects
- **180/45 days:** Extended pre-crisis period establishes robust baseline "normalcy," shorter post-crisis period isolates immediate impact
- Dual approach provides comprehensive view: longer baseline vs. immediate response
- Avoids overlap with other major events (halvings, regulatory news)

### 4.4 Statistical Approach
- **Dual window analysis:** Results reported for both 90/90 and 180/45 day configurations
- **Descriptive statistics:** Mean, median, std dev for pre vs. crisis periods (both windows)
- **Percent change:** ((crisis_mean - pre_mean) / pre_mean) × 100
- **Rolling averages:** 30-day MA for smoothing
- **Visualization:** Time series with shaded event windows (both configurations)

**Limitations (acknowledged upfront):**
- **Descriptive, not causal:** We observe correlations, not mechanisms
- **Small sample:** Only 3 events (more research needed)
- **Confounds:** Price, halvings, L2 adoption, inscriptions
- **Data gaps:** Historical mempool data scarce (use indirect proxies)

---

## 5. Results

### 5.1 Cyprus Crisis (2013)
**Context:** Bank runs, capital controls, Bitcoin price surge from $40 to $260

**Findings (90/90 day window):** [TO BE COMPLETED]
- Median fee rate: X% increase
- Urgency spread: Y% increase
- Fee-to-subsidy: Z percentage points increase
- BDD: Spike on [date], indicating dormancy break
- Tx/day: Increased by W%

**Findings (180/45 day window):** [TO BE COMPLETED]
- Median fee rate: X% increase (immediate impact)
- Urgency spread: Y% increase (immediate impact)
- Fee-to-subsidy: Z percentage points increase (immediate impact)
- BDD: Spike on [date], indicating dormancy break
- Tx/day: Increased by W% (immediate impact)

**Interpretation:**
- Evidence of liquidity preference behavior (both windows)
- Fee market benefited from crisis demand
- Miner revenue from fees increased
- 180/45 window shows stronger immediate impact vs. 90/90 sustained effects

### 5.2 Venezuela Crisis (2016-2017)
**Context:** Hyperinflation, currency collapse, LocalBitcoins volume surge

**Findings (90/90 day window):** [TO BE COMPLETED]
- [Similar structure to 5.1]

**Findings (180/45 day window):** [TO BE COMPLETED]
- [Similar structure to 5.1 with immediate impact focus]

**Interpretation:**
- Different from Cyprus: Prolonged crisis, peer-to-peer focus
- [Analysis of unique patterns]
- Comparison of immediate vs. sustained effects across window configurations

### 5.3 COVID Lockdown (2020)
**Context:** Economic shutdown, market panic, lockdown uncertainty

**Findings (90/90 day window):** [TO BE COMPLETED]
- [Similar structure to 5.1]

**Findings (180/45 day window):** [TO BE COMPLETED]
- [Similar structure to 5.1 with immediate impact focus]

**Interpretation:**
- Post-halving context (subsidy = 6.25 BTC)
- Fee-to-subsidy ratio more sensitive
- [Analysis]
- Comparison of immediate vs. sustained effects across window configurations

### 5.4 Cross-Event Comparison
**Table 1: 90/90 day window results**

| Metric | Cyprus Δ% | Venezuela Δ% | COVID Δ% | Average |
|--------|-----------|--------------|----------|---------|
| Median sat/vB | ... | ... | ... | ... |
| Urgency spread | ... | ... | ... | ... |
| Fee-to-subsidy | ... | ... | ... | ... |
| BDD | ... | ... | ... | ... |
| Tx/day | ... | ... | ... | ... |

**Table 2: 180/45 day window results (immediate impact)**

| Metric | Cyprus Δ% | Venezuela Δ% | COVID Δ% | Average |
|--------|-----------|--------------|----------|---------|
| Median sat/vB | ... | ... | ... | ... |
| Urgency spread | ... | ... | ... | ... |
| Fee-to-subsidy | ... | ... | ... | ... |
| BDD | ... | ... | ... | ... |
| Tx/day | ... | ... | ... | ... |

**Patterns:**
- Consistent increases across events? (both windows)
- Which metrics are most sensitive? (immediate vs. sustained)
- Event-specific variations (e.g., Venezuela as extended crisis)
- Window sensitivity: Do 180/45 results show stronger immediate effects?

### 5.5 Figures

**Individual Crisis Analysis (6 figures):**
- **Figure 1:** Cyprus 90/90 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)
- **Figure 2:** Cyprus 180/45 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)
- **Figure 3:** Venezuela 90/90 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)
- **Figure 4:** Venezuela 180/45 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)
- **Figure 5:** COVID 90/90 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)
- **Figure 6:** COVID 180/45 day window (4 panels: fees BTC, transactions, fee-to-subsidy, BDD)

**Cross-Crisis Comparison (2 figures):**
- **Figure 7:** 90/90 window cross-crisis overlay (4 panels: all 3 crises overlaid)
- **Figure 8:** 180/45 window cross-crisis overlay (4 panels: all 3 crises overlaid)

**Summary Analysis (2 figures):**
- **Figure 9:** Pre vs. crisis bar charts (6 metrics × 3 crises × 2 windows = 36 bars)
- **Figure 10:** Fee-to-subsidy ratio over full Bitcoin history (2009-2024) with halving markers

**Visual Design:**
- Dual shaded regions: Light blue (90/90), light red (180/45)
- Vertical line: Crisis anchor date
- 30-day rolling average for smoothing
- Color scheme: Cyprus (blue), Venezuela (red), COVID (green)
- BTC-native units throughout

---

## 6. Discussion

### 6.1 Interpretation of Findings
- Do results support the productive liquid asset thesis?
- Magnitude of effects: Economically significant?
- Consistency across events

### 6.2 Theoretical Implications
**For Keynesian Economics:**
- Liquidity preference theory still holds (people seek liquidity in crises)
- BUT: Bitcoin's productive layer changes the policy prescription
- No need for monetary expansion if fee market creates counter-cyclical force

**For Bitcoin Economics:**
- Fee market as security mechanism (not just post-subsidy concern)
- Crisis behavior may accelerate fee-dependency transition
- Base layer remains relevant despite L2 adoption

### 6.3 Policy Implications
**For Governments:**
- Bitcoin adoption limits monetary expansion tools
- Need alternative crisis-response mechanisms (fiscal policy?)
- Capital controls become ineffective (cypherpunk resilience)

**For Bitcoin Protocol:**
- Fee market health is critical for long-term security
- Trade-offs: Base-layer capacity vs. fee urgency
- Lightning Network's role: Reduce everyday use, preserve base layer for high-value settlement

### 6.4 Limitations & Confounds
**Acknowledged weaknesses:**
1. **Descriptive analysis:** Cannot prove causation
2. **Price confounding:** BTC price volatility correlated with crises (but we use BTC-native units)
3. **Inscriptions:** 2023+ non-monetary demand inflates metrics (not present in 2013/2017 events)
4. **Halving effects:** Mechanical reduction in subsidy increases fee-to-subsidy ratio
5. **Lightning adoption:** Unclear how much activity shifted off-chain
6. **Sample size:** Only 3 events — need more crises (unfortunately)

**Robustness checks (future work):**
- Segment fee activity: Monetary vs. non-monetary (inscriptions)
- Placebo tests: Non-crisis periods with similar volatility
- Difference-in-differences: Bitcoin vs. altcoins during same crises

### 6.5 Alternative Explanations
- **Speculation hypothesis:** Users moving BTC for trading, not liquidity
  - Counter: BDD spike suggests HODLers, not traders
- **Exchange flows:** Not liquidity preference, just technical repositioning
  - Counter: Tx/day increase suggests broad activity, not just whale movements
- **Media attention:** Crisis → news → more users
  - Counter: Possible, but doesn't negate liquidity preference behavior

---

## 7. Future Research

### 7.1 Expand Event Catalog
- Greek crisis (2015)
- Brexit (2016)
- SVB collapse (2023)
- Longer time series → panel data analysis

### 7.2 Causal Inference Methods
- Synthetic controls (compare Bitcoin to altcoins)
- Difference-in-differences (crisis vs. non-crisis countries)
- Natural experiments (e.g., country-specific capital controls)

### 7.3 Mechanism Studies
- How do fees flow to energy/infrastructure?
- Geographic analysis: Which countries show strongest crisis response?
- Individual wallet analysis: HODLer vs. trader behavior (privacy-preserving)

### 7.4 Layer 2 Integration
- How does Lightning adoption affect base-layer crisis response?
- Will fee market remain robust if most activity moves off-chain?
- Interplay between L1 security and L2 usability

### 7.5 Inscriptions & Non-Monetary Use
- Segment fee activity by transaction type
- How do inscriptions affect fee market dynamics?
- Policy question: Should protocol limit non-monetary use?

---

## 8. Conclusion

### 8.1 Summary of Findings
- [Recap key results]
- Bitcoin exhibits liquidity preference behavior during crises
- Fee market benefits from crisis-driven demand
- Evidence for productive liquid asset thesis

### 8.2 Contribution to Literature
- First systematic BTC-native event study of crisis behavior
- Bridges Keynesian monetary theory and Bitcoin economics
- Policy-relevant for post-fiat monetary systems

### 8.3 Implications for Monetary Theory
- Keynes was right about liquidity preference...
- ...but wrong about money being unproductive
- Bitcoin suggests alternative to monetary expansion: Productive asset with counter-cyclical fee market

### 8.4 The Path Forward
- Bitcoin's threat to monetary expansion is real
- But Bitcoin's fee market may provide alternative stabilization mechanism
- More research needed on long-term dynamics (post-subsidy era)

### 8.5 Final Thought
*"In a world where Bitcoin is widely adopted, economic crises do not require monetary expansion. Instead, they organically increase miner revenue through the fee market, channeling resources to the productive layer (energy, infrastructure) precisely when the economy needs capital investment. Keynes's liquidity preference theory remains valid, but the policy prescription changes fundamentally."*

---

## 9. References

### Primary Sources
- Keynes, J.M. (1936). *The General Theory of Employment, Interest and Money.*
- Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System.*

### Bitcoin Economics
- Carlsten et al. (2016). On the Instability of Bitcoin Without the Block Reward
- Budish, E. (2022). The Economic Limits of Bitcoin and Anonymous, Decentralized Trust
- Rizun, P. (2015). A Transaction Fee Market Exists Without a Block Size Limit

### Monetary Theory
- [Austrian economics references]
- [Post-Keynesian references]
- [Central banking literature]

### Crisis & Capital Controls
- [Cyprus crisis papers]
- [Venezuela hyperinflation studies]
- [COVID-19 economic impacts]

### Empirical Bitcoin Studies
- [Fee market studies]
- [Mining economics]
- [Layer 2 adoption]

---

## Appendices

### Appendix A: Data Sources & Availability
- Blockchain.com API documentation
- Mempool.space limitations
- Code repository: [GitHub link]
- Replication package: [Data & scripts]

### Appendix B: Event Window Robustness
- Sensitivity analysis: ±60 days, ±120 days
- Results stable across window sizes?

### Appendix C: Additional Figures
- Full time series (2009–2024) for all metrics
- Halving events overlaid
- Mempool pressure proxy (if used)

### Appendix D: Technical Details
- Block subsidy calculation formula
- Bitcoin Days Destroyed computation
- Fee rate aggregation methods

### Appendix E: Code Snippets
- Key functions (date windowing, metric computation)
- Reproducibility instructions

---

## Notes for Writing

### Tone & Style
- **Academic but accessible:** Ledger has technical and non-technical readers
- **BTC-native perspective:** Avoid USD-centrism where possible
- **Balanced:** Acknowledge limitations honestly
- **Policy-relevant:** Connect to real-world implications

### Target Audience
- Bitcoin researchers & developers
- Monetary economists
- Policymakers interested in crypto
- Hardcore Bitcoiners (avoid appearing anti-Bitcoin)

### Key Strengths to Emphasize
- First BTC-native crisis study
- Theoretical contribution (productive liquidity)
- Policy relevance (post-fiat scenarios)
- Reproducible (open-source code/data)

### Potential Reviewer Concerns
1. **Sample size:** Only 3 events
   - Response: Exploratory study, more research needed, consistent patterns
2. **Causation:** Descriptive only
   - Response: Acknowledged upfront, suggest future causal methods
3. **USD price confound:** BTC price surges during crises
   - Response: BTC-native metrics isolate on-chain behavior
4. **Inscriptions:** Inflate 2023+ metrics
   - Response: Our events (2013, 2017, 2022) predate major inscription activity

### Writing Timeline
1. **Intro & Lit Review:** Draft from existing knowledge
2. **Methods:** Complete once data pipeline is finalized
3. **Results:** After running full analysis (scripts 01-03)
4. **Discussion:** Interpret findings
5. **Conclusion:** Synthesize contributions
6. **Abstract:** Write last (distill entire paper)

---

## Word Count Targets

| Section | Target Words | Notes |
|---------|--------------|-------|
| Abstract | 250 | Concise summary |
| Introduction | 1,500 | Set up problem & contribution |
| Literature Review | 2,000 | Comprehensive but focused |
| Theoretical Framework | 1,500 | Clear propositions & testable predictions |
| Data & Methodology | 1,500 | Reproducibility priority |
| Results | 2,000 | Heavy on figures & tables |
| Discussion | 2,500 | Interpret, connect theory, policy |
| Conclusion | 500 | Concise, impactful |
| References | N/A | 40–60 citations |
| **Total** | **~11,750** | Within Ledger range |

---

**END OF OUTLINE**

**Next Steps:**
1. Complete data collection (scripts/01_fetch_data.py)
2. Compute metrics (scripts/02_compute_metrics.py)
3. Generate figures (scripts/03_make_figures.py)
4. Run statistical analysis
5. Fill in Results section (Section 5)
6. Write Discussion & Conclusion
7. Revise for Ledger submission guidelines
8. Peer review (informal) before submission

