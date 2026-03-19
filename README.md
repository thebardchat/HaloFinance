# 💫 HaloFinance

**AI-powered Financial Consultant for Working Families**
*Part of the [Angel Cloud](https://github.com/thebardchat) Ecosystem*

[![Constitution](https://img.shields.io/badge/governed%20by-ShaneTheBrain%20Constitution-blue)](https://github.com/thebardchat/constitution)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)
[![Built With](https://img.shields.io/badge/built%20with-Claude%20by%20Anthropic-orange)](https://claude.ai)

---

## What Is HaloFinance?

HaloFinance is a comprehensive financial guidance system that runs as a [Claude Project](https://claude.ai). It acts as your personal CFO — covering everything from tax season to retirement planning to financial independence — powered by structured knowledge files and a carefully crafted system prompt.

**It is not an app.** It's a knowledge architecture that makes Claude behave like a senior financial consultant who knows your situation, your state's tax rules, your employer benefits, and your goals.

### Who It's For

- Working families who can't afford a $300/hr financial planner
- Anyone filing their own taxes who wants CPA-level guidance
- People trying to understand what their 401(k) actually does for them
- Families building toward financial freedom on a single income
- **The ~800 million users Big Tech forgot** (Pillar 6)

### What It Covers

| Module | What It Does |
|--------|-------------|
| **Tax Strategy** | Year-round tax optimization, filing prep, deduction identification, W-4 tuning |
| **Employer Benefits** | 401(k) contribution modeling, match maximization, insurance plan comparison |
| **Retirement Planning** | Compound growth projections, FIRE calculator, IRA strategy |
| **Budgeting** | Paycheck flow analysis, emergency fund sizing, expense tracking |
| **Debt Strategy** | Avalanche vs. snowball, refinancing analysis, payoff timelines |
| **Financial Freedom** | FIRE number, Coast FIRE milestones, net worth tracking |
| **Insurance & Risk** | Life insurance needs, disability gaps, coverage review |
| **Small Business** | Schedule C planning, entity selection, quarterly estimates |

---

## The Ecosystem

```
ShaneBrain (Pi 5 · local AI · private)
  └── Angel Cloud (VPS · public platform)
       ├── Pulsar AI (engine · enterprise)
       ├── HaloFinance (financial brain) ← you are here
       └── TheirNameBrain (legacy AI · generational)
            └── ~800M users losing Windows 10 support
```

This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).

---

## Quick Start

### 0. Read [SECURITY.md](SECURITY.md) First

**DO NOT fork this repo for personal data.** Forks stay public. Create a **new private repo** instead. Full instructions in [SECURITY.md](SECURITY.md).

### 1. Clone → Create Private Repo

```bash
# Clone into your own private folder
git clone https://github.com/thebardchat/HaloFinance.git HaloFinance-private
cd HaloFinance-private

# Create a NEW private repo on GitHub (github.com/new → PRIVATE)
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/HaloFinance-private.git
git push -u origin main

# Copy templates and fill in your data
cp -r templates/personal/ personal/
```

### 2. Deploy as Claude Project

1. Go to [claude.ai](https://claude.ai) → Projects → **New Project**
2. Name it **HaloFinance**
3. Paste contents of `prompts/system_instructions.md` into **Project Instructions**
4. Upload all files from `knowledge/` into **Project Knowledge**
5. Start a conversation

### 3. Test It

Ask any of these:
- *"If I raise my 401k to $200/week, what's the real cost to my take-home?"*
- *"What's my financial freedom number?"*
- *"Walk me through my 2025 tax filing checklist"*
- *"Should I itemize or take the standard deduction?"*

See `docs/SETUP.md` for the full deployment guide.

---

## Repo Structure

```
HaloFinance/
├── CLAUDE.md                          # Claude Code operating manual
├── README.md                          # You are here
├── .gitignore
│
├── prompts/                           # The brain
│   ├── system_instructions.md         # ★ Main system prompt
│   └── persona_changelog.md           # Version history
│
├── knowledge/                         # The memory
│   ├── tax_2025/                      # Tax year 2025 docs (6 files)
│   ├── retirement/                    # 401(k), IRA, FIRE guides
│   ├── budgeting/                     # Cash flow templates
│   └── financial_freedom/             # FIRE roadmaps
│
├── calculators/                       # Interactive HTML tools
├── templates/                         # Reusable checklists
│
└── docs/                              # Meta-docs
    ├── SETUP.md                       # Deployment guide
    ├── ANNUAL_UPDATE.md               # January update checklist
    └── CONTRIBUTING.md                # How to add modules
```

---

## How It Works

HaloFinance isn't magic. It's **structured knowledge + a well-crafted prompt**.

**The system prompt** (`prompts/system_instructions.md`) tells Claude:
- What persona to adopt (Senior Financial Consultant)
- What modules are available (tax, retirement, budgeting, etc.)
- What calculation engines to use (take-home impact, compound growth, FIRE)
- What tax parameters are current (brackets, limits, rates)
- How to format responses (dollar amounts, action steps, trade-offs)
- What disclaimers to include (not a real CPA/CFP)

**The knowledge files** give Claude:
- State-specific tax rules (Alabama by default — swap for your state)
- Dependent qualification logic
- Medical expense tracking guides
- Charitable giving strategy
- CPA review flags for borderline situations

**The result:** Claude responds with the specificity and structure of a real financial professional — personalized to your exact situation.

---

## Forking for Your Situation

HaloFinance ships configured for an Alabama-based married couple filing jointly with dependents. **It's designed to be forked.**

### What to Change

1. **State tax rules** — Replace `knowledge/tax_2025/alabama_tax_specifics.md` with your state
2. **Household profile** — Update the filing status, dependents, and income sources in the system prompt
3. **Contribution amounts** — Change the 401(k)/IRA defaults to match your employer
4. **Slider defaults** — Update calculator starting values

### What Stays the Same

- Federal tax brackets (same nationwide)
- 401(k)/IRA contribution limits (same nationwide)
- FIRE math and compound growth formulas (universal)
- Response format and structure (works for everyone)
- CPA review flags (universal safety net)

See `CLAUDE.md` → "For Contributors" for the complete adaptation guide.

---

## Annual Maintenance

Every January, update the tax parameters for the new year. HaloFinance includes a complete checklist:

```bash
# See the full checklist
cat docs/ANNUAL_UPDATE.md
```

**Key updates:**
- Federal tax brackets and standard deduction
- 401(k) and IRA contribution limits
- FICA wage base
- Mileage rates
- State-specific changes

**Where to find the numbers:** IRS publishes new brackets in October/November, contribution limits in November, and mileage rates in December. See `docs/ANNUAL_UPDATE.md` for exact URLs.

---

## Tax Year Support

| Year | Status | Branch |
|------|--------|--------|
| 2025 | ✅ Active | `main` |
| 2026 | 📋 Planned | `tax/2026-update` |

---

## The Nine Pillars

HaloFinance follows the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md):

| # | Pillar | How It Applies |
|---|--------|---------------|
| 1 | Faith First | Honest guidance. No predatory strategies. Generosity built in. |
| 2 | Family Stability | Every recommendation weighs family impact. |
| 3 | Sobriety Integrity | Reduces financial anxiety through clarity. |
| 4 | Local-First AI | Knowledge lives in version control, not locked in a platform. |
| 5 | 80/20 Shipping | Working checklists over perfect apps. |
| 6 | Serve the Left-Behind | Financial planning for families, not hedge funds. |
| 7 | Open by Default | Fork it. Adapt it. Make it yours. |
| 8 | ADHD-Aware Design | Short blocks. Checkboxes. One next step. |
| 9 | Gratitude is Infrastructure | Credits IRS sources. Flags when you need a real CPA. |

---

## Built With

| Partner | Role |
|---------|------|
| [**Claude by Anthropic**](https://claude.ai) | Co-built the entire system — prompt engineering, knowledge architecture, calculations |
| **IRS Publications** | Tax law source of truth (Pub 501, Pub 970, Rev. Proc. 2024-40) |
| **Alabama Dept. of Revenue** | State-specific tax rules |

---

## Roadmap

### Active
- [x] Tax Strategy module (year-round)
- [x] Employer Benefit Optimization (401k modeling)
- [x] Retirement Planning (compound growth, FIRE)
- [x] System prompt v2.0 (full financial consultant)
- [x] Repo scaffolding and documentation

### In Progress
- [ ] Budget template (household cash flow)
- [ ] Debt payoff calculator
- [ ] FIRE roadmap knowledge file
- [ ] 401(k) optimization deep-dive guide

### Planned
- [ ] Insurance needs calculator
- [ ] Schedule C / self-employment module
- [ ] Estate planning basics
- [ ] Education funding (529) guide
- [ ] Real estate analysis module
- [ ] Multi-state tax support templates

---

## Contributing

HaloFinance is open source. Contributions welcome — especially:

- **New state tax files** — Help us cover all 50 states
- **Calculator improvements** — Better UX, mobile optimization
- **Module expansion** — Deep-dive guides for planned modules
- **Bug fixes** — Tax math errors are critical bugs

See `docs/CONTRIBUTING.md` for the full guide and `CLAUDE.md` for Claude Code conventions.

---

## License

MIT — Use it, fork it, adapt it, share it. Financial literacy shouldn't be paywalled.

---

## Links

| Resource | URL |
|----------|-----|
| **GitHub Profile** | https://github.com/thebardchat |
| **Constitution** | https://github.com/thebardchat/constitution |
| **HaloFinance** | https://github.com/thebardchat/HaloFinance |

---

## Philosophy

> *A working parent shouldn't need to pay $300/hour to understand their own money.*

HaloFinance exists because the tools Wall Street uses to optimize wealth should be accessible to the family trying to figure out if they can afford to put an extra $100 into their retirement this week.

This isn't about getting rich. It's about getting **free**.

Free from money anxiety. Free from tax-season panic. Free from wondering if you're doing it right. Free to focus on what actually matters.

---

*Built with faith, for family.*
*Hazel Green, Alabama · [@thebardchat](https://github.com/thebardchat)*
*Co-built with [Claude by Anthropic](https://claude.ai)*
