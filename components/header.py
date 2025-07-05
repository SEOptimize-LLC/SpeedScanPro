import streamlit as st

def render_header():
    """Render the application header with 3D effects and credits"""
    # Custom CSS for 3D effects and dark mode
    st.markdown("""
        <style>
        @keyframes rotate {
            from { transform: rotate3d(0, 1, 0, 0deg); }
            to { transform: rotate3d(0, 1, 0, 360deg); }
        }
        
        .earth-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(24, 98, 204, 0.1) 0%, rgba(13, 37, 87, 0.1) 100%);
            z-index: -1;
            animation: rotate 60s linear infinite;
            pointer-events: none;
        }
        
        .title-3d, .section-title {
            font-size: min(3em, 10vw);
            color: #FF4B4B;
            text-shadow: 2px 2px 0px #B83333,
                         4px 4px 0px #982B2B;
            padding: 20px 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            border-radius: 15px;
            margin: 20px;
            text-align: center;
            font-weight: bold;
        }
        .section-title {
            font-size: min(2em, 8vw);
        }
        .credits {
            font-style: italic;
            color: #666;
            margin: 10px 0;
        }
        .features-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
            transform: perspective(1000px) rotateX(5deg);
            transition: transform 0.3s ease;
        }
        .features-box:hover {
            transform: perspective(1000px) rotateX(0deg);
        }
        </style>
        """, unsafe_allow_html=True)

    # Custom CSS for header components
    st.markdown("""
    <style>
    .title-3d {
        text-align: center;
        color: white;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .credits {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .features-box {
        background: rgba(30, 35, 41, 0.75);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    .features-box h3 {
        margin-bottom: 1.5rem;
        color: #FF4B4B;
        text-align: center;
        font-size: 1.5em;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        padding: 0.5rem;
    }
    .feature-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .feature-item:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.1);
    }
    .feature-icon {
        font-size: 1.5em;
        margin-right: 0.75rem;
    }
    .feature-text {
        font-size: 1em;
    }
    .dev-link {
        color: #FF4B4B;
        text-decoration: none;
        transition: color 0.2s;
    }
    .dev-link:hover {
        color: #FF7676;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title with 3D effect
    st.markdown('<h1 class="title-3d">🔍 SEO Audit Tool</h1>', unsafe_allow_html=True)

    # Developer credits
    st.markdown('<p class="credits">Developed with ❤️ by <a href="https://in.linkedin.com/in/amal-alexander-305780131" target="_blank" class="dev-link">Amal Alexander</a></p>', unsafe_allow_html=True)

    # Features in 3D box
    st.markdown("""
    <h2 class="section-title">Features</h2>
    <div class="features-box">
        <div class="feature-grid">
            <div class="feature-item">
                <span class="feature-icon">🚀</span>
                <span class="feature-text">Page Speed Analysis</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📱</span>
                <span class="feature-text">Mobile & Desktop Performance</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🔍</span>
                <span class="feature-text">On-page SEO Analysis</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <span class="feature-text">Downloadable Reports</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")