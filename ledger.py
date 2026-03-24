#!/usr/bin/env python3
"""
HaloFinance Ledger — Personal financial tracking dashboard
Self-hosted, SQLite-backed, runs on anything (Pi, laptop, VPS)

Usage:
  python3 ledger.py
  Open http://localhost:9998

Change AUTH_USER/AUTH_PASS below or set HALO_PASSWORD env var.
Edit seed_bills() with YOUR real bills, debts, and income.
"""

import os
import json
import re
import sqlite3
import base64
import hashlib
from datetime import datetime, date, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, parse_qs, urlparse

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "halofinance.db")
PORT = 9998
HOST = "0.0.0.0"

# Simple auth — change the password to something your family shares
AUTH_USER = os.environ.get("HALO_USER", "family")
AUTH_PASS = os.environ.get("HALO_PASSWORD", "changeme")

# Base path for links — empty for direct access, "/finance" for Tailscale Funnel
# Detected automatically from request
def get_base(path):
    return "/finance" if path.startswith("/finance") else ""


# ─── Database Setup ───────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'checking',
            institution TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            active INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL DEFAULT 'deposit',
            category TEXT DEFAULT 'general',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        );

        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            due_day INTEGER DEFAULT 1,
            frequency TEXT DEFAULT 'monthly',
            category TEXT DEFAULT 'general',
            total_owed REAL DEFAULT 0,
            interest_rate REAL DEFAULT 0,
            notes TEXT DEFAULT '',
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_txn_date ON transactions(date DESC);
        CREATE INDEX IF NOT EXISTS idx_txn_account ON transactions(account_id);
    """)
    conn.commit()

    # Seed bills if table is empty
    count = conn.execute("SELECT COUNT(*) FROM bills").fetchone()[0]
    if count == 0:
        seed_bills(conn)

    conn.close()


def seed_bills(conn):
    """Seed example bills so the dashboard isn't empty on first run.
    REPLACE THESE WITH YOUR REAL BILLS, DEBTS, AND INCOME.
    Delete halofinance.db to re-seed after editing, or use the + Add button in the UI."""
    known_bills = [
        # (name, monthly_amount, due_day, frequency, category, total_owed, interest_rate, notes)

        # ═══ INCOME — your take-home pay ═══
        ("Paycheck", 1000.00, 0, "weekly", "paycheck", 0, 0, "Your weekly take-home after deductions"),

        # ═══ HOUSING ═══
        ("Mortgage / Rent", 1500.00, 1, "monthly", "mortgage", 200000.00, 6.5, "Your monthly housing payment"),

        # ═══ AUTO ═══
        ("Car Payment", 400.00, 15, "monthly", "car-payment", 20000.00, 6.0, "Auto loan"),
        ("Car Insurance", 200.00, 8, "monthly", "insurance", 0, 0, ""),

        # ═══ UTILITIES ═══
        ("Internet", 80.00, 19, "monthly", "utilities", 0, 0, ""),
        ("Phone", 100.00, 14, "monthly", "utilities", 0, 0, ""),
        ("Electric", 250.00, 20, "monthly", "utilities", 0, 0, "Average"),
        ("Water", 50.00, 15, "monthly", "utilities", 0, 0, ""),

        # ═══ FOOD ═══
        ("Groceries", 600.00, 0, "monthly", "groceries", 0, 0, ""),

        # ═══ GAS ═══
        ("Gas / Fuel", 300.00, 0, "monthly", "gas", 0, 0, ""),

        # ═══ CREDIT CARDS — add yours here ═══
        ("Credit Card 1", 35.00, 17, "monthly", "credit-card", 500.00, 24.99, "Example — replace with your real card"),
        ("Credit Card 2", 50.00, 3, "monthly", "credit-card", 1200.00, 27.99, "Example — replace with your real card"),
        ("Credit Card 3", 75.00, 21, "monthly", "credit-card", 2000.00, 29.99, "Example — replace with your real card"),

        # ═══ BUY NOW PAY LATER (Affirm, Klarna, etc.) ═══
        ("BNPL Loan 1", 50.00, 5, "monthly", "debt-payment", 300.00, 30.00, "Example — replace with your real loan"),
        ("BNPL Loan 2", 35.00, 10, "monthly", "debt-payment", 200.00, 0.00, "Example — 0% promo"),

        # ═══ SUBSCRIPTIONS ═══
        ("Streaming / Subscriptions", 50.00, 1, "monthly", "subscriptions", 0, 0, "Netflix, Spotify, etc."),

        # ═══ PAYROLL DEDUCTIONS (auto-deducted from gross, not from take-home) ═══
        ("Health Insurance (payroll)", 400.00, 0, "payroll", "insurance", 0, 0, "Pre-tax payroll deduction"),
        ("401(k) (payroll)", 200.00, 0, "payroll", "401k", 0, 0, "Your retirement contribution"),
    ]

    conn.executemany("""
        INSERT INTO bills (name, amount, due_day, frequency, category, total_owed, interest_rate, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, known_bills)
    conn.commit()


