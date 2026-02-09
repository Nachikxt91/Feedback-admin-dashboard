import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
import plotly.graph_objects as go


# ==================== CONFIGURATION ====================
load_dotenv()
API_URL = st.secrets.get("API_URL", "http://localhost:8000/api")
API_KEY = st.secrets.get("API_KEY", "")


st.set_page_config(
    page_title="ADMIN DASHBOARD",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================== HELPER FUNCTIONS ====================
def fetch_analytics():
    """Fetch analytics data from API"""
    try:
        response = requests.get(
            f"{API_URL}/admin/analytics",
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Analytics fetch error: {str(e)}")
        return None


def fetch_feedbacks(limit=100):
    """Fetch feedback data from API"""
    try:
        response = requests.get(
            f"{API_URL}/admin/feedbacks",
            headers={"X-API-Key": API_KEY},
            params={"limit": limit},
            timeout=30
        )
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Feedback fetch error: {str(e)}")
        return []


def normalize_sentiment(feedback):
    """Extract and normalize sentiment value"""
    return feedback.get("sentiment", "Unknown").rstrip(".")


def filter_feedbacks(feedbacks, rating_filter, sentiment_filter, category_filter, search_query):
    """Apply filters to feedback list"""
    return [
        fb for fb in feedbacks
        if fb["rating"] in rating_filter
        and normalize_sentiment(fb) in sentiment_filter
        and fb.get("category", "General") in category_filter
        and (not search_query or 
             search_query.lower() in fb.get("review", "").lower() or
             search_query.lower() in fb.get("ai_summary", "").lower())
    ]


def export_to_csv(feedbacks, selected_columns):
    """Convert feedback list to CSV format for download with selected columns"""
    if not feedbacks or not selected_columns:
        return None
    
    export_data = []
    for fb in feedbacks:
        row = {}
        if "ID" in selected_columns:
            row["ID"] = fb.get("_id", "")
        if "Rating" in selected_columns:
            row["Rating"] = fb.get("rating", "")
        if "Review" in selected_columns:
            row["Review"] = fb.get("review", "")
        if "Category" in selected_columns:
            row["Category"] = fb.get("category", "General")
        if "Sentiment" in selected_columns:
            row["Sentiment"] = normalize_sentiment(fb)
        if "AI Summary" in selected_columns:
            row["AI Summary"] = fb.get("ai_summary", "")
        if "AI Actions" in selected_columns:
            row["AI Actions"] = fb.get("ai_actions", "")
        if "AI Response" in selected_columns:
            row["AI Response"] = fb.get("ai_response", "")
        if "Created At" in selected_columns:
            row["Created At"] = fb.get("created_at", "")
        export_data.append(row)
    
    df = pd.DataFrame(export_data)
    return df.to_csv(index=False).encode('utf-8')


# ==================== CYBERPUNK THEME ====================
def apply_cyberpunk_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'JetBrains Mono', monospace; }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #0f0f23 100%);
        color: #e5e5e5;
    }
    
    .block-container {
        padding: 2rem 2rem 4rem 2rem;
        max-width: 1600px;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ===== HEADER ===== */
    .dash-header {
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .dash-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.1em;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .dash-subtitle {
        font-size: 0.875rem;
        color: #00ffff;
        letter-spacing: 0.3em;
        text-transform: uppercase;
    }
    
    /* ===== METRICS ===== */
    div[data-testid="stMetric"] {
        background: rgba(15, 15, 35, 0.7);
        border: 1px solid rgba(0, 255, 255, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 255, 255, 0.6);
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
    }
    
    div[data-testid="stMetric"] label {
        color: #888 !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* ===== DIVIDERS ===== */
    .neon-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffff, #ff00ff, transparent);
        margin: 2.5rem 0;
        opacity: 0.5;
    }
    
    .section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 1.5rem;
        padding-left: 1rem;
        border-left: 3px solid #ff00ff;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        padding: 1.25rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #e5e5e5 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 255, 255, 0.5) !important;
        transform: translateX(8px);
    }
    
    .streamlit-expanderContent {
        background: rgba(10, 10, 25, 0.9) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1.75rem !important;
        backdrop-filter: blur(10px);
    }
    
    /* ===== MULTISELECT ===== */
    .stMultiSelect > div > div {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(0, 255, 255, 0.15) !important;
        color: #00ffff !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 6px !important;
    }
    
    /* ===== INPUT ===== */
    input {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 0.875rem 1.25rem !important;
        backdrop-filter: blur(10px);
    }
    
    input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.15) !important;
    }
    
    /* ===== INFO BOXES ===== */
    .stInfo, .stWarning, .stError {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        border-left: 3px solid #00ffff !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px);
    }
    
    /* ===== CONTENT BOX ===== */
    .content-box {
        background: rgba(15, 15, 35, 0.9);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
        line-height: 1.7;
    }
    
    .terminal-box {
        background: rgba(0, 0, 0, 0.6);
        border-left: 3px solid #00ff00;
        border-radius: 6px;
        padding: 1rem;
        color: #00ff00;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    
    /* ===== STATS BAR ===== */
    .stats-bar {
        display: flex;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: rgba(15, 15, 35, 0.7);
        border: 1px solid rgba(0, 255, 255, 0.25);
        border-radius: 12px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .stats-label {
        font-size: 0.8rem;
        color: #888;
    }
    
    .stats-value {
        font-weight: 700;
        color: #00ffff;
        margin-left: 0.5rem;
    }
    
    /* ===== FAB ===== */
    .cyber-fab {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 9999;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        border: none;
        color: #000;
        font-size: 1.75rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .cyber-fab:hover {
        transform: rotate(360deg) scale(1.15);
        box-shadow: 0 0 50px rgba(0, 255, 255, 0.6);
    }
    
    /* ===== AUTH SCREEN ===== */
    .auth-card {
        background: rgba(15, 15, 35, 0.95);
        border: 1px solid rgba(0, 255, 255, 0.4);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        max-width: 480px;
        margin: 10rem auto;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }
    
    .auth-title {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        letter-spacing: 0.1em;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        font-size: clamp(0.65rem, 2vw, 0.8rem);
        color: #00ffff;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-bottom: 2rem;
    }
    
    /* ===== RESPONSIVE BREAKPOINTS ===== */
    
    /* Tablets and below */
    @media (max-width: 1024px) {
        .block-container {
            padding: 1.5rem 1.5rem 3rem 1.5rem !important;
        }
        
        .dash-title {
            font-size: clamp(1.5rem, 4vw, 2.5rem) !important;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }
        
        .stats-bar {
            flex-wrap: wrap;
            gap: 0.75rem;
        }
    }
    
    /* Mobile phones */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2rem 1rem !important;
        }
        
        .dash-header {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
        }
        
        .dash-title {
            font-size: 1.5rem !important;
        }
        
        .dash-subtitle {
            font-size: 0.7rem !important;
            letter-spacing: 0.15em !important;
        }
        
        div[data-testid="stMetric"] {
            padding: 1rem !important;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        div[data-testid="stMetric"] label {
            font-size: 0.6rem !important;
        }
        
        .section-title {
            font-size: 0.75rem !important;
            padding-left: 0.75rem;
        }
        
        .stats-bar {
            flex-direction: column;
            gap: 0.5rem;
            padding: 1rem;
        }
        
        .content-box, .terminal-box {
            padding: 0.75rem;
            font-size: 0.8rem;
        }
        
        .streamlit-expanderHeader {
            padding: 1rem !important;
            font-size: 0.75rem !important;
        }
        
        .streamlit-expanderContent {
            padding: 1rem !important;
        }
        
        .auth-card {
            margin: 3rem 1rem;
            padding: 2rem 1.5rem;
        }
        
        .cyber-fab {
            width: 50px;
            height: 50px;
            font-size: 1.25rem;
            bottom: 1rem;
            right: 1rem;
        }
    }
    
    /* Small phones */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.75rem 0.75rem 1.5rem 0.75rem !important;
        }
        
        .dash-title {
            font-size: 1.25rem !important;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== UI COMPONENTS ====================
def render_header():
    """Render dashboard header"""
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("""
        <div class="dash-header">
            <div class="dash-title">ADMIN</div>
            <div class="dash-subtitle">Real-Time Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Use a container that updates with each rerun
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"""
        <div style="text-align: right; padding-top: 1rem;">
            <div style="font-size: 0.7rem; color: #888; letter-spacing: 0.1em;">SYSTEM TIME</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #00ffff; margin-top: 0.2rem;">
                {current_time}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_metrics(analytics):
    """Render metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    total_fb = analytics.get("total_feedback", 0)
    avg_rating = analytics.get("average_rating", 0)
    sentiment_data = analytics.get("sentiment_breakdown", {})
    positive_count = sentiment_data.get("Positive", 0)
    positive_rate = (positive_count / max(1, total_fb)) * 100
    
    with col1:
        st.metric("TOTAL FEEDBACK", total_fb, delta="+3.2%" if total_fb > 0 else None)
    
    with col2:
        trend = "↑" if avg_rating > 3.5 else "↓" if avg_rating < 3 else "→"
        st.metric("AVG RATING", f"{avg_rating:.1f}", delta=trend)
    
    with col3:
        st.metric("POSITIVE RATE", f"{positive_rate:.1f}%", delta="+2.1%")
    
    with col4:
        latest = analytics.get("latest_submission")
        if latest:
            latest_date = datetime.fromisoformat(latest.replace("Z", "+00:00"))
            time_diff = (datetime.now() - latest_date).seconds // 60
            st.metric("LAST SYNC", f"{time_diff}m", delta="LIVE")
        else:
            st.metric("LAST SYNC", "—", delta="OFFLINE")


def render_charts(analytics):
    """Render interactive charts with improved visuals"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">⭐ RATING DISTRIBUTION</div>', unsafe_allow_html=True)
        rating_dist = analytics.get("rating_distribution", {})
        
        if rating_dist and any(rating_dist.values()):
            # Create bar chart instead of radar for better clarity
            ratings = [str(i) for i in range(1, 6)]
            counts = [rating_dist.get(str(i), 0) for i in range(1, 6)]
            
            # Gradient colors from red to green
            colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e']
            
            fig = go.Figure(go.Bar(
                x=ratings,
                y=counts,
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(255,255,255,0.2)', width=1)
                ),
                text=counts,
                textposition='outside',
                textfont=dict(color='#ffffff', size=14, family='JetBrains Mono')
            ))
            
            fig.update_layout(
                height=280,
                margin=dict(l=40, r=20, t=30, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 15, 35, 0.4)',
                font={'color': "#888", 'family': "JetBrains Mono"},
                xaxis=dict(
                    title="Stars",
                    showgrid=False,
                    tickfont=dict(color='#00ffff', size=12)
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0, 255, 255, 0.1)',
                    tickfont=dict(color='#888')
                ),
                bargap=0.3
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No rating data available yet")
    
    with col2:
        st.markdown('<div class="section-title">💭 SENTIMENT BREAKDOWN</div>', unsafe_allow_html=True)
        sentiment_data = analytics.get("sentiment_breakdown", {})
        
        if sentiment_data and any(sentiment_data.values()):
            # Pie/Donut chart for sentiment
            labels = list(sentiment_data.keys())
            values = list(sentiment_data.values())
            
            # Sentiment colors
            color_map = {
                'Positive': '#22c55e',
                'Neutral': '#eab308', 
                'Negative': '#ef4444',
                'Unknown': '#6b7280'
            }
            colors = [color_map.get(l, '#6b7280') for l in labels]
            
            fig = go.Figure(go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color='#1a1a2e', width=2)),
                textinfo='label+percent',
                textfont=dict(color='#ffffff', size=11, family='JetBrains Mono'),
                hovertemplate='%{label}: %{value} (%{percent})<extra></extra>'
            ))
            
            fig.update_layout(
                height=280,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ffffff", 'family': "JetBrains Mono"},
                showlegend=False,
                annotations=[dict(
                    text=f"{sum(values)}<br>Total",
                    x=0.5, y=0.5,
                    font=dict(size=18, color='#00ffff', family='JetBrains Mono'),
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No sentiment data available yet")
    
    # Category Distribution Chart
    st.markdown('<div class="section-title">📂 CATEGORY BREAKDOWN</div>', unsafe_allow_html=True)
    category_data = analytics.get("category_distribution", {})
    
    if category_data and any(category_data.values()):
        categories = list(category_data.keys())
        cat_counts = list(category_data.values())
        
        # Modern gradient colors
        cat_colors = {
            "General": "#6366f1",      # Indigo
            "Bug Report": "#ef4444",   # Red
            "Feature Request": "#22c55e",  # Green
            "Praise": "#f59e0b",       # Amber
            "Complaint": "#f97316",    # Orange
            "Suggestion": "#8b5cf6"    # Purple
        }
        colors = [cat_colors.get(cat, "#6b7280") for cat in categories]
        
        fig = go.Figure(go.Bar(
            x=categories,
            y=cat_counts,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.1)', width=1)
            ),
            text=cat_counts,
            textposition='outside',
            textfont=dict(color='#ffffff', size=12, family='JetBrains Mono')
        ))
        
        fig.update_layout(
            height=220,
            margin=dict(l=40, r=20, t=20, b=60),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 15, 35, 0.4)',
            font={'color': "#888", 'family': "JetBrains Mono"},
            xaxis=dict(
                showgrid=False,
                tickangle=-30,
                tickfont=dict(color='#00ffff', size=10)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0, 255, 255, 0.08)',
                tickfont=dict(color='#888')
            ),
            bargap=0.25
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No category data available yet")


