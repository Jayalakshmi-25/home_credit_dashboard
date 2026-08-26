from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.risk_page import render_risk_page

render_risk_page("Time Series", "AGE_YEARS")
