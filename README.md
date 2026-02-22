# Gen Z vs Millennials — Investment Analysis 📊

Generational investing behavior analysis using **real data** from three primary sources. No estimates, no fabricated numbers.

## 🔴 Live Dashboard
👉 **[Open Interactive Dashboard](https://siddhanzade1.github.io/Genz-VS-Millenials-investment-analysis/genz_vs_millennials_dashboard.html)**

## 📁 Data Sources
| Source | Year | Sample |
|--------|------|--------|
| FINRA Foundation & CFA Institute | 2023 | n=2,872 |
| Charles Schwab Modern Wealth Survey Wave 2 | 2025 | n=2,400 |
| Motley Fool Generational Investing Trends Survey | July 2025 | n=2,000 |

## 📂 Files
| File | Description |
|------|-------------|
| `genz_vs_millennials_dashboard.html` | ✅ Interactive HTML dashboard — open in any browser |
| `genz_vs_millennials_dashboard.py` | 🐍 Python source — run to regenerate the PNG dashboard |
| `genz_vs_millennials_dashboard.png` | 🖼️ Full dashboard image (4400×5600px) |
| `GenZ_vs_Millennials_MultiSource_Report.docx` | 📄 Full Word report with all charts |
| `build_full.py` | ⚙️ Script that generates all charts + Word report |
| `source_Schwab_Modern_Wealth_2025.pdf` | 📊 Schwab 2025 data extract |
| `source_FINRA_2025_Investor_Report.pdf` | 📊 FINRA 2025 data extract |
| `c1_ownership_finra.png` … `c9_dividends_motley.png` | 📈 Individual chart exports |

## 🔑 Key Findings
- Crypto ownership is nearly identical: **Gen Z 55%** vs **Millennials 57%** *(FINRA 2023)*
- But Gen Z started with crypto as first investment far more: **44% vs 35%**
- Gen Z trades daily or weekly at **50%** vs Millennials **43%** *(Motley Fool 2025)*
- **64% of Gen Z** view dividends as a "side hustle" — highest of any generation
- Gen Z started investing at avg age **19** vs **25** for Millennials *(Schwab 2025)*

## 🚀 How to Run the Python Dashboard
```bash
pip install matplotlib numpy python-docx reportlab
python3 genz_vs_millennials_dashboard.py
```
