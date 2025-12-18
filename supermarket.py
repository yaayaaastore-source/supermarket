import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
import io
import json
warnings.filterwarnings('ignore')

# ⚠️ HARUS di baris pertama setelah import
st.set_page_config(
    page_title="Supermarket Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== MULTI-LANGUAGE SUPPORT ====================
language_dict = {
    "English": {
        "title": "🛒 Supermarket Analytics Dashboard",
        "upload_title": "📤 Upload Excel File",
        "upload_desc": "Upload your supermarket data (Excel format)",
        "sample_data": "Use Sample Data",
        "filter_data": "Filter Data",
        "value_column": "Select Value Column",
        "date_column": "Select Date Column",
        "date_range": "Date Range",
        "category": "Select Category",
        "products": "Select Products (Optional)",
        "overview": "Overview",
        "categories": "Categories",
        "products_tab": "Products",
        "timeseries": "Time Series",
        "total": "Total",
        "average": "Average",
        "transactions": "Transactions",
        "unique_products": "Unique Products",
        "category_dist": "Category Distribution",
        "profit_margin": "Profit Margin by Category",
        "top_products": "Top 10 Best Selling Products",
        "product_details": "Product Details",
        "daily_trend": "Daily Trend",
        "monthly": "Monthly",
        "weekly": "Weekly",
        "export": "Export Data",
        "download_csv": "Download Data (CSV)",
        "footer": "Supermarket Analytics Dashboard • Made with Streamlit & Plotly • Updated: {date}",
        "no_file": "No file uploaded. Using sample data.",
        "file_loaded": "File successfully loaded!",
        "invalid_file": "Invalid file format. Please upload Excel file.",
        "error_chart": "Error displaying chart",
        "refresh_page": "Try refreshing the page or check your data.",
        "debug_info": "Debug Info",
        "data_shape": "Data Shape",
        "columns": "Columns",
        "sample_rows": "Sample Data",
        "search_product": "Search Product",
        "select_all": "Select All",
        "clear_all": "Clear All",
        "revenue": "Revenue",
        "quantity": "Quantity",
        "profit": "Profit",
        "unit_price": "Unit Price",
        "total_price": "Total Price"
    },
    "Bahasa Indonesia": {
        "title": "🛒 Dashboard Analisis Supermarket",
        "upload_title": "📤 Unggah File Excel",
        "upload_desc": "Unggah data supermarket Anda (format Excel)",
        "sample_data": "Gunakan Data Contoh",
        "filter_data": "Filter Data",
        "value_column": "Pilih Kolom Nilai",
        "date_column": "Pilih Kolom Tanggal",
        "date_range": "Rentang Tanggal",
        "category": "Pilih Kategori",
        "products": "Pilih Produk (Opsional)",
        "overview": "Ringkasan",
        "categories": "Kategori",
        "products_tab": "Produk",
        "timeseries": "Deret Waktu",
        "total": "Total",
        "average": "Rata-rata",
        "transactions": "Transaksi",
        "unique_products": "Produk Unik",
        "category_dist": "Distribusi Kategori",
        "profit_margin": "Margin Profit per Kategori",
        "top_products": "10 Produk Terlaris Teratas",
        "product_details": "Detail Produk",
        "daily_trend": "Tren Harian",
        "monthly": "Bulanan",
        "weekly": "Mingguan",
        "export": "Ekspor Data",
        "download_csv": "Unduh Data (CSV)",
        "footer": "Dashboard Analisis Supermarket • Dibuat dengan Streamlit & Plotly • Diperbarui: {date}",
        "no_file": "Tidak ada file yang diunggah. Menggunakan data contoh.",
        "file_loaded": "File berhasil dimuat!",
        "invalid_file": "Format file tidak valid. Harap unggah file Excel.",
        "error_chart": "Error menampilkan grafik",
        "refresh_page": "Coba refresh halaman atau periksa data Anda.",
        "debug_info": "Info Debug",
        "data_shape": "Bentuk Data",
        "columns": "Kolom",
        "sample_rows": "Data Contoh",
        "search_product": "Cari Produk",
        "select_all": "Pilih Semua",
        "clear_all": "Hapus Semua",
        "revenue": "Pendapatan",
        "quantity": "Jumlah",
        "profit": "Profit",
        "unit_price": "Harga Satuan",
        "total_price": "Total Harga"
    },
    "中文": {
        "title": "🛒 超市分析仪表板",
        "upload_title": "📤 上传Excel文件",
        "upload_desc": "上传您的超市数据（Excel格式）",
        "sample_data": "使用示例数据",
        "filter_data": "筛选数据",
        "value_column": "选择数值列",
        "date_column": "选择日期列",
        "date_range": "日期范围",
        "category": "选择类别",
        "products": "选择产品（可选）",
        "overview": "概览",
        "categories": "类别",
        "products_tab": "产品",
        "timeseries": "时间序列",
        "total": "总计",
        "average": "平均",
        "transactions": "交易",
        "unique_products": "唯一产品",
        "category_dist": "类别分布",
        "profit_margin": "按类别利润率",
        "top_products": "前10个畅销产品",
        "product_details": "产品详情",
        "daily_trend": "每日趋势",
        "monthly": "月度",
        "weekly": "周度",
        "export": "导出数据",
        "download_csv": "下载数据（CSV）",
        "footer": "超市分析仪表板 • 使用Streamlit和Plotly制作 • 更新时间: {date}",
        "no_file": "未上传文件。使用示例数据。",
        "file_loaded": "文件加载成功！",
        "invalid_file": "文件格式无效。请上传Excel文件。",
        "error_chart": "显示图表时出错",
        "refresh_page": "尝试刷新页面或检查您的数据。",
        "debug_info": "调试信息",
        "data_shape": "数据形状",
        "columns": "列",
        "sample_rows": "示例数据",
        "search_product": "搜索产品",
        "select_all": "全选",
        "clear_all": "清除全部",
        "revenue": "收入",
        "quantity": "数量",
        "profit": "利润",
        "unit_price": "单价",
        "total_price": "总价"
    }
}

# CSS kustom
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .error-box {
        background-color: #FEE2E2;
        border: 1px solid #EF4444;
        padding: 1rem;
        border-radius: 8px;
        color: #991B1B;
    }
    .success-box {
        background-color: #D1FAE5;
        border: 1px solid #10B981;
        padding: 1rem;
        border-radius: 8px;
        color: #065F46;
    }
    .language-selector {
        position: absolute;
        top: 10px;
        right: 20px;
        z-index: 1000;
    }
    .upload-section {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #3B82F6;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Pilih bahasa di pojok kanan atas
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    language = st.selectbox("", ["English", "Bahasa Indonesia", "中文"], label_visibility="collapsed")

# Ambil teks berdasarkan bahasa
text = language_dict[language]

# Header
st.markdown(f'<h1 class="main-header">{text["title"]}</h1>', unsafe_allow_html=True)

# ==================== UPLOAD FILE EXCEL ====================
st.markdown(f'<div class="upload-section"><h3>{text["upload_title"]}</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        text["upload_desc"],
        type=['xlsx', 'xls', 'csv'],
        help="Upload Excel file containing supermarket data"
    )

with col2:
    use_sample = st.checkbox(text["sample_data"], value=True)

# Fungsi untuk generate data sampel
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')  # Kurangi untuk performa
    
    # Multi-language categories
    categories = {
        'English': ['Food', 'Beverages', 'Electronics', 'Clothing', 'Household'],
        'Bahasa Indonesia': ['Makanan', 'Minuman', 'Elektronik', 'Pakaian', 'Rumah Tangga'],
        '中文': ['食品', '饮料', '电子产品', '服装', '家居用品']
    }
    
    products = {
        'Food': ['Bread', 'Milk', 'Eggs'],
        'Beverages': ['Water', 'Juice', 'Coffee'],
        'Electronics': ['Charger', 'Headphones', 'Cable'],
        'Clothing': ['T-Shirt', 'Pants', 'Jacket'],
        'Household': ['Soap', 'Toothpaste', 'Shampoo']
    }
    
    data = []
    for date in dates:
        for category_en in categories['English']:
            for product in products[category_en]:
                quantity = np.random.randint(1, 50)
                unit_price = np.random.uniform(1000, 50000)
                total_price = quantity * unit_price
                profit = total_price * np.random.uniform(0.1, 0.4)
                
                # Create entry for selected language
                category = categories[language][categories['English'].index(category_en)]
                
                data.append({
                    'Date': date,
                    'Category': category,
                    'Product': product,
                    'Quantity': quantity,
                    'Unit_Price': unit_price,
                    'Total_Price': total_price,
                    'Profit': profit,
                    'Month': date.strftime('%B'),
                    'Day': date.strftime('%A'),
                    'Week': date.isocalendar().week
                })
    
    df = pd.DataFrame(data)
    return df

# Load data from uploaded file or use sample
df = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Clean column names
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        
        # Ensure date column exists
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'tanggal' in col.lower() or '日期' in col.lower()]
        if date_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
        
        st.success(f"✅ {text['file_loaded']}")
        st.info(f"📊 {len(df)} rows, {len(df.columns)} columns loaded")
        
    except Exception as e:
        st.error(f"{text['invalid_file']}: {str(e)}")
        df = generate_sample_data()
        use_sample = True
elif use_sample:
    df = generate_sample_data()
    st.info(f"📋 {text['no_file']}")

# Inisialisasi session state untuk selected_products
if 'selected_products' not in st.session_state:
    st.session_state.selected_products = []

# Sidebar untuk filter
with st.sidebar:
    st.header("⚙️ " + text["filter_data"])
    
    if df is not None:
        # Kolom-kolom yang tersedia
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        object_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Auto-detect kolom
        # Cari kolom kategori (object dengan unique values < 20)
        category_cols = [col for col in object_cols if df[col].nunique() < 20 and df[col].nunique() > 1]
        product_cols = [col for col in object_cols if col not in category_cols and df[col].nunique() < 100]
        
        # Pilih kolom value
        default_value_col = None
        priority_cols = ['Total_Price', 'Revenue', 'Sales', 'Amount', 'Profit', 'Quantity', 'Unit_Price']
        for col in priority_cols:
            if col in df.columns:
                default_value_col = col
                break
        if not default_value_col and numeric_cols:
            default_value_col = numeric_cols[0]
        
        value_column = st.selectbox(
            text["value_column"],
            options=numeric_cols if numeric_cols else [],
            index=numeric_cols.index(default_value_col) if default_value_col in numeric_cols else 0
        ) if numeric_cols else st.selectbox(text["value_column"], options=[])
        
        # Pilih kolom date
        default_date_col = None
        date_priority_cols = ['Date', 'Tanggal', '日期', 'Transaction_Date', 'Order_Date']
        for col in date_priority_cols:
            if col in df.columns:
                default_date_col = col
                break
        if not default_date_col and date_cols:
            default_date_col = date_cols[0]
        
        date_column = st.selectbox(
            text["date_column"],
            options=date_cols if date_cols else [],
            index=date_cols.index(default_date_col) if default_date_col in date_cols else 0
        ) if date_cols else st.selectbox(text["date_column"], options=[])
        
        # Filter berdasarkan tanggal
        if date_column and date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            min_date = df[date_column].min().date()
            max_date = df[date_column].max().date()
            
            date_range = st.date_input(
                text["date_range"],
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df[(df[date_column].dt.date >= start_date) & (df[date_column].dt.date <= end_date)]
            else:
                df_filtered = df
        else:
            df_filtered = df
        
        # Filter kategori
        if category_cols:
            category_column = st.selectbox(
                "Category Column",
                options=category_cols,
                index=0
            )
            
            categories = st.multiselect(
                text["category"],
                options=df_filtered[category_column].unique(),
                default=df_filtered[category_column].unique()[:3] if len(df_filtered[category_column].unique()) > 3 else df_filtered[category_column].unique()
            )
            
            if categories:
                df_filtered = df_filtered[df_filtered[category_column].isin(categories)]
        
        # Filter produk dengan search
        if product_cols:
            product_column = st.selectbox(
                "Product Column",
                options=product_cols,
                index=0
            )
            
            if product_column:
                # Search box untuk produk
                search_term = st.text_input(text["search_product"], "")
                
                all_products = df_filtered[product_column].unique()
                
                if search_term:
                    filtered_products = [p for p in all_products if search_term.lower() in str(p).lower()]
                else:
                    filtered_products = all_products
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(text["select_all"]):
                        st.session_state.selected_products = list(filtered_products)
                with col2:
                    if st.button(text["clear_all"]):
                        st.session_state.selected_products = []
                
                selected_products = st.multiselect(
                    text["products"],
                    options=filtered_products,
                    default=st.session_state.selected_products
                )
                
                if selected_products:
                    df_filtered = df_filtered[df_filtered[product_column].isin(selected_products)]
    else:
        st.warning("No data available. Please upload a file or use sample data.")
        df_filtered = pd.DataFrame()

# Fungsi untuk membuat grafik dengan error handling - FIXED VERSION
def create_safe_plotly_chart(fig, chart_title=""):
    """Fungsi aman untuk membuat plotly chart dengan error handling"""
    try:
        if fig is None:
            raise ValueError("Figure is None")
        
        # PERBAIKAN: Gunang isinstance yang benar untuk plotly Figure
        if not isinstance(fig, (go.Figure)):
            # Coba konversi jika itu adalah plotly express figure
            try:
                if hasattr(fig, '_graph_obj'):
                    fig = go.Figure(fig)
                else:
                    raise TypeError(f"Object must be Plotly Figure, not {type(fig)}")
            except:
                raise TypeError(f"Object must be Plotly Figure, not {type(fig)}")
        
        if chart_title:
            fig.update_layout(title=chart_title)
        
        if fig.layout is None:
            fig.update_layout()
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <strong>⚠️ {text['error_chart']}:</strong><br>
            {str(e)}<br><br>
            <small>{text['refresh_page']}</small>
        </div>
        """, unsafe_allow_html=True)
        # Debug info
        with st.expander("Technical Details"):
            st.write(f"Error type: {type(e).__name__}")
            st.write(f"Figure type: {type(fig) if 'fig' in locals() else 'N/A'}")

# Main dashboard hanya jika ada data
if df_filtered is not None and not df_filtered.empty:
    # Tab utama
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📈 {text['overview']}",
        f"📊 {text['categories']}",
        f"🛍️ {text['products_tab']}",
        f"📅 {text['timeseries']}"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value = df_filtered[value_column].sum() if value_column in df_filtered.columns else 0
            st.metric(
                label=text["total"],
                value=f"${total_value:,.0f}" if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else f"{total_value:,.0f}",
                delta=f"{total_value * 0.05:,.0f}"
            )
        
        with col2:
            avg_value = df_filtered[value_column].mean() if value_column in df_filtered.columns else 0
            st.metric(
                label=text["average"],
                value=f"${avg_value:,.2f}" if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else f"{avg_value:,.2f}",
                delta=f"{avg_value * 0.03:,.2f}"
            )
        
        with col3:
            total_transactions = len(df_filtered)
            st.metric(
                label=text["transactions"],
                value=f"{total_transactions:,}",
                delta=f"{int(total_transactions * 0.02):,}"
            )
        
        with col4:
            if 'product_column' in locals() and product_column in df_filtered.columns:
                unique_products = df_filtered[product_column].nunique()
            else:
                unique_products = df_filtered.select_dtypes(include=['object']).iloc[:, 0].nunique() if len(df_filtered.select_dtypes(include=['object']).columns) > 0 else 0
            st.metric(
                label=text["unique_products"],
                value=f"{unique_products}",
                delta=f"{int(unique_products * 0.01)}"
            )
        
        # Grafik 1: Value per Kategori
        st.subheader(f"{value_column} by Category")
        try:
            if 'category_column' in locals() and category_column in df_filtered.columns:
                value_by_category = df_filtered.groupby(category_column)[value_column].sum().reset_index()
                
                fig1 = go.Figure(data=[
                    go.Bar(
                        x=value_by_category[category_column],
                        y=value_by_category[value_column],
                        marker_color=['#1E3A8A', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#E0F2FE'],
                        text=[f"${x:,.0f}" if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else f"{x:,.0f}" 
                              for x in value_by_category[value_column]],
                        textposition='auto'
                    )
                ])
                
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title=f"{value_column} ({'$' if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else 'Units'})",
                    xaxis_title=text["category"],
                    height=400,
                    showlegend=False
                )
                
                create_safe_plotly_chart(fig1)
        except Exception as e:
            st.error(f"{text['error_chart']}: {str(e)}")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(text["category_dist"])
            try:
                if 'category_column' in locals() and category_column in df_filtered.columns:
                    category_dist = df_filtered[category_column].value_counts().reset_index()
                    category_dist.columns = ['Category', 'Count']
                    
                    # PERBAIKAN: Gunang px.pie langsung, tidak perlu konversi
                    fig2 = px.pie(
                        category_dist,
                        values='Count',
                        names='Category',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Blues_r
                    )
                    
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    
                    create_safe_plotly_chart(fig2)
            except Exception as e:
                st.error(f"{text['error_chart']}: {str(e)}")
        
        with col2:
            st.subheader(text["profit_margin"])
            try:
                if 'Profit' in df_filtered.columns and 'Total_Price' in df_filtered.columns:
                    profit_margin = df_filtered.groupby(category_column if 'category_column' in locals() else 'Category').agg({
                        'Total_Price': 'sum',
                        'Profit': 'sum'
                    }).reset_index()
                    
                    profit_margin['Margin'] = (profit_margin['Profit'] / profit_margin['Total_Price']) * 100
                    
                    fig3 = go.Figure(data=[
                        go.Bar(
                            x=profit_margin[category_column if 'category_column' in locals() else 'Category'],
                            y=profit_margin['Margin'],
                            marker_color=profit_margin['Margin'],
                            colorscale='Blues',
                            text=[f"{x:.1f}%" for x in profit_margin['Margin']],
                            textposition='auto'
                        )
                    ])
                    
                    fig3.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis_title="Profit Margin (%)",
                        xaxis_title=text["category"],
                        height=400
                    )
                    
                    create_safe_plotly_chart(fig3)
                else:
                    st.info("Profit data not available for this chart")
            except Exception as e:
                st.error(f"{text['error_chart']}: {str(e)}")
    
    with tab3:
        st.subheader(text["top_products"])
        try:
            if 'product_column' in locals() and product_column in df_filtered.columns:
                top_products = df_filtered.groupby(product_column).agg({
                    value_column: 'sum'
                }).nlargest(10, value_column).reset_index()
                
                fig4 = go.Figure(data=[
                    go.Bar(
                        y=top_products[product_column],
                        x=top_products[value_column],
                        orientation='h',
                        marker_color='#3B82F6',
                        text=[f"${x:,.0f}" if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else f"{x:,.0f}" 
                              for x in top_products[value_column]],
                        textposition='auto'
                    )
                ])
                
                fig4.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title=f"{value_column} ({'$' if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else 'Units'})",
                    yaxis_title=text["products_tab"],
                    height=500
                )
                
                create_safe_plotly_chart(fig4)
        except Exception as e:
            st.error(f"{text['error_chart']}: {str(e)}")
        
        # Tabel detail produk
        st.subheader(text["product_details"])
        try:
            if 'product_column' in locals() and product_column in df_filtered.columns and 'category_column' in locals() and category_column in df_filtered.columns:
                product_detail = df_filtered.groupby([category_column, product_column]).agg({
                    value_column: 'sum'
                }).reset_index().sort_values(value_column, ascending=False).head(20)
                
                # Format angka
                if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower():
                    product_detail[value_column] = product_detail[value_column].apply(lambda x: f"${x:,.2f}")
                
                st.dataframe(
                    product_detail,
                    column_config={
                        category_column: st.column_config.TextColumn(text["category"]),
                        product_column: st.column_config.TextColumn(text["products_tab"]),
                        value_column: st.column_config.TextColumn(text["total"])
                    },
                    use_container_width=True,
                    hide_index=True
                )
        except Exception as e:
            st.error(f"Error displaying product table: {str(e)}")
    
    with tab4:
        st.subheader(text["daily_trend"])
        try:
            if date_column and date_column in df_filtered.columns:
                daily_data = df_filtered.groupby(date_column)[value_column].sum().reset_index()
                
                fig5 = go.Figure()
                
                fig5.add_trace(go.Scatter(
                    x=daily_data[date_column],
                    y=daily_data[value_column],
                    mode='lines+markers',
                    name=value_column,
                    line=dict(color='#3B82F6', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(59, 130, 246, 0.1)'
                ))
                
                fig5.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title=f"{value_column} ({'$' if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else 'Units'})",
                    xaxis_title=text["date_range"],
                    hovermode='x unified',
                    height=500
                )
                
                create_safe_plotly_chart(fig5)
        except Exception as e:
            st.error(f"{text['error_chart']}: {str(e)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(text["monthly"])
            try:
                if date_column and date_column in df_filtered.columns:
                    df_filtered['Month'] = df_filtered[date_column].dt.strftime('%Y-%m')
                    monthly_revenue = df_filtered.groupby('Month')[value_column].sum().reset_index()
                    
                    # PERBAIKAN: Gunang px.bar langsung
                    fig6 = px.bar(
                        monthly_revenue,
                        x='Month',
                        y=value_column,
                        color=value_column,
                        color_continuous_scale='Blues'
                    )
                    
                    fig6.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        xaxis_title="Month",
                        yaxis_title=f"{value_column} ({'$' if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else 'Units'})"
                    )
                    
                    create_safe_plotly_chart(fig6)
            except Exception as e:
                st.error(f"{text['error_chart']}: {str(e)}")
        
        with col2:
            st.subheader(text["weekly"])
            try:
                if date_column and date_column in df_filtered.columns:
                    df_filtered['Week'] = df_filtered[date_column].dt.isocalendar().week
                    weekly_avg = df_filtered.groupby('Week')[value_column].mean().reset_index()
                    
                    # PERBAIKAN: Gunang px.line langsung
                    fig7 = px.line(
                        weekly_avg,
                        x='Week',
                        y=value_column,
                        markers=True,
                        line_shape='spline'
                    )
                    
                    fig7.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        xaxis_title="Week",
                        yaxis_title=f"Average {value_column} ({'$' if 'price' in value_column.lower() or 'revenue' in value_column.lower() or 'profit' in value_column.lower() else 'Units'})"
                    )
                    
                    create_safe_plotly_chart(fig7)
            except Exception as e:
                st.error(f"{text['error_chart']}: {str(e)}")
    
    # Bagian bawah: Download data
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("📥 " + text["export"])
        
        # Konversi dataframe ke CSV
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=text["download_csv"],
            data=csv,
            file_name=f"supermarket_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{language}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Debug panel di sidebar
    with st.sidebar.expander("🔧 " + text["debug_info"]):
        st.write(f"**{text['data_shape']}:** {df_filtered.shape}")
        st.write(f"**{text['columns']}:** {list(df_filtered.columns)}")
        if value_column:
            st.write(f"**Value Column:** {value_column}")
        if date_column:
            st.write(f"**Date Column:** {date_column}")
        if 'category_column' in locals():
            st.write(f"**Category Column:** {category_column}")
        if 'product_column' in locals():
            st.write(f"**Product Column:** {product_column}")
        st.write(f"**{text['sample_rows']}:**")
        st.dataframe(df_filtered.head(3))
else:
    st.warning("⚠️ No data available. Please upload an Excel file or use sample data.")
    st.info("""
    **Expected Excel format:**
    - Date column (e.g., 'Date', 'Tanggal', '日期')
    - Value column (e.g., 'Total_Price', 'Revenue', 'Quantity')
    - Category column (e.g., 'Category', 'Kategori', '类别')
    - Product column (e.g., 'Product', 'Produk', '产品')
    
    **Sample data will be generated automatically if no file is uploaded.**
    """)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #6B7280;'>
        {text['footer'].format(date=datetime.now().strftime("%d %B %Y %H:%M"))}
    </div>
    """,
    unsafe_allow_html=True
)

# Info tambahan
with st.expander("ℹ️ How to use this dashboard"):
    st.write("""
    1. **Upload your Excel file** containing supermarket data
    2. **Select your language** from the top-right dropdown
    3. **Choose value column** (e.g., Total Price, Quantity)
    4. **Select date column** for time series analysis
    5. **Filter by category** and products as needed
    6. **Navigate through tabs** to see different visualizations
    7. **Download filtered data** as CSV for further analysis
    
    **Supported file formats:** Excel (.xlsx, .xls), CSV (.csv)
    **Languages:** English, Bahasa Indonesia, 中文 (Chinese)
    """)
