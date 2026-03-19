# Security & Privacy — HaloFinance

## The Two-Repo Model

HaloFinance uses a **public/private split** to keep your financial data safe while sharing the tools with everyone:

| Repo | Visibility | Contains | Purpose |
|------|-----------|----------|---------|
| **thebardchat/HaloFinance** | Public | Knowledge files, blank templates, docs | The free tools — anyone can use |
| **YOUR_USERNAME/HaloFinance-private** | **PRIVATE** | Your real financial data | Your personal CFO — only you see this |

*Each user's private repo lives under their own GitHub account. The name `HaloFinance-private` is the recommended convention, but what matters is: it's a NEW repo, set to PRIVATE, completely disconnected from the public repo.*

---

## Setting Up Your Private Repo (DO NOT FORK)

**CRITICAL: Do NOT fork this repo for your personal data.** GitHub forks of public repos inherit the public visibility setting and remain linked to the original. Your financial data could become publicly visible.

Instead, **clone and create a new private repo:**

### Step 1: Clone the public repo
```bash
git clone https://github.com/thebardchat/HaloFinance.git HaloFinance-private
cd HaloFinance-private
```

### Step 2: Create a NEW private repo on GitHub
1. Go to [github.com/new](https://github.com/new)
2. Name it `HaloFinance-private` (or whatever you want)
3. **Set visibility to PRIVATE** — this is non-negotiable
4. Do NOT initialize with README (you already have files)
5. Click **Create repository**

### Step 3: Point your local clone to YOUR private repo
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/HaloFinance-private.git
git push -u origin main
```

### Step 4: Copy templates and fill in your data
```bash
cp -r templates/personal/ personal/
```
Now edit the files in `personal/` with your real numbers.

### Step 5: Verify your repo is private
1. Go to your repo on GitHub → **Settings** → **General**
2. Scroll to **Danger Zone**
3. Confirm it says **"Change repository visibility"** and the current setting is **Private**

---

## Private Repo Lockdown Rules

Once your private repo contains real financial data, follow these rules:

### Repository Settings (GitHub)
- [ ] **Visibility: PRIVATE** — verify in Settings → General → Danger Zone
- [ ] **No collaborators** — unless you trust them with your SSN, account numbers, and balances
- [ ] **No GitHub Pages** — this would make your data publicly accessible
- [ ] **No third-party app access** — review Settings → Integrations → GitHub Apps
- [ ] **Branch protection on main** — prevent accidental force pushes

### What NEVER Goes in a Public Repo
- Real names of family members
- Social Security Numbers (even partial)
- Account numbers (credit cards, bank accounts, loans)
- Real dollar amounts from your finances (income, debts, balances)
- Employer name and compensation details
- Tax return details (refund amounts, filing specifics)
- W-2 box values
- Home address or mortgage details

### What's Safe for Public
- Knowledge files (financial education — no personal data)
- Blank templates with `[PLACEHOLDER]` markers
- Documentation and setup guides
- The system prompt (prompts/system_instructions.md)
- .gitignore and project configuration

---

## Data Ownership Philosophy

**You own everything.** This is not negotiable.

- Your financial data lives in YOUR private repo on YOUR GitHub account
- No third-party service stores your data (unless you choose to integrate one)
- Claude reads your files in-session — conversations are not stored permanently
- If you self-host (future feature), data never leaves your hardware
- If you delete your repo, your data is gone — no backups on our end

### Future: Pulsar Sentinel (Coming Soon)

Pulsar Sentinel will provide automated security monitoring for your private repos:
- Alerts if repo visibility changes from private to public
- Scans for accidentally committed sensitive data (SSNs, account numbers)
- Verifies GitHub settings remain locked down
- Monitors for unauthorized collaborator additions
- Continuous compliance checking

*Pulsar Sentinel is part of the Angel Cloud ecosystem. A small subscription keeps the infrastructure running and the dream alive — financial freedom tools that outlast any one person.*

---

## If You Accidentally Expose Data

If you accidentally push personal data to a public repo:

1. **Immediately** make the repo private (Settings → Danger Zone → Change visibility)
2. **Remove the sensitive data** from the files
3. **Rewrite git history** to remove it from past commits:
   ```bash
   # Install git-filter-repo (better than filter-branch)
   pip install git-filter-repo

   # Remove a file from ALL history
   git filter-repo --invert-paths --path personal/financial_profile.md

   # Force push (this rewrites history)
   git push --force
   ```
4. **Rotate any exposed credentials** (change passwords, get new IP PINs, etc.)
5. **Monitor credit reports** if SSNs or account numbers were exposed
6. Consider [credit freezes](https://www.usa.gov/credit-freeze) at all three bureaus

**Prevention is 1000x easier than cleanup.** Follow the setup steps above and you'll never need this section.

---

## Security Checklist (Monthly)

Run this check on the 1st of each month alongside your financial review:

- [ ] Private repo is still set to Private (GitHub Settings → General)
- [ ] No unexpected collaborators (GitHub Settings → Collaborators)
- [ ] No GitHub Pages enabled (GitHub Settings → Pages)
- [ ] No third-party apps with repo access (GitHub Settings → Integrations)
- [ ] `.gitignore` still blocks `/personal/` in the public repo
- [ ] No sensitive files accidentally committed to public repo

---

*Your money. Your data. Your control. No exceptions.*
