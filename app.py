
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="Northbeam Weekly Performance Dashboard", layout="wide")

st.title("Northbeam Weekly Performance Dashboard")
st.caption("Week-ending time axis · Hover to see exact values · Platforms include AppLovin")

@st.cache_data
def load_data():
    df = pd.read_csv("data/northbeam_tracking.csv", parse_dates=["period_end"])
    # Clean numeric for plotting
    df["value_num"] = (
        df["value"]
        .str.replace("%", "", regex=False)
        .str.replace("+", "", regex=False)
        .astype(float)
    )
    return df

df = load_data()

# Controls
metrics = ["CPM", "CTR", "CPC", "CAC", "CvR", "ROAS", "BUDGET_SHARE", "SHARE_DELTA"]
default_metric = st.sidebar.selectbox("Metric", metrics, index=0)
all_platforms = ["Meta","Google","AppLovin","TikTok","YouTube","Microsoft","Pinterest","Snapchat"]
sel_platforms = st.sidebar.multiselect("Platforms", all_platforms, default=all_platforms[:3])

# Filter
sub = df[(df["metric"] == default_metric) & (df["platform"].isin(sel_platforms))].copy()
sub = sub.sort_values(["platform","period_end"])

# Build figure
fig = go.Figure()
for plat in sel_platforms:
    s2 = sub[sub["platform"] == plat]
    if s2.empty:
        continue
    fig.add_trace(
        go.Scatter(
            x=s2["period_end"],
            y=s2["value_num"],
            mode="lines+markers",
            name=plat,
            customdata=s2["value"],
            hovertemplate=(
                "<b>" + plat + "</b><br>"
                "Week ending: %{x|%Y-%m-%d}<br>"
                + default_metric + ": %{customdata}<extra></extra>"
            ),
        )
    )

fig.update_layout(
    title=f"{default_metric} — Weekly (hover to see values)",
    xaxis_title="Week ending",
    yaxis_title=default_metric,
    legend=dict(orientation="h", y=-0.2),
    margin=dict(l=40, r=20, t=60, b=60),
)

st.plotly_chart(fig, use_container_width=True)

# Data preview / download
with st.expander("Data preview & download"):
    st.dataframe(sub[["period_start","period_end","platform","metric","value"]].sort_values(["period_end","platform"]), use_container_width=True)
    st.download_button("Download CSV (current full dataset)", data=df.to_csv(index=False), file_name="northbeam_tracking.csv", mime="text/csv")

st.markdown("---")
st.markdown("**How to update weekly**")
st.markdown("""
1. Click **Upload a new CSV** below and select an updated `northbeam_tracking.csv` (same columns).  
2. This will replace the dataset for the current running app instance.  
3. To make it permanent on Streamlit Cloud, commit the CSV to your GitHub repo.
""")

uploaded = st.file_uploader("Upload a new CSV to preview/replace in session", type=["csv"])
if uploaded is not None:
    new_df = pd.read_csv(uploaded, parse_dates=["period_end"])
    new_df.to_csv("data/northbeam_tracking.csv", index=False)
    st.success("CSV replaced for this session. Refresh the page to reload the chart.")
    st.experimental_rerun()