# Available categories
CATEGORIES = ["General", "Bug Report", "Feature Request", "Praise", "Complaint", "Suggestion"]

def render_filters():
    """Render filter panel and return filter values"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        rating_filter = st.multiselect(
            "RATING FILTER",
            options=[1, 2, 3, 4, 5],
            default=[1, 2, 3, 4, 5],
            format_func=lambda x: f"{x} STARS",
            key="rating_filter"
        )
    
    with col2:
        sentiment_filter = st.multiselect(
            "SENTIMENT FILTER",
            options=["Positive", "Neutral", "Negative", "Unknown"],
            default=["Positive", "Neutral", "Negative", "Unknown"],
            key="sentiment_filter"
        )
    
    with col3:
        category_filter = st.multiselect(
            "CATEGORY FILTER",
            options=CATEGORIES,
            default=CATEGORIES,
            key="category_filter"
        )
    
    with col4:
        date_range = st.date_input(
            "DATE RANGE",
            value=(datetime.now().date(), datetime.now().date()),
            key="date_range",
            label_visibility="visible"
        )
    
    with col5:
        search_query = st.text_input(
            "SEARCH",
            placeholder="KEYWORDS...",
            key="search_filter",
            label_visibility="visible"
        )
    
    return rating_filter, sentiment_filter, category_filter, search_query


def render_feedback_item(feedback, idx):
    """Render individual feedback item with classification badge"""
    sentiment = normalize_sentiment(feedback)
    category = feedback.get("category", "General")
    sentiment_colors = {
        "Positive": "#22c55e",
        "Neutral": "#eab308",
        "Negative": "#ef4444",
        "Unknown": "#6b7280"
    }
    
    sentiment_color = sentiment_colors.get(sentiment, "#6b7280")
    rating_display = f"{feedback['rating']} STARS"
    
    # Create badge for classification
    classification_badge = f"""
    <span style="background: {sentiment_color}22; color: {sentiment_color}; 
         padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.7rem; 
         font-weight: 600; border: 1px solid {sentiment_color}55; 
         margin-left: 0.5rem; letter-spacing: 0.05em;">
        {sentiment.upper()}
    </span>
    """
    
    with st.expander(
        f"[ {rating_display} ] {category} • {feedback['created_at'][:10]}",
        expanded=False
    ):
        # Add classification badge at the top of expander
        st.markdown(f'<div style="margin-bottom: 1rem;">{classification_badge}</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns([3, 2])
        
        with col_a:
            st.markdown("### ORIGINAL REVIEW")
            st.markdown(f'<div class="terminal-box">{feedback["review"]}</div>', unsafe_allow_html=True)
            
            st.markdown("### AI ANALYSIS")
            summary = feedback.get("ai_summary", "PROCESSING...")
            st.markdown(f'<div class="content-box">{summary}</div>', unsafe_allow_html=True)
        
        with col_b:
            st.markdown("### METADATA")
            
            rating_display_full = "★" * feedback["rating"] + "☆" * (5 - feedback["rating"])
            st.markdown(f'<div style="font-size: 1.2rem; color: #ffff00;">{rating_display_full}</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(0, 255, 0, 0.1); border-left: 3px solid {sentiment_color};
                     padding: 0.75rem; border-radius: 6px; margin: 1rem 0;">
                <div style="font-weight: 600; color: {sentiment_color};">{sentiment.upper()}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### RECOMMENDED ACTIONS")
            actions = feedback.get("ai_actions", "PROCESSING...")
            st.markdown(f'<div class="content-box" style="color: #ffaa00;">{actions}</div>', unsafe_allow_html=True)
        
        st.markdown("### AI RESPONSE")
        ai_response = feedback.get("ai_response", "")
        st.markdown(f'<div class="content-box" style="color: #aaaaaa;">{ai_response}</div>', unsafe_allow_html=True)



def render_sidebar():
    """Render sidebar controls"""
    with st.sidebar:
        st.markdown("""
        <div style="border-bottom: 1px solid rgba(0, 255, 255, 0.3); padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
            <div style="font-size: 1rem; font-weight: 700; color: #00ffff;">CONTROL PANEL</div>
            <div style="font-size: 0.7rem; color: #888;">SYSTEM CONFIGURATION</div>
        </div>
        """, unsafe_allow_html=True)

        
        st.markdown(f"""
        <div style="background: rgba(15, 15, 35, 0.6); border: 1px solid rgba(0, 255, 255, 0.2);
                 border-radius: 8px; padding: 1rem;">
            <div style="font-size: 0.8rem; color: #888; margin-bottom: 0.5rem;">SYSTEM STATUS</div>
            <div style="display: flex; align-items: center;">
                <div style="width: 8px; height: 8px; background: #00ff00; border-radius: 50%; margin-right: 0.5rem;"></div>
                <div style="color: #ffffff;">ONLINE</div>
            </div>
            <div style="font-size: 0.7rem; color: #888; margin-top: 0.5rem;">LAST: {datetime.now().strftime("%H:%M:%S")}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("LOGOUT", use_container_width=True, type="primary", key="logout_button"):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 0.7rem; color: #888;">ADMIN DASHBOARD</div>
            <div style="font-size: 0.6rem; color: #444;">CYBER SYSTEMS</div>
        </div>
        """, unsafe_allow_html=True)


# ==================== AUTHENTICATION ====================
def render_auth_screen():
    """Render authentication screen"""
    st.markdown("""
    <div class="auth-card">
        <div class="auth-title">ADMIN</div>
        <div class="auth-subtitle">Secure Access Terminal</div>
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(0,255,255,0.3), transparent); margin: 1.5rem 0;"></div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        # Use form to enable Enter key submission
        with st.form(key="auth_form", clear_on_submit=False):
            api_key_input = st.text_input(
                "API Key",
                type="password",
                placeholder="ENTER ACCESS KEY",
                label_visibility="collapsed",
                key="api_key_input"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("AUTHENTICATE", type="primary", use_container_width=True)
            
            if submit_button:
                if api_key_input == API_KEY:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED - INVALID CREDENTIALS")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== MAIN APPLICATION ====================
def main():
    """Main application logic"""
    # Apply theme
    apply_cyberpunk_theme()
    
    # Auto-refresh logic (disabled by default for better control)
    if st.session_state.get("authenticated", False):
        try:
            from streamlit_autorefresh import st_autorefresh
            # Only enable if user wants auto-refresh
            enable_autorefresh = st.sidebar.toggle("AUTO-REFRESH", value=False, key="enable_autorefresh")
            if enable_autorefresh:
                # refresh_interval in milliseconds (10s to 300s)
                refresh_rate = st.sidebar.slider("REFRESH RATE (SEC)", 10, 300, 30, key="refresh_rate_slider")
                st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")
        except ImportError:
            st.sidebar.warning("Install 'streamlit-autorefresh' for auto-updates")
            if st.sidebar.button("REFRESH DATA"):
                st.rerun()

    # Manual Refresh Button (Floating style workaround not needed, sidebar has controls)
    # Using sidebar for primary actions to keep UI clean
    
    # Authentication check
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        render_auth_screen()
        st.stop()
    
    # Render main dashboard
    render_header()
    
    # Analytics section
    analytics = fetch_analytics()
    if analytics:
        render_metrics(analytics)
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        render_charts(analytics)
    else:
        st.markdown('<div class="terminal-box">ERROR: FAILED TO CONNECT TO DATA SOURCE</div>', unsafe_allow_html=True)
    
    # Feedback section
    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    
    # Feedback section header with export button
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown('<div class="section-title">FEEDBACK STREAM</div>', unsafe_allow_html=True)
    with col_header2:
        pass  # Export button will be added after feedbacks are fetched
    
    feedbacks = fetch_feedbacks()
    if feedbacks:
        feedbacks = sorted(feedbacks, key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Filters
        rating_filter, sentiment_filter, category_filter, search_query = render_filters()
        
        # Apply filters
        filtered_feedbacks = filter_feedbacks(feedbacks, rating_filter, sentiment_filter, category_filter, search_query)
        
        # Stats bar
        st.markdown(f"""
        <div class="stats-bar">
            <div class="stats-label">DISPLAYING <span class="stats-value">{len(filtered_feedbacks)}</span> OF <span class="stats-value">{len(feedbacks)}</span> RECORDS</div>
            <div class="stats-label">STATUS: <span class="stats-value">ACTIVE</span></div>
            <div class="stats-label">UPDATED: <span class="stats-value">{datetime.now().strftime('%H:%M:%S')}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export section with column selection
        st.markdown("---")
        
        # Column selector (full width for better visibility)
        available_columns = ["ID", "Rating", "Review", "Category", "Sentiment", 
                            "AI Summary", "AI Actions", "AI Response", "Created At"]
        selected_columns = st.multiselect(
            "📋 SELECT COLUMNS TO EXPORT",
            options=available_columns,
            default=["Rating", "Review", "Category", "Sentiment", "Created At"],
            key="export_columns",
            help="Choose which fields to include in your CSV export"
        )
        
        # Export button
        csv_data = export_to_csv(filtered_feedbacks, selected_columns)
        if csv_data and selected_columns:
            st.download_button(
                label="📥 EXPORT REVIEWS",
                data=csv_data,
                file_name=f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="export_button",
                use_container_width=False,
                type="primary"
            )
        elif not selected_columns:
            st.warning("⚠️ Please select at least one column to export")
        
        st.markdown("---")

        

        
        # Render feedback items
        for idx, feedback in enumerate(filtered_feedbacks[:20]):
            render_feedback_item(feedback, idx)
    else:
        st.markdown('<div class="terminal-box">NO FEEDBACK STREAM DETECTED</div>', unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()


# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
