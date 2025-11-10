
# Northbeam Weekly Performance Dashboard (Streamlit)

A shareable, interactive weekly dashboard with hover-to-see values and metric/platform controls.
Platforms include **AppLovin**.

## One-click Deploy (Streamlit Cloud)

1. Create a **public GitHub repo** and upload these files:
   - `app.py`
   - `requirements.txt`
   - `data/northbeam_tracking.csv`
2. Go to **https://share.streamlit.io** (Streamlit Community Cloud) and click **New app**.
3. Select your repo and set:
   - **Main file path**: `app.py`
4. Click **Deploy**. You'll get a shareable URL like:
   `https://your-repo-name.streamlit.app`

## Updating data each week
- Replace `data/northbeam_tracking.csv` in your GitHub repo (use the **Edit file** button on GitHub) and Commit.  
- The app will auto-redeploy and show the new week.
- Columns must be: `period_start, period_end, platform, metric, value` (value is a string like `63.24%`).

## Optional (upload in-session)
- The app includes a **CSV uploader** to preview or temporarily replace data for the current session.
- To make changes permanent, commit the CSV to the repo.

## Notes
- X-axis is **week ending**.
- Hover shows the **original percentage string** from the CSV (no rounding drift).
- Default platforms shown: Meta, Google, AppLovin (you can toggle more in the sidebar).
