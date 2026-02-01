import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CUSTOM CSS - DEEP SPACE / CYBERPUNK PROFESSIONAL THEME
# ═══════════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
    /* ══════════════════════════════════════════════════════════════════════════
       GOOGLE FONTS IMPORT
    ══════════════════════════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ══════════════════════════════════════════════════════════════════════════
       ROOT VARIABLES - SYNTHETIX AI COLOR PALETTE
    ══════════════════════════════════════════════════════════════════════════ */
    :root {
        --midnight-blue: #0E1117;
        --slate-gray: #161B22;
        --border-gray: #30363D;
        --electric-blue: #58A6FF;
        --electric-cyan: #79C0FF;
        --success-green: #3FB950;
        --warning-orange: #D29922;
        --error-red: #F85149;
        --text-primary: #E6EDF3;
        --text-secondary: #8B949E;
        --gradient-blue: linear-gradient(135deg, #58A6FF 0%, #79C0FF 50%, #A5D6FF 100%);
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       GLOBAL STYLES
    ══════════════════════════════════════════════════════════════════════════ */
    .stApp {
        background: var(--midnight-blue);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       SIDEBAR STYLING
    ══════════════════════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: var(--slate-gray);
        border-right: 1px solid var(--border-gray);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1 {
        background: var(--gradient-blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       INPUT FIELDS
    ══════════════════════════════════════════════════════════════════════════ */
    .stTextInput > div > div > input {
        background: var(--slate-gray) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--electric-blue) !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       BUTTONS - GRADIENT WITH HOVER ANIMATION
    ══════════════════════════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #58A6FF 0%, #39D5FF 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: #0E1117 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 12px 32px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(88, 166, 255, 0.25) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(88, 166, 255, 0.35) !important;
        background: linear-gradient(135deg, #79C0FF 0%, #58A6FF 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       CUSTOM CARD CONTAINERS
    ══════════════════════════════════════════════════════════════════════════ */
    .custom-card {
        background: var(--slate-gray);
        border: 1px solid var(--border-gray);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        border-color: var(--electric-blue);
        box-shadow: 0 8px 30px rgba(88, 166, 255, 0.1);
    }
    
    .card-title {
        color: var(--electric-blue);
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .card-content {
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       JOB DETAILS CARD
    ══════════════════════════════════════════════════════════════════════════ */
    .job-card {
        background: linear-gradient(135deg, var(--slate-gray) 0%, #1C2128 100%);
        border: 1px solid var(--border-gray);
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
    }
    
    .job-role {
        color: var(--text-primary);
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .job-meta {
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    .skill-tag {
        display: inline-block;
        background: rgba(88, 166, 255, 0.15);
        color: var(--electric-blue);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin: 4px 4px 4px 0;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       EMAIL OUTPUT STYLING
    ══════════════════════════════════════════════════════════════════════════ */
    .email-card {
        background: var(--slate-gray);
        border: 1px solid var(--success-green);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(63, 185, 80, 0.1);
    }
    
    .email-header {
        color: var(--success-green);
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-gray);
    }
    
    .email-content {
        color: var(--text-primary);
        font-size: 15px;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       STATUS INDICATORS
    ══════════════════════════════════════════════════════════════════════════ */
    .stStatus {
        background: var(--slate-gray) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 8px !important;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       METRICS & STATS
    ══════════════════════════════════════════════════════════════════════════ */
    .stat-box {
        background: var(--slate-gray);
        border: 1px solid var(--border-gray);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        margin: 8px 0;
    }
    
    .stat-value {
        color: var(--electric-blue);
        font-size: 28px;
        font-weight: 700;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       CODE BLOCKS
    ══════════════════════════════════════════════════════════════════════════ */
    .stCodeBlock {
        background: var(--midnight-blue) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 8px !important;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       ERROR STYLING
    ══════════════════════════════════════════════════════════════════════════ */
    .stAlert {
        background: rgba(248, 81, 73, 0.1) !important;
        border: 1px solid var(--error-red) !important;
        border-radius: 8px !important;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       SCROLLBAR STYLING
    ══════════════════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--midnight-blue);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-gray);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       DIVIDER
    ══════════════════════════════════════════════════════════════════════════ */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-gray), transparent);
        margin: 24px 0;
    }
    
    /* ══════════════════════════════════════════════════════════════════════════
       HEADER STYLING
    ══════════════════════════════════════════════════════════════════════════ */
    .main-header {
        text-align: center;
        padding: 20px 0 30px 0;
    }
    
    .main-title {
        font-size: 42px;
        font-weight: 700;
        background: var(--gradient-blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .main-subtitle {
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 400;
    }
</style>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 CACHED RESOURCE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_chain():
    """Initialize and cache the LLM Chain for optimal performance."""
    return Chain()

@st.cache_resource
def get_portfolio():
    """Initialize and cache the Portfolio vector store."""
    return Portfolio()

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def render_job_card(job: dict, index: int) -> str:
    """Render a styled job details card."""
    skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in job.get('skills', [])])
    
    return f"""
    <div class="job-card">
        <div class="job-role">📋 {job.get('role', 'Unknown Role')}</div>
        <div class="job-meta">
            <strong>Experience:</strong> {job.get('experience', 'Not specified')}
        </div>
        <div style="margin-bottom: 12px;">
            <strong style="color: #8B949E; font-size: 12px; text-transform: uppercase;">Required Skills</strong>
        </div>
        <div>{skills_html}</div>
        <div class="custom-divider"></div>
        <div style="color: #E6EDF3; font-size: 14px; line-height: 1.6;">
            {job.get('description', '')}
        </div>
    </div>
    """

def render_email_card(email: str, job_role: str) -> str:
    """Render a styled email output card."""
    return f"""
    <div class="email-card">
        <div class="email-header">
            ✉️ Generated Email for: {job_role}
        </div>
        <div class="email-content">{email}</div>
    </div>
    """

def create_streamlit_app():
    """Main Streamlit application with Synthetix AI branding."""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PAGE CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════════
    st.set_page_config(
        page_title="Cold Mail Generator Pro | Synthetix AI",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject Custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize cached resources
    chain = get_chain()
    portfolio = get_portfolio()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SIDEBAR - BRANDING & STATS
    # ═══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("# 🚀 Synthetix AI")
        st.markdown("---")
        
        st.markdown("""
        <div class="stat-box">
            <div class="stat-value">Pro</div>
            <div class="stat-label">Edition</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚡ Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-value">70B</div>
                <div class="stat-label">LLM Model</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-value">&lt;3s</div>
                <div class="stat-label">Gen Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        st.success("✅ LLM Chain: Online")
        st.success("✅ Vector Store: Ready")
        st.success("✅ Web Scraper: Active")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #8B949E; font-size: 12px;">
            <p>Built with ❤️ by</p>
            <p style="color: #58A6FF; font-weight: 600;">Mustafa @ Synthetix AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN CONTENT AREA
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">📧 Cold Mail Generator Pro</div>
        <div class="main-subtitle">AI-Powered Hyper-Personalized Business Outreach</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown("""
    <div class="custom-card">
        <div class="card-title">🔗 Target Job Posting</div>
        <div class="card-content" style="color: #8B949E; margin-bottom: 16px;">
            Enter the URL of a job posting to generate a personalized cold email.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    url_input = st.text_input(
        label="Job URL",
        value="https://careers.nike.com/generative-ai-design-expert/job/R-71324",
        placeholder="https://example.com/careers/job-posting",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.button("🚀 Generate Cold Email", use_container_width=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PROCESSING PIPELINE
    # ═══════════════════════════════════════════════════════════════════════════
    
    if submit_button:
        try:
            with st.status("🔄 Processing your request...", expanded=True) as status:
                
                # Step 1: Web Scraping
                st.write("🌐 **Step 1/4:** Fetching job posting...")
                loader = WebBaseLoader([url_input])
                raw_content = loader.load().pop().page_content
                st.write("✅ Page content retrieved successfully")
                
                # Step 2: Text Cleaning
                st.write("🧹 **Step 2/4:** Cleaning and preprocessing text...")
                cleaned_data = clean_text(raw_content)
                st.write(f"✅ Processed {len(cleaned_data):,} characters")
                
                # Step 3: Job Extraction
                st.write("🧠 **Step 3/4:** Extracting job details with Llama 3.3...")
                portfolio.load_portfolio()
                jobs = chain.extract_jobs(cleaned_data)
                st.write(f"✅ Found {len(jobs)} job posting(s)")
                
                # Step 4: Email Generation
                st.write("✍️ **Step 4/4:** Generating personalized emails...")
                
                status.update(label="✅ Processing complete!", state="complete", expanded=False)
            
            # ═══════════════════════════════════════════════════════════════════
            # RESULTS DISPLAY
            # ═══════════════════════════════════════════════════════════════════
            
            if not jobs:
                st.warning("⚠️ No job postings found on this page. Please try a different URL.")
            else:
                for idx, job in enumerate(jobs):
                    # Display Job Details
                    st.markdown(f"### 📋 Job #{idx + 1} Details")
                    st.markdown(render_job_card(job, idx), unsafe_allow_html=True)
                    
                    # Get relevant portfolio links
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    
                    # Generate and display email
                    with st.spinner("✨ Crafting your personalized email..."):
                        email = chain.write_mail(job, links)
                    
                    st.markdown(f"### ✉️ Generated Email")
                    st.markdown(render_email_card(email, job.get('role', 'Position')), unsafe_allow_html=True)
                    
                    # Copy button
                    st.code(email, language="markdown")
                    
                    if idx < len(jobs) - 1:
                        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                
                # Success message
                st.markdown("""
                <div class="custom-card" style="border-color: #3FB950;">
                    <div class="card-title" style="color: #3FB950;">🎉 Success!</div>
                    <div class="card-content">
                        Your personalized cold email(s) have been generated. 
                        Copy the email above and customize it further if needed.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"❌ **An error occurred:** {str(e)}")
            st.markdown("""
            <div class="custom-card" style="border-color: #F85149;">
                <div class="card-title" style="color: #F85149;">🔧 Troubleshooting Tips</div>
                <div class="card-content">
                    <ul style="color: #E6EDF3;">
                        <li>Verify the URL is accessible and contains a job posting</li>
                        <li>Check your internet connection</li>
                        <li>Ensure your GROQ_API_KEY is set correctly in .env</li>
                        <li>Try refreshing the page and submitting again</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 🏁 ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    create_streamlit_app()
