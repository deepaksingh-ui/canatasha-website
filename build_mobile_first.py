import json
import os
import sys
import io
import shutil

dest_dir = r"C:\Users\deepa\Downloads\Canatasha_Modern_Website"

orig_sag = os.path.join(dest_dir, 'images', 'banner-orig-sag.webp')
target_banner = os.path.join(dest_dir, 'images', 'banner-1.webp')
if os.path.exists(orig_sag):
    shutil.copyfile(orig_sag, target_banner)

with open(os.path.join(dest_dir, "blogs_curated.json"), "r", encoding="utf-8") as f:
    curated_posts = json.load(f)

# Master Stylesheet with Themes, Responsive Team Grid, Google Reviews, and Zero Blur
master_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --ca-primary: #006B63;
    --ca-secondary: #002e5b;
    --ca-accent: #fde428;
    --ca-dark: #0f172a;
    --ca-light: #f8fafc;
    --ca-easing: cubic-bezier(0.16, 1, 0.3, 1);
    --ca-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ==========================================================================
   THEME VARIATIONS: 1. CLASSIC EMERALD (DEFAULT), 2. EXECUTIVE B&W, 3. CORPORATE SLATE GREY
   ========================================================================== */
body.theme-bw {
    --ca-primary: #18181b !important;
    --ca-secondary: #000000 !important;
    --ca-accent: #f5f5f5 !important;
    --ca-dark: #09090b !important;
    --ca-light: #f4f4f5 !important;
}
body.theme-bw .header-main.bg-green { background: #000000 !important; border-bottom-color: #27272a !important; }
body.theme-bw .header-main.white:before { background: #ffffff !important; }
body.theme-bw .header-main.white:after { background: #ffffff !important; border-right-color: #18181b !important; }
body.theme-bw .top-bar-custom { background: #09090b !important; color: #d4d4d8 !important; }
body.theme-bw .top-bar-custom a { color: #d4d4d8 !important; }
body.theme-bw .top-bar-custom a:hover { color: #ffffff !important; }
body.theme-bw .quote-btn button { background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; }
body.theme-bw .quote-btn button:hover { background: #d4d4d8 !important; color: #000000 !important; }
body.theme-bw .text-content h1.title { color: #ffffff !important; }
body.theme-bw .text-content h3.sub-title { color: #ffffff !important; }
body.theme-bw .service-badge { background: #f4f4f5 !important; color: #18181b !important; border-color: #e4e4e7 !important; }
body.theme-bw .navbar-nav > li:hover > a, body.theme-bw .navbar-nav > li.active > a { color: #18181b !important; }
body.theme-bw .navbar-nav > li > a:after { background: #18181b !important; }
body.theme-bw #scroll-progress-bar { background: linear-gradient(90deg, #18181b 0%, #a1a1aa 50%, #000000 100%) !important; }
body.theme-bw #trusted-stats-section { background: linear-gradient(135deg, #09090b 0%, #27272a 100%) !important; }
body.theme-bw .btn-ca-primary, body.theme-bw .theme-btn:hover { background: #18181b !important; border-color: #18181b !important; color: #ffffff !important; }
body.theme-bw .badge-success { background-color: #18181b !important; }
body.theme-bw .text-success { color: #18181b !important; }
body.theme-bw .page-banner { background: linear-gradient(135deg, #09090b 0%, #27272a 100%) !important; }
body.theme-bw .modal-header { background: #18181b !important; }
body.theme-bw .sticky-action-btn.consult-btn { background: #18181b !important; }
body.theme-bw table thead { background-color: #18181b !important; }
body.theme-bw .footer { background: #09090b !important; }
body.theme-bw .banner-btn, body.theme-bw .theme-btn { border-color: #ffffff !important; background: #ffffff !important; color: #000000 !important; }

body.theme-grey {
    --ca-primary: #334155 !important;
    --ca-secondary: #1e293b !important;
    --ca-accent: #38bdf8 !important;
    --ca-dark: #0f172a !important;
    --ca-light: #f1f5f9 !important;
}
body.theme-grey .header-main.bg-green { background: #1e293b !important; border-bottom-color: #334155 !important; }
body.theme-grey .header-main.white:before { background: #ffffff !important; }
body.theme-grey .header-main.white:after { background: #ffffff !important; border-right-color: #38bdf8 !important; }
body.theme-grey .top-bar-custom { background: #0f172a !important; color: #e2e8f0 !important; }
body.theme-grey .top-bar-custom a { color: #e2e8f0 !important; }
body.theme-grey .top-bar-custom a:hover { color: #38bdf8 !important; }
body.theme-grey .quote-btn button { background: #38bdf8 !important; color: #0f172a !important; font-weight: 800 !important; }
body.theme-grey .quote-btn button:hover { background: #ffffff !important; color: #1e293b !important; box-shadow: 0 8px 20px rgba(56,189,248,0.4) !important; }
body.theme-grey .text-content h1.title { color: #ffffff !important; }
body.theme-grey .text-content h3.sub-title { color: #38bdf8 !important; }
body.theme-grey .service-badge { background: #e2e8f0 !important; color: #1e293b !important; border-color: #cbd5e1 !important; }
body.theme-grey .navbar-nav > li:hover > a, body.theme-grey .navbar-nav > li.active > a { color: #0284c7 !important; }
body.theme-grey .navbar-nav > li > a:after { background: #0284c7 !important; }
body.theme-grey #scroll-progress-bar { background: linear-gradient(90deg, #334155 0%, #38bdf8 50%, #0f172a 100%) !important; }
body.theme-grey #trusted-stats-section { background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important; }
body.theme-grey .btn-ca-primary, body.theme-grey .theme-btn:hover { background: #1e293b !important; border-color: #1e293b !important; color: #ffffff !important; }
body.theme-grey .badge-success { background-color: #334155 !important; }
body.theme-grey .text-success { color: #0284c7 !important; }
body.theme-grey .page-banner { background: linear-gradient(135deg, #0f172a 0%, #334155 100%) !important; }
body.theme-grey .modal-header { background: #334155 !important; }
body.theme-grey .sticky-action-btn.consult-btn { background: #334155 !important; }
body.theme-grey table thead { background-color: #334155 !important; }
body.theme-grey .footer { background: #0f172a !important; }
body.theme-grey .banner-btn, body.theme-grey .theme-btn { border-color: #38bdf8 !important; background: #38bdf8 !important; color: #0f172a !important; }

/* THEME SWITCHER CONTROLS */
.theme-switcher-top {
    display: inline-flex;
    align-items: center;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    padding: 2px 6px;
    border-radius: 20px;
    margin-left: 12px;
}
.theme-switch-btn {
    transition: all 0.25s ease;
    cursor: pointer;
}
.theme-switch-btn.active {
    background: #002e5b !important;
    color: #ffffff !important;
    border-color: #002e5b !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.18) !important;
}
body.theme-bw .theme-switch-btn.active {
    background: #000000 !important;
    color: #ffffff !important;
    border-color: #000000 !important;
}
body.theme-grey .theme-switch-btn.active {
    background: #1e293b !important;
    color: #ffffff !important;
    border-color: #1e293b !important;
}

/* STICKY MOBILE BOTTOM ACTION BAR */
.mobile-sticky-action-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #ffffff;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 6px 8px;
    z-index: 99998;
    box-shadow: 0 -3px 12px rgba(0,0,0,0.08);
}
.sticky-action-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    font-size: 11px;
    font-weight: 700;
    padding: 5px 0;
    border-radius: 6px;
    margin: 0 3px;
    transition: 0.2s ease;
}
.sticky-action-btn i { font-size: 16px; margin-bottom: 2px; }
.sticky-action-btn.call-btn { color: #002e5b; background: #f1f5f9; }
.sticky-action-btn.wa-btn { color: #ffffff; background: #25D366; }
.sticky-action-btn.consult-btn { color: #ffffff; background: var(--ca-primary, #006B63); }

/* TRUST BADGES */
.trust-badge-pill {
    display: inline-flex;
    align-items: center;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    margin-right: 8px;
}

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
}

body {
    font-family: 'Poppins', sans-serif;
    color: #334155;
    background: #ffffff;
    overflow-x: hidden;
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
}

@media (max-width: 767px) {
    body {
        padding-bottom: 60px;
    }
}

/* SCROLL PROGRESS BAR */
#scroll-progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3.5px;
    width: 0%;
    background: linear-gradient(90deg, #006B63 0%, #fde428 50%, #002e5b 100%);
    z-index: 9999999;
    transition: width 0.08s linear;
}

/* TOP BAR */
.top-bar-custom {
    background: #111a24;
    color: #d1e3ff;
    padding: 8px 0;
    font-size: 13px;
}
.top-bar-custom a {
    color: #d1e3ff;
    margin-right: 14px;
    text-decoration: none;
    transition: 0.3s;
}
.top-bar-custom a:hover {
    color: #00a896;
}
.social-icons-top a {
    color: #d1e3ff;
    margin-left: 8px;
    font-size: 13.5px;
    transition: 0.3s;
}
.social-icons-top a:hover {
    color: #00a896;
}

/* HEADER */
.header {
    position: relative;
    z-index: 101;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.header-main.bg-green {
    background: #006B63 !important;
    position: relative;
    overflow: hidden;
}
.header-main.white:before {
    background: #ffffff;
    content: "";
    height: 100%;
    left: -40px;
    position: absolute;
    transform: skewX(39deg);
    width: 38%;
    z-index: 1;
}
.header-main.white:after {
    background: #ffffff;
    border-right: 14px solid #fde428;
    content: "";
    height: 100%;
    left: 33.5%;
    position: absolute;
    top: 0;
    transform: skewX(39deg);
    width: 70px;
    z-index: 1;
}
.header-main .container-fluid {
    padding-left: 45px;
    padding-right: 45px;
}
.header-main-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    min-height: 84px;
    position: relative;
    z-index: 2;
}
.logo-wrapper {
    width: 32%;
    position: relative;
    z-index: 5;
}
.logo {
    padding: 14px 0;
    display: flex;
    align-items: center;
}
.logo img {
    height: 54px;
    width: auto;
    max-width: 100%;
    object-fit: contain;
    display: block;
}
.header-main-content {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 48%;
    padding-right: 15px;
}
.header-info {
    display: flex;
    align-items: center;
    margin-left: 22px;
}
.header-info img {
    height: 34px;
    width: 34px;
    margin-right: 9px;
}
.header-info-text h4 {
    color: #ffffff;
    font-size: 15.5px;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
}
.header-info-text span {
    color: rgba(255,255,255,0.85);
    font-size: 12px;
}

/* QUOTE BUTTON */
.quote-btn button {
    background: #fde428 !important;
    color: #002e5b !important;
    border: none;
    font-size: 14px;
    font-weight: 800;
    line-height: 42px;
    padding: 0 24px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.quote-btn button:hover {
    background: #ffffff !important;
    color: #006B63 !important;
    box-shadow: 0 6px 18px rgba(253, 228, 40, 0.4);
}

/* NAVBAR */
.mainmenu-area {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    width: 100%;
    background: rgba(245, 245, 245, 0.94);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 99;
    display: block;
    border-bottom: 1px solid rgba(0, 46, 91, 0.12);
}
.navbar {
    padding: 0;
    background: transparent !important;
    width: 100%;
}
.navbar-nav {
    display: flex;
    align-items: center;
    margin: 0;
    padding: 0;
}
.navbar-nav > li > a {
    color: #002e5b;
    font-size: 15px;
    font-weight: 700;
    padding: 0 22px;
    line-height: 52px;
    display: block;
    transition: 0.25s ease;
    text-decoration: none;
    position: relative;
}
.navbar-nav > li:first-child > a {
    padding-left: 0 !important;
}
.navbar-nav > li > a:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 22px;
    right: 22px;
    height: 3.5px;
    background: #006B63;
    transform: scaleX(0);
    transition: transform 0.25s var(--ca-easing);
}
.navbar-nav > li:first-child > a:after {
    left: 0 !important;
    right: 22px !important;
}
.navbar-nav > li:hover > a:after,
.navbar-nav > li.active > a:after {
    transform: scaleX(1);
}
.navbar-nav > li:hover > a,
.navbar-nav > li.active > a {
    color: #006B63 !important;
    background: transparent;
}

/* STICKY HEADER */
.fixedhead {
    position: fixed !important;
    top: 0;
    left: 0;
    width: 100%;
    background: #ffffff !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    animation: slideDown 0.3s ease;
    z-index: 9999;
}
.fixedhead .mainmenu-area {
    position: relative;
    top: 0;
    background: #ffffff;
}

/* HERO SLIDER */
.static-hero-area {
    position: relative;
    width: 100%;
    max-width: 100%;
    margin: 0;
    padding: 0;
    height: 620px;
    background-image: url('images/banner-1.webp');
    background-size: cover;
    background-position: center right;
    background-repeat: no-repeat;
    overflow: hidden;
}
.static-hero-area .container-fluid {
    padding-left: 45px;
    padding-right: 45px;
}
.hero-zoom-slider {
    position: relative;
    height: 620px;
    width: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}
.zoom-slide {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.35s ease, visibility 0.35s ease;
    z-index: 1;
}
.zoom-slide.active {
    opacity: 1;
    visibility: visible;
    z-index: 2;
}
.text-slide-item {
    height: 600px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-top: 50px;
}
.text-content {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
@keyframes caZoomOutReveal {
    0% { transform: scale(1.45) translateY(-8px); opacity: 0; }
    100% { transform: scale(1.0) translateY(0); opacity: 1; }
}
@keyframes caZoomOutDismiss {
    0% { transform: scale(1.0) translateY(0); opacity: 1; }
    100% { transform: scale(0.85) translateY(6px); opacity: 0; }
}
.zoom-slide .text-content h3.sub-title,
.zoom-slide .text-content h1.title,
.zoom-slide .text-content p.description,
.zoom-slide .text-content .btn-box {
    opacity: 0;
    transform: scale(1.45);
    will-change: transform, opacity;
}
.zoom-slide.active .text-content h3.sub-title { animation: caZoomOutReveal 0.62s var(--ca-easing) 0.04s both; }
.zoom-slide.active .text-content h1.title { animation: caZoomOutReveal 0.70s var(--ca-easing) 0.15s both; }
.zoom-slide.active .text-content p.description { animation: caZoomOutReveal 0.78s var(--ca-easing) 0.26s both; }
.zoom-slide.active .text-content .btn-box { animation: caZoomOutReveal 0.85s var(--ca-easing) 0.38s both; }

.zoom-slide.leaving .text-content h3.sub-title,
.zoom-slide.leaving .text-content h1.title,
.zoom-slide.leaving .text-content p.description,
.zoom-slide.leaving .text-content .btn-box {
    animation: caZoomOutDismiss 0.35s ease both !important;
}

.text-content h3.sub-title {
    color: #002e5b !important;
    font-size: 21px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 12px !important;
    text-transform: uppercase !important;
}
.text-content h1.title {
    color: #006B63 !important;
    font-size: 60px !important;
    font-weight: 900 !important;
    line-height: 1.10 !important;
    margin-bottom: 18px !important;
    letter-spacing: -0.5px !important;
    text-transform: uppercase !important;
}
.text-content p.description {
    color: #334155 !important;
    font-size: 16px !important;
    line-height: 1.70 !important;
    max-width: 600px;
    margin-bottom: 30px !important;
    font-weight: 500 !important;
}
.banner-btn, .theme-btn {
    border: 2px solid #002e5b !important;
    border-radius: 3px !important;
    color: #002e5b !important;
    display: inline-block !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    line-height: 42px !important;
    padding: 0 28px !important;
    margin-right: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-decoration: none !important;
    background: transparent !important;
    transition: all 0.35s var(--ca-spring) !important;
}
.banner-btn:hover, .theme-btn:hover {
    background: #002e5b !important;
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 46, 91, 0.25);
}

/* PRACTICE AREAS */
.service-badge {
    background: #e6f7f5;
    color: #006B63;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 30px;
    display: inline-block;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 1px solid #b2ece6;
}
.single-item {
    background: #ffffff;
    padding: 35px 25px;
    border-radius: 8px;
    border: 1px solid #eef2f6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    transition: all 0.35s var(--ca-spring);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.single-item:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 30px rgba(0, 107, 99, 0.1);
    border-color: #006B63;
}
.single-item img {
    height: 52px;
    width: 52px;
    margin-bottom: 20px;
    object-fit: contain;
}
.single-item h4 {
    color: #002e5b;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}
.single-item p {
    color: #64748b;
    font-size: 14px;
    line-height: 1.65;
    margin-bottom: 20px;
}

/* TEAM CARDS (PERFECT ASPECT RATIO & FIT) */
.team-card-unified {
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.team-card-unified:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 30px rgba(0, 46, 91, 0.12);
}
.team-img-box {
    height: 240px;
    width: 100%;
    background: #f1f5f9;
    overflow: hidden;
    position: relative;
}
.team-img-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    display: block;
    transition: transform 0.4s ease;
}
.team-card-unified:hover .team-img-box img {
    transform: scale(1.05);
}
.team-social-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #f1f5f9;
    color: #002e5b;
    margin: 0 2px;
    font-size: 13px;
    transition: all 0.2s ease;
    text-decoration: none !important;
}
.team-social-btn:hover {
    background: #006B63;
    color: #ffffff;
}
.team-connect-btn {
    display: block;
    width: 100%;
    padding: 7px 12px;
    background: #006B63;
    color: #ffffff !important;
    font-weight: 700;
    font-size: 12.5px;
    border-radius: 6px;
    text-align: center;
    text-decoration: none !important;
    transition: all 0.2s ease;
    margin-top: 10px;
}
.team-connect-btn:hover {
    background: #002e5b;
}

/* GOOGLE REVIEWS SECTION */
.google-badge-box {
    background: #ffffff;
    border-radius: 10px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.review-card-item {
    background: #ffffff;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.reviewer-avatar {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50%;
    object-fit: cover;
}

/* STATS COUNTER */
.stat-counter-box {
    padding: 20px 10px;
}
.counter-num {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.1;
}

/* MOBILE MENU DRAWER */
.hamburger-morph-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 8px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    width: 40px;
    height: 40px;
    z-index: 100001;
}
.hamburger-morph-btn .bar {
    width: 24px;
    height: 3px;
    background: #002e5b;
    border-radius: 2px;
    transition: all 0.35s var(--ca-spring);
}
.hamburger-morph-btn.is-active .bar-1 {
    transform: translateY(7.5px) rotate(45deg);
    background: #006B63;
}
.hamburger-morph-btn.is-active .bar-2 {
    opacity: 0;
    transform: translateX(-10px);
}
.hamburger-morph-btn.is-active .bar-3 {
    transform: translateY(-7.5px) rotate(-45deg);
    background: #006B63;
}

/* CINEMATIC STORYTELLING REVEAL ENGINE */
.cinematic-scene {
    position: relative;
    will-change: transform, opacity;
}

/* Base unrevealed state: elements start below with blur and scale */
.cinematic-reveal,
.single-item,
.team-card-unified,
.stat-counter-box,
.review-card-item,
.blog-card,
.service-badge,
.google-badge-box {
    opacity: 0;
    transform: translateY(36px) scale(0.95);
    filter: blur(4px);
    transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.75s cubic-bezier(0.16, 1, 0.3, 1), 
                filter 0.55s ease;
    will-change: opacity, transform, filter;
}

/* Active in-view revealed state */
.cinematic-reveal.is-in-view,
.single-item.is-in-view,
.team-card-unified.is-in-view,
.stat-counter-box.is-in-view,
.review-card-item.is-in-view,
.blog-card.is-in-view,
.service-badge.is-in-view,
.google-badge-box.is-in-view {
    opacity: 1 !important;
    transform: translateY(0) scale(1) !important;
    filter: blur(0px) !important;
}

/* Staggered cascading entrance delays for cards in grids */
.row > div:nth-child(1) .single-item,
.row > div:nth-child(1) .team-card-unified,
.row > div:nth-child(1) .stat-counter-box,
.row > div:nth-child(1) .blog-card { transition-delay: 0.04s; }

.row > div:nth-child(2) .single-item,
.row > div:nth-child(2) .team-card-unified,
.row > div:nth-child(2) .stat-counter-box,
.row > div:nth-child(2) .blog-card { transition-delay: 0.14s; }

.row > div:nth-child(3) .single-item,
.row > div:nth-child(3) .team-card-unified,
.row > div:nth-child(3) .stat-counter-box,
.row > div:nth-child(3) .blog-card { transition-delay: 0.24s; }

.row > div:nth-child(4) .single-item,
.row > div:nth-child(4) .team-card-unified,
.row > div:nth-child(4) .stat-counter-box,
.row > div:nth-child(4) .blog-card { transition-delay: 0.34s; }

.row > div:nth-child(5) .single-item { transition-delay: 0.44s; }
.row > div:nth-child(6) .single-item { transition-delay: 0.54s; }

/* TACTILE MICRO-INTERACTIONS */
.btn, .theme-btn, .banner-btn, .quote-btn button, .team-connect-btn, .sticky-action-btn {
    transition: transform 0.2s var(--ca-easing), box-shadow 0.2s ease, background 0.2s ease !important;
}
.btn:active, .theme-btn:active, .banner-btn:active, .quote-btn button:active, .team-connect-btn:active, .sticky-action-btn:active {
    transform: scale(0.96) !important;
}
.card, .single-item, .team-card-unified, .calc-box-card, .review-card-item, .blog-card {
    transition: transform 0.35s var(--ca-easing), box-shadow 0.35s ease, border-color 0.25s ease;
}
.card:active, .single-item:active, .team-card-unified:active, .calc-box-card:active, .review-card-item:active, .blog-card:active {
    transform: scale(0.985);
}

/* BODY DRAWER OPEN LOCK */
body.drawer-open {
    overflow: hidden !important;
}

/* MOBILE BACKDROP OVERLAY (ZERO BLUR, CRISP DARK DIM) */
#mobile-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.55);
    z-index: 999990 !important;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.3s ease, visibility 0.3s ease;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}
#mobile-backdrop.open {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
}

/* APP-LIKE MOBILE DRAWER (100% SOLID & CRISP) */
#mobile-menu-drawer {
    position: fixed;
    top: 0;
    right: -100%;
    width: 85%;
    max-width: 340px;
    height: 100vh;
    background: #ffffff !important;
    box-shadow: -6px 0 25px rgba(0,0,0,0.25) !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
    transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    overflow-y: auto;
    padding: 24px 20px 30px;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    transform: translateZ(0);
}
#mobile-menu-drawer.open {
    right: 0 !important;
}
#mobile-menu-drawer ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
#mobile-menu-drawer ul li {
    border-bottom: 1px solid #f1f5f9;
    opacity: 0;
    transform: translateX(18px);
    transition: transform 0.35s var(--ca-easing), opacity 0.35s ease;
}
#mobile-menu-drawer.open ul li {
    opacity: 1;
    transform: translateX(0);
}
#mobile-menu-drawer.open ul li:nth-child(1) { transition-delay: 0.05s; }
#mobile-menu-drawer.open ul li:nth-child(2) { transition-delay: 0.09s; }
#mobile-menu-drawer.open ul li:nth-child(3) { transition-delay: 0.13s; }
#mobile-menu-drawer.open ul li:nth-child(4) { transition-delay: 0.17s; }
#mobile-menu-drawer.open ul li:nth-child(5) { transition-delay: 0.21s; }
#mobile-menu-drawer.open ul li:nth-child(6) { transition-delay: 0.25s; }
#mobile-menu-drawer.open ul li:nth-child(7) { transition-delay: 0.29s; }

#mobile-menu-drawer ul li a,
.mobile-nav-link {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 13px 10px !important;
    color: #002e5b !important;
    font-weight: 700 !important;
    font-size: 15.5px !important;
    text-decoration: none !important;
    border-radius: 6px;
    transition: all 0.2s ease;
    cursor: pointer !important;
    position: relative !important;
    z-index: 10 !important;
    pointer-events: auto !important;
    touch-action: manipulation;
}
#mobile-menu-drawer ul li a *,
.mobile-nav-link * {
    pointer-events: none !important;
}
#mobile-menu-drawer ul li a:hover,
#mobile-menu-drawer ul li.active a {
    color: #006B63 !important;
    background: rgba(0, 107, 99, 0.08) !important;
    padding-left: 14px !important;
}
#mobile-menu-drawer ul li a .nav-arrow {
    transition: transform 0.25s ease;
}
#mobile-menu-drawer ul li a:hover .nav-arrow,
#mobile-menu-drawer ul li.active a .nav-arrow {
    transform: translateX(4px);
    color: #006B63;
}
.theme-switch-btn {
    cursor: pointer !important;
    position: relative;
    z-index: 5;
    touch-action: manipulation;
}

/* OWL CAROUSEL AUTO ZOOM & SLIDE DYNAMICS */
.owl-carousel .owl-stage {
    display: flex;
    align-items: stretch;
}
.owl-carousel .owl-item {
    display: flex;
    transition: transform 0.4s var(--ca-easing), opacity 0.4s ease;
}
.owl-carousel .owl-item .single-item,
.owl-carousel .owl-item .team-card-unified,
.owl-carousel .owl-item .impact-card,
.owl-carousel .owl-item .blog-card {
    width: 100%;
    margin-bottom: 0 !important;
    transition: transform 0.35s var(--ca-spring), box-shadow 0.35s ease;
}
.owl-carousel .owl-item .single-item:hover,
.owl-carousel .owl-item .team-card-unified:hover,
.owl-carousel .owl-item .impact-card:hover,
.owl-carousel .owl-item .blog-card:hover {
    transform: translateY(-4px) scale(1.02);
}
.owl-dots {
    text-align: center;
    margin-top: 18px;
}
.owl-dots .owl-dot {
    display: inline-block;
    zoom: 1;
}
.owl-dots .owl-dot span {
    width: 10px;
    height: 10px;
    margin: 4px 5px;
    background: #cbd5e1;
    display: block;
    border-radius: 20px;
    transition: all 0.3s ease;
}
.owl-dots .owl-dot.active span {
    width: 28px;
    background: var(--ca-primary, #006B63);
}

@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* FLOATING WHATSAPP (DESKTOP ONLY - ON MOBILE WE HAVE STICKY BOTTOM BAR) */
.whatsapp-float {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background-color: #25d366;
    color: #ffffff !important;
    border-radius: 50px;
    text-align: center;
    font-size: 28px;
    box-shadow: 0 6px 20px rgba(37, 211, 102, 0.45);
    z-index: 99999;
    height: 54px;
    width: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    transition: all 0.25s ease;
}
.whatsapp-float:hover {
    transform: scale(1.1);
}
@media (max-width: 991px) {
    .whatsapp-float {
        display: none !important;
    }
}

.modal {
    z-index: 10000000 !important;
}
.modal-backdrop {
    z-index: 9999999 !important;
}

/* PAGE BANNER */
.page-banner {
    background: linear-gradient(135deg, #002e5b 0%, #006B63 100%);
    padding: 60px 0 40px;
    color: #ffffff;
    text-align: center;
}
.page-banner h1 {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}
.page-banner p {
    font-size: 15px;
    color: #f1f5f9;
    margin-bottom: 0;
}

/* FOOTER */
.footer {
    background: #0f172a;
    color: #94a3b8;
}
.footer h4, .footer h5 {
    color: #ffffff;
}
.footer a {
    color: #94a3b8;
    text-decoration: none;
    transition: 0.2s;
}
.footer a:hover {
    color: #38bdf8;
}
.footer-logo-badge {
    background: #ffffff;
    padding: 6px 12px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 15px;
}

/* BLOG CARD */
.blog-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.blog-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.1) !important;
}

/* RESPONSIVE OVERRIDES */
@media (max-width: 991px) {
    .top-bar-custom { display: none !important; }
    .header {
        position: sticky !important;
        top: 0;
        z-index: 9999;
        background: #ffffff !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
    }
    .header-main.bg-green {
        background: var(--ca-primary, #006B63) !important;
        padding: 6px 0 !important;
        min-height: 54px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .header-main.white:before {
        display: block !important;
        position: absolute !important;
        top: 0 !important;
        left: -30px !important;
        height: 100% !important;
        width: 55% !important;
        background: #ffffff !important;
        transform: skewX(30deg) !important;
        z-index: 1 !important;
    }
    .header-main.white:after {
        display: block !important;
        position: absolute !important;
        top: 0 !important;
        left: calc(55% - 30px) !important;
        height: 100% !important;
        width: 24px !important;
        background: #ffffff !important;
        border-right: 8px solid var(--ca-accent, #fde428) !important;
        transform: skewX(30deg) !important;
        z-index: 1 !important;
    }
    .header-main .container-fluid { padding-left: 12px !important; padding-right: 12px !important; }
    .header-main-wrapper { min-height: 44px !important; padding: 0 !important; }
    .logo-wrapper { width: auto !important; max-width: 50% !important; position: relative !important; z-index: 5 !important; }
    .logo { padding: 0 !important; }
    .logo img { height: 32px !important; max-height: 32px !important; width: auto !important; }
    .header-main-content { display: none !important; }
    .mobile-header-actions { display: flex !important; align-items: center !important; gap: 8px !important; position: relative !important; z-index: 5 !important; }
    .quote-btn button {
        background: var(--ca-accent, #fde428) !important;
        color: #002e5b !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        line-height: 32px !important;
        padding: 0 12px !important;
        border-radius: 4px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }
    .hamburger-morph-btn .bar {
        background: #ffffff !important;
    }
    .hamburger-morph-btn.is-active .bar-1 {
        transform: translateY(7px) rotate(45deg);
        background: var(--ca-accent, #fde428) !important;
    }
    .hamburger-morph-btn.is-active .bar-3 {
        transform: translateY(-7px) rotate(-45deg);
        background: var(--ca-accent, #fde428) !important;
    }
    .static-hero-area {
        height: 520px !important;
        background-image: linear-gradient(90deg, rgba(0, 32, 65, 0.92) 0%, rgba(0, 32, 65, 0.68) 55%, rgba(0, 32, 65, 0.08) 100%), url('images/banner-1.webp') !important;
        background-size: cover !important;
        background-position: 85% center !important;
    }
    .static-hero-area .container-fluid {
        padding-left: 14px !important;
        padding-right: 14px !important;
    }
    .hero-zoom-slider { height: 520px !important; }
    .text-slide-item { 
        height: 520px !important; 
        padding: 30px 0 20px 0 !important; 
        justify-content: center !important; 
        align-items: flex-start !important;
    }
    .text-content { 
        text-align: left !important; 
        max-width: 295px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .text-content h3.sub-title { 
        font-size: 13.5px !important; 
        color: #fde428 !important; 
        margin-bottom: 6px !important; 
        text-align: left !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6) !important;
    }
    .text-content h1.title { 
        font-size: 27px !important; 
        color: #ffffff !important; 
        line-height: 1.15 !important; 
        margin-bottom: 10px !important; 
        text-align: left !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6) !important;
    }
    .text-content p.description { 
        font-size: 13.5px !important; 
        color: rgba(255,255,255,0.92) !important; 
        line-height: 1.55 !important; 
        margin-bottom: 18px !important; 
        text-align: left !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.6) !important;
    }
    .text-content .btn-box {
        text-align: left !important;
    }
    .banner-btn, .theme-btn {
        border: 2px solid #fde428 !important;
        background: #fde428 !important;
        color: #002e5b !important;
        padding: 0 16px !important;
        font-size: 11.5px !important;
        font-weight: 800 !important;
        line-height: 36px !important;
        border-radius: 4px !important;
        display: inline-block !important;
        margin: 0 6px 6px 0 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3) !important;
    }
    .page-banner { padding: 40px 15px 25px 15px !important; }
    .page-banner h1 { font-size: 24px !important; }
    .page-banner p { font-size: 13.5px !important; }
    .whatsapp-float { bottom: 68px !important; right: 16px !important; width: 46px !important; height: 46px !important; font-size: 22px !important; }
}
"""

with open(os.path.join(dest_dir, "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(master_css)

# Load full extracted subpage bodies
from extracted_bodies import (
    about_us_body,
    services_body,
    knowledge_base_body,
    career_body,
    blog_body,
    contact_us_body,
    privacy_policy_body,
    terms_and_conditions_body
)

# Resolve blog cards in blog_body
blog_cards_html = ""
for idx, p in enumerate(curated_posts):
    blog_cards_html += f"""
    <div class="col-lg-6 col-md-6 mb-4 blog-item">
        <div class="card h-100 shadow-sm border-0 rounded overflow-hidden blog-card" onclick="window.location.href='{p['slug']}.html'">
            <div class="card-img-wrapper position-relative" style="height: 220px; overflow: hidden;">
                <img src="{p['img']}" class="card-img-top w-100 h-100" alt="{p['title']}" style="object-fit: cover;" onerror="this.src='images/banner-1.webp'"/>
                <div style="position: absolute; top: 12px; left: 12px;">
                    <span class="badge badge-{p['badge_color']} px-3 py-1 font-weight-bold shadow-sm">{p['category']}</span>
                </div>
            </div>
            <div class="card-body p-4 d-flex flex-column justify-content-between bg-white">
                <div>
                    <div class="d-flex align-items-center text-muted small mb-2" style="font-size: 12px;">
                        <span><i class="fa fa-user-circle text-success mr-1"></i> {p['author']}</span>
                        <span class="mx-2">&bull;</span>
                        <span><i class="fa fa-calendar text-muted mr-1"></i> {p['date']}</span>
                    </div>
                    <h5 class="font-weight-bold mb-2" style="color: #002e5b; font-size: 17.5px; line-height: 1.4;">
                        <a href="{p['slug']}.html" class="text-decoration-none" style="color: #002e5b;">{p['title']}</a>
                    </h5>
                    <p class="text-muted small mb-0" style="line-height: 1.6; font-size: 13.5px;">{p['excerpt']}</p>
                </div>
                <div class="mt-3 pt-3 border-top d-flex justify-content-between align-items-center">
                    <span class="font-weight-bold text-success small read-more-link">
                        Read Full Article <i class="fa fa-arrow-right ml-1"></i>
                    </span>
                    <span class="badge badge-light text-muted small px-2 py-1"><i class="fa fa-clock-o mr-1"></i> {p['read_time']}</span>
                </div>
            </div>
        </div>
    </div>
    """

recent_sidebar_html = "<ul class='list-unstyled mb-0'>"
for p in curated_posts[:5]:
    recent_sidebar_html += f"""
    <li class="mb-3 pb-3 border-bottom d-flex align-items-center">
        <img src="{p['img']}" style="width: 58px; height: 58px; object-fit: cover; border-radius: 6px;" class="mr-3" onerror="this.src='images/banner-1.webp'"/>
        <div>
            <a href="{p['slug']}.html" class="font-weight-bold text-dark text-decoration-none small d-block" style="line-height: 1.3;">{p['title']}</a>
            <small class="text-muted" style="font-size: 11px;"><i class="fa fa-calendar text-success mr-1"></i> {p['date']}</small>
        </div>
    </li>
    """
recent_sidebar_html += "</ul>"

blog_body_resolved = blog_body.replace('{blog_cards_html}', blog_cards_html).replace('{recent_sidebar_html}', recent_sidebar_html).replace('{len(curated_posts)}', str(len(curated_posts)))

# Homepage body with perfect team cards, Google reviews, and latest blogs
home_body = f"""
    <!-- HERO SECTION -->
    <section class="static-hero-area cinematic-scene" id="home">
        <div class="hero-zoom-slider">
            <!-- SLIDE 1: WELCOME TO NATASHA & COMPANY / CA NATASHA RAJVAIDYA -->
            <div class="zoom-slide active">
                <div class="container-fluid h-100 position-relative" style="z-index: 5;">
                    <div class="row h-100">
                        <div class="col-lg-7 col-md-9 col-12">
                            <div class="text-slide-item">
                                <div class="text-content">
                                    <div class="d-inline-flex align-items-center mb-2">
                                        <span class="badge badge-success px-3 py-1 font-weight-bold mr-2" style="background-color: var(--ca-primary, #006B63); font-size: 11.5px;">
                                            <i class="fa fa-check-circle mr-1"></i> ISO 9001:2015 CERTIFIED
                                        </span>
                                        <span class="badge badge-light text-dark px-2 py-1 font-weight-bold border small d-none d-sm-inline">
                                            UDYAM-MP-10-0002966
                                        </span>
                                    </div>
                                    <h3 class="sub-title">WELCOME TO NATASHA &amp; COMPANY</h3>
                                    <h1 class="title">CA NATASHA RAJVAIDYA</h1>
                                    <p class="description">Leading ISO 9001:2015 certified Chartered Accountancy firm in Bhopal offering strategic Tax Planning, Statutory Audits, GST Litigation, and Corporate Advisory.</p>
                                    <div class="btn-box">
                                        <a class="theme-btn" href="about-us.html">About Firm</a>
                                        <a class="theme-btn" href="#" data-toggle="modal" data-target="#consultationModal">Consult CA</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 2: FOR YOUR BUSINESS -->
            <div class="zoom-slide">
                <div class="container-fluid h-100 position-relative" style="z-index: 5;">
                    <div class="row h-100">
                        <div class="col-lg-7 col-md-9 col-12">
                            <div class="text-slide-item">
                                <div class="text-content">
                                    <div class="d-inline-flex align-items-center mb-2">
                                        <span class="badge badge-warning text-dark px-3 py-1 font-weight-bold mr-2" style="font-size: 11.5px;">
                                            <i class="fa fa-star mr-1"></i> TOP CA FIRM IN BHOPAL
                                        </span>
                                    </div>
                                    <h3 class="sub-title">WE PROVIDE BEST FINANCIAL SOLUTIONS</h3>
                                    <h1 class="title">FOR YOUR BUSINESS</h1>
                                    <p class="description">Natasha &amp; Company is an ISO 9001:2015 Certified Chartered Accountant firm delivering Strategic Tax Planning, Audits, GST, and Corporate Advisory services.</p>
                                    <div class="btn-box">
                                        <a class="theme-btn" href="services.html">View Services</a>
                                        <a class="theme-btn" href="#" data-toggle="modal" data-target="#consultationModal">Get a Quote</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 3: NATASHA & COMPANY -->
            <div class="zoom-slide">
                <div class="container-fluid h-100 position-relative" style="z-index: 5;">
                    <div class="row h-100">
                        <div class="col-lg-7 col-md-9 col-12">
                            <div class="text-slide-item">
                                <div class="text-content">
                                    <div class="d-inline-flex align-items-center mb-2">
                                        <span class="badge badge-info px-3 py-1 font-weight-bold mr-2" style="font-size: 11.5px;">
                                            <i class="fa fa-building mr-1"></i> MP NAGAR, BHOPAL
                                        </span>
                                    </div>
                                    <h3 class="sub-title">ISO 9001:2015 CERTIFIED FIRM</h3>
                                    <h1 class="title">NATASHA &amp; COMPANY</h1>
                                    <p class="description">Comprehensive startup registration, annual ROC filings, virtual CFO support, and society / trust legal compliances registered under UDYAM-MP-10-0002966.</p>
                                    <div class="btn-box">
                                        <a class="theme-btn" href="contact-us.html">Contact Us</a>
                                        <a class="theme-btn" href="#" data-toggle="modal" data-target="#consultationModal">Book Consultation</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- PRACTICE AREAS -->
    <section class="py-5 cinematic-scene" style="background-color: #f8fafc; overflow: hidden;">
        <div class="container">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 col-lg-10 offset-lg-1">
                    <div class="text-center mb-40">
                        <span class="service-badge">Practice Areas</span>
                        <h2 class="font-weight-bold" style="color: #002e5b;">Our Specialized Services</h2>
                        <p class="text-muted">Comprehensive suite of professional financial, legal, and compliance services to accelerate businesses, startups, and individuals across Bhopal &amp; Pan-India.</p>
                    </div>
                </div>
            </div>
            
            <div class="row services-auto-carousel">
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/hand.webp" alt="Accounting & Bookkeeping Services Bhopal"/>
                        <h4>Accounting &amp; Bookkeeping</h4>
                        <p class="text-muted">End-to-end accounting setup, ledger maintenance, MIS reporting, and balance sheet finalization under Indian Accounting Standards.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/cash.webp" alt="Direct Tax & ITR Filing Bhopal"/>
                        <h4>Direct Taxation &amp; ITR</h4>
                        <p class="text-muted">Proactive tax planning for individuals &amp; corporates, Advance Tax calculation, TDS filing, and representation before assessing officers.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/plan.webp" alt="GST Registration & Notice Litigation MP Nagar Bhopal"/>
                        <h4>GST Advisory &amp; Litigation</h4>
                        <p class="text-muted">GST registration, monthly return filing, Input Tax Credit (ITC) optimization, ISD mechanism, and defense against show cause notices.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/brif.webp" alt="Statutory & Tax Audit Bhopal"/>
                        <h4>Auditing &amp; Assurance</h4>
                        <p class="text-muted">Statutory Audits under Companies Act 2013, Tax Audits under Section 44AB, Internal Audits, Stock Audits, and Forensic Verification.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/commo.webp" alt="Company & LLP Registration MP Nagar Bhopal"/>
                        <h4>Company &amp; LLP Formation</h4>
                        <p class="text-muted">Private Limited, OPC, and LLP incorporation in Bhopal. Digital Signatures, DIN, MOA/AOA drafting, and annual MCA ROC filings.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="single-item">
                        <img src="images/reti.webp" alt="Trust NGO 12A 80G Registration Bhopal"/>
                        <h4>Societies, Trust &amp; NGO Laws</h4>
                        <p class="text-muted">Registration of Charitable Trusts and Societies, Section 12A &amp; 80G tax exemptions, CSR compliance, and FCRA representations.</p>
                        <a href="services.html" class="text-success font-weight-bold">Learn More &rarr;</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ABOUT NATASHA & COMPANY -->
    <section class="py-5 cinematic-scene" style="background-color: #ffffff;">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <span class="service-badge">About Firm</span>
                    <h2 class="font-weight-bold mb-3" style="color: #002e5b;">Leading Chartered Accountancy Firm in Bhopal</h2>
                    <p class="text-muted"><strong>Natasha &amp; Company</strong> is an <strong>ISO 9001:2015 Certified</strong> Chartered Accountancy firm registered under MSME Udyam (<strong>UDYAM-MP-10-0002966</strong>). Headquartered in MP Nagar Bhopal, we provide end-to-end strategic tax, audit, and legal consulting to clients across India.</p>
                    <div class="row mt-4">
                        <div class="col-6 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-check-circle fa-2x text-success mr-2"></i>
                                <div>
                                    <h6 class="font-weight-bold mb-0">ISO 9001:2015</h6>
                                    <small class="text-muted">Quality Certified</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-shield fa-2x text-primary mr-2"></i>
                                <div>
                                    <h6 class="font-weight-bold mb-0">Govt Registered</h6>
                                    <small class="text-muted">MSME Udyam Verified</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-gavel fa-2x text-warning mr-2"></i>
                                <div>
                                    <h6 class="font-weight-bold mb-0">ICAI Compliant</h6>
                                    <small class="text-muted">Strict Ethical Standards</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-lock fa-2x text-danger mr-2"></i>
                                <div>
                                    <h6 class="font-weight-bold mb-0">100% Confidential</h6>
                                    <small class="text-muted">Encrypted Data Vault</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 text-center">
                    <div class="p-4 bg-light rounded shadow-sm border">
                        <img src="images/team-1.webp" alt="CA Natasha Rajvaidya FCA - Best CA in Bhopal" class="rounded-circle mb-3 shadow" style="width: 160px; height: 160px; object-fit: cover; border: 4px solid #006B63;" onerror="this.src='images/team-1.webp'"/>
                        <h4 class="font-weight-bold mb-1" style="color: #002e5b;">CA Natasha Rajvaidya</h4>
                        <span class="badge badge-success px-3 py-1 mb-2" style="background-color: #006B63;">Fellow Chartered Accountant (FCA) &bull; Founder</span>
                        <p class="text-muted small px-3">Expert in Direct Tax planning, Corporate Audits, GST Litigation, and Business Advisory with over 8 years of dedicated practice in Bhopal.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- OUR TEAM SECTION -->
    <section class="py-5 cinematic-scene" style="background-color: #f8fafc; overflow: hidden;">
        <div class="container">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 col-lg-10 offset-lg-1 text-center mb-5">
                    <span class="service-badge">Meet the Experts</span>
                    <h2 class="font-weight-bold" style="color: #002e5b; font-size: 36px;">Our Team</h2>
                    <p class="text-muted">A distinguished team of Chartered Accountants, Senior Tax Consultants, and Corporate Advisors committed to your financial excellence.</p>
                </div>
            </div>

            <div class="row team-auto-carousel">
                <!-- 1. CA Natasha -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="team-card-unified p-3 text-center h-100">
                        <div>
                            <div class="team-img-box mb-3 rounded">
                                <img src="images/team-1.webp" alt="CA Natasha Rajvaidya - Principal Partner" onerror="this.src='images/team-1.webp'"/>
                            </div>
                            <h5 class="font-weight-bold mb-1" style="color: #002e5b; font-size: 17px;">CA Natasha Rajvaidya</h5>
                            <div class="mb-2">
                                <span class="badge badge-success px-2 py-1" style="background-color: #006B63; font-size: 11px;">FCA &bull; Principal Partner</span>
                            </div>
                            <p class="text-muted small mb-3" style="font-size: 12.5px; line-height: 1.4;">Direct Tax Specialist &bull; Statutory Audits &bull; Startup Mentor</p>
                        </div>
                        <div>
                            <div class="d-flex justify-content-center align-items-center mb-2">
                                <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" class="team-social-btn" title="LinkedIn"><i class="fa fa-linkedin"></i></a>
                                <a href="https://twitter.com/canatasharaj" target="_blank" class="team-social-btn" title="Twitter"><i class="fa fa-twitter"></i></a>
                                <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20would%20like%20to%20consult%20with%20you." target="_blank" class="team-social-btn" title="WhatsApp"><i class="fa fa-whatsapp text-success"></i></a>
                                <a href="tel:+919407000157" class="team-social-btn" title="Call"><i class="fa fa-phone text-primary"></i></a>
                            </div>
                            <a href="#" data-toggle="modal" data-target="#consultationModal" class="team-connect-btn">
                                <i class="fa fa-comments mr-1"></i> Connect / Consult
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 2. Senior Partner -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="team-card-unified p-3 text-center h-100">
                        <div>
                            <div class="team-img-box mb-3 rounded">
                                <img src="images/team-2.webp" alt="Ashish & Associates - Senior Partner"/>
                            </div>
                            <h5 class="font-weight-bold mb-1" style="color: #002e5b; font-size: 17px;">Ashish &amp; Associates</h5>
                            <div class="mb-2">
                                <span class="badge badge-primary px-2 py-1" style="font-size: 11px;">Senior Partner &bull; Audit Lead</span>
                            </div>
                            <p class="text-muted small mb-3" style="font-size: 12.5px; line-height: 1.4;">Company Law &bull; Ind AS Compliance &bull; Forensic Audit</p>
                        </div>
                        <div>
                            <div class="d-flex justify-content-center align-items-center mb-2">
                                <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" class="team-social-btn" title="LinkedIn"><i class="fa fa-linkedin"></i></a>
                                <a href="https://twitter.com/canatasharaj" target="_blank" class="team-social-btn" title="Twitter"><i class="fa fa-twitter"></i></a>
                                <a href="https://wa.me/919407000157?text=Hello%2C%20I%20need%20assistance%20with%20Auditing%20Services." target="_blank" class="team-social-btn" title="WhatsApp"><i class="fa fa-whatsapp text-success"></i></a>
                                <a href="tel:+919407000157" class="team-social-btn" title="Call"><i class="fa fa-phone text-primary"></i></a>
                            </div>
                            <a href="contact-us.html" class="team-connect-btn">
                                <i class="fa fa-envelope mr-1"></i> Connect with Lead
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 3. Tax Advisor -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="team-card-unified p-3 text-center h-100">
                        <div>
                            <div class="team-img-box mb-3 rounded">
                                <img src="images/team-3.webp" alt="Senior Tax Advisor"/>
                            </div>
                            <h5 class="font-weight-bold mb-1" style="color: #002e5b; font-size: 17px;">Senior Tax Advisor</h5>
                            <div class="mb-2">
                                <span class="badge badge-warning text-dark px-2 py-1 font-weight-bold" style="font-size: 11px;">GST &amp; Litigation Lead</span>
                            </div>
                            <p class="text-muted small mb-3" style="font-size: 12.5px; line-height: 1.4;">Indirect Taxes &bull; Show Cause Notice Defense &bull; ITC Audit</p>
                        </div>
                        <div>
                            <div class="d-flex justify-content-center align-items-center mb-2">
                                <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" class="team-social-btn" title="LinkedIn"><i class="fa fa-linkedin"></i></a>
                                <a href="https://twitter.com/canatasharaj" target="_blank" class="team-social-btn" title="Twitter"><i class="fa fa-twitter"></i></a>
                                <a href="https://wa.me/919407000157?text=Hello%2C%20I%20need%20assistance%20with%20GST%20Litigation." target="_blank" class="team-social-btn" title="WhatsApp"><i class="fa fa-whatsapp text-success"></i></a>
                                <a href="tel:+919407000157" class="team-social-btn" title="Call"><i class="fa fa-phone text-primary"></i></a>
                            </div>
                            <a href="contact-us.html" class="team-connect-btn">
                                <i class="fa fa-envelope mr-1"></i> Connect with Advisor
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 4. Corporate Law -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="team-card-unified p-3 text-center h-100">
                        <div>
                            <div class="team-img-box mb-3 rounded">
                                <img src="images/team-4.webp" alt="Corporate Law Head"/>
                            </div>
                            <h5 class="font-weight-bold mb-1" style="color: #002e5b; font-size: 17px;">Corporate Law Head</h5>
                            <div class="mb-2">
                                <span class="badge badge-info px-2 py-1" style="font-size: 11px;">ROC &amp; Startup Advisor</span>
                            </div>
                            <p class="text-muted small mb-3" style="font-size: 12.5px; line-height: 1.4;">LLP &amp; Pvt Ltd Formations &bull; NGO/Trust 12A 80G Filings</p>
                        </div>
                        <div>
                            <div class="d-flex justify-content-center align-items-center mb-2">
                                <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" class="team-social-btn" title="LinkedIn"><i class="fa fa-linkedin"></i></a>
                                <a href="https://twitter.com/canatasharaj" target="_blank" class="team-social-btn" title="Twitter"><i class="fa fa-twitter"></i></a>
                                <a href="https://wa.me/919407000157?text=Hello%2C%20I%20need%20assistance%20with%20Company%20Formation." target="_blank" class="team-social-btn" title="WhatsApp"><i class="fa fa-whatsapp text-success"></i></a>
                                <a href="tel:+919407000157" class="team-social-btn" title="Call"><i class="fa fa-phone text-primary"></i></a>
                            </div>
                            <a href="contact-us.html" class="team-connect-btn">
                                <i class="fa fa-envelope mr-1"></i> Connect with Legal
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FINANCIAL CALCULATORS SECTION -->
    <section class="py-5 cinematic-scene" style="background-color: #ffffff;">
        <div class="container">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 col-lg-10 offset-lg-1 text-center mb-4">
                    <span class="service-badge">Financial Tools</span>
                    <h2 class="font-weight-bold" style="color: #002e5b; font-size: 34px;">Live Financial &amp; Tax Calculators</h2>
                    <p class="text-muted">Instant calculation tools for Income Tax planning and monthly loan installments.</p>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="p-4 bg-white rounded shadow-sm border h-100">
                        <h4 class="font-weight-bold mb-3" style="color: #002e5b;"><i class="fa fa-calculator text-success mr-2"></i> Income Tax Calculator (FY 2024-25)</h4>
                        <p class="text-muted small">Compare estimated tax payable under the New vs Old Tax Regime.</p>
                        <div class="form-group mb-3">
                            <label class="font-weight-bold small text-dark">Annual Taxable Income (₹)</label>
                            <input type="number" class="form-control" id="calc-income" placeholder="e.g. 1200000" value="1200000"/>
                        </div>
                        <div class="form-group mb-3">
                            <label class="font-weight-bold small text-dark">Deductions (80C, 80D, HRA under Old Regime)</label>
                            <input type="number" class="form-control" id="calc-deductions" placeholder="e.g. 150000" value="150000"/>
                        </div>
                        <button type="button" class="btn btn-block font-weight-bold text-white py-2" style="background: #006B63;" onclick="calculateTax()">Calculate Tax Comparison</button>
                        
                        <div class="mt-4 p-3 bg-light rounded border" id="tax-result">
                            <div class="row text-center">
                                <div class="col-6 border-right">
                                    <small class="text-muted font-weight-bold">New Tax Regime</small>
                                    <h5 class="text-success font-weight-bold mb-0" id="res-new">₹82,500</h5>
                                </div>
                                <div class="col-6">
                                    <small class="text-muted font-weight-bold">Old Tax Regime</small>
                                    <h5 class="text-primary font-weight-bold mb-0" id="res-old">₹1,32,600</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-6 mb-4">
                    <div class="p-4 bg-white rounded shadow-sm border h-100">
                        <h4 class="font-weight-bold mb-3" style="color: #002e5b;"><i class="fa fa-percent text-success mr-2"></i> Business / Home Loan EMI Calculator</h4>
                        <p class="text-muted small">Calculate monthly EMI and total interest outflow.</p>
                        <div class="form-group mb-3">
                            <label class="font-weight-bold small text-dark">Loan Amount (₹)</label>
                            <input type="number" class="form-control" id="emi-amount" placeholder="e.g. 2500000" value="2500000"/>
                        </div>
                        <div class="row">
                            <div class="col-6 form-group mb-3">
                                <label class="font-weight-bold small text-dark">Interest Rate (% p.a.)</label>
                                <input type="number" class="form-control" id="emi-rate" placeholder="e.g. 8.5" value="8.5" step="0.1"/>
                            </div>
                            <div class="col-6 form-group mb-3">
                                <label class="font-weight-bold small text-dark">Tenure (Years)</label>
                                <input type="number" class="form-control" id="emi-tenure" placeholder="e.g. 10" value="10"/>
                            </div>
                        </div>
                        <button type="button" class="btn btn-block font-weight-bold text-white py-2" style="background: #006B63;" onclick="calculateEMI()">Calculate Monthly EMI</button>
                        
                        <div class="mt-4 p-3 bg-light rounded border" id="emi-result">
                            <div class="row text-center">
                                <div class="col-6 border-right">
                                    <small class="text-muted font-weight-bold">Monthly EMI</small>
                                    <h5 class="text-success font-weight-bold mb-0" id="res-emi">₹31,005</h5>
                                </div>
                                <div class="col-6">
                                    <small class="text-muted font-weight-bold">Total Interest</small>
                                    <h5 class="text-dark font-weight-bold mb-0" id="res-interest">₹12,20,560</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- STRATEGIC GROWTH & INDUSTRY IMPACT -->
    <section class="py-5 cinematic-scene" id="trusted-stats-section" style="background: #0B132B; color: #ffffff; overflow: hidden;">
        <div class="container">
            <div class="text-center mb-4">
                <span class="badge px-3 py-1 text-warning font-weight-bold" style="background: rgba(253, 228, 40, 0.12); border: 1px solid #fde428; border-radius: 20px; font-size: 11.5px; letter-spacing: 1px;">OUR PROVEN TRACK RECORD</span>
                <h2 class="font-weight-bold text-white mt-2" style="font-size: 32px;">Strategic Growth &amp; Industry Impact</h2>
            </div>
            
            <div class="row track-record-auto-carousel">
                <!-- 1. Tax Optimization & Defense -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="impact-card p-4 rounded h-100" style="background: #111D3E; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; min-height: 280px;">
                        <div>
                            <div class="impact-icon-box mb-3" style="width: 48px; height: 48px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa fa-line-chart text-white" style="font-size: 22px;"></i>
                            </div>
                            <h4 class="font-weight-bold text-white mb-2" style="font-size: 18px;">Tax Optimization &amp; Defense</h4>
                            <p class="text-white-50 small mb-4" style="line-height: 1.6;">Saved over ₹15+ Crores in legitimate tax deductions and resolved 150+ high-stakes Income Tax &amp; GST appellate notices with zero penalties for our corporate clients.</p>
                        </div>
                        <h4 class="font-weight-bold mb-0" style="color: #f97316; font-size: 20px;">₹ 15Cr+ Optimized</h4>
                    </div>
                </div>

                <!-- 2. Startup Incorporation -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="impact-card p-4 rounded h-100" style="background: #111D3E; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; min-height: 280px;">
                        <div>
                            <div class="impact-icon-box mb-3" style="width: 48px; height: 48px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa fa-rocket text-white" style="font-size: 22px;"></i>
                            </div>
                            <h4 class="font-weight-bold text-white mb-2" style="font-size: 18px;">Startup Incorporation</h4>
                            <p class="text-white-50 small mb-4" style="line-height: 1.6;">Helped 200+ emerging startups register their legal entities, structure founder equity, register trademarks, and maintain 100% statutory adherence from Day 1.</p>
                        </div>
                        <h4 class="font-weight-bold mb-0" style="color: #f97316; font-size: 20px;">200+ Startups Built</h4>
                    </div>
                </div>

                <!-- 3. Multi-City Corporate Reach -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="impact-card p-4 rounded h-100" style="background: #111D3E; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; min-height: 280px;">
                        <div>
                            <div class="impact-icon-box mb-3" style="width: 48px; height: 48px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa fa-globe text-white" style="font-size: 22px;"></i>
                            </div>
                            <h4 class="font-weight-bold text-white mb-2" style="font-size: 18px;">Multi-City Corporate Reach</h4>
                            <p class="text-white-50 small mb-4" style="line-height: 1.6;">Providing seamless cloud-driven accounting and compliance audits across Bhopal, Indore, Jabalpur, Gwalior, Delhi NCR, and 25+ cities in Central India.</p>
                        </div>
                        <h4 class="font-weight-bold mb-0" style="color: #f97316; font-size: 20px;">25+ Cities Covered</h4>
                    </div>
                </div>

                <!-- 4. 100% On-Time Guarantee -->
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="impact-card p-4 rounded h-100" style="background: #111D3E; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; min-height: 280px;">
                        <div>
                            <div class="impact-icon-box mb-3" style="width: 48px; height: 48px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa fa-check-square-o text-white" style="font-size: 22px;"></i>
                            </div>
                            <h4 class="font-weight-bold text-white mb-2" style="font-size: 18px;">100% On-Time Guarantee</h4>
                            <p class="text-white-50 small mb-4" style="line-height: 1.6;">Zero late filing defaults across Income Tax, GST, ROC, and EPFO calendars through our automated compliance monitoring system with dedicated chartered accountants.</p>
                        </div>
                        <h4 class="font-weight-bold mb-0" style="color: #f97316; font-size: 20px;">100% Flawless Record</h4>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- PERFECT AUTO-SLIDING GOOGLE REVIEWS SECTION -->
    <section class="py-5 cinematic-scene" style="background-color: #f8fafc; overflow: hidden;">
        <div class="container">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 col-lg-10 offset-lg-1 text-center mb-4">
                    <span class="service-badge">Client Testimonials</span>
                    <h2 class="font-weight-bold" style="color: #002e5b; font-size: 36px;">See What Our Clients Say</h2>
                    <p class="text-muted">Real feedback and 5-star ratings from verified business clients and individuals on Google.</p>
                </div>
            </div>

            <div class="row align-items-stretch">
                <div class="col-lg-4 col-md-5 mb-4 mb-md-0">
                    <div class="google-badge-box">
                        <div class="mb-3">
                            <img src="images/brand-logo.png" alt="Natasha &amp; Co." style="height: 42px; width: auto; object-fit: contain; margin-bottom: 8px;"/>
                            <h6 class="font-weight-bold mb-0 text-dark" style="font-size: 15px;">Natasha &amp; Co.</h6>
                            <small class="text-muted" style="font-size: 12px;">Chartered Accountants &bull; Bhopal</small>
                        </div>
                        
                        <div class="mb-3">
                            <div class="text-warning mb-1" style="font-size: 22px;">
                                <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                            </div>
                            <h4 class="font-weight-bold text-dark mb-0">141 Google reviews</h4>
                            <small class="text-success font-weight-bold"><i class="fa fa-check-circle mr-1"></i> Verified Google Business</small>
                        </div>

                        <div class="mt-2">
                            <a href="https://search.google.com/local/writereview?placeid=ChIJ8_T3bmdCfDkRsIwuR8aLNxw" target="_blank" class="btn btn-outline-dark btn-block py-2 font-weight-bold shadow-sm" style="border-radius: 6px; font-size: 13.5px;">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="height: 16px; margin-right: 6px; margin-top: -3px;" alt="G"/>
                                Write a review
                            </a>
                        </div>
                    </div>
                </div>

                <div class="col-lg-8 col-md-7">
                    <div class="owl-carousel reviews-carousel">
                        <!-- Review 1 -->
                        <div class="item p-1">
                            <div class="review-card-item">
                                <div>
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <div class="d-flex align-items-center">
                                            <div class="rounded-circle d-flex align-items-center justify-content-center mr-2 text-white font-weight-bold" style="width: 40px; height: 40px; background: #002e5b; font-size: 14px;">
                                                RS
                                            </div>
                                            <div>
                                                <h6 class="font-weight-bold mb-0 text-dark" style="font-size: 14px;">Rahul Sharma</h6>
                                                <small class="text-muted" style="font-size: 11px;">1 year ago</small>
                                            </div>
                                        </div>
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="height: 18px;" alt="Google"/>
                                    </div>
                                    <div class="text-warning mb-2" style="font-size: 13px;">
                                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                    </div>
                                    <p class="text-muted small mb-0" style="line-height: 1.55; font-size: 13px;">
                                        "Best CA in Bhopal for startup registration and GST notice resolution. Resolved our pending refund smoothly!"
                                    </p>
                                </div>
                                <div class="mt-2 text-right">
                                    <small class="text-muted" style="font-size: 10.5px;"><i class="fa fa-check text-success mr-1"></i> Verified Client</small>
                                </div>
                            </div>
                        </div>

                        <!-- Review 2 -->
                        <div class="item p-1">
                            <div class="review-card-item">
                                <div>
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <div class="d-flex align-items-center">
                                            <div class="rounded-circle d-flex align-items-center justify-content-center mr-2 text-white font-weight-bold" style="width: 40px; height: 40px; background: #006B63; font-size: 14px;">
                                                SS
                                            </div>
                                            <div>
                                                <h6 class="font-weight-bold mb-0 text-dark" style="font-size: 14px;">Sohan Shukla</h6>
                                                <small class="text-muted" style="font-size: 11px;">3 years ago</small>
                                            </div>
                                        </div>
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="height: 18px;" alt="Google"/>
                                    </div>
                                    <div class="text-warning mb-2" style="font-size: 13px;">
                                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                    </div>
                                    <p class="text-muted small mb-0" style="line-height: 1.55; font-size: 13px;">
                                        "Excellent services providing friendly as and when needs from them. Always accessible for tax matters and prompt advice."
                                    </p>
                                </div>
                                <div class="mt-2 text-right">
                                    <small class="text-muted" style="font-size: 10.5px;"><i class="fa fa-check text-success mr-1"></i> Verified Client</small>
                                </div>
                            </div>
                        </div>

                        <!-- Review 3 -->
                        <div class="item p-1">
                            <div class="review-card-item">
                                <div>
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <div class="d-flex align-items-center">
                                            <div class="rounded-circle d-flex align-items-center justify-content-center mr-2 text-white font-weight-bold" style="width: 40px; height: 40px; background: #c05621; font-size: 14px;">
                                                PS
                                            </div>
                                            <div>
                                                <h6 class="font-weight-bold mb-0 text-dark" style="font-size: 14px;">Dr. Priya Saxena</h6>
                                                <small class="text-muted" style="font-size: 11px;">2 years ago</small>
                                            </div>
                                        </div>
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="height: 18px;" alt="Google"/>
                                    </div>
                                    <div class="text-warning mb-2" style="font-size: 13px;">
                                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                    </div>
                                    <p class="text-muted small mb-0" style="line-height: 1.55; font-size: 13px;">
                                        "Outstanding support for medical professionals tax planning and trust registrations. Extremely knowledgeable and trustworthy."
                                    </p>
                                </div>
                                <div class="mt-2 text-right">
                                    <small class="text-muted" style="font-size: 10.5px;"><i class="fa fa-check text-success mr-1"></i> Verified Client</small>
                                </div>
                            </div>
                        </div>

                        <!-- Review 4 -->
                        <div class="item p-1">
                            <div class="review-card-item">
                                <div>
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <div class="d-flex align-items-center">
                                            <div class="rounded-circle d-flex align-items-center justify-content-center mr-2 text-white font-weight-bold" style="width: 40px; height: 40px; background: #2b6cb0; font-size: 14px;">
                                                MV
                                            </div>
                                            <div>
                                                <h6 class="font-weight-bold mb-0 text-dark" style="font-size: 14px;">Manish Kumar Vishwakarma</h6>
                                                <small class="text-muted" style="font-size: 11px;">3 years ago</small>
                                            </div>
                                        </div>
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="height: 18px;" alt="Google"/>
                                    </div>
                                    <div class="text-warning mb-2" style="font-size: 13px;">
                                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                                    </div>
                                    <p class="text-muted small mb-0" style="line-height: 1.55; font-size: 13px;">
                                        "Very Responsive humble and professional. File my ITR in time. Thanks to Natasha and Company for seamless compliance."
                                    </p>
                                </div>
                                <div class="mt-2 text-right">
                                    <small class="text-muted" style="font-size: 10.5px;"><i class="fa fa-check text-success mr-1"></i> Verified Client</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- LATEST BLOGS & INSIGHTS (HOMEPAGE SECTION) -->
    <section class="py-5 cinematic-scene" style="background-color: #ffffff;">
        <div class="container">
            <div class="row align-items-center mb-4">
                <div class="col-md-8">
                    <span class="service-badge">Insights &amp; Articles</span>
                    <h2 class="font-weight-bold mb-1" style="color: #002e5b; font-size: 34px;">Latest Financial &amp; Tax Insights</h2>
                    <p class="text-muted">Stay informed with expert analysis, regulatory updates, and strategic tax advice.</p>
                </div>
                <div class="col-md-4 text-md-right">
                    <a href="blog.html" class="btn btn-outline-dark font-weight-bold px-4 py-2" style="border-radius: 4px;">View All Insights &rarr;</a>
                </div>
            </div>

            <div class="row blogs-auto-carousel">
                <!-- Blog 1 -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100 shadow-sm border-0 rounded overflow-hidden blog-card" onclick="window.location.href='7-key-points-every-salaried-employee-must-know-before-filing-income-tax-return.html'">
                        <div class="card-img-wrapper position-relative" style="height: 200px; overflow: hidden;">
                            <img src="images/blog-1.webp" class="card-img-top w-100 h-100" alt="Income Tax Guide" style="object-fit: cover;" onerror="this.src='images/banner-1.webp'"/>
                            <div style="position: absolute; top: 12px; left: 12px;">
                                <span class="badge badge-primary px-3 py-1 font-weight-bold shadow-sm">Income Tax</span>
                            </div>
                        </div>
                        <div class="card-body p-4 d-flex flex-column justify-content-between">
                            <div>
                                <small class="text-muted d-block mb-2"><i class="fa fa-calendar text-success mr-1"></i> May 2026</small>
                                <h5 class="font-weight-bold mb-2" style="color: #002e5b; font-size: 16.5px; line-height: 1.4;">7 Key Points Every Salaried Employee Must Know Before Filing ITR</h5>
                                <p class="text-muted small mb-0" style="line-height: 1.55;">Essential tax-saving insights, deduction checks under Section 80C, 80D, and AIS reconciliation tips.</p>
                            </div>
                            <div class="mt-3 pt-3 border-top text-right">
                                <span class="text-success font-weight-bold small">Read More &rarr;</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Blog 2 -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100 shadow-sm border-0 rounded overflow-hidden blog-card" onclick="window.location.href='isd-registration-now-mandatory-from-april-2025-dont-lose-your-gst-credit.html'">
                        <div class="card-img-wrapper position-relative" style="height: 200px; overflow: hidden;">
                            <img src="images/blog-2.webp" class="card-img-top w-100 h-100" alt="GST Input Service Distributor" style="object-fit: cover;" onerror="this.src='images/banner-1.webp'"/>
                            <div style="position: absolute; top: 12px; left: 12px;">
                                <span class="badge badge-warning text-dark px-3 py-1 font-weight-bold shadow-sm">GST Advisory</span>
                            </div>
                        </div>
                        <div class="card-body p-4 d-flex flex-column justify-content-between">
                            <div>
                                <small class="text-muted d-block mb-2"><i class="fa fa-calendar text-success mr-1"></i> April 2026</small>
                                <h5 class="font-weight-bold mb-2" style="color: #002e5b; font-size: 16.5px; line-height: 1.4;">ISD Registration Now Mandatory: Don't Lose Your GST Credit</h5>
                                <p class="text-muted small mb-0" style="line-height: 1.55;">Understanding the new mandatory Input Service Distributor mechanism for multi-branch businesses.</p>
                            </div>
                            <div class="mt-3 pt-3 border-top text-right">
                                <span class="text-success font-weight-bold small">Read More &rarr;</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Blog 3 -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100 shadow-sm border-0 rounded overflow-hidden blog-card" onclick="window.location.href='invest-madhya-pradesh-global-investors-summit-2025-a-catalyst-for-growth.html'">
                        <div class="card-img-wrapper position-relative" style="height: 200px; overflow: hidden;">
                            <img src="images/blog-3.webp" class="card-img-top w-100 h-100" alt="Corporate Law & Investment" style="object-fit: cover;" onerror="this.src='images/banner-1.webp'"/>
                            <div style="position: absolute; top: 12px; left: 12px;">
                                <span class="badge badge-info px-3 py-1 font-weight-bold shadow-sm">Corporate Growth</span>
                            </div>
                        </div>
                        <div class="card-body p-4 d-flex flex-column justify-content-between">
                            <div>
                                <small class="text-muted d-block mb-2"><i class="fa fa-calendar text-success mr-1"></i> March 2026</small>
                                <h5 class="font-weight-bold mb-2" style="color: #002e5b; font-size: 16.5px; line-height: 1.4;">Invest Madhya Pradesh: Industrial Growth &amp; MSME Opportunities</h5>
                                <p class="text-muted small mb-0" style="line-height: 1.55;">Opportunities, tax incentives, and policy subsidies for new enterprises setting up base in Bhopal.</p>
                            </div>
                            <div class="mt-3 pt-3 border-top text-right">
                                <span class="text-success font-weight-bold small">Read More &rarr;</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- LIVE NEWS & DUE DATE REMINDERS -->
    <section class="py-5 cinematic-scene" style="background-color: #f8fafc;">
        <div class="container">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 col-lg-10 offset-lg-1">
                    <div class="text-center mb-40">
                        <span class="service-badge">Stay Updated</span>
                        <h2 class="font-weight-bold" style="color: #002e5b;">Tax Updates &amp; Statutory Due Dates</h2>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="p-4 bg-white rounded shadow-sm border h-100">
                        <h4 class="font-weight-bold text-dark border-bottom pb-2 mb-3"><i class="fa fa-newspaper-o text-success"></i> Latest Tax News</h4>
                        <marquee direction="up" height="230" scrollamount="2" scrolldelay="30" onmouseover="this.stop();" onmouseout="this.start();">
                            <div class="mb-3 border-bottom pb-2">
                                <span class="badge badge-danger">Important</span> <small class="text-muted">Income Tax</small>
                                <p class="font-weight-bold mb-1 mt-1">E-filing of Income Tax Returns for AY 2026-27 is open.</p>
                            </div>
                            <div class="mb-3 border-bottom pb-2">
                                <span class="badge badge-primary">GST</span> <small class="text-muted">Notification</small>
                                <p class="font-weight-bold mb-1 mt-1">Updated E-Invoicing and GSTR-1 mandatory reconciliation guidelines issued by CBIC.</p>
                            </div>
                            <div class="mb-3 border-bottom pb-2">
                                <span class="badge badge-success">MCA</span> <small class="text-muted">Company Law</small>
                                <p class="font-weight-bold mb-1 mt-1">Annual Filing for Private Limited Companies &amp; LLPs compliance reminders.</p>
                            </div>
                        </marquee>
                    </div>
                </div>
                <div class="col-md-8 mb-4">
                    <div class="p-4 bg-white rounded shadow-sm border h-100">
                        <h4 class="font-weight-bold text-dark border-bottom pb-2 mb-3"><i class="fa fa-calendar-check-o text-success"></i> Monthly Statutory Compliance Calendar</h4>
                        <div class="table-responsive">
                            <table class="table table-hover table-striped mb-0 small">
                                <thead style="background-color: #006B63; color: #fff;">
                                    <tr>
                                        <th>Due Date</th>
                                        <th>Statutory Compliance</th>
                                        <th>Authority</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>07th Monthly</strong></td>
                                        <td>TDS / TCS Deposit for previous month</td>
                                        <td>Income Tax</td>
                                        <td><span class="badge badge-warning">Deposit Challan 281</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>11th Monthly</strong></td>
                                        <td>GSTR-1 Monthly Outward Supplies Filing</td>
                                        <td>GST Portal</td>
                                        <td><span class="badge badge-primary">Form GSTR-1</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>20th Monthly</strong></td>
                                        <td>GSTR-3B Monthly Return &amp; Tax Payment</td>
                                        <td>GST Portal</td>
                                        <td><span class="badge badge-success">Form GSTR-3B</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>31st Quarterly</strong></td>
                                        <td>TDS Quarterly Return (Form 24Q, 26Q, 27Q)</td>
                                        <td>Income Tax</td>
                                        <td><span class="badge badge-info">Quarterly Filing</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- GET IN TOUCH CONSULTATION FORM -->
    <section class="py-5 cinematic-scene" style="background-color: #ffffff;">
        <div class="container">
            <div class="p-4 p-md-5 bg-white rounded shadow-sm border">
                <div class="row align-items-center">
                    <div class="col-lg-6 mb-4 mb-lg-0">
                        <span class="service-badge">Send a Message</span>
                        <h2 class="font-weight-bold mb-3" style="color: #002e5b; font-size: 36px;">Get in Touch</h2>
                        <p class="text-muted mb-4">Have questions regarding Income Tax, GST, Statutory Audit, or Company Registration in Bhopal? Our certified Chartered Accountants are here to assist you.</p>
                        
                        <form onsubmit="handleQuickContact(event)">
                            <div class="form-group mb-3">
                                <input type="text" id="contact-name" class="form-control" placeholder="Your Name" required/>
                            </div>
                            <div class="form-group mb-3">
                                <input type="email" id="contact-email" class="form-control" placeholder="Your Email ID" required/>
                            </div>
                            <div class="form-group mb-3">
                                <input type="tel" id="contact-phone" class="form-control" placeholder="Your Phone / WhatsApp Number" required/>
                            </div>
                            <div class="form-group mb-3">
                                <textarea id="contact-msg" class="form-control" rows="4" placeholder="Type Your Requirement / Message..." required></textarea>
                            </div>
                            <button type="submit" class="btn btn-ca-primary px-5 py-2 font-weight-bold" style="background: #006B63; color: #ffffff; border-radius: 4px;">Send Message</button>
                        </form>
                    </div>
                    <div class="col-lg-6 text-center">
                        <div class="p-4 bg-light rounded border text-center">
                            <i class="fa fa-headphones fa-4x text-success mb-3"></i>
                            <h4 class="font-weight-bold" style="color: #002e5b;">Need Direct Assistance?</h4>
                            <p class="text-muted small mb-4">Contact our Bhopal headquarters directly in MP Nagar for instant corporate &amp; individual advisory.</p>
                            <div class="d-flex justify-content-center gap-3">
                                <a href="tel:+919407000157" class="btn btn-outline-success font-weight-bold mr-2"><i class="fa fa-phone mr-1"></i> +91 9407000157</a>
                                <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20need%20assistance%20from%20your%20website." target="_blank" class="btn btn-success font-weight-bold"><i class="fa fa-whatsapp mr-1"></i> WhatsApp</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

# Unified SEO Metadata Directory
seo_meta = {
    "home": {
        "title": "Best Chartered Accountant in Bhopal | CA Natasha & Co. – Tax & GST Experts",
        "description": "Looking for top Chartered Accountants in Bhopal? CA Natasha & Co. is an ISO 9001:2015 certified CA firm in MP Nagar offering GST litigation, ITR, statutory audits & startup advisory.",
        "keywords": "Best CA in Bhopal, Chartered Accountant MP Nagar Bhopal, Tax Consultant Bhopal, GST Registration Bhopal, Top CA Firm Madhya Pradesh, CA Natasha Rajvaidya",
        "url": "https://canatasha-website.vercel.app/"
    },
    "about": {
        "title": "About CA Natasha Rajvaidya (FCA) | Top CA Firm in MP Nagar, Bhopal",
        "description": "Meet CA Natasha Rajvaidya (FCA) and the expert team at Natasha & Company – ISO 9001:2015 certified CA firm in MP Nagar, Bhopal with 12+ years of financial excellence.",
        "keywords": "About CA Natasha Rajvaidya, CA Firm in Bhopal, FCA Natasha Rajvaidya, ISO Certified CA Firm MP Nagar",
        "url": "https://canatasha-website.vercel.app/about-us.html"
    },
    "services": {
        "title": "CA Services in Bhopal | Tax, GST, Company Registration & Audits | CA Natasha & Co.",
        "description": "Comprehensive CA & financial services in Bhopal: Income tax filing, GST litigation, Statutory Audits, Company & LLP incorporation, NGO 12A 80G registrations.",
        "keywords": "CA Services Bhopal, GST Registration MP Nagar, Company Incorporation Bhopal, Tax Audit Bhopal, ITR Filing Bhopal",
        "url": "https://canatasha-website.vercel.app/services.html"
    },
    "knowledge": {
        "title": "Financial Knowledge Base & Tax Calculators | CA Natasha & Co. Bhopal",
        "description": "Free online tax calculators (New vs Old Regime), EMI calculators, statutory compliance due date calendars, and tax compliance guides by CA Natasha & Co.",
        "keywords": "Income Tax Calculator Bhopal, EMI Calculator, Tax Compliance Calendar, GST Due Dates, CA Knowledge Base",
        "url": "https://canatasha-website.vercel.app/knowledge-base.html"
    },
    "career": {
        "title": "CA Articleship & Career Opportunities in Bhopal | Natasha & Company",
        "description": "Apply for CA Articleship, Semi-Qualified CA roles, and tax associate positions at Natasha & Company Chartered Accountants in MP Nagar, Bhopal.",
        "keywords": "CA Articleship Bhopal, CA Jobs Bhopal, Articleship MP Nagar, Natasha and Company Careers",
        "url": "https://canatasha-website.vercel.app/career.html"
    },
    "blog": {
        "title": "Tax, GST & Financial Insights Blog | CA Natasha & Co. Bhopal",
        "description": "Stay updated with the latest income tax notifications, GST tribunal rulings, budget analyses, and company law compliance updates by CA Natasha & Co.",
        "keywords": "Tax Blog Bhopal, GST Updates, Income Tax News, Indian Tax Laws, CA Natasha Blog",
        "url": "https://canatasha-website.vercel.app/blog.html"
    },
    "contact": {
        "title": "Contact Top CA in Bhopal | Natasha & Co. Chartered Accountants MP Nagar",
        "description": "Get in touch with CA Natasha & Company. Visit our corporate office at 195-A, Zone-1 MP Nagar Bhopal or call +91 9407000157 for quick consultation.",
        "keywords": "Contact CA Bhopal, CA Office MP Nagar, Natasha and Company Phone, Chartered Accountant Consultation",
        "url": "https://canatasha-website.vercel.app/contact-us.html"
    },
    "privacy": {
        "title": "Privacy Policy | Natasha & Company – Chartered Accountants Bhopal",
        "description": "Read the official privacy policy and client data confidentiality standards maintained by Natasha & Company Chartered Accountants in Bhopal.",
        "keywords": "Privacy Policy, Natasha & Company, Client Data Protection CA Bhopal",
        "url": "https://canatasha-website.vercel.app/privacy-policy.html"
    },
    "terms": {
        "title": "Terms & Conditions | Natasha & Company – Chartered Accountants Bhopal",
        "description": "Read the official terms and conditions of professional engagement, ICAI ethical compliance guidelines, and advisory standards by Natasha & Company.",
        "keywords": "Terms and Conditions, Natasha & Company, Client Engagement Terms Bhopal",
        "url": "https://canatasha-website.vercel.app/terms-and-conditions.html"
    }
}

schema_json = {
  "@context": "https://schema.org",
  "@type": "AccountingService",
  "@id": "https://canatasha-website.vercel.app/#organization",
  "name": "Natasha & Co. Chartered Accountants",
  "alternateName": "CA Natasha Rajvaidya & Associates",
  "url": "https://canatasha-website.vercel.app",
  "logo": "https://canatasha-website.vercel.app/images/brand-logo.png",
  "image": "https://canatasha-website.vercel.app/images/banner-1.webp",
  "description": "Leading ISO 9001:2015 Certified Chartered Accountancy firm in Bhopal led by CA Natasha Rajvaidya (FCA). Specialized in Direct & Indirect Tax, GST Litigation, Statutory Audits, Company Incorporation, and Startup Advisory.",
  "telephone": "+919407000157",
  "email": "info@canatasha.com",
  "priceRange": "₹₹",
  "founder": {
    "@type": "Person",
    "name": "CA Natasha Rajvaidya",
    "jobTitle": "Fellow Chartered Accountant (FCA)",
    "sameAs": "https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "195-A, 2nd Floor, Zone-1 M.P. Nagar, In front of DB Mall",
    "addressLocality": "Bhopal",
    "addressRegion": "Madhya Pradesh",
    "postalCode": "462011",
    "addressCountry": "IN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 23.2332,
    "longitude": 77.4343
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      "opens": "09:30",
      "closes": "19:30"
    }
  ],
  "areaServed": [
    { "@type": "City", "name": "Bhopal" },
    { "@type": "AdministrativeArea", "name": "Madhya Pradesh" },
    { "@type": "City", "name": "Indore" },
    { "@type": "City", "name": "Jabalpur" },
    { "@type": "Country", "name": "India" }
  ],
  "sameAs": [
    "https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/",
    "https://twitter.com/canatasharaj",
    "https://www.facebook.com/canatasharaj/",
    "https://www.instagram.com/natasharajvaidya/?hl=en"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Chartered Accountancy & Financial Services",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Income Tax & ITR Filing in Bhopal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "GST Registration & Litigation MP Nagar" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Statutory & Tax Audits Bhopal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Company & LLP Incorporation MP Nagar Bhopal" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "NGO, Trust 12A 80G Registration" } },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Startup India & MSME Udyam Advisory" } }
    ]
  }
}
schema_json_str = json.dumps(schema_json, ensure_ascii=False, indent=2)

master_layout_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
    
    <!-- PRIMARY LOCALIZED SEO TAGS -->
    <title>__META_TITLE__</title>
    <meta name="description" content="__META_DESC__"/>
    <meta name="keywords" content="__META_KEYWORDS__"/>
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
    <link rel="canonical" href="__CANONICAL_URL__"/>
    
    <!-- OPEN GRAPH / SOCIAL CARDS -->
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="__META_TITLE__"/>
    <meta property="og:description" content="__META_DESC__"/>
    <meta property="og:url" content="__CANONICAL_URL__"/>
    <meta property="og:site_name" content="Natasha &amp; Co. Chartered Accountants"/>
    <meta property="og:image" content="https://canatasha-website.vercel.app/images/banner-1.webp"/>
    
    <!-- TWITTER CARDS -->
    <meta name="twitter:card" content="summary_large_image"/>
    <meta name="twitter:title" content="__META_TITLE__"/>
    <meta name="twitter:description" content="__META_DESC__"/>
    <meta name="twitter:image" content="https://canatasha-website.vercel.app/images/banner-1.webp"/>
    <meta name="twitter:creator" content="@canatasharaj"/>

    <!-- LOCALBUSINESS / ACCOUNTING SERVICE STRUCTURED SCHEMA (JSON-LD) -->
    <script type="application/ld+json">
__SCHEMA_JSON__
    </script>
    
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon"/>
    <link rel="stylesheet" href="css/bootstrap.min.css"/>
    <link rel="stylesheet" href="css/font-awesome.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
    <link rel="stylesheet" href="css/owl.carousel.css"/>
    <link rel="stylesheet" href="css/style.css?v=38000"/>

    <style id="master-inlined-css">
__MASTER_CSS__
    </style>
</head>
<body>
    <!-- MOBILE BACKDROP OVERLAY -->
    <div id="mobile-backdrop" class="d-lg-none"></div>

    <!-- SLEEK SCROLL PROGRESS INDICATOR -->
    <div id="scroll-progress-bar"></div>

    <!-- TOP HEADER (DESKTOP) WITH TRUST CREDENTIALS & THEME SWITCHER -->
    <div class="top-bar-custom d-none d-md-block">
        <div class="container-fluid">
            <div class="row align-items-center">
                <div class="col-lg-7 col-md-6">
                    <span><i class="fa fa-phone" style="color: #00a896;"></i> <a href="tel:+919407000157">+91 9407000157</a></span>
                    <span><i class="fa fa-envelope" style="color: #00a896;"></i> <a href="mailto:info@canatasha.com">info@canatasha.com</a></span>
                    <span class="trust-badge-pill d-none d-xl-inline"><i class="fa fa-certificate text-warning mr-1"></i> ISO 9001:2015</span>
                    <span class="trust-badge-pill d-none d-xl-inline"><i class="fa fa-shield text-info mr-1"></i> UDYAM-MP-10-0002966</span>
                </div>
                <div class="col-lg-5 col-md-6 text-right d-flex align-items-center justify-content-end">
                    <div class="social-icons-top mr-2">
                        <a href="https://www.facebook.com/canatasharaj/" target="_blank" title="Facebook"><i class="fa fa-facebook"></i></a>
                        <a href="https://www.instagram.com/natasharajvaidya/?hl=en" target="_blank" title="Instagram"><i class="fa fa-instagram"></i></a>
                        <a href="https://twitter.com/canatasharaj" target="_blank" title="Twitter"><i class="fa fa-twitter"></i></a>
                        <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" title="LinkedIn"><i class="fa fa-linkedin"></i></a>
                    </div>
                    <!-- CLEAN IN-HEADER THEME SWITCHER -->
                    <div class="theme-switcher-top">
                        <span class="small font-weight-bold mr-1 text-white-50"><i class="fa fa-paint-brush text-warning mr-1"></i>Theme:</span>
                        <button type="button" class="theme-switch-btn active" data-theme="emerald">Emerald</button>
                        <button type="button" class="theme-switch-btn" data-theme="bw">B&amp;W</button>
                        <button type="button" class="theme-switch-btn" data-theme="grey">Slate</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- MAIN HEADER -->
    <header class="header" id="header">
        <div class="header-main bg-green white">
            <div class="container-fluid">
                <div class="header-main-wrapper">
                    <!-- CLEAN UNIFIED BRAND LOGO -->
                    <div class="logo-wrapper">
                        <div class="logo">
                            <a href="index.html">
                                <img src="images/brand-logo.png" alt="Natasha &amp; Co. Chartered Accountants" loading="lazy" decoding="async"/>
                            </a>
                        </div>
                    </div>

                    <!-- CONTACT DETAILS (DESKTOP) -->
                    <div class="header-main-content">
                        <div class="header-info">
                            <img src="images/phone.webp" alt="Phone" loading="lazy" decoding="async"/>
                            <div class="header-info-text">
                                <h4>+91 9407000157</h4>
                                <span>Call for Consultation</span>
                            </div>
                        </div>
                        <div class="header-info">
                            <img src="images/message.webp" alt="Email" loading="lazy" decoding="async"/>
                            <div class="header-info-text">
                                <h4>canatasha.com</h4>
                                <span>ISO 9001:2015 Certified</span>
                            </div>
                        </div>
                    </div>

                    <!-- HEADER ACTIONS (DESKTOP & MOBILE) -->
                    <div class="mobile-header-actions">
                        <div class="quote-btn">
                            <a href="#" data-toggle="modal" data-target="#consultationModal" class="text-decoration-none">
                                <button type="button">Get a Quote</button>
                            </a>
                        </div>
                        <!-- MORPHING HAMBURGER BUTTON (3 LINES TO X) -->
                        <button class="hamburger-morph-btn d-lg-none" type="button" id="mobile-toggle-btn" aria-label="Toggle Navigation Menu">
                            <span class="bar bar-1"></span>
                            <span class="bar bar-2"></span>
                            <span class="bar bar-3"></span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- DESKTOP NAVBAR MENU (DIRECT CLICKABLE LINKS) -->
        <div class="mainmenu-area d-none d-lg-block">
            <div class="container-fluid">
                <nav class="navbar navbar-expand-lg navbar-light">
                    <div class="collapse navbar-collapse" id="navbar-collapse">
                        <ul class="navbar-nav mr-auto">
__DESKTOP_NAV__
                        </ul>
                    </div>
                </nav>
        </div>
    </header>

    <!-- 10-POINT LUXURY MOBILE DRAWER (ROOT LEVEL FOR INSTANT UNINTERRUPTED CLICKS) -->
    <div id="mobile-menu-drawer" class="d-lg-none">
        <div class="container px-0">
            <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
                <span class="font-weight-bold text-dark" style="font-size: 15px;"><i class="fa fa-bars text-success mr-1"></i> Navigation Menu</span>
                <button type="button" class="btn btn-sm btn-light rounded-circle mobile-drawer-close-btn" style="width: 32px; height: 32px; padding: 0; line-height: 30px; border: 1px solid #e2e8f0;" aria-label="Close Menu">
                    <i class="fa fa-times text-dark"></i>
                </button>
            </div>
            <!-- THEME SWITCHER CONTROLS -->
            <div class="mb-3 p-2 rounded" style="background: #f8fafc; border: 1px solid #e2e8f0;">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="font-weight-bold text-dark small"><i class="fa fa-paint-brush text-success mr-1"></i> Choose Theme:</span>
                </div>
                <div class="d-flex justify-content-between" style="gap: 5px;">
                    <button type="button" class="btn btn-sm flex-fill theme-switch-btn py-1" data-theme="emerald" style="border-radius: 6px; font-size: 11.5px; font-weight: 700; border: 1px solid #cbd5e1; background: #ffffff;">
                        <span style="display:inline-block; width:9px; height:9px; background:#006B63; border-radius:50%; margin-right:3px;"></span>Emerald
                    </button>
                    <button type="button" class="btn btn-sm flex-fill theme-switch-btn py-1" data-theme="bw" style="border-radius: 6px; font-size: 11.5px; font-weight: 700; border: 1px solid #cbd5e1; background: #ffffff;">
                        <span style="display:inline-block; width:9px; height:9px; background:#18181b; border-radius:50%; margin-right:3px;"></span>B&amp;W
                    </button>
                    <button type="button" class="btn btn-sm flex-fill theme-switch-btn py-1" data-theme="grey" style="border-radius: 6px; font-size: 11.5px; font-weight: 700; border: 1px solid #cbd5e1; background: #ffffff;">
                        <span style="display:inline-block; width:9px; height:9px; background:#475569; border-radius:50%; margin-right:3px;"></span>Slate
                    </button>
                </div>
            </div>
            <ul>
__MOBILE_NAV__
            </ul>
            <div class="mobile-drawer-bottom mt-3 pt-3 border-top d-flex justify-content-between align-items-center">
                <a href="tel:+919407000157" class="btn btn-sm btn-outline-success font-weight-bold" style="border-radius: 6px; padding: 7px 16px;">
                    <i class="fa fa-phone mr-1"></i> +91 9407000157
                </a>
                <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20need%20assistance%20from%20your%20website." target="_blank" class="btn btn-sm btn-success font-weight-bold" style="border-radius: 6px; padding: 7px 16px;">
                    <i class="fa fa-whatsapp mr-1"></i> WhatsApp
                </a>
            </div>
        </div>
    </div>

__BODY_CONTENT__

    <!-- FOOTER -->
    <footer class="footer pt-5 mt-5">
        <div class="container pb-4">
            <div class="row">
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="footer-logo-badge">
                        <img src="images/brand-logo.png" alt="Natasha &amp; Co." style="height: 38px; width: auto;" loading="lazy" decoding="async"/>
                    </div>
                    <p class="small text-muted">Natasha &amp; Company is an ISO 9001:2015 Certified Chartered Accountancy firm in Bhopal (MSME Udyam: <strong>UDYAM-MP-10-0002966</strong>) led by CA Natasha Rajvaidya (FCA) offering Audit, Direct Tax, GST Litigation, Corporate Law, and Business Advisory services.</p>
                    <div class="social-icons-top mt-3">
                        <a href="https://www.facebook.com/canatasharaj/" target="_blank" class="btn btn-sm btn-outline-light rounded-circle mr-1"><i class="fa fa-facebook"></i></a>
                        <a href="https://www.instagram.com/natasharajvaidya/?hl=en" target="_blank" class="btn btn-sm btn-outline-light rounded-circle mr-1"><i class="fa fa-instagram"></i></a>
                        <a href="https://twitter.com/canatasharaj" target="_blank" class="btn btn-sm btn-outline-light rounded-circle mr-1"><i class="fa fa-twitter"></i></a>
                        <a href="https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/" target="_blank" class="btn btn-sm btn-outline-light rounded-circle mr-1"><i class="fa fa-linkedin"></i></a>
                    </div>
                </div>

                <div class="col-lg-2 col-md-6 mb-4">
                    <h5 class="text-white font-weight-bold mb-3">Quick Links</h5>
                    <ul class="list-unstyled foot-ul-link small">
                        <li class="mb-2"><a href="index.html">Home</a></li>
                        <li class="mb-2"><a href="about-us.html">About Us</a></li>
                        <li class="mb-2"><a href="services.html">Our Services</a></li>
                        <li class="mb-2"><a href="knowledge-base.html">Knowledge Base</a></li>
                        <li class="mb-2"><a href="career.html">Career</a></li>
                        <li class="mb-2"><a href="blog.html">Blog &amp; Insights</a></li>
                        <li class="mb-2"><a href="contact-us.html">Contact Us</a></li>
                        <li class="mb-2"><a href="privacy-policy.html">Privacy Policy</a></li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6 mb-4">
                    <h5 class="text-white font-weight-bold mb-3">Our Practice</h5>
                    <ul class="list-unstyled foot-ul-link small">
                        <li class="mb-2"><a href="services.html">Income Tax &amp; TDS Filing</a></li>
                        <li class="mb-2"><a href="services.html">GST Registration &amp; Returns</a></li>
                        <li class="mb-2"><a href="services.html">Statutory &amp; Tax Audits</a></li>
                        <li class="mb-2"><a href="services.html">Company &amp; LLP Formation</a></li>
                        <li class="mb-2"><a href="services.html">Societies, Trust &amp; NGO Laws</a></li>
                    </ul>
                </div>

                <div class="col-lg-3 col-md-6 mb-4">
                    <h5 class="text-white font-weight-bold mb-3">Offices in Bhopal</h5>
                    <ul class="list-unstyled text-muted small">
                        <li class="mb-2 d-flex">
                            <i class="fa fa-building text-success mr-2 mt-1"></i>
                            <span><strong>Corp:</strong> 195-A, 2nd Floor, Zone-1 M.P. Nagar, In front of DB Mall, Bhopal - 462011</span>
                        </li>
                        <li class="mb-2 d-flex">
                            <i class="fa fa-map-marker text-success mr-2 mt-1"></i>
                            <span><strong>Reg:</strong> 28 C, Samrat Colony, Ashoka Garden, Bhopal - 462023</span>
                        </li>
                        <li class="mb-2 d-flex">
                            <i class="fa fa-phone text-success mr-2 mt-1"></i>
                            <a href="tel:+919407000157" class="text-white font-weight-bold">+91 9407000157</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="copy-right py-3 border-top" style="background: #091017; border-color: rgba(255,255,255,0.06) !important;">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-7 text-center text-md-left">
                        <p class="mb-0 text-muted small">&copy; 2026 <strong>Natasha &amp; Company</strong>. All Rights Reserved. | <a href="privacy-policy.html" class="text-muted">Privacy Policy</a> • <a href="terms-and-conditions.html" class="text-muted">Terms &amp; Conditions</a></p>
                    </div>
                    <div class="col-md-5 text-center text-md-right mt-2 mt-md-0">
                        <p class="mb-0 text-muted small">Designed for <strong>CA Natasha &amp; Co.</strong></p>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- FLOATING WHATSAPP -->
    <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20visited%20your%20website%20and%20need%20assistance." class="whatsapp-float" target="_blank" title="Chat on WhatsApp">
        <i class="fa fa-whatsapp"></i>
    </a>

    <!-- STICKY MOBILE BOTTOM ACTION BAR -->
    <div class="mobile-sticky-action-bar d-md-none">
        <a href="tel:+919407000157" class="sticky-action-btn call-btn">
            <i class="fa fa-phone"></i><span>Call</span>
        </a>
        <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20need%20assistance%20from%20your%20website." target="_blank" class="sticky-action-btn wa-btn">
            <i class="fa fa-whatsapp"></i><span>WhatsApp</span>
        </a>
        <button type="button" class="sticky-action-btn consult-btn border-0" onclick="$('#consultationModal').modal('show');" style="cursor: pointer; outline: none; background: var(--ca-primary, #006B63);">
            <i class="fa fa-calendar-check-o" style="pointer-events: none;"></i><span style="pointer-events: none;">Book CA</span>
        </button>
    </div>

    <!-- INTERACTIVE CONSULTATION BOOKING MODAL -->
    <div class="modal fade" id="consultationModal" tabindex="-1" role="dialog" aria-labelledby="consultModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content border-0 shadow-lg" style="border-radius: 12px; overflow: hidden;">
                <div class="modal-header text-white" style="background: var(--ca-primary, #006B63); border: none;">
                    <h5 class="modal-title font-weight-bold" id="consultModalLabel"><i class="fa fa-calendar-check-o mr-2"></i> Book CA Consultation</h5>
                    <button type="button" class="close text-white" data-dismiss="modal" aria-label="Close" style="opacity: 0.9;">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body p-4">
                    <p class="small text-muted mb-3">Connect directly with <strong>CA Natasha &amp; Co.</strong> for tailored tax planning, GST advice, company registration, or statutory audit.</p>
                    <form id="ca-quick-consult-form" onsubmit="handleConsultSubmit(event)">
                        <div class="form-group mb-3">
                            <label class="small font-weight-bold text-dark">Full Name *</label>
                            <input type="text" id="consult-name" class="form-control" placeholder="e.g. Rahul Sharma" required/>
                        </div>
                        <div class="form-group mb-3">
                            <label class="small font-weight-bold text-dark">Phone / WhatsApp Number *</label>
                            <input type="tel" id="consult-phone" class="form-control" placeholder="e.g. +91 9876543210" required/>
                        </div>
                        <div class="form-group mb-3">
                            <label class="small font-weight-bold text-dark">Select Service Required *</label>
                            <select id="consult-service" class="form-control" required>
                                <option value="Income Tax & ITR Filing">Income Tax Planning &amp; ITR Filing</option>
                                <option value="GST Registration & Notice Litigation">GST Registration &amp; Notice Defense</option>
                                <option value="Company / LLP Incorporation in Bhopal">Company / LLP Incorporation in Bhopal</option>
                                <option value="Statutory / Internal Audit">Statutory &amp; Internal Audit</option>
                                <option value="NGO / Trust 12A 80G Filings">NGO / Trust 12A &amp; 80G Filings</option>
                                <option value="General Financial Advisory">General Financial Advisory</option>
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label class="small font-weight-bold text-dark">Brief Message / Requirement</label>
                            <textarea id="consult-notes" class="form-control" rows="2" placeholder="Brief note about your requirement..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-block font-weight-bold text-white py-2" style="background: var(--ca-primary, #006B63); border-radius: 6px;">
                            <i class="fa fa-whatsapp mr-1"></i> Connect on WhatsApp
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/owl.carousel.min.js"></script>
    <script>
        // THEME SWITCHER LOGIC (EMERALD, B&W, SLATE GREY)
        function applyTheme(themeName) {
            $('body').removeClass('theme-bw theme-grey');
            if (themeName === 'bw') {
                $('body').addClass('theme-bw');
            } else if (themeName === 'grey') {
                $('body').addClass('theme-grey');
            }
            $('.theme-switch-btn').removeClass('active');
            $('.theme-switch-btn[data-theme="' + themeName + '"]').addClass('active');
            try { localStorage.setItem('canatasha_theme', themeName); } catch(e) {}
        }

        // Fast consultation form WhatsApp bridge
        function handleConsultSubmit(e) {
            e.preventDefault();
            var name = $('#consult-name').val();
            var phone = $('#consult-phone').val();
            var service = $('#consult-service').val();
            var notes = $('#consult-notes').val();
            
            var text = "Hello CA Natasha & Co.,\\n\\nI would like to book a consultation from your website.\\n\\n*Name:* " + name + "\\n*Phone:* " + phone + "\\n*Service:* " + service + (notes ? ("\\n*Note:* " + notes) : "");
            var waUrl = "https://wa.me/919407000157?text=" + encodeURIComponent(text);
            $('#consultationModal').modal('hide');
            window.open(waUrl, '_blank');
        }

        function handleQuickContact(e) {
            e.preventDefault();
            var name = $('#contact-name').val();
            var email = $('#contact-email').val();
            var phone = $('#contact-phone').val();
            var msg = $('#contact-msg').val();
            var text = "Hello CA Natasha & Co.,\\n\\n*New Inquiry from Website:*\\n*Name:* " + name + "\\n*Email:* " + email + "\\n*Phone:* " + phone + "\\n*Message:* " + msg;
            window.open("https://wa.me/919407000157?text=" + encodeURIComponent(text), '_blank');
        }

        $(document).ready(function(){
            // Load saved theme
            var savedTheme = 'emerald';
            try {
                var urlParams = new URLSearchParams(window.location.search);
                var queryTheme = urlParams.get('theme');
                if (queryTheme && (queryTheme === 'emerald' || queryTheme === 'bw' || queryTheme === 'grey')) {
                    savedTheme = queryTheme;
                } else {
                    savedTheme = localStorage.getItem('canatasha_theme') || 'emerald';
                }
            } catch(e) {}
            applyTheme(savedTheme);

            $('.theme-switch-btn').on('click', function(e){
                e.preventDefault();
                var theme = $(this).attr('data-theme');
                applyTheme(theme);
            });

            // Mobile Menu Drawer Toggle with Backdrop and Scroll Lock
            function openMobileMenu() {
                $('#mobile-toggle-btn').addClass('is-active');
                $('#mobile-menu-drawer').addClass('open');
                $('#mobile-backdrop').addClass('open');
                $('body').addClass('drawer-open');
            }
            function closeMobileMenu() {
                $('#mobile-toggle-btn').removeClass('is-active');
                $('#mobile-menu-drawer').removeClass('open');
                $('#mobile-backdrop').removeClass('open');
                $('body').removeClass('drawer-open');
            }

            $(document).on('click', '#mobile-toggle-btn', function(e){
                e.preventDefault();
                e.stopPropagation();
                if ($('#mobile-menu-drawer').hasClass('open')) {
                    closeMobileMenu();
                } else {
                    openMobileMenu();
                }
            });

            $(document).on('click', '.mobile-drawer-close-btn, #mobile-backdrop', function(e){
                e.preventDefault();
                closeMobileMenu();
            });

            $(document).on('click touchstart', '.theme-switch-btn', function(e){
                e.preventDefault();
                e.stopPropagation();
                var theme = $(this).attr('data-theme');
                if (theme) {
                    applyTheme(theme);
                }
            });

            $(document).on('click touchend', '#mobile-menu-drawer ul li a', function(e){
                var href = $(this).attr('href');
                if (href && href !== '#' && !href.startsWith('javascript:')) {
                    window.location.assign(href);
                }
            });

            $(document).on('click', '.consult-btn, [data-target="#consultationModal"]', function(e){
                e.preventDefault();
                $('#consultationModal').modal('show');
            });

            // REAL-TIME SCROLL-DRIVEN CINEMATIC SCENE CONTROLLER (60FPS GPU ENGINE)
            (function initCinematicScrollController() {
                var scenes = document.querySelectorAll('.cinematic-scene');
                if (!scenes.length) return;

                var ticking = false;
                function updateCinematicScenes() {
                    var winH = window.innerHeight || document.documentElement.clientHeight;
                    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

                    scenes.forEach(function(scene) {
                        var rect = scene.getBoundingClientRect();
                        
                        // 1. Scene entering from bottom
                        if (rect.top > 0 && rect.top < winH) {
                            var enterProgress = 1 - (rect.top / winH);
                            var scale = 1.05 - (enterProgress * 0.05); // 1.05 -> 1.00
                            var translateY = (1 - enterProgress) * 20; // 20px -> 0px
                            scene.style.transform = 'scale(' + scale.toFixed(3) + ') translateY(' + translateY.toFixed(1) + 'px)';
                            scene.style.opacity = Math.min(1, 0.65 + enterProgress * 0.35).toFixed(2);
                        }
                        // 2. Scene leaving towards top
                        else if (rect.top <= 0 && rect.bottom > 0) {
                            var leaveProgress = Math.min(1, Math.abs(rect.top) / (rect.height || winH));
                            var scale = 1.00 - (leaveProgress * 0.05); // 1.00 -> 0.95
                            var translateY = leaveProgress * -12;
                            scene.style.transform = 'scale(' + scale.toFixed(3) + ') translateY(' + translateY.toFixed(1) + 'px)';
                            scene.style.opacity = Math.max(0.75, (1 - leaveProgress * 0.25)).toFixed(2);
                        }
                        // 3. Fully inside view
                        else if (rect.top <= 0 && rect.bottom >= winH) {
                            scene.style.transform = 'scale(1) translateY(0px)';
                            scene.style.opacity = '1';
                        }
                    });

                    // Background parallax for Hero
                    var heroEl = document.querySelector('.static-hero-area');
                    if (heroEl && scrollY < 750) {
                        heroEl.style.backgroundPositionY = 'calc(50% + ' + (scrollY * 0.25) + 'px)';
                    }

                    ticking = false;
                }

                function onScroll() {
                    if (!ticking) {
                        window.requestAnimationFrame(updateCinematicScenes);
                        ticking = true;
                    }
                }

                window.addEventListener('scroll', onScroll, { passive: true });
                window.addEventListener('touchmove', onScroll, { passive: true });
                setTimeout(updateCinematicScenes, 80);
            })();

            // CINEMATIC STORYTELLING SCROLL REVEAL OBSERVER (MOVIE-LIKE ENTRANCES)
            (function initCinematicStorytellingObserver() {
                var revealElements = document.querySelectorAll(
                    '.cinematic-reveal, .single-item, .team-card-unified, .stat-counter-box, .review-card-item, .blog-card, .service-badge, .google-badge-box, .p-4.bg-white, .p-4.bg-light'
                );
                
                if (!revealElements.length) return;

                if ('IntersectionObserver' in window) {
                    var observer = new IntersectionObserver(function(entries) {
                        entries.forEach(function(entry) {
                            if (entry.isIntersecting) {
                                entry.target.classList.add('is-in-view');
                                
                                var counters = entry.target.querySelectorAll('.counter-val');
                                counters.forEach(function(c) {
                                    if (!c.getAttribute('data-counted')) {
                                        c.setAttribute('data-counted', 'true');
                                        var target = parseInt(c.getAttribute('data-target') || '0', 10);
                                        var suffix = c.getAttribute('data-suffix') || '';
                                        animateValue(c, 0, target, 1800, suffix);
                                    }
                                });
                            }
                        });
                    }, {
                        threshold: 0.08,
                        rootMargin: '0px 0px -20px 0px'
                    });

                    revealElements.forEach(function(el) {
                        observer.observe(el);
                    });
                } else {
                    revealElements.forEach(function(el) {
                        el.classList.add('is-in-view');
                    });
                }
            })();

            // SCROLL PROGRESS INDICATOR
            function updateScrollProgress() {
                var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                var scrolled = (winScroll / height) * 100;
                var bar = document.getElementById("scroll-progress-bar");
                if (bar) {
                    bar.style.width = scrolled + "%";
                }
            }
            window.addEventListener('scroll', updateScrollProgress, { passive: true });
            window.addEventListener('touchmove', updateScrollProgress, { passive: true });

            // HERO ZOOM-OUT ROTATOR
            (function initTemplate89ZoomOutRotator() {
                var $slides = $('.hero-zoom-slider .zoom-slide');
                if (!$slides.length) return;
                
                var currentIndex = 0;
                var totalSlides = $slides.length;
                var zoomTimer = null;
                var autoInterval = 3800;
                
                function goToSlide(nextIndex) {
                    if (nextIndex === currentIndex) return;
                    
                    var $current = $slides.eq(currentIndex);
                    var $next = $slides.eq(nextIndex);
                    
                    $current.addClass('leaving').removeClass('active');
                    
                    setTimeout(function(){
                        $current.removeClass('leaving');
                    }, 350);
                    
                    $next.addClass('active');
                    currentIndex = nextIndex;
                }
                
                function slideNext() {
                    var next = (currentIndex + 1) % totalSlides;
                    goToSlide(next);
                }
                
                function slidePrev() {
                    var prev = (currentIndex - 1 + totalSlides) % totalSlides;
                    goToSlide(prev);
                }
                
                function startAutoPlay() {
                    stopAutoPlay();
                    zoomTimer = setInterval(slideNext, autoInterval);
                }
                
                function stopAutoPlay() {
                    if (zoomTimer) clearInterval(zoomTimer);
                }
                
                var touchStartX = 0;
                var touchStartY = 0;
                var touchEndX = 0;
                var touchEndY = 0;
                var sliderEl = document.querySelector('.hero-zoom-slider') || document.querySelector('.static-hero-area');
                if (sliderEl) {
                    sliderEl.addEventListener('touchstart', function(e) {
                        if (e.touches && e.touches[0]) {
                            touchStartX = e.touches[0].clientX;
                            touchStartY = e.touches[0].clientY;
                        }
                        stopAutoPlay();
                    }, { passive: true });
                    
                    sliderEl.addEventListener('touchend', function(e) {
                        if (e.changedTouches && e.changedTouches[0]) {
                            touchEndX = e.changedTouches[0].clientX;
                            touchEndY = e.changedTouches[0].clientY;
                        }
                        var diffX = touchStartX - touchEndX;
                        var diffY = touchStartY - touchEndY;
                        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 30) {
                            if (diffX > 0) {
                                slideNext();
                            } else {
                                slidePrev();
                            }
                        }
                        startAutoPlay();
                    }, { passive: true });
                }
                
                setTimeout(function(){
                    $slides.eq(0).removeClass('active');
                    void $slides.eq(0)[0].offsetWidth;
                    $slides.eq(0).addClass('active');
                }, 60);

                startAutoPlay();
            })();

            // MULTI-SECTION AUTO ZOOM & SLIDE CAROUSEL ENGINE (MOBILE ONLY < 992px)
            function initMobileOnlyCarousels() {
                var isMobile = $(window).width() < 992;
                
                var mobileCarousels = [
                    { selector: '.services-auto-carousel', interval: 3200 },
                    { selector: '.team-auto-carousel', interval: 3400 },
                    { selector: '.track-record-auto-carousel', interval: 3300 },
                    { selector: '.blogs-auto-carousel', interval: 3500 }
                ];

                mobileCarousels.forEach(function(cfg) {
                    var $el = $(cfg.selector);
                    if ($el.length) {
                        if (isMobile) {
                            if (!$el.hasClass('owl-loaded')) {
                                $el.addClass('owl-carousel').owlCarousel({
                                    items: 1,
                                    loop: true,
                                    margin: 16,
                                    autoplay: true,
                                    autoplayTimeout: cfg.interval,
                                    autoplayHoverPause: false,
                                    smartSpeed: 650,
                                    dots: true,
                                    nav: false,
                                    touchDrag: true,
                                    mouseDrag: true
                                });
                            }
                        } else {
                            if ($el.hasClass('owl-loaded')) {
                                $el.trigger('destroy.owl.carousel').removeClass('owl-carousel owl-loaded');
                            }
                        }
                    }
                });
            }

            initMobileOnlyCarousels();
            $(window).on('resize', function(){
                initMobileOnlyCarousels();
            });

            // REVIEWS CAROUSEL (ALWAYS ACTIVE ON BOTH MOBILE & DESKTOP)
            if ($(".reviews-carousel").length) {
                var $revCarousel = $(".reviews-carousel").owlCarousel({
                    loop: true,
                    margin: 16,
                    autoplay: true,
                    autoplayTimeout: 3500,
                    autoplayHoverPause: false,
                    smartSpeed: 650,
                    responsive: {
                        0: { items: 1 },
                        768: { items: 1 },
                        992: { items: 2 }
                    },
                    dots: true,
                    nav: false,
                    touchDrag: true,
                    mouseDrag: true
                });

                setInterval(function(){
                    if ($revCarousel.length) {
                        $revCarousel.trigger('next.owl.carousel', [650]);
                    }
                }, 3500);
            }

            // Sticky Header
            function checkSticky() {
                var header = document.getElementById("header");
                if (!header) return;
                if (window.pageYOffset > 100) {
                    header.classList.add("fixedhead");
                } else {
                    header.classList.remove("fixedhead");
                }
            }
            window.addEventListener('scroll', checkSticky, { passive: true });

            // Count up numbers
            function animateValue(obj, start, end, duration, suffix) {
                let startTimestamp = null;
                const step = (timestamp) => {
                    if (!startTimestamp) startTimestamp = timestamp;
                    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                    const current = Math.floor(progress * (end - start) + start);
                    obj.innerHTML = current + suffix;
                    if (progress < 1) {
                        window.requestAnimationFrame(step);
                    }
                };
                window.requestAnimationFrame(step);
            }

            let animated = false;
            function checkCounters() {
                const statsSec = document.getElementById('trusted-stats-section');
                if (statsSec && !animated) {
                    const rect = statsSec.getBoundingClientRect();
                    if (rect.top < window.innerHeight && rect.bottom >= 0) {
                        animated = true;
                        document.querySelectorAll('.counter-val').forEach(el => {
                            const target = parseInt(el.getAttribute('data-target'));
                            const suffix = el.getAttribute('data-suffix') || '';
                            animateValue(el, 0, target, 1800, suffix);
                        });
                    }
                }
            }
            window.addEventListener('scroll', checkCounters, { passive: true });
            setTimeout(checkCounters, 200);
        });
    </script>
</body>
</html>"""

def master_layout(page_title, active_key, body_content, custom_meta=None):
    nav_items = [
        ("home", "index.html", "Home"),
        ("about", "about-us.html", "About Us"),
        ("services", "services.html", "Services"),
        ("knowledge", "knowledge-base.html", "Knowledge Base"),
        ("career", "career.html", "Career"),
        ("blog", "blog.html", "Blog"),
        ("contact", "contact-us.html", "Contact Us")
    ]

    desktop_nav_html = ""
    mobile_nav_html = ""

    for key, url, label in nav_items:
        is_active = (active_key == key)
        active_cls = 'active' if is_active else ''
        desktop_nav_html += f'<li class="{active_cls}"><a href="{url}">{label}</a></li>\n'
        mobile_nav_html += f'<li class="{active_cls}"><a href="{url}" class="mobile-nav-link" onclick="window.location.href=\'{url}\'; return true;"><span>{label}</span><i class="fa fa-angle-right nav-arrow"></i></a></li>\n'

    meta = custom_meta or seo_meta.get(active_key, {
        "title": f"{page_title} | Natasha & Company – Chartered Accountants",
        "description": "Natasha & Company is an ISO 9001:2015 Certified Chartered Accountancy firm in Bhopal offering Audit, Tax, GST, Corporate Law, and Business Advisory.",
        "keywords": "CA in Bhopal, Natasha and Company, Chartered Accountants MP Nagar",
        "url": "https://canatasha-website.vercel.app/"
    })

    html = master_layout_template
    html = html.replace("__PAGE_TITLE__", page_title)
    html = html.replace("__META_TITLE__", meta['title'])
    html = html.replace("__META_DESC__", meta['description'])
    html = html.replace("__META_KEYWORDS__", meta['keywords'])
    html = html.replace("__CANONICAL_URL__", meta['url'])
    html = html.replace("__SCHEMA_JSON__", schema_json_str)
    html = html.replace("__MASTER_CSS__", master_css)
    html = html.replace("__DESKTOP_NAV__", desktop_nav_html)
    html = html.replace("__MOBILE_NAV__", mobile_nav_html)
    html = html.replace("__BODY_CONTENT__", body_content)
    return html

# Write all 9 master pages
pages = [
    ("index.html", "Home", "home", home_body),
    ("about-us.html", "About Us", "about", about_us_body),
    ("services.html", "Our Services", "services", services_body),
    ("knowledge-base.html", "Knowledge Base & Calculators", "knowledge", knowledge_base_body),
    ("career.html", "Career & Articleship", "career", career_body),
    ("blog.html", "Blog & Insights", "blog", blog_body_resolved),
    ("contact-us.html", "Contact Us", "contact", contact_us_body),
    ("privacy-policy.html", "Privacy Policy", "privacy", privacy_policy_body),
    ("terms-and-conditions.html", "Terms & Conditions", "terms", terms_and_conditions_body)
]

for filename, title, key, body in pages:
    filepath = os.path.join(dest_dir, filename)
    with open(filepath, "w", encoding="utf-8") as fp:
        fp.write(master_layout(title, key, body))
    print(f"Generated page: {filename}")

# Generate all single blog pages
for p in curated_posts:
    custom_blog_meta = {
        "title": f"{p['title']} | CA Natasha & Co. Bhopal",
        "description": p['excerpt'],
        "keywords": f"{p['category']}, CA Bhopal, Tax Updates, {p['title']}",
        "url": f"https://canatasha-website.vercel.app/{p['slug']}.html"
    }
    post_html = f"""
    <div class="page-banner">
        <div class="container">
            <span class="badge badge-warning mb-2 px-3 py-1 text-dark font-weight-bold">{p['category']}</span>
            <h1 style="font-size: 32px; max-width: 850px; margin: 0 auto 10px;">{p['title']}</h1>
            <p><i class="fa fa-user-circle mr-1"></i> {p['author']} &bull; <i class="fa fa-calendar ml-2 mr-1"></i> {p['date']} &bull; <i class="fa fa-clock-o ml-2 mr-1"></i> {p['read_time']}</p>
        </div>
    </div>

    <section class="py-5" style="background-color: #f8fafc;">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="bg-white p-4 p-md-5 rounded shadow-sm border mb-4">
                        <div class="mb-4 text-center overflow-hidden rounded">
                            <img src="{p['img']}" class="img-fluid rounded shadow-sm w-100" style="max-height: 440px; object-fit: cover;" alt="{p['title']}" loading="lazy" decoding="async" onerror="this.src='images/banner-1.webp'"/>
                        </div>
                        
                        <div class="article-content" style="font-size: 16px; line-height: 1.85; color: #334155;">
                            <p class="lead font-weight-normal text-muted mb-4">{p['excerpt']}</p>
                            
                            <h4 class="font-weight-bold mb-3" style="color: #002e5b;">Strategic Analysis &amp; Practical Implications</h4>
                            <p>In today's fast-evolving regulatory landscape, having absolute clarity on statutory mandates and financial positioning is the cornerstone of sustainable growth. At <strong>Natasha &amp; Company</strong>, our advisory desk continually monitors legislative updates under the Direct Tax Code, GST enactments, and Corporate Laws to provide proactive guidance.</p>
                            
                            <div class="p-4 bg-light rounded border-left border-success my-4" style="border-left-width: 5px !important;">
                                <h6 class="font-weight-bold text-success mb-2"><i class="fa fa-check-circle mr-1"></i> Key Takeaway for Businesses &amp; Investors:</h6>
                                <p class="small mb-0 text-dark">Ensure proper documentation, timely reconciliations with official government portals (AIS/TIS, GSTR-2B), and consult a certified Chartered Accountant prior to major financial commitments.</p>
                            </div>

                            <p>For dedicated assistance, custom financial modeling, or filing representations, our experienced team of Chartered Accountants in Bhopal is always ready to guide you.</p>
                        </div>

                        <div class="mt-5 p-4 rounded bg-light border">
                            <div class="d-flex align-items-center">
                                <img src="images/team-1.webp" class="rounded-circle mr-3" style="width: 70px; height: 70px; object-fit: cover; border: 2px solid #006B63;" loading="lazy" decoding="async" onerror="this.src='images/team-1.webp'"/>
                                <div>
                                    <h6 class="font-weight-bold mb-1" style="color: #002e5b;">Published by CA Natasha &amp; Company</h6>
                                    <p class="small text-muted mb-0">ISO 9001:2015 Certified Chartered Accountant Firm in Bhopal | Tax, Audit, Compliances.</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-4 text-center">
                            <a href="https://wa.me/919407000157?text=Hello%20CA%20Natasha%2C%20I%20read%20your%20article%20'{p['title'][:35]}'%20and%20would%20like%20to%20consult." target="_blank" class="btn btn-success px-4 py-2 font-weight-bold shadow">
                                <i class="fa fa-whatsapp mr-1"></i> Consult CA Natasha on this Topic
                            </a>
                            <a href="blog.html" class="btn btn-outline-dark px-4 py-2 font-weight-bold ml-2">
                                <i class="fa fa-th-large mr-1"></i> Back to All Blogs
                            </a>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4">
                    <div class="bg-white p-4 rounded shadow-sm border mb-4 text-center">
                        <img src="images/team-1.webp" alt="CA Natasha" style="width: 95px; height: 95px; border-radius: 50%; object-fit: cover;" loading="lazy" decoding="async" onerror="this.src='images/team-1.webp'"/>
                        <h5 class="font-weight-bold mb-1 mt-2" style="color: #002e5b;">CA Natasha Rajvaidya</h5>
                        <span class="badge badge-success px-3 py-1 mb-2" style="background-color: #006B63;">Founder &amp; Principal Partner</span>
                        <p class="text-muted small mt-2">Expert in Direct Tax planning, Statutory Audits, Corporate Law, and Startup Advisory in Bhopal.</p>
                        <a href="contact-us.html" class="btn btn-sm btn-outline-dark font-weight-bold px-3">Contact Firm</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    with open(os.path.join(dest_dir, f"{p['slug']}.html"), "w", encoding="utf-8") as fp:
        fp.write(master_layout(p['title'], 'blog', post_html, custom_meta=custom_blog_meta))

print("Master site built successfully with full rich subpages, balanced team cards, and clean theme switcher!")
