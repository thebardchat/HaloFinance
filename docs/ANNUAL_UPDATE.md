# HaloFinance — Annual Update Checklist

## When: First Week of January (Every Year)

### Step 1: Update System Prompt Parameters

Edit `prompts/system_instructions.md` and update ALL dollar amounts:

- [ ] Federal tax brackets (MFJ and Single)
- [ ] Standard deduction amounts
- [ ] 401(k) contribution limits (under 50, catch-up, super catch-up)
- [ ] IRA contribution limits
- [ ] Child Tax Credit amount
- [ ] Other Dependent Credit amount
- [ ] FICA Social Security wage base
- [ ] Standard mileage rate

### Step 2: Update Knowledge Files

- [ ] `knowledge/tax_brackets_2025.md` → copy to new year, update brackets
- [ ] `knowledge/401k_basics.md` → update contribution limits
- [ ] `knowledge/overtime_tax_guide.md` → check if WFTCA extended/changed
- [ ] `knowledge/alabama_tax_guide.md` → check for state law changes (or your state's file)
- [ ] `knowledge/dependent_support_test.md` → update gross income threshold

### Step 3: Update Templates

- [ ] `templates/personal/tax_filing_tracker.md` → update year references
- [ ] `templates/personal/401k_status.md` → update limit references

### Step 4: Test

- [ ] Deploy updated files to a test Claude Project
- [ ] Ask: "What are the 2026 tax brackets for married filing jointly?"
- [ ] Ask: "What's the 401(k) contribution limit this year?"
- [ ] Ask: "If I make $85K, what's my effective tax rate?"
- [ ] Verify all numbers match IRS publications

### Step 5: Commit and Push

```bash
git checkout -b tax/YYYY-update
git add .
git commit -m "halofinance(tax): update parameters for YYYY tax year"
git push -u origin tax/YYYY-update
# Create PR, merge to main after verification
```

---

## Where to Find Updated Numbers

| Parameter | Source | When Published |
|-----------|--------|---------------|
| Tax brackets | IRS Revenue Procedure | October/November |
| Standard deduction | IRS Revenue Procedure | October/November |
| 401(k)/IRA limits | IRS Notice | November |
| Mileage rates | IRS Notice | December |
| FICA wage base | SSA Announcement | October |
| Child Tax Credit | Legislative (changes by law) | Varies |

### Official URLs
| Source | URL |
|--------|-----|
| IRS Newsroom | irs.gov/newsroom |
| IRS Retirement Plans | irs.gov/retirement-plans |
| IRS Mileage Rates | irs.gov/tax-professionals/standard-mileage-rates |
| SSA COLA | ssa.gov/oact/cola |

---

## What Doesn't Change Annually
- Decision framework (easier, faster, biggest return)
- Debt payoff strategies (avalanche, snowball, hybrid)
- FIRE math (expenses x 25)
- Template structures
- Setup instructions

---

*Set a calendar reminder for January 2 to run this checklist.*