# ─── Frequency → Monthly Conversion ────────────────────────────────

FREQ_TO_MONTHLY = {
    "weekly": 4.33,
    "biweekly": 2.167,
    "monthly": 1.0,
    "quarterly": 1/3,
    "annual": 1/12,
    "payroll": 1.0,  # already stored as monthly
}

def to_monthly(amount, frequency):
    """Convert any frequency amount to monthly equivalent."""
    return amount * FREQ_TO_MONTHLY.get(frequency, 1.0)


# ─── Pay Structure (from paycheck_calculator.md) ───────────────────

# YOUR hourly rate — change these to match your pay
CURRENT_RATE = 20.00  # Your current hourly rate
# If you're expecting a raise, set the new rate and date
RAISE_RATE = 22.00
RAISE_DATE = date(2026, 7, 1)  # When the raise kicks in

def get_hourly_rate(for_date=None):
    d = for_date or date.today()
    return RAISE_RATE if d >= RAISE_DATE else CURRENT_RATE

def calc_weekly_takehome(hours, rate=None):
    """Calculate weekly take-home for given hours at current rate.
    Based on paycheck_calculator.md deductions."""
    rate = rate or get_hourly_rate()
    reg_hrs = min(hours, 40)
    ot_hrs = max(0, hours - 40)
    ot_rate = rate * 1.5

    gross = (reg_hrs * rate) + (ot_hrs * ot_rate)
    # Deductions (from paycheck calculator)
    federal = max(0, (gross - 1100) * 0.018 + 5)  # approximate from table
    fica = gross * 0.0765
    four01k = 200.00  # $200/wk employee contribution
    insurance = 225.00  # health/dental/vision weekly

    takehome = gross - federal - fica - four01k - insurance
    return round(takehome, 2), round(gross, 2)

def hours_needed_for(weekly_target, rate=None):
    """How many hours/week needed to take home a target amount."""
    rate = rate or get_hourly_rate()
    # Binary search
    lo, hi = 0, 80
    for _ in range(50):
        mid = (lo + hi) / 2
        th, _ = calc_weekly_takehome(mid, rate)
        if th < weekly_target:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 1)


# ─── Data Helpers ──────────────────────────────────────────────────

def get_accounts(conn):
    return conn.execute(
        "SELECT * FROM accounts WHERE active=1 ORDER BY type, name"
    ).fetchall()


def get_account_balance(conn, account_id):
    row = conn.execute("""
        SELECT COALESCE(SUM(CASE WHEN type='deposit' THEN amount ELSE -amount END), 0) as balance
        FROM transactions WHERE account_id=?
    """, (account_id,)).fetchone()
    return row["balance"]


def get_all_balances(conn):
    accounts = get_accounts(conn)
    result = []
    for acct in accounts:
        bal = get_account_balance(conn, acct["id"])
        result.append({**dict(acct), "balance": bal})
    return result


