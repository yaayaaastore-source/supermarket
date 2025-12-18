import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Supermarket",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Dashboard Analisis Supermarket</h1>', unsafe_allow_html=True)

# Sidebar untuk filter
with st.sidebar:
    st.header("⚙️ Pengaturan Filter")
    
    # Generate data dummy jika tidak ada data
    @st.cache_data
    def generate_sample_data():
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        categories = ['Makanan', 'Minuman', 'Elektronik', 'Pakaian', 'Rumah Tangga']
        products = {
            'Makanan': ['Roti', 'Susu', 'Telur', 'Daging', 'Sayuran'],
            'Minuman': ['Air Mineral', 'Jus', 'Kopi', 'Teh', 'Soda'],
            'Elektronik': ['Charger', 'Headphone', 'Kabel', 'Baterai', 'Adapter'],
            'Pakaian': ['Kaos', 'Celana', 'Jaket', 'Topi', 'Sepatu'],
            'Rumah Tangga': ['Sabun', 'Pasta Gigi', 'Shampoo', 'Sapu', 'Pel']
        }
        
        data = []
        for date in dates:
            for category in categories:
                for product in products[category][:3]:  # Ambil 3 produk per kategori
                    quantity = np.random.randint(1, 50)
                    price = np.random.uniform(1000, 500000)
                    revenue = quantity * price
                    profit = revenue * np.random.uniform(0.1, 0.4)
                    
                    data.append({
                        'Tanggal': date,
                        'Kategori': category,
                        'Produk': product,
                        'Jumlah': quantity,
                        'Harga': price,
                        'Pendapatan': revenue,
                        'Profit': profit,
                        'Bulan': date.strftime('%B'),
                        'Hari': date.strftime('%A')
                    })
        
        return pd.DataFrame(data)
    
    df = generate_sample_data()
    
    # Filter berdasarkan tanggal
    min_date = df['Tanggal'].min().date()
    max_date = df['Tanggal'].max().date()
    
    date_range = st.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['Tanggal'].dt.date >= start_date) & (df['Tanggal'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    # Filter kategori
    categories = st.multiselect(
        "Pilih Kategori",
        options=df['Kategori'].unique(),
        default=df['Kategori'].unique()
    )
    
    if categories:
        df_filtered = df_filtered[df_filtered['Kategori'].isin(categories)]
    
    # Filter produk
    selected_products = st.multiselect(
        "Pilih Produk (Opsional)",
        options=df_filtered['Produk'].unique()
    )
    
    if selected_products:
        df_filtered = df_filtered[df_filtered['Produk'].isin(selected_products)]

# Bagian utama dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Kategori", "🛍️ Produk", "📅 Time Series"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df_filtered['Pendapatan'].sum()
        st.metric(
            label="Total Pendapatan",
            value=f"Rp {total_revenue:,.0f}",
            delta=f"Rp {total_revenue * 0.05:,.0f}"
        )
    
    with col2:
        total_profit = df_filtered['Profit'].sum()
        st.metric(
            label="Total Profit",
            value=f"Rp {total_profit:,.0f}",
            delta=f"Rp {total_profit * 0.03:,.0f}"
        )
    
    with col3:
        total_transactions = len(df_filtered)
        st.metric(
            label="Total Transaksi",
            value=f"{total_transactions:,}",
            delta=f"{int(total_transactions * 0.02):,}"
        )
    
    with col4:
        avg_transaction = df_filtered['Pendapatan'].mean()
        st.metric(
            label="Rata-rata Transaksi",
            value=f"Rp {avg_transaction:,.0f}",
            delta=f"Rp {avg_transaction * 0.01:,.0f}"
        )
    
    # Grafik Pendapatan per Kategori
    st.subheader("Pendapatan per Kategori")
    revenue_by_category = df_filtered.groupby('Kategori')['Pendapatan'].sum().reset_index()
    
    fig1 = go.Figure(data=[
        go.Bar(
            x=revenue_by_category['Kategori'],
            y=revenue_by_category['Pendapatan'],
            marker_color=['#1E3A8A', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE'],
            text=[f"Rp {x:,.0f}" for x in revenue_by_category['Pendapatan']],
            textposition='auto'
        )
    ])
    
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Pendapatan (Rp)",
        xaxis_title="Kategori",
        height=400
    )
    
    # FIXED: Menggunakan st.plotly_chart dengan parameter yang benar
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Kategori")
        
        # Pie chart untuk kategori
        category_dist = df_filtered['Kategori'].value_counts().reset_index()
        category_dist.columns = ['Kategori', 'Jumlah']
        
        fig2 = px.pie(
            category_dist,
            values='Jumlah',
            names='Kategori',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("Profit Margin per Kategori")
        
        profit_margin = df_filtered.groupby('Kategori').agg({
            'Pendapatan': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        profit_margin['Margin'] = (profit_margin['Profit'] / profit_margin['Pendapatan']) * 100
        
        fig3 = go.Figure(data=[
            go.Bar(
                x=profit_margin['Kategori'],
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
            xaxis_title="Kategori",
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Top 10 Produk Terlaris")
    
    top_products = df_filtered.groupby('Produk').agg({
        'Jumlah': 'sum',
        'Pendapatan': 'sum'
    }).nlargest(10, 'Pendapatan').reset_index()
    
    fig4 = go.Figure(data=[
        go.Bar(
            y=top_products['Produk'],
            x=top_products['Pendapatan'],
            orientation='h',
            marker_color='#3B82F6',
            text=[f"Rp {x:,.0f}" for x in top_products['Pendapatan']],
            textposition='auto'
        )
    ])
    
    fig4.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Pendapatan (Rp)",
        yaxis_title="Produk",
        height=500
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # Tabel detail produk
    st.subheader("Detail Produk")
    product_detail = df_filtered.groupby(['Kategori', 'Produk']).agg({
        'Jumlah': 'sum',
        'Pendapatan': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    product_detail['Profit Margin'] = (product_detail['Profit'] / product_detail['Pendapatan'] * 100).round(2)
    
    # Format angka
    product_detail['Pendapatan'] = product_detail['Pendapatan'].apply(lambda x: f"Rp {x:,.0f}")
    product_detail['Profit'] = product_detail['Profit'].apply(lambda x: f"Rp {x:,.0f}")
    product_detail['Profit Margin'] = product_detail['Profit Margin'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        product_detail,
        column_config={
            "Kategori": "Kategori",
            "Produk": "Produk",
            "Jumlah": "Jumlah Terjual",
            "Pendapatan": "Total Pendapatan",
            "Profit": "Total Profit",
            "Profit Margin": "Profit Margin"
        },
        use_container_width=True
    )

with tab4:
    st.subheader("Trend Pendapatan Harian")
    
    # Data time series
    daily_revenue = df_filtered.groupby('Tanggal')['Pendapatan'].sum().reset_index()
    
    fig5 = go.Figure()
    
    fig5.add_trace(go.Scatter(
        x=daily_revenue['Tanggal'],
        y=daily_revenue['Pendapatan'],
        mode='lines+markers',
        name='Pendapatan',
        line=dict(color='#3B82F6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    fig5.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Pendapatan (Rp)",
        xaxis_title="Tanggal",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pendapatan per Bulan")
        monthly_revenue = df_filtered.groupby('Bulan')['Pendapatan'].sum().reset_index()
        
        # Urutkan bulan
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_revenue['Bulan'] = pd.Categorical(monthly_revenue['Bulan'], categories=month_order, ordered=True)
        monthly_revenue = monthly_revenue.sort_values('Bulan')
        
        fig6 = px.bar(
            monthly_revenue,
            x='Bulan',
            y='Pendapatan',
            color='Pendapatan',
            color_continuous_scale='Blues'
        )
        
        fig6.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        st.subheader("Pendapatan per Hari")
        daily_avg = df_filtered.groupby('Hari')['Pendapatan'].mean().reset_index()
        
        # Urutkan hari
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_avg['Hari'] = pd.Categorical(daily_avg['Hari'], categories=day_order, ordered=True)
        daily_avg = daily_avg.sort_values('Hari')
        
        fig7 = px.line(
            daily_avg,
            x='Hari',
            y='Pendapatan',
            markers=True,
            line_shape='spline'
        )
        
        fig7.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig7, use_container_width=True)

# Bagian bawah: Download data
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("📥 Ekspor Data")
    
    # Konversi dataframe ke CSV
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Data Filtered (CSV)",
        data=csv,
        file_name=f"supermarket_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6B7280;'>
        Dashboard Supermarket Analytics • Dibuat dengan Streamlit dan Plotly • 
        Data diperbarui: {date}
    </div>
    """.format(date=datetime.now().strftime("%d %B %Y %H:%M")),
    unsafe_allow_html=True
)

# Debug info (bisa dihilangkan di production)
with st.expander("ℹ️ Info Debug"):
    st.write(f"Jumlah baris data: {len(df_filtered):,}")
    st.write(f"Rentang tanggal: {df_filtered['Tanggal'].min().date()} hingga {df_filtered['Tanggal'].max().date()}")
    st.write(f"Kategori aktif: {', '.join(df_filtered['Kategori'].unique())}")
