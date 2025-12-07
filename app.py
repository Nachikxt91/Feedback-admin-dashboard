import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
import plotly.graph_objects as go


# ==================== CONFIGURATION ====================
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")


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


def filter_feedbacks(feedbacks, rating_filter, sentiment_filter, search_query):
    """Apply filters to feedback list"""
    return [
        fb for fb in feedbacks
        if fb["rating"] in rating_filter
        and normalize_sentiment(fb) in sentiment_filter
        and (not search_query or 
             search_query.lower() in fb.get("review", "").lower() or
             search_query.lower() in fb.get("ai_summary", "").lower())
    ]


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
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        letter-spacing: 0.1em;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        font-size: 0.8rem;
        color: #00ffff;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-bottom: 2rem;
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
    """Render interactive charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">RATING DISTRIBUTION</div>', unsafe_allow_html=True)
        rating_dist = analytics.get("rating_distribution", {})
        
        if rating_dist:
            ratings = list(map(int, rating_dist.keys()))
            counts = list(rating_dist.values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=counts + [counts[0]],
                theta=[f'{r} STARS' for r in ratings] + [f'{ratings[0]} STARS'],
                fill='toself',
                fillcolor='rgba(0, 255, 255, 0.2)',
                line=dict(color='#00ffff', width=2)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, showline=False, showticklabels=False),
                    bgcolor='rgba(15, 15, 35, 0.6)'
                ),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown('<div class="section-title">SENTIMENT ANALYSIS</div>', unsafe_allow_html=True)
        sentiment_data = analytics.get("sentiment_breakdown", {})
        
        if sentiment_data:
            total_fb = analytics.get("total_feedback", 1)
            positive_rate = (sentiment_data.get("Positive", 0) / total_fb) * 100
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=positive_rate,
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "#00ffff"},
                    'bar': {'color': "#00ffff"},
                    'bgcolor': "rgba(15, 15, 35, 0.6)",
                    'bordercolor': "#00ffff",
                    'steps': [
                        {'range': [0, 33], 'color': 'rgba(255, 0, 0, 0.3)'},
                        {'range': [33, 66], 'color': 'rgba(255, 255, 0, 0.3)'},
                        {'range': [66, 100], 'color': 'rgba(0, 255, 0, 0.3)'}
                    ]
                }
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ffffff", 'family': "JetBrains Mono"}
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_filters():
    """Render filter panel and return filter values"""
    col1, col2, col3, col4 = st.columns(4)
    
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
        date_range = st.date_input(
            "DATE RANGE",
            value=(datetime.now().date(), datetime.now().date()),
            key="date_range",
            label_visibility="visible"
        )
    
    with col4:
        search_query = st.text_input(
            "SEARCH",
            placeholder="ENTER KEYWORDS...",
            key="search_filter",
            label_visibility="visible"
        )
    
    return rating_filter, sentiment_filter, search_query


def render_feedback_item(feedback, idx):
    """Render individual feedback item"""
    sentiment = normalize_sentiment(feedback)
    sentiment_colors = {
        "Positive": "#00ff00",
        "Neutral": "#ffff00",
        "Negative": "#ff0000",
        "Unknown": "#888888"
    }
    
    rating_display = f"{feedback['rating']} STARS"
    
    with st.expander(
        f"[ {rating_display} ] {sentiment.upper()} • {feedback['created_at'][:10]}",
        expanded=False
    ):
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
            
            sentiment_color = sentiment_colors.get(sentiment, "#888888")
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
        <div style="border-bottom: 1px solid rgba(0, 255, 255, 0.3); padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <div style="font-size: 1rem; font-weight: 700; color: #00ffff;">CONTROL PANEL</div>
            <div style="font-size: 0.7rem; color: #888;">SYSTEM CONFIGURATION</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("SYSTEM SETTINGS", expanded=False):
            auto_refresh = st.toggle(
                "AUTO-REFRESH",
                value=False,
                key="auto_refresh_toggle"
            )
            if auto_refresh:
                st.slider(
                    "REFRESH RATE (SECONDS)",
                    min_value=10,
                    max_value=300,
                    value=60,
                    key="refresh_rate_slider"
                )
            st.slider(
                "MAX RECORDS",
                min_value=50,
                max_value=1000,
                value=100,
                key="max_records_slider"
            )
        
        st.markdown("---")
        
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
        api_key_input = st.text_input(
            "API Key",
            type="password",
            placeholder="ENTER ACCESS KEY",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("AUTHENTICATE", type="primary", use_container_width=True):
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
    
    # FAB button
    st.markdown("""
    <button class="cyber-fab" onclick="window.location.reload()" title="SYNC DATA">↻</button>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div class="section-title">FEEDBACK STREAM</div>', unsafe_allow_html=True)
    
    feedbacks = fetch_feedbacks()
    if feedbacks:
        feedbacks = sorted(feedbacks, key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Filters
        rating_filter, sentiment_filter, search_query = render_filters()
        
        # Apply filters
        filtered_feedbacks = filter_feedbacks(feedbacks, rating_filter, sentiment_filter, search_query)
        
        # Stats bar
        st.markdown(f"""
        <div class="stats-bar">
            <div class="stats-label">DISPLAYING <span class="stats-value">{len(filtered_feedbacks)}</span> OF <span class="stats-value">{len(feedbacks)}</span> RECORDS</div>
            <div class="stats-label">STATUS: <span class="stats-value">ACTIVE</span></div>
            <div class="stats-label">UPDATED: <span class="stats-value">{datetime.now().strftime('%H:%M:%S')}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
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
