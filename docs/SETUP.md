# HaloFinance — Setup Guide

## How to Deploy HaloFinance as a Claude Project

### What You Need
- A [Claude](https://claude.ai) account (Pro, Team, or Enterprise — for the Projects feature)
- This repository cloned to your computer

### Step 1: Clone the Repo

```bash
git clone https://github.com/thebardchat/HaloFinance.git
cd HaloFinance
```

### Step 2: Fill In Your Personal Data

Copy the template files to a `personal/` directory (which is gitignored — your data stays local):

```bash
cp -r templates/personal/ personal/
```

Start with these three files (in order):
1. **`personal/financial_profile.md`** — Your identity, income, filing status, tax bracket
2. **`personal/monthly_expenses.md`** — Your household budget (fill in real numbers)
3. **`personal/debt_inventory.md`** — All debts with balances, APRs, and minimums

Then fill in the rest as needed:
- `personal/goals.md` — What you're working toward
- `personal/401k_status.md` — Your retirement account details
- `personal/w2_summary.md` — Your W-2 breakdown (when you have it)
- `personal/tax_filing_tracker.md` — Track your tax return progress
- And more — see `templates/personal/` for all available templates

### Step 3: Create a Claude Project

1. Go to [claude.ai](https://claude.ai) → **Projects** → **New Project**
2. Name it **HaloFinance** (or whatever you like)
3. Open `prompts/system_instructions.md` and **paste the entire contents** into the **Project Instructions** field
4. Upload all files from the `knowledge/` directory into **Project Knowledge**
5. Upload your filled-in `personal/` files into **Project Knowledge** as well

### Step 4: Start a Conversation

Ask any of these to test it:
- *"What's my financial freedom number?"*
- *"If I raise my 401k to $200/week, what's the real cost to my take-home?"*
- *"Walk me through my tax filing checklist"*
- *"Should I pay off my credit cards with avalanche or snowball?"*
- *"What's my debt-to-income ratio and is it healthy?"*

---

## Customization

### Change Your State's Tax Rules

HaloFinance ships with Alabama tax rules by default. To use your state:

1. Delete or rename `knowledge/alabama_tax_guide.md`
2. Create `knowledge/[your_state]_tax_guide.md` following the template in `CLAUDE.md` → "Adding a New State"
3. Re-upload to your Claude Project

**No-income-tax states:** TX, FL, NV, WA, WY, SD, AK, NH (interest/dividends only), TN (no earned income tax). If you're in one of these, just note "State income tax: 0%" in your financial profile.

### Update Tax Year Parameters

Each January, update `prompts/system_instructions.md` with new:
- Federal tax brackets
- Standard deduction amounts
- 401(k) and IRA limits
- FICA wage base
- Mileage rates

See `docs/ANNUAL_UPDATE.md` for the full checklist.

---

## Alternative: Using Without Claude Projects

If you don't have Claude Pro/Team, you can still use HaloFinance:

1. Open any Claude conversation
2. Paste the system instructions at the start of your conversation
3. Paste relevant knowledge files as context
4. Paste your personal data as needed

It works the same way — Claude Projects just makes it persistent across conversations.

---

## Security Notes

- Your `personal/` directory is gitignored — it will NOT be pushed to GitHub
- Never commit files with real financial data to a public repo
- Your data stays on your machine and in your Claude Project
- Claude does not retain conversation data between sessions (unless using Projects)

---

*Questions? Open an issue at github.com/thebardchat/HaloFinance/issues*
