# Streamlit Business Dashboard
# Save this file as streamlit_dashboard.py and run: streamlit run streamlit_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 Streamlit Business Dashboard")
st.markdown("""
Upload an Excel file (.xlsx or .xls). The app will try to detect date, numeric, and categorical columns and
show five useful charts + a small KPI area.
""")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read all sheets and let user pick
    try:
        xl = pd.read_excel(uploaded_file, sheet_name=None)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    sheet_names = list(xl.keys())
    sheet = st.selectbox("Pilih sheet", sheet_names)
    df = xl[sheet].copy()

    st.write("### Preview data")
    st.dataframe(df.head(100))

    # Basic cleaning: drop completely empty columns
    df.dropna(axis=1, how="all", inplace=True)

    # Detect column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime"]).columns.tolist()
    if not datetime_cols:
        # try to parse any column that looks like date
        for c in df.columns:
            if df[c].dtype == object:
                try:
                    parsed = pd.to_datetime(df[c], errors="coerce")
                    if parsed.notna().sum() / max(1, len(parsed)) > 0.5:
                        df[c] = parsed
                        datetime_cols.append(c)
                except Exception:
                    pass

    categorical_cols = [c for c in df.columns if c not in numeric_cols + datetime_cols]

    st.sidebar.header("Controls")
    st.sidebar.write(f"Rows: {len(df):,} | Columns: {len(df.columns):,}")

    # KPI row
    st.markdown("## Key performance indicators")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Rows", f"{len(df):,}")
    # Biggest numeric sum column
    if numeric_cols:
        sums = df[numeric_cols].sum(numeric_only=True)
        top_sum_col = sums.abs().sort_values(ascending=False).index[0]
        k2.metric(f"Top sum: {top_sum_col}", f"{sums[top_sum_col]:,.0f}")
        k3.metric("Numeric cols", len(numeric_cols))
    else:
        k2.metric("Top sum", "-")
        k3.metric("Numeric cols", 0)

    if categorical_cols:
        k4.metric("Unique categories (sample)", 
                  ", ".join([f"{c}: {df[c].nunique()}" for c in (categorical_cols[:3])]))
    else:
        k4.metric("Unique categories", "No categorical columns found")

    st.markdown("---")

    # Chart selection / defaults
    st.sidebar.header("Chart settings")
    # Chart 1: Time series
    st.sidebar.subheader("Time series")
    date_col = st.sidebar.selectbox("Pilih kolom tanggal (opsional)", [None] + datetime_cols)
    ts_value_col = st.sidebar.selectbox("Value untuk time series", [None] + numeric_cols)

    # Chart 2: Top categories
    st.sidebar.subheader("Top by Category")
    cat_col = st.sidebar.selectbox("Kategori", [None] + categorical_cols)
    cat_value = st.sidebar.selectbox("Value untuk kategori", [None] + numeric_cols)
    top_n = st.sidebar.slider("Top N", 3, 20, 8)

    # Chart 3: Distribution
    st.sidebar.subheader("Distribution")
    dist_col = st.sidebar.selectbox("Pilih kolom numerik untuk histogram", [None] + numeric_cols, key="dist")

    # Chart 4: Correlation
    st.sidebar.subheader("Correlation")
    corr_cols = st.sidebar.multiselect("Pilih kolom numerik untuk korelasi (default: semua)", numeric_cols, default=numeric_cols[:8])

    # Chart 5: Category share
    st.sidebar.subheader("Category share")
    share_cat = st.sidebar.selectbox("Kategori untuk pie/treemap", [None] + categorical_cols, key="share")

    # Layout: 2 rows
    # Row A: Time series (big) + Top categories
    row_a1, row_a2 = st.columns([2, 1])

    # Chart 1: Time series
    with row_a1:
        st.subheader("1) Time series")
        if date_col and ts_value_col:
            ts = df[[date_col, ts_value_col]].dropna()
            ts = ts.groupby(date_col)[ts_value_col].sum().reset_index()
            fig_ts = px.line(ts, x=date_col, y=ts_value_col, markers=True, title=f"{ts_value_col} over time")
            st.plotly_chart(fig_ts, use_container_width=True)
        else:
            st.info("Pilih kolom tanggal dan nilai numerik di sidebar untuk menampilkan time series.")

    # Chart 2: Top categories
    with row_a2:
        st.subheader("2) Top categories")
        if cat_col and cat_value:
            tmp = df.groupby(cat_col)[cat_value].sum().sort_values(ascending=False).head(top_n).reset_index()
            fig_bar = px.bar(tmp, x=cat_value, y=cat_col, orientation="h", title=f"Top {top_n} {cat_col} by {cat_value}")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Pilih kategori dan nilai numerik di sidebar untuk menampilkan top categories.")

    st.markdown("---")

    # Row B: Distribution, Correlation, Share
    row_b1, row_b2, row_b3 = st.columns(3)

    # Chart 3: Distribution
    with row_b1:
        st.subheader("3) Distribution / Histogram")
        if dist_col:
            fig_hist = px.histogram(df, x=dist_col, nbins=30, title=f"Distribution of {dist_col}")
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Pilih kolom numerik untuk histogram di sidebar.")

    # Chart 4: Correlation heatmap
    with row_b2:
        st.subheader("4) Correlation heatmap")
        if len(corr_cols) >= 2:
            corr = df[corr_cols].corr()
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='Viridis'
            ))
            fig_corr.update_layout(title="Correlation matrix")
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Pilih minimal 2 kolom numerik untuk korelasi.")

    # Chart 5: Category share (pie or treemap)
    with row_b3:
        st.subheader("5) Category share")
        if share_cat:
            counts = df[share_cat].value_counts().reset_index()
            counts.columns = [share_cat, 'count']
            if counts.shape[0] <= 8:
                fig_pie = px.pie(counts, values='count', names=share_cat, title=f"Share of {share_cat}")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                fig_tree = px.treemap(counts, path=[share_cat], values='count', title=f"Share of {share_cat}")
                st.plotly_chart(fig_tree, use_container_width=True)
        else:
            st.info("Pilih kategori di sidebar untuk menampilkan share (pie/treemap).")

    st.markdown("---")
    st.write("### Notes & tips")
    st.write("• Jika kolom tanggal tidak dikenali, pastikan format kolom adalah tanggal atau reformattable.\n"
             "• Gunakan sidebar untuk memilih kolom yang relevan.\n"
             "• Untuk dataset besar, pertimbangkan agregasi sebelum plotting.")

    # Allow user to download a cleaned / aggregated summary
    if st.button("Download aggregated CSV (top-level)"):
        # create a small summary
        summary = {
            'rows': [len(df)],
            'columns': [len(df.columns)],
        }
        sum_df = pd.DataFrame(summary)
        st.download_button("Download summary CSV", sum_df.to_csv(index=False).encode('utf-8'), "summary.csv", "text/csv")

else:
    st.info("Upload file Excel untuk memulai. Contoh: dataset penjualan dengan kolom tanggal, produk, kategori, dan revenue/nilai.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit — modify the code to fit your business rules and KPIs.")
