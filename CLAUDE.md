# CLAUDE.md — HaloFinance Operating Manual

> This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).
> Every decision, every line of code, every recommendation follows the Nine Pillars.

---

## Project Identity

**Name:** HaloFinance
**Type:** AI-powered Financial Consultant System (Claude Project + Knowledge Base)
**Owner:** [@thebardchat](https://github.com/thebardchat) — Shane, Hazel Green, Alabama
**Ecosystem Position:** ShaneBrain → Angel Cloud → **HaloFinance** (financial brain)
**Constitution:** https://github.com/thebardchat/constitution

HaloFinance is a comprehensive financial guidance system delivered through a Claude Project. It provides tax strategy, retirement planning, employer benefit optimization, budgeting, debt elimination, and financial freedom goal-setting — tailored for working families.

Born from a CPA tax assistant (TaxAid), expanded into a full-spectrum financial consultant (MoneyAid/HaloFinance) on 12/31/2025.

---

## The Nine Pillars — How They Apply Here

| # | Pillar | HaloFinance Application |
|---|--------|------------------------|
| 1 | **Faith First** | Financial advice respects Christian values. No gambling strategies, no predatory schemes, no prosperity-gospel nonsense. Honest math, honest guidance. Generosity and tithing are features, not afterthoughts. |
| 2 | **Family Stability** | Every recommendation considers the user's full household. No advice that trades family time for marginal financial gain. Financial freedom MEANS more time with family. |
| 3 | **Wellness Integrity** | Financial stress compounds existing life challenges. HaloFinance reduces money anxiety through clarity and actionable steps, never through avoidance or denial. |
| 4 | **Local-First AI** | Prompt files and knowledge docs live in version control, not locked in a SaaS platform. If Claude disappears tomorrow, the knowledge base still works as reference docs. |
| 5 | **80/20 Shipping** | A working financial checklist beats a perfect financial app that never ships. Start with markdown, graduate to calculators, then apps — only when needed. |
| 6 | **Serve the Left-Behind User** | Built for families living paycheck-to-paycheck who can't afford a $300/hr CFP. This system democratizes financial guidance. |
| 7 | **Open by Default** | Core knowledge and prompts are open source. Anyone can clone this and adapt it for their state, their family, their situation. |
| 8 | **ADHD-Aware Design** | Short blocks. Checkboxes. One next step. Dollar amounts, not paragraphs. Visual calculators over spreadsheets. |
| 9 | **Gratitude is Infrastructure** | Credit sources. Cite IRS publications. Acknowledge when advice needs a real CPA. Never pretend to be more than an informed assistant. |

---

## Repository Structure

```
HaloFinance/
├── CLAUDE.md                          # YOU ARE HERE — Claude Code operating manual
├── README.md                          # Public-facing repo documentation
├── .gitignore
│
├── prompts/
│   ├── system_instructions.md         # PRIMARY: Drop into Claude Project Instructions
│   └── persona_changelog.md           # Version history of prompt evolution
│
├── knowledge/                         # Upload these to Claude Project Knowledge
│   ├── tax_2025/                      # Tax year 2025 reference docs
│   │   ├── dependent_qualification_guide.md
│   │   ├── medical_mileage_tracker.md
│   │   ├── charitable_giving_strategy.md
│   │   ├── alabama_tax_specifics.md
│   │   ├── cpa_review_flags.md
│   │   └── dependents_standard_deduction_and_filing.pdf
│   ├── retirement/                    # 401(k), IRA, FIRE planning
│   │   └── (guides added as built)
│   ├── budgeting/                     # Cash flow, emergency fund
│   │   └── (templates added as built)
│   └── financial_freedom/             # FIRE roadmap, net worth milestones
│       └── (roadmaps added as built)
│
├── calculators/                       # Standalone HTML tools
│   └── (interactive calculators)
│
├── templates/                         # Reusable checklists and frameworks
│   ├── annual_tax_checklist.md
│   ├── monthly_financial_review.md
│   └── year_end_tax_moves.md
│
└── docs/                              # Meta-documentation
    ├── SETUP.md                       # How to deploy as Claude Project
    ├── ANNUAL_UPDATE.md               # January update checklist
    └── CONTRIBUTING.md                # How to add new modules
```

---

## For Claude Code — Rules of Engagement

### Identity
You are working inside HaloFinance, a financial guidance repo. You are NOT a licensed CPA, CFP, or registered investment advisor. You are an AI assistant that organizes financial knowledge, performs calculations, and helps users make informed decisions.

### Commit Message Format
```
halofinance(module): description

Examples:
halofinance(tax): add 2026 bracket updates
halofinance(retirement): create 401k optimization guide
halofinance(calc): build take-home impact calculator
halofinance(docs): update annual checklist for 2026
halofinance(prompt): expand small business module
halofinance(fix): correct FICA rate in system instructions
```

### Branch Strategy
```
main                    # Production — what's deployed in the Claude Project
├── tax/2026-update     # Annual tax parameter updates
├── module/retirement   # New module development
├── calc/debt-payoff    # New calculator
└── fix/bracket-typo    # Bug fixes
```

### File Conventions

**Knowledge files (.md):**
- Written in plain markdown — no HTML, no embedded scripts
- First line: `# Title` (H1)
- Include source citations (IRS Publication numbers, URLs)
- Dollar amounts always include the tax year: `$23,500 (2025 limit)`
- Use tables for comparisons, not paragraphs
- End each file with a "CPA Review Items" section for borderline cases
- Keep files under 500 lines — split into multiple files if larger

**Calculators (.html):**
- Single-file HTML (inline CSS + JS, no external dependencies except CDN)
- Mobile-responsive (min-width 320px)
- Use sliders for variable inputs with visible current value
- Always show: weekly, monthly, AND annual impact
- Include compound growth projections where applicable
- Add disclaimer footer on every calculator
- Use CSS variables for theming (light/dark mode ready)

**Templates (.md):**
- Checkbox format: `- [ ] Action item`
- Include date placeholders: `[DATE]`, `[YEAR]`
- Group by priority: Must Do → Should Do → Nice to Do
- Keep under 100 lines

**System prompt (system_instructions.md):**
- This is the CORE artifact — changes here affect every conversation
- Version number and date in the header
- Tax parameters in clearly labeled tables
- Modules numbered sequentially
- Response format examples included
- Disclaimers at the bottom
- **Test changes in a separate Claude Project before merging to main**

---

## Financial Domain Rules

### Accuracy Standards
- Tax brackets, limits, and rates MUST match current IRS publications
- State-specific rules must cite the state revenue department
- When in doubt, flag for CPA review — never guess on tax law
- Projections must state assumptions (return rate, inflation, time horizon)
- Never use the word "guarantee" with financial projections

### Calculation Requirements
- All tax calculations: show the math step-by-step
- Retirement projections: use 7% average return (historical S&P 500 inflation-adjusted)
- Conservative projections available at 5%
- Aggressive projections available at 10%
- ALWAYS account for Alabama's 0% W-2 wage tax
- FICA (7.65%) is NOT reduced by 401(k) contributions — never miscalculate this
- Pre-tax contribution "real cost" = contribution × (1 - marginal federal rate)

### Disclaimer Requirements
Every file that contains tax calculations MUST include:
```
⚠️ This is informational guidance based on current tax law and publicly
available financial knowledge. Verify all tax positions with a licensed
CPA or tax professional before filing.
```

Every file with investment projections MUST include:
```
⚠️ Projections assume historical average returns and are not guaranteed.
Past performance does not predict future results.
```

---

## For Contributors (Cloning This Repo)

### Welcome
HaloFinance is designed to be cloned and adapted. The system prompt and knowledge files are tailored for an Alabama-based family with specific circumstances, but the framework works for anyone.

**IMPORTANT: Do NOT fork this repo for personal data.** Forks of public repos stay public. See [SECURITY.md](SECURITY.md) for the safe setup.

### How to Adapt for Your Situation

**Step 1: Clone into a NEW private repo**
```bash
# Clone the public repo into a private folder
git clone https://github.com/thebardchat/HaloFinance.git HaloFinance-private
cd HaloFinance-private

# Create a NEW private repo on GitHub (github.com/new → set to PRIVATE)
# Your repo will be: github.com/YOUR_USERNAME/HaloFinance-private
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/HaloFinance-private.git
git push -u origin main
```

**Step 2: Update the system prompt**
Edit `prompts/system_instructions.md`:

1. **Change the tax parameters** for your state
   - Find your state's income tax rates and rules
   - Update the "Alabama Tax" section with your state's specifics
   - Note: Some states (TX, FL, NV, WA, WY, SD, AK, NH, TN) have no income tax

2. **Update the household profile**
   - Filing status (Single, MFJ, HoH, etc.)
   - Number/ages of dependents
   - Income sources
   - Retirement account types
   - Business structure (if applicable)

3. **Adjust the financial parameters**
   - Tax brackets are federal (same for everyone)
   - State brackets vary — research yours
   - Employer match amounts
   - Current contribution levels

**Step 3: Update knowledge files**
- Replace `knowledge/tax_YYYY/alabama_tax_specifics.md` with your state
- Adjust dependent qualification if your situation differs
- Keep the CPA review flags — they apply universally

**Step 4: Deploy**
Follow `docs/SETUP.md` to create your Claude Project.

### What to Keep vs. What to Change

| Keep As-Is | Customize |
|-----------|-----------|
| Federal tax brackets | State tax rules |
| 401(k)/IRA limits | Your contribution amounts |
| FIRE calculation formulas | Your expense numbers |
| CPA review flags | Your specific red flags |
| Response format structure | Your household profile |
| Disclaimer language | Your state's resources |
| Annual update checklist | Your state's update sources |
| Calculator HTML structure | Your default slider values |

### Adding a New State

Create `knowledge/tax_YYYY/[state]_tax_specifics.md` following this template:
```markdown
# [State] Tax Specifics for Tax Year [YYYY]

## Income Tax
- Filing statuses recognized
- Tax brackets
- Standard deduction amounts
- Notable exemptions

## What [State] Taxes
- W-2 wages: Yes/No
- Self-employment: Yes/No
- Investment income: Yes/No
- Retirement distributions: Yes/No

## What [State] Doesn't Tax
- List exemptions

## State-Specific Deductions
- List unique deductions

## Resources
- State revenue department URL
- Forms URL
- Contact information
```

---

## Annual Maintenance Workflow

### Every January (First Week)

```bash
git checkout -b tax/YYYY-update

# 1. Update system prompt parameters
# Edit prompts/system_instructions.md — all dollar amounts and limits

# 2. Copy tax knowledge for new year
cp -r knowledge/tax_OLDYEAR knowledge/tax_NEWYEAR
# Edit each file for updated amounts

# 3. Update changelog
# Edit prompts/persona_changelog.md

# 4. Test in Claude Project (separate test project)

# 5. Merge when verified
git add .
git commit -m "halofinance(tax): update parameters for YYYY tax year"
git checkout main
git merge tax/YYYY-update
git push
```

### What Changes Annually
- Federal tax brackets (inflation-adjusted every October)
- Standard deduction amounts
- 401(k) and IRA contribution limits (announced November)
- FICA Social Security wage base
- Mileage rates (announced December)
- Child Tax Credit amounts (if legislation changes)
- State-specific parameters

### Where to Find Updated Numbers
| Parameter | Source | URL |
|-----------|--------|-----|
| Tax brackets | IRS Revenue Procedure | irs.gov/newsroom |
| 401(k) limits | IRS Notice | irs.gov/retirement-plans |
| IRA limits | IRS Notice | irs.gov/retirement-plans |
| Mileage rates | IRS Notice | irs.gov/tax-professionals/standard-mileage-rates |
| FICA wage base | SSA Announcement | ssa.gov/oact/cola |
| Alabama updates | AL Dept of Revenue | revenue.alabama.gov |

---

## Module Development Guide

### Adding a New Module

1. **Define scope** in `prompts/system_instructions.md` under PRIMARY CAPABILITIES
2. **Create knowledge file(s)** in `knowledge/module_name/`
3. **Build calculator** (if math-heavy) in `calculators/`
4. **Create template** (if recurring workflow) in `templates/`
5. **Update persona changelog** in `prompts/persona_changelog.md`
6. **Test** in Claude Project with 3+ diverse prompts

### Module Quality Checklist
- [ ] Knowledge file has IRS/official source citations
- [ ] Dollar amounts include tax year
- [ ] Calculations show step-by-step math
- [ ] Alabama-specific notes included (or state-agnostic flag)
- [ ] CPA review triggers documented
- [ ] Disclaimer included
- [ ] Tested with edge cases (low income, high income, borderline)
- [ ] ADHD-friendly: short blocks, checkboxes, single next step

### Planned Modules (Roadmap)

| Priority | Module | Status | Description |
|----------|--------|--------|-------------|
| P0 | Tax Strategy | ✅ Complete | Year-round tax optimization |
| P0 | Employer Benefits | ✅ Complete | 401(k), insurance, W-4 |
| P0 | Retirement Planning | ✅ Complete | Compound growth, FIRE targets |
| P1 | Budgeting | 🔨 In Progress | Cash flow, emergency fund |
| P1 | Debt Strategy | 🔨 In Progress | Payoff calculators |
| P1 | Financial Freedom | 🔨 In Progress | FIRE roadmap |
| P2 | Insurance & Risk | 📋 Planned | Life, disability, umbrella |
| P2 | Small Business | 📋 Planned | Schedule C, entity selection |
| P3 | Estate Planning | 📋 Planned | Wills, trusts, beneficiaries |
| P3 | Education Funding | 📋 Planned | 529, Coverdell, scholarships |
| P3 | Real Estate | 📋 Planned | Mortgage analysis, rental ROI |

---

## Testing

### Before Merging Any Change

1. **Parameter accuracy** — Verify all dollar amounts against IRS/official sources
2. **Calculation correctness** — Run 3 scenarios through each calculator:
   - Low income scenario ($30K household)
   - Middle income scenario ($80-100K household)
   - High income scenario ($200K+ household)
3. **Prompt testing** — Ask the Claude Project:
   - A basic question the change affects
   - A "what if" comparison scenario
   - A cross-module question (e.g., "How does raising my 401k affect my tax refund?")
4. **Edge cases** — Test boundary conditions:
   - Bracket thresholds ($96,950 MFJ 12%→22% boundary)
   - Phase-out ranges (IRA deduction, Child Tax Credit)
   - Contribution limits ($23,500 401k max)
5. **State check** — Ensure Alabama-specific rules are correctly applied

### Test Prompts (Use These)
```
"If I raise my 401k contribution to $300/week, what happens to my take-home?"
"What's my financial freedom number?"
"Walk me through my 2025 tax filing checklist"
"Should I itemize or take the standard deduction?"
"How much should I have in my emergency fund?"
"What's the tax impact of starting side business revenue?"
"Compare contributing to Traditional vs Roth 401k for me"
```

---

## Dependencies

### Required for Claude Project Deployment
- Claude Pro/Team/Enterprise account (for Projects feature)
- Files from this repo uploaded to Project Knowledge

### Required for Calculator Development
- Modern browser (HTML/CSS/JS only — no build tools)
- Optional: Chart.js via CDN for data visualization

### No External Dependencies
- No npm packages
- No Python requirements
- No databases
- No APIs (beyond Claude's built-in capabilities)
- **Pillar 4: Local-first. The knowledge works offline as markdown files.**

---

## Security & Privacy

- **Never commit** real financial data (account numbers, SSNs, balances)
- **Never commit** real names of family members
- Knowledge files use generic examples, not real personal data
- Calculator defaults are illustrative, not based on actual accounts
- `.gitignore` excludes environment files and editor configs

---

## Philosophy

HaloFinance exists because a working parent shouldn't need to pay $300/hour to understand their own money. The tools Wall Street uses to optimize wealth should be accessible to the family trying to figure out if they can afford to put an extra $100/week into their 401(k).

This isn't about getting rich. It's about getting free.

Free from money anxiety. Free from tax-season panic. Free from wondering if you're doing it right. Free to focus on what matters — faith, family, and building something that outlasts you.

> *"Build for the ~800M Big Tech forgot."* — Pillar 6

---

## Links

- **GitHub:** https://github.com/thebardchat
- **Constitution:** https://github.com/thebardchat/constitution
- **HaloFinance:** https://github.com/thebardchat/HaloFinance

---

*Built with faith, for family. Hazel Green, Alabama.*
*Co-built with [Claude by Anthropic](https://claude.ai).*
