# Contributing to HaloFinance

## Welcome

HaloFinance is open source because financial literacy shouldn't be paywalled. Contributions are welcome — especially in these areas:

### High-Impact Contributions

1. **New state tax files** — Help us cover all 50 states
2. **Knowledge file improvements** — Better explanations, updated numbers, new topics
3. **Template improvements** — Better structure, clearer placeholders
4. **Bug fixes** — Tax math errors are critical bugs

---

## Adding a New State Tax File

Create `knowledge/[state]_tax_guide.md` following this template:

```markdown
# [State] Tax Guide — Tax Year [YYYY]

## Income Tax
- Filing statuses recognized
- Tax brackets (table format)
- Standard deduction amounts
- Notable exemptions

## What [State] Taxes
- W-2 wages: Yes/No
- Self-employment: Yes/No
- Investment income: Yes/No
- Retirement distributions: Yes/No

## What [State] Doesn't Tax
- List exemptions (e.g., Social Security, military pay, overtime)

## State-Specific Deductions
- List unique deductions

## Key Differences from Federal
- What catches people off guard

## Resources
- State revenue department URL
- Forms URL
- Contact information

---
⚠️ This is informational guidance. Verify with your state's
Department of Revenue and a licensed tax professional.
```

### Source Requirements
- Cite the state's Department of Revenue as primary source
- Include the tax year prominently
- Note any sunset provisions (rules that expire)

---

## Adding a Knowledge File

1. Write in **plain English** — target a high school reading level
2. **No jargon without explanation** — define terms in context
3. **Show the math** — worked examples with real (but generic) numbers
4. **Bust myths** — call out common misconceptions explicitly
5. **Make it actionable** — end with clear steps the reader can take
6. **No personal data** — use generic examples only
7. **Tables over paragraphs** — easier to scan
8. **State the year** — tax rules change; note when the info applies
9. **Flag CPA items** — if something needs professional review, say so
10. **Keep under 500 lines** — split into multiple files if larger

---

## Improving Templates

Templates live in `templates/personal/`. When improving them:
- Use `[PLACEHOLDER]` format: `$[AMOUNT]`, `[YOUR NAME]`, `[DATE]`, `[X]%`
- Include brief instructions/comments explaining what to put in each field
- Preserve the structure (tables, sections) that Claude expects
- Test by filling in sample data and asking Claude questions about it

---

## Commit Message Format

```
halofinance(module): description

Examples:
halofinance(tax): add Florida state tax guide
halofinance(knowledge): update 401k contribution limits for 2026
halofinance(template): improve debt inventory with student loan section
halofinance(docs): update setup guide for new project structure
halofinance(fix): correct FICA rate in system instructions
```

---

## Pull Request Process

1. Fork the repo
2. Create a branch (`tax/florida-guide`, `knowledge/hsa-guide`, etc.)
3. Make your changes
4. Verify accuracy against official sources
5. Submit a PR with:
   - What you changed
   - Source citations
   - Tax year the info applies to

---

## Knowledge Files Still Needed

- [ ] HSA (Health Savings Account) guide
- [ ] Roth IRA vs Traditional IRA guide
- [ ] Emergency fund sizing guide
- [ ] Credit score basics and repair guide
- [ ] Insurance basics (life, disability, umbrella)
- [ ] Home buying / mortgage guide
- [ ] Self-employment tax guide (Schedule C, SE tax, quarterly estimates)
- [ ] Estate planning basics (wills, beneficiaries, POA)
- [ ] College savings (529 plans)
- [ ] FIRE (Financial Independence, Retire Early) guide
- [ ] Social Security optimization guide
- [ ] VA benefits guide for veterans and dependents
- [ ] Side hustle / gig economy tax guide
- [ ] State tax guides for all 50 states

---

## Code of Conduct

- Be helpful, be honest, be kind
- Financial mistakes cost real families real money — accuracy matters
- When in doubt, flag for CPA review rather than guessing
- Credit your sources

---

*Built with faith, for family. Thank you for contributing.*
