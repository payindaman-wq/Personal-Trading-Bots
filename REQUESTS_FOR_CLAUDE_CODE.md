# Requests for Claude Code

## Sprint Scaling Issue (2026-03-11 17:18 UTC)

**Problem:**
When we changed `STARTING_CAPITAL` from $10,000 → $1,000 in both competition_start.py scripts, the active sprint (comp-20260311-1300) was already mid-execution with trades at the $10k scale.

Modifying only the `starting_capital` field in meta.json and portfolio files created a mismatch:
- `starting_capital`: $1,000 (just changed)
- Actual portfolio equity: ~$10,000 (trades executed at old scale)
- Cash/positions/P&L: All calculated against $10k baseline

**Impact:**
Dashboard shows equity as $10,000 per bot because the actual trading data is still $10k-scaled. This breaks the visualization and accounting.

**Root Cause:**
Can't retroactively rescale an in-flight sprint. The tick engine executed all trades against the original $10k initialization.

**Options:**
1. **Recommended:** Archive comp-20260311-1300 (Tier 2 action), start fresh sprint at next 5 AM PST with proper $1,000 initialization
2. **If needed:** Retroactively rescale all portfolio data in comp-20260311-1300 (multiply all values by 0.1), but this is complex

**What I've Verified:**
- `STARTING_CAPITAL = 1000.00` ✓ in both competition_start.py and swing_competition_start.py
- Portfolio files show `"starting_capital": 1000.0` ✓ (manually edited)
- But actual cash/positions/closed_trades values are still $10k-scaled (unedited)

**Who Should Handle:**
Claude Code — needs to either:
- Execute retroactive scaling on comp-20260311-1300, OR
- Confirm archiving is OK and next sprint will auto-initialize correctly

**Status:**
Waiting for direction before taking action.

---

*Request filed by SYN (day trading commander) at 2026-03-11 17:18 UTC*
