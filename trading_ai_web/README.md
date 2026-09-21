# Trading AI — Web Edition

`index.html` is the whole app. Double-click it (or drag it into a browser) —
no install, no server, no Python required. It needs an internet connection
once, the first time it loads, to pull two small libraries (Chart.js and a
web font); after that it runs entirely offline in your browser. Nothing you
upload ever leaves your machine — there is no backend and no network call
made with your data.

## What's new vs. the original `web_interface.html`

The original web page was a front-end mockup: every number on screen (RSI
62.45, "Win Probability 62%", etc.) was hard-coded HTML — pressing "Analyze"
just swapped in the same fake numbers regardless of what you typed. This
version replaces that with a real, from-scratch JavaScript port of the
Python engine (`chart_analyzer.py` + `pnl_predictor.py`) plus a materially
deeper probability model:

1. **Real indicators, computed from your data** — SMA(20/50/200), RSI(14),
   MACD(12,26,9), Bollinger Bands(20, 2σ), ATR(14), and swing-based
   support/resistance, all recomputed live from whatever CSV you load.
2. **Analytic probability** — a closed-form Brownian-motion-with-drift
   barrier-hitting formula estimates P(target hit before stop) from your
   data's own historical drift and volatility, instead of a fixed
   0.65/0.58/0.42/0.35 lookup table.
3. **Monte Carlo simulation** — thousands of simulated price paths (GBM,
   configurable path count and horizon) cross-check the analytic formula
   and report a 95% confidence interval, so you can see how much
   uncertainty is really in the estimate.
4. **Walk-forward backtest** — the same entry/stop/target rule is replayed
   across your actual historical bars (out-of-sample at each point) to
   produce a genuine, data-driven win rate — the "based on the chart, tell
   me what actually happened" number.
5. **Blended probability** — the four sources (trend heuristic, analytic,
   Monte Carlo, backtest) are combined by inverse-variance weighting, so
   sources with a tighter confidence interval count for more.
6. **Kelly-criterion position sizing**, a fixed-risk sizing calculator tied
   to your account size and risk %, JSON/CSV export, a printable report,
   and a light/dark theme.

## Using it

- **Upload CSV** — needs `Open,High,Low,Close` columns (`Date` and `Volume`
  are optional but recommended). This is the same format the original
  Python tool's CSV mode expects, and the same format `sample_uptrend.csv`
  / `sample_downtrend.csv` / `sample_sideways.csv` in `data_samples/` use —
  drop one of those in to try it immediately.
- **Paste CSV** — same format, pasted as text instead of a file.
- **Sample data** — generates a synthetic random-walk series in the browser
  (uptrend / downtrend / sideways / volatile) for exploring the tool
  without any data of your own.

There is deliberately no "look up a live stock symbol" box: a static HTML
file with no backend can't fetch live market data without exposing an API
key in client-side JavaScript, which isn't something you should ever do.
The Python backend (below) is still the right tool for pulling live data.

## The Python backend

`python_backend_src/` is the original command-line tool, unchanged, for
anyone who wants to pull live data (`python trading_ai.py AAPL`) or run
things outside a browser. See `python_backend_src/README_original.md` and
`python_backend_src/config.json` for that side of the toolkit.

## Important

This is an educational analysis tool, not financial advice. Every
probability on the page comes from a model (Brownian-motion assumptions,
historical volatility, a finite backtest sample) — none of it predicts the
future with certainty, small samples produce wide confidence intervals, and
past performance does not guarantee future results. Always use a stop
loss and manage risk with real position sizing before trading real money.