def get_transactions(conn, account_id=None, days=30, limit=100):
    since = (date.today() - timedelta(days=days)).isoformat()
    if account_id:
        rows = conn.execute("""
            SELECT t.*, a.name as account_name FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE t.account_id=? AND t.date >= ?
            ORDER BY t.date DESC, t.id DESC LIMIT ?
        """, (account_id, since, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT t.*, a.name as account_name FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE t.date >= ?
            ORDER BY t.date DESC, t.id DESC LIMIT ?
        """, (since, limit)).fetchall()
    return [dict(r) for r in rows]


def get_daily_summary(conn, days=30):
    since = (date.today() - timedelta(days=days)).isoformat()
    rows = conn.execute("""
        SELECT date,
               SUM(CASE WHEN type='deposit' THEN amount ELSE 0 END) as total_in,
               SUM(CASE WHEN type='withdrawal' THEN amount ELSE 0 END) as total_out,
               COUNT(*) as txn_count
        FROM transactions
        WHERE date >= ?
        GROUP BY date ORDER BY date DESC
    """, (since,)).fetchall()
    return [dict(r) for r in rows]


def wednesday_before(due_date):
    """Get the Wednesday on or before a due date. If due date IS Wed, return it."""
    d = due_date
    # Walk backwards to find Wednesday (weekday 2)
    while d.weekday() != 2:  # 0=Mon, 2=Wed
        d -= timedelta(days=1)
    return d


def get_next_due(due_day, today=None):
    """Get next occurrence of a due day (1-28). Returns (due_date, pay_by_date)."""
    today = today or date.today()
    if due_day <= 0:
        return None, None
    # This month or next
    try:
        this_month = date(today.year, today.month, min(due_day, 28))
    except ValueError:
        this_month = date(today.year, today.month, 28)
    if this_month < today:
        # Next month
        if today.month == 12:
            next_due = date(today.year + 1, 1, min(due_day, 28))
        else:
            next_due = date(today.year, today.month + 1, min(due_day, 28))
    else:
        next_due = this_month
    pay_by = wednesday_before(next_due)
    return next_due, pay_by


def get_bills(conn, active_only=True):
    where = "WHERE active=1" if active_only else ""
    return conn.execute(f"SELECT * FROM bills {where} ORDER BY category, name").fetchall()


CATEGORIES = [
    "paycheck", "overtime", "bonus", "refund", "transfer-in",
    "mortgage", "rent", "utilities", "groceries", "gas", "insurance",
    "medical", "childcare", "dining", "subscriptions", "tithe",
    "father-support", "car-payment", "credit-card", "savings",
    "401k", "debt-payment", "misc-income", "misc-expense", "transfer-out",
    "general"
]

ACCOUNT_TYPES = ["checking", "savings", "credit-card", "401k", "cash", "other"]


# ─── HTML Templates ────────────────────────────────────────────────

def render_page(title, body_html, accounts=None, base=""):
    nav_links = """
    <a href="/">Home</a>
    <a href="/bills">Bills</a>
    <a href="/cards">Cards</a>
    <a href="/hours">Hours</a>
    <a href="/add-bill">+ Add</a>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — HaloFinance</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background:#111; color:#eee; }}
nav {{ display:flex; background:#1a1a1a; border-bottom:2px solid #d4a017; overflow-x:auto; }}
nav a {{ flex:1; text-align:center; padding:14px 8px; color:#999; text-decoration:none; font-size:0.85em; white-space:nowrap; }}
nav a:hover {{ color:#fff; background:#222; }}
.p {{ padding:16px; max-width:800px; margin:0 auto; }}

/* Big number cards */
.big {{ background:#1a1a1a; border-radius:12px; padding:20px; margin-bottom:12px; text-align:center; }}
.big .label {{ color:#999; font-size:0.8em; text-transform:uppercase; letter-spacing:1px; }}
.big .num {{ font-size:2.2em; font-weight:700; margin:4px 0; }}
.big .sub {{ color:#777; font-size:0.8em; }}
.green {{ color:#4ade80; }}
.red {{ color:#f87171; }}
.gold {{ color:#d4a017; }}
.blue {{ color:#60a5fa; }}

/* Two-column grid */
.g2 {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px; }}

/* Bill item */
.bill {{ background:#1a1a1a; border-radius:10px; padding:14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center; gap:10px; }}
.bill .left {{ flex:1; min-width:0; }}
.bill .name {{ font-size:0.95em; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.bill .detail {{ color:#777; font-size:0.75em; margin-top:2px; }}
.bill .right {{ text-align:right; flex-shrink:0; }}
.bill .amt {{ font-size:1.1em; font-weight:700; }}
.bill .due {{ color:#777; font-size:0.75em; }}
.bill.urgent {{ border-left:3px solid #f87171; }}
.bill.soon {{ border-left:3px solid #d4a017; }}
.bill.action {{ border-left:3px solid #60a5fa; }}

/* Progress bar */
.bar-wrap {{ background:#333; border-radius:4px; height:8px; margin-top:6px; overflow:hidden; }}
.bar {{ height:100%; border-radius:4px; }}

/* Section header */
.sh {{ color:#d4a017; font-size:0.85em; text-transform:uppercase; letter-spacing:1px; padding:16px 0 8px; border-bottom:1px solid #333; margin-bottom:10px; }}

/* Buttons */
.btn {{ display:inline-block; padding:10px 20px; border:none; border-radius:8px; cursor:pointer; font-size:0.9em; text-decoration:none; text-align:center; }}
.btn-g {{ background:#4ade80; color:#000; }}
.btn-b {{ background:#60a5fa; color:#000; }}
.btn-r {{ background:#f87171; color:#fff; font-size:0.75em; padding:6px 10px; }}
.btn-o {{ background:#d4a017; color:#000; }}

/* Forms */
.fc {{ background:#1a1a1a; border-radius:12px; padding:20px; max-width:500px; margin:0 auto; }}
.fg {{ margin-bottom:14px; }}
.fg label {{ display:block; color:#999; font-size:0.8em; margin-bottom:4px; }}
.fg input, .fg select, .fg textarea {{ width:100%; padding:10px; border-radius:8px; border:1px solid #333; background:#111; color:#eee; font-size:1em; }}

/* Alert box */
.alert {{ background:rgba(248,113,113,0.1); border:1px solid #f87171; border-radius:10px; padding:14px; margin-bottom:12px; }}
.alert-gold {{ background:rgba(212,160,23,0.1); border-color:#d4a017; }}
.alert b {{ display:block; margin-bottom:4px; }}
.msg {{ padding:12px; border-radius:8px; margin-bottom:12px; }}
.msg-ok {{ background:rgba(74,222,128,0.1); color:#4ade80; border:1px solid #4ade80; }}

/* Hours table */
.ht {{ width:100%; border-collapse:collapse; font-size:0.85em; }}
.ht th {{ color:#999; font-size:0.7em; text-transform:uppercase; padding:8px 6px; text-align:right; }}
.ht th:first-child {{ text-align:left; }}
.ht td {{ padding:8px 6px; border-top:1px solid #222; text-align:right; }}
.ht td:first-child {{ text-align:left; font-weight:600; }}
.ht .hl {{ background:rgba(74,222,128,0.08); }}

@media (max-width:500px) {{ .g2 {{ grid-template-columns:1fr; }} .big .num {{ font-size:1.8em; }} }}
</style>
</head>
<body>
<nav>{nav_links}</nav>
<div class="p">{body_html}</div>
<script>
(function(){{ var b=''; if(location.pathname.startsWith('/finance'))b='/finance'; if(!b)return;
document.querySelectorAll('a[href^="/"]').forEach(function(a){{ if(!a.getAttribute('href').startsWith('/finance'))a.setAttribute('href',b+a.getAttribute('href')); }});
document.querySelectorAll('form[action^="/"]').forEach(function(f){{ if(!f.getAttribute('action').startsWith('/finance'))f.setAttribute('action',b+f.getAttribute('action')); }});
}})();
</script>
</body>
</html>"""


# ─── Request Handler ───────────────────────────────────────────────

class LedgerHandler(SimpleHTTPRequestHandler):

    def check_auth(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Basic "):
            try:
                decoded = base64.b64decode(auth_header[6:]).decode()
                user, pw = decoded.split(":", 1)
                if user == AUTH_USER and pw == AUTH_PASS:
                    return True
            except Exception:
                pass
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="HaloFinance"')
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>Login required</h2>")
        return False

    def _strip(self, p):
        self._base = get_base(p)
        if p.startswith("/finance"):
            p = p[8:] or "/"
        return p.rstrip("/") or "/"

    def do_GET(self):
        if not self.check_auth(): return
        parsed = urlparse(self.path)
        path = self._strip(parsed.path)
        params = parse_qs(parsed.query)
        routes = {
            "/": self.page_home, "/bills": self.page_bills, "/cards": self.page_cards,
            "/hours": self.page_hours, "/add-bill": self.page_add_bill,
            "/edit-bill": self.page_edit_bill,
        }
        handler = routes.get(path)
        if handler: handler(params)
        else: self.send_error(404)

    def do_POST(self):
        if not self.check_auth(): return
        path = self._strip(self.path)
        length = int(self.headers.get("Content-Length", 0))
        data = {k: v[0] if len(v)==1 else v for k,v in parse_qs(self.rfile.read(length).decode()).items()}
        if path == "/add-bill": self.handle_add_bill(data)
        elif path == "/edit-bill": self.handle_edit_bill(data)
        elif path.startswith("/delete-bill/"): self.handle_delete_bill(path.split("/")[-1])
        else: self.send_error(404)

    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def redirect(self, url):
        self.send_response(303)
        self.send_header("Location", getattr(self, '_base', '') + url)
        self.end_headers()

    # ─── Helper: load and compute all bill data ─────────────────

    def _load_data(self):
        conn = get_db()
        bills = [dict(b) for b in get_bills(conn)]
        conn.close()
        today = date.today()
        rate = get_hourly_rate(today)

        cc = sorted([b for b in bills if b["category"]=="credit-card"], key=lambda x: x["total_owed"])
        affirm = sorted([b for b in bills if b["category"]=="debt-payment"], key=lambda x: x["total_owed"])
        housing = [b for b in bills if b["category"] in ("mortgage","car-payment")]
        recurring = [b for b in bills if b["category"] not in ("paycheck","misc-income","credit-card","debt-payment","mortgage","car-payment") and b["frequency"]!="payroll"]
        payroll = [b for b in bills if b["frequency"]=="payroll"]
        income = [b for b in bills if b["category"] in ("paycheck","misc-income")]

        def ms(lst): return sum(to_monthly(b["amount"], b["frequency"]) for b in lst)
        all_out = cc + affirm + housing + recurring
        monthly_in = ms(income)
        monthly_out = ms(all_out)
        weekly_bills = monthly_out / 4.33
        takehome_60, gross_60 = calc_weekly_takehome(60, rate)

        # Upcoming (due within 7 days)
        upcoming = []
        for b in all_out:
            if b["due_day"] > 0:
                nd, pb = get_next_due(b["due_day"], today)
                if pb:
                    days = (pb - today).days
                    if 0 <= days <= 7:
                        upcoming.append({**b, "pay_by": pb, "days_left": days})
        upcoming.sort(key=lambda x: x["days_left"])

        return dict(
            bills=bills, cc=cc, affirm=affirm, housing=housing, recurring=recurring,
            payroll=payroll, income=income, today=today, rate=rate,
            monthly_in=monthly_in, monthly_out=monthly_out, weekly_bills=weekly_bills,
            takehome_60=takehome_60, gross_60=gross_60, upcoming=upcoming,
            cc_owed=sum(b["total_owed"] for b in cc),
            affirm_owed=sum(b["total_owed"] for b in affirm),
        )

    # ─── Pages ─────────────────────────────────────────────────
    # ─── Pages ─────────────────────────────────────────────────

    def page_home(self, params):
        d = self._load_data()
        gap = d["monthly_in"] - d["monthly_out"]
        weekly_gap = d["takehome_60"] - d["weekly_bills"]
        hrs = hours_needed_for(d["weekly_bills"], d["rate"])

        # Upcoming bills
        up_html = ""
        for b in d["upcoming"]:
            dl = b["days_left"]
            cls = "urgent" if dl <= 1 else "soon"
            when = "PAY TODAY" if dl == 0 else f"Pay by {b['pay_by'].strftime('%a %b %d')}"
            up_html += f"""<div class="bill {cls}">
              <div class="left"><div class="name">{b['name']}</div><div class="detail">{when}</div></div>
              <div class="right"><div class="amt red">${b['amount']:,.2f}</div></div>
            </div>"""

        if not up_html:
            up_html = '<div class="big" style="padding:14px"><span class="green">Nothing due this week</span></div>'

        body = f"""
        <div class="big">
          <div class="label">What We Bring Home</div>
          <div class="num green">${d['monthly_in']:,.0f}<span style="font-size:0.4em;color:#777">/mo</span></div>
          <div class="sub">${d['monthly_in']/4.33:,.0f}/week (paycheck + dad's SS)</div>
        </div>

        <div class="g2">
          <div class="big">
            <div class="label">What Goes Out</div>
            <div class="num red">${d['monthly_out']:,.0f}<span style="font-size:0.4em;color:#777">/mo</span></div>
            <div class="sub">${d['weekly_bills']:,.0f}/week</div>
          </div>
          <div class="big">
            <div class="label">{'We Are Short' if gap < 0 else 'Left Over'}</div>
            <div class="num {'red' if gap < 0 else 'green'}">${abs(gap):,.0f}<span style="font-size:0.4em;color:#777">/mo</span></div>
            <div class="sub">${abs(weekly_gap):,.0f}/week {'short' if weekly_gap < 0 else 'left'}</div>
          </div>
        </div>

        <div class="g2">
          <div class="big">
            <div class="label">Credit Card Debt</div>
            <div class="num red">${d['cc_owed']:,.0f}</div>
            <div class="sub">11 cards &middot; ${sum(b['amount'] for b in d['cc']):,.0f}/mo minimums</div>
          </div>
          <div class="big">
            <div class="label">Affirm Debt</div>
            <div class="num red">${d['affirm_owed']:,.0f}</div>
            <div class="sub">10 loans &middot; ${sum(b['amount'] for b in d['affirm']):,.0f}/mo</div>
          </div>
        </div>

        <div class="big" style="border:1px solid #d4a017">
          <div class="label gold">Hours Needed to Cover Bills</div>
          <div class="num gold">{hrs} hrs/week</div>
          <div class="sub">{hrs/5:.1f} hours/day &times; 5 days &middot; <a href="/hours" style="color:#60a5fa">See breakdown</a></div>
        </div>

        <div class="sh">Due This Week (Pay Wednesday)</div>
        {up_html}
        """

        self.send_html(render_page("Home", body))

    def page_bills(self, params):
        d = self._load_data()
        today = d["today"]
        msg = params.get("msg", [""])[0]
        msg_html = f'<div class="msg msg-ok">{msg}</div>' if msg else ""

        def bill_card(b, show_owed=False):
            due_str = ""
            cls = ""
            if b["due_day"] > 0:
                nd, pb = get_next_due(b["due_day"], today)
                if pb:
                    days = (pb - today).days
                    due_str = f"Pay by {pb.strftime('%a %b %d')}"
                    if days < 0: cls = "urgent"; due_str = "OVERDUE"
                    elif days <= 3: cls = "soon"

            owed = ""
            if show_owed and b["total_owed"] > 0:
                owed = f' &middot; <span class="red">${b["total_owed"]:,.0f} owed</span>'
                if b["interest_rate"] > 0:
                    owed += f' @ {b["interest_rate"]}%'

            warn = ""
            if "CANCEL" in b.get("notes",""):
                cls = "action"
                warn = '<div class="detail blue">Call and cancel credit protection</div>'

            return f"""<div class="bill {cls}">
              <div class="left">
                <div class="name">{b['name']}</div>
                <div class="detail">{due_str}{owed}</div>
                {warn}
              </div>
              <div class="right">
                <div class="amt">${b['amount']:,.2f}</div>
                <a href="/edit-bill?id={b['id']}" style="color:#60a5fa;font-size:0.75em">Edit</a>
                <form method="post" action="/delete-bill/{b['id']}" style="display:inline" onsubmit="return confirm('Delete?')">
                  <button class="btn-r" type="submit" style="margin-left:4px">X</button>
                </form>
              </div>
            </div>"""

        sections = [
            ("Mortgage & Car", d["housing"], True),
            ("Utilities & Phones", [b for b in d["recurring"] if b["category"]=="utilities"], False),
            ("Insurance", [b for b in d["recurring"] if b["category"]=="insurance"], False),
            ("Food & Gas", [b for b in d["recurring"] if b["category"] in ("groceries","gas")], False),
            ("Dad's Support", [b for b in d["recurring"] if b["category"]=="father-support"], False),
            ("Subscriptions & Other", [b for b in d["recurring"] if b["category"] not in ("utilities","insurance","groceries","gas","father-support")], False),
        ]

        body = msg_html
        for title, items, show_owed in sections:
            if not items: continue
            total = sum(b["amount"] for b in items)
            body += f'<div class="sh">{title} &mdash; ${total:,.0f}/mo</div>'
            for b in items:
                body += bill_card(b, show_owed)

        body += f"""
        <div style="text-align:center;margin:24px 0">
          <a href="/add-bill" class="btn btn-g" style="padding:14px 32px;font-size:1.1em">+ Add New Bill</a>
        </div>"""

        self.send_html(render_page("All Bills", body))

    def page_cards(self, params):
        d = self._load_data()
        today = d["today"]
        msg = params.get("msg", [""])[0]
        msg_html = f'<div class="msg msg-ok">{msg}</div>' if msg else ""

        body = msg_html
        body += f"""
        <div class="big" style="border:1px solid #f87171">
          <div class="label">Total Credit Card Debt</div>
          <div class="num red">${d['cc_owed']:,.2f}</div>
          <div class="sub">11 cards &middot; ${sum(b['amount'] for b in d['cc']):,.2f}/mo in minimums</div>
        </div>
        <p style="color:#999;font-size:0.85em;margin-bottom:12px">
          Ordered by balance &mdash; pay off #1 first, then roll that payment into #2. That's the snowball.
        </p>"""

        for i, b in enumerate(d["cc"], 1):
            nd, pb = get_next_due(b["due_day"], today)
            due_str = f"Due {nd.strftime('%b %d')} &middot; Pay by {pb.strftime('%a %b %d')}" if nd else ""
            pct = min(100, (b["total_owed"] / max(b["total_owed"], 1)) * 100) if b["total_owed"] > 0 else 0

            warn = ""
            cls = ""
            if "CANCEL" in b.get("notes",""):
                cls = "action"
                warn = '<div class="detail" style="color:#60a5fa;font-weight:600">CALL &amp; CANCEL credit protection fees</div>'
            if "OVERLIMIT" in b.get("notes",""):
                warn += '<div class="detail red">Over limit</div>'

            body += f"""<div class="bill {cls}">
              <div class="left">
                <div class="name"><span class="gold" style="font-size:1.2em">#{i}</span> {b['name']}</div>
                <div class="detail">{due_str} &middot; {b['interest_rate']}% APR</div>
                {warn}
                <div class="bar-wrap"><div class="bar" style="width:100%;background:{'#f87171' if b['interest_rate']>29 else '#d4a017' if b['interest_rate']>25 else '#4ade80'}"></div></div>
              </div>
              <div class="right">
                <div class="amt red">${b['total_owed']:,.2f}</div>
                <div class="due">${b['amount']:,.2f}/mo min</div>
                <a href="/edit-bill?id={b['id']}" style="color:#60a5fa;font-size:0.75em">Edit</a>
              </div>
            </div>"""

        # Affirm section
        body += f"""
        <div class="big" style="border:1px solid #f87171;margin-top:20px">
          <div class="label">Affirm Buy Now Pay Later</div>
          <div class="num red">${d['affirm_owed']:,.2f}</div>
          <div class="sub">10 loans &middot; 8 of 10 are 30-36% APR</div>
        </div>"""

        for i, b in enumerate(d["affirm"], 1):
            nd, pb = get_next_due(b["due_day"], today)
            due_str = f"Pay by {pb.strftime('%a %b %d')}" if pb else ""
            last = "LAST PAYMENT" if b.get("notes","") == "Last payment" else ""

            body += f"""<div class="bill {'soon' if last else ''}">
              <div class="left">
                <div class="name"><span class="gold">#{i}</span> {b['name']}</div>
                <div class="detail">{due_str} {(' &middot; ' + b['interest_rate'].__str__() + '% APR') if b['interest_rate'] > 0 else ' &middot; 0% APR'} {'<span class="green">&middot; ' + last + '</span>' if last else ''}</div>
              </div>
              <div class="right">
                <div class="amt red">${b['total_owed']:,.2f}</div>
                <div class="due">${b['amount']:,.2f}/mo</div>
              </div>
            </div>"""

        self.send_html(render_page("Cards & Loans", body))

    def page_hours(self, params):
        d = self._load_data()
        rate = d["rate"]
        raise_rate = RAISE_RATE
        wb = d["weekly_bills"]

        hrs_now = hours_needed_for(wb, rate)
        hrs_raise = hours_needed_for(wb, raise_rate)
        hrs_comf_now = hours_needed_for(wb + 200, rate)
        hrs_comf_raise = hours_needed_for(wb + 200, raise_rate)
        th60_now, _ = calc_weekly_takehome(60, rate)
        th60_raise, _ = calc_weekly_takehome(60, raise_rate)

        rows = ""
        for hrs in [40, 45, 50, 55, 58, 60, 65, 70, 75]:
            th1, g1 = calc_weekly_takehome(hrs, rate)
            th2, g2 = calc_weekly_takehome(hrs, raise_rate)
            l1, l2 = th1 - wb, th2 - wb
            hl = ' class="hl"' if hrs == 60 else ""
            mark = " *" if hrs == 60 else ""
            rows += f"""<tr{hl}>
              <td>{hrs}hr{mark}</td>
              <td>${th1:,.0f}</td><td class="{'green' if l1>=0 else 'red'}">${l1:+,.0f}</td>
              <td style="border-left:2px solid #d4a017">${th2:,.0f}</td><td class="{'green' if l2>=0 else 'red'}">${l2:+,.0f}</td>
            </tr>"""

        body = f"""
        <div class="big">
          <div class="label">Weekly Bills to Cover</div>
          <div class="num gold">${wb:,.0f}</div>
          <div class="sub">That's what needs to come out of each Wednesday paycheck</div>
        </div>

        <div class="g2">
          <div class="big" style="border:1px solid #f87171">
            <div class="label">Now ${rate:.2f}/hr</div>
            <div class="num red">{hrs_now} hrs</div>
            <div class="sub">to break even</div>
          </div>
          <div class="big" style="border:1px solid #4ade80">
            <div class="label">After Raise ${raise_rate:.2f}/hr</div>
            <div class="num green">{hrs_raise} hrs</div>
            <div class="sub">to break even</div>
          </div>
        </div>

        <div class="big" style="border:1px solid #60a5fa">
          <div class="label">The Raise Saves You</div>
          <div class="num blue">{hrs_now - hrs_raise:.1f} hrs/week</div>
          <div class="sub">and puts ${th60_raise - th60_now:,.0f} more in your pocket every Wednesday at 60hrs</div>
        </div>

        <div class="sh">Side by Side &mdash; Every Hour Scenario</div>
        <p style="color:#777;font-size:0.8em;margin-bottom:10px">* = your current 60hr target &middot; Green = money left after bills</p>
        <table class="ht">
          <tr><th>Hours</th><th colspan="2">Now ${rate:.2f}/hr</th><th colspan="2" style="border-left:2px solid #d4a017">After Raise ${raise_rate:.2f}/hr</th></tr>
          <tr><th></th><th>Take-Home</th><th>Left</th><th style="border-left:2px solid #d4a017">Take-Home</th><th>Left</th></tr>
          {rows}
        </table>

        <div class="big" style="margin-top:16px">
          <div class="label">Saturday Shift (8 hrs extra OT)</div>
          <div class="sub" style="font-size:1em">Now: <span class="green">+${calc_weekly_takehome(68, rate)[0] - th60_now:,.0f} extra</span> &nbsp;&nbsp; After Raise: <span class="green">+${calc_weekly_takehome(68, raise_rate)[0] - th60_raise:,.0f} extra</span></div>
        </div>
        """

        self.send_html(render_page("Hours Calculator", body))

    def page_add_bill(self, params):
        msg = params.get("msg", [""])[0]
        msg_html = f'<div class="msg msg-ok">{msg}</div>' if msg else ""
        cat_opts = "".join(f'<option value="{c}">{c}</option>' for c in CATEGORIES)
        freq_opts = "".join(f'<option value="{f}">{f}</option>' for f in ["monthly","weekly","biweekly","payroll","quarterly","annual"])

        body = f"""{msg_html}
        <div class="fc">
          <div class="sh" style="margin-top:0">Add New Bill</div>
          <form method="post" action="/add-bill">
            <div class="fg"><label>Name</label><input type="text" name="name" placeholder="e.g. Netflix, AT&T" required></div>
            <div class="fg"><label>Payment Amount ($)</label><input type="number" name="amount" step="0.01" min="0" placeholder="0.00" required></div>
            <div class="fg"><label>Due Day (1-28, or 0 for no fixed day)</label><input type="number" name="due_day" min="0" max="28" value="1"></div>
            <div class="fg"><label>How Often</label><select name="frequency">{freq_opts}</select></div>
            <div class="fg"><label>Category</label><select name="category">{cat_opts}</select></div>
            <div class="fg"><label>Total Owed ($) (0 if not a debt)</label><input type="number" name="total_owed" step="0.01" min="0" value="0"></div>
            <div class="fg"><label>Interest Rate % (0 if none)</label><input type="number" name="interest_rate" step="0.01" min="0" value="0"></div>
            <div class="fg"><label>Notes</label><textarea name="notes"></textarea></div>
            <button type="submit" class="btn btn-g" style="width:100%">Add Bill</button>
          </form>
        </div>"""
        self.send_html(render_page("Add Bill", body))

    def page_edit_bill(self, params):
        bill_id = params.get("id", [None])[0]
        if not bill_id: return self.redirect("/bills")
        conn = get_db()
        bill = conn.execute("SELECT * FROM bills WHERE id=?", (int(bill_id),)).fetchone()
        conn.close()
        if not bill: return self.redirect("/bills")
        b = dict(bill)
        cat_opts = "".join(f'<option value="{c}" {"selected" if c==b["category"] else ""}>{c}</option>' for c in CATEGORIES)
        freq_opts = "".join(f'<option value="{f}" {"selected" if f==b["frequency"] else ""}>{f}</option>' for f in ["monthly","weekly","biweekly","payroll","quarterly","annual"])

        body = f"""
        <div class="fc">
          <div class="sh" style="margin-top:0">Edit: {b['name']}</div>
          <form method="post" action="/edit-bill">
            <input type="hidden" name="id" value="{b['id']}">
            <div class="fg"><label>Name</label><input type="text" name="name" value="{b['name']}" required></div>
            <div class="fg"><label>Payment Amount ($)</label><input type="number" name="amount" step="0.01" min="0" value="{b['amount']}" required></div>
            <div class="fg"><label>Due Day (1-28)</label><input type="number" name="due_day" min="0" max="28" value="{b['due_day']}"></div>
            <div class="fg"><label>How Often</label><select name="frequency">{freq_opts}</select></div>
            <div class="fg"><label>Category</label><select name="category">{cat_opts}</select></div>
            <div class="fg"><label>Total Owed ($)</label><input type="number" name="total_owed" step="0.01" min="0" value="{b['total_owed']}"></div>
            <div class="fg"><label>Interest Rate %</label><input type="number" name="interest_rate" step="0.01" min="0" value="{b['interest_rate']}"></div>
            <div class="fg"><label>Notes</label><textarea name="notes">{b.get('notes','')}</textarea></div>
            <button type="submit" class="btn btn-g" style="width:100%">Save</button>
          </form>
          <div style="text-align:center;margin-top:12px"><a href="/bills" style="color:#999">Cancel</a></div>
        </div>"""
        self.send_html(render_page(f"Edit {b['name']}", body))

    # ─── Form Handlers ────────────────────────────────────────

    def handle_add_bill(self, data):
        conn = get_db()
        conn.execute("INSERT INTO bills (name,amount,due_day,frequency,category,total_owed,interest_rate,notes) VALUES (?,?,?,?,?,?,?,?)", (
            data.get("name",""), float(data.get("amount",0)), int(data.get("due_day",1)),
            data.get("frequency","monthly"), data.get("category","general"),
            float(data.get("total_owed",0)), float(data.get("interest_rate",0)), data.get("notes",""),
        ))
        conn.commit(); conn.close()
        self.redirect("/bills?msg=Added!")

    def handle_edit_bill(self, data):
        conn = get_db()
        conn.execute("UPDATE bills SET name=?,amount=?,due_day=?,frequency=?,category=?,total_owed=?,interest_rate=?,notes=? WHERE id=?", (
            data.get("name",""), float(data.get("amount",0)), int(data.get("due_day",1)),
            data.get("frequency","monthly"), data.get("category","general"),
            float(data.get("total_owed",0)), float(data.get("interest_rate",0)), data.get("notes",""),
            int(data.get("id",0)),
        ))
        conn.commit(); conn.close()
        self.redirect("/bills?msg=Updated!")

    def handle_delete_bill(self, bill_id):
        conn = get_db()
        conn.execute("DELETE FROM bills WHERE id=?", (int(bill_id),))
        conn.commit(); conn.close()
        self.redirect("/bills?msg=Deleted")

    def log_message(self, format, *args):
        pass


# ─── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("HaloFinance Ledger Dashboard")
    print(f"Database: {DB_PATH}")
    print(f"Serving: http://localhost:{PORT}")
    print(f"Login:   {AUTH_USER} / {'(from HALO_PASSWORD env)' if os.environ.get('HALO_PASSWORD') else AUTH_PASS}")
    print()
    print("Edit seed_bills() in this file with YOUR real bills, then delete")
    print(f"{DB_PATH} and restart to re-seed.")
    server = HTTPServer((HOST, PORT), LedgerHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
