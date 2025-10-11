# Contributing to Productive Liquidity Thesis Research

Thank you for your interest in this research! This is an academic project preparing for publication in Ledger journal.

## How You Can Contribute

### 1. **Report Issues or Suggest Improvements**
- Found a bug? [Open an issue](https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin/issues)
- Have suggestions for additional metrics? Open an issue with the `enhancement` label
- Spotted errors in calculations? Please report them!

### 2. **Data Contributions**
If you have access to relevant data sources:
- Historical mempool snapshots
- Alternative Bitcoin APIs with better historical coverage
- Additional crisis events to analyze (SVB 2023, Greek crisis 2015, etc.)
- Pre-computed datasets from community archives

Share via issues or pull requests with clear documentation.

### 3. **Code Improvements**
We welcome contributions that improve code quality and functionality:

**Bug fixes:**
- API endpoint issues (e.g., Blockchain.com endpoint changes)
- Data parsing errors
- Calculation bugs

**Enhancements:**
- Performance optimizations
- Better documentation/comments
- Additional data source adapters
- Testing and validation
- Improved visualizations

**Important:** Major changes to analysis methodology require discussion first (academic integrity).

### 4. **Academic Collaboration**
Interested in collaborating on this research or extending the framework?

- **Email:** peytonallworth0001@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/peytonallworth/

Potential collaboration areas:
- Additional crisis event analysis
- Causal inference methods (synthetic controls, DiD)
- Layer 2 effects on base-layer behavior
- Geographic/regional analysis
- Extended time series (more years of data)

---

## What NOT to Contribute

### Please Avoid:

**Don't alter core thesis/conclusions** — The "productive liquid asset" framework is original research by Peyton Allworth

**Don't plagiarize the ideas** — If you use the theoretical framework elsewhere, cite the paper

**Don't submit PRs that change research methodology** without prior discussion — Methodology changes affect paper validity

**Don't copy paper content** — The `paper/` directory is copyrighted (see License section)

---

## Citation Requirements

If you extend this work, build upon the framework, or use significant portions of the code:

### For Academic Papers:
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

### For Code Attribution:
```python
# Based on Bitcoin Liquidity Crisis Research by Peyton Allworth
# https://github.com/PeytonAllworth/productive-liquidity-thesis-bitcoin
# Licensed under MIT License
```

---

## License

This project has **two separate licenses**:

### Code & Software → MIT License
The code, scripts, and software are **open source** under the MIT License.
- Free to use, modify, distribute
- No permission needed
- Must include copyright notice

### Research Paper & Ideas → Copyright
The research paper, theoretical contributions, and written content in `paper/` are **© 2025 Peyton Allworth. All Rights Reserved.**
- Cannot copy without permission
- Must cite if using the framework
- Protected intellectual property

See [README.md](README.md) for full details.

---

## Pull Request Process

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/productive-liquidity-thesis-bitcoin.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b fix/api-endpoint
   # or
   git checkout -b feature/new-data-source
   ```

3. **Make your changes**
   - Write clean, commented code
   - Follow existing code style (PEP 8 for Python)
   - Test thoroughly

4. **Test your changes**
   ```bash
   # Ensure existing functionality still works
   python scripts/01_fetch_data.py --sources blockchain_com --timespan 30days
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Fix: Update Blockchain.com API endpoint for blocks/day"
   ```

6. **Submit pull request**
   - Provide clear description of changes
   - Explain why the change is needed
   - Reference any related issues

7. **Wait for review**
   - PRs will be reviewed within a few days
   - May request changes or clarifications
   - Be patient and respectful

---

## Types of PRs Most Likely to Be Accepted

**Bug fixes** — Fixes to broken functionality

**Documentation** — Better explanations, examples, comments

**Data sources** — New API adapters (following existing patterns)

**Performance** — Optimizations that don't change results

**Testing** — Unit tests, validation scripts

**Methodology changes** — Need discussion first (may affect paper)

**Research conclusions** — These are Peyton's original contribution

---

## Code Style Guidelines

- **Python:** Follow PEP 8
- **Docstrings:** Use Google/NumPy style
- **Comments:** Explain WHY, not just WHAT
- **BTC-native:** Prefer BTC/sats over USD when possible
- **Reproducibility:** Document data sources and assumptions

---

## Questions?

- **General questions:** Open a GitHub issue
- **Collaboration inquiries:** Email peytonallworth0001@gmail.com
- **Bug reports:** GitHub issues with `bug` label
- **Feature requests:** GitHub issues with `enhancement` label

---

## Thank You! 

Your contributions help make this research more robust and reproducible. By improving the code, you're contributing to better understanding of Bitcoin's role in economic crises.

**Academic credit will be acknowledged** for substantial contributions that improve the research methodology or data quality.

---

**Ledger Publication:** Once published in Ledger, this research will be timestamped on the Bitcoin blockchain, providing permanent proof of authorship and academic priority.

