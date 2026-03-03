#!/usr/bin/env python3
"""
generate_index.py — BizOPS index.html 자동 생성 스크립트

HTML 파일을 스캔하여 prefix 기반 카테고리 분류 후 index.html을 생성한다.
GitHub Actions에서 push 이벤트 시 자동 실행된다.

사용법:
    python scripts/generate_index.py          # 리포 루트에서 실행
    python scripts/generate_index.py --dry-run  # 변경 없이 stdout 출력
"""

import os
import re
import sys
from datetime import datetime, timezone, timedelta

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

# 상단 KPI 스탯 그룹
STAT_GROUPS = [
    {"id": "cs", "label": "CS 운영"},
    {"id": "chatbot", "label": "AI 챗봇"},
    {"id": "chargeback", "label": "차지백"},
    {"id": "ip", "label": "IP 보호"},
    {"id": "dashboard", "label": "대시보드"},
]

# 섹션 정의 (표시 순서)
SECTIONS = [
    {"id": "cs_manual",     "title": "CS 운영 매뉴얼",              "icon": "M", "ic": "ic-blue",   "stat": "cs"},
    {"id": "cs_analysis",   "title": "CS 분석 · 시각화",            "icon": "A", "ic": "ic-cyan",   "stat": "cs"},
    {"id": "cs_process",    "title": "CS 프로세스",                 "icon": "P", "ic": "ic-green",  "stat": "cs"},
    {"id": "chargeback",    "title": "차지백",                      "icon": "$", "ic": "ic-amber",  "stat": "chargeback"},
    {"id": "chatbot_plan",  "title": "AI 챗봇 — 기획 · 개요",      "icon": "B", "ic": "ic-purple", "stat": "chatbot"},
    {"id": "chatbot_ops",   "title": "AI 챗봇 — 운영 · 교육",      "icon": "O", "ic": "ic-purple", "stat": "chatbot"},
    {"id": "chatbot_flow",  "title": "AI 챗봇 — 플로우 · 에스컬레이션", "icon": "F", "ic": "ic-purple", "stat": "chatbot"},
    {"id": "ip_ops",        "title": "IP 보호 운영",                "icon": "IP","ic": "ic-green",  "stat": "ip"},
    {"id": "weekly",        "title": "주간 리포트",                 "icon": "R", "ic": "ic-cyan",   "stat": "cs"},
    {"id": "dashboard",     "title": "대시보드",                    "icon": "D", "ic": "ic-blue",   "stat": "dashboard"},
    {"id": "other",         "title": "기타",                        "icon": "?", "ic": "ic-blue",   "stat": "cs"},
]

# 파일명 prefix → (section_id, card_icon, badge_class)
# 긴 prefix 우선 매칭 (순서 중요)
PREFIX_RULES = [
    # CS 매뉴얼
    ("cs_manual_enhanced",      "cs_manual",    "+",  "bg-blue"),
    ("cs_manual_EN",            "cs_manual",    "EN", "bg-blue"),
    ("cs_manual_KO",            "cs_manual",    "KO", "bg-blue"),
    ("cs_manual",               "cs_manual",    "M",  "bg-blue"),
    ("cs_repeat",               "cs_manual",    "R",  "bg-blue"),
    # CS 분석
    ("cs_l1_l2_l3",             "cs_analysis",  "L",  "bg-cyan"),
    ("cs_weekly_analysis",      "weekly",       "W",  "bg-cyan"),
    ("cs_weekly",               "weekly",       "W",  "bg-cyan"),
    ("cs_infographic",          "cs_analysis",  "I",  "bg-cyan"),
    ("cs_fraud",                "cs_analysis",  "F",  "bg-red"),
    # CS 프로세스
    ("cs_flow",                 "cs_process",   "F",  "bg-green"),
    ("cs_automation",           "cs_process",   "R",  "bg-green"),
    ("chargeback_flow",         "cs_process",   "C",  "bg-amber"),
    # 차지백
    ("chargeback_operation",    "chargeback",   "M",  "bg-amber"),
    ("chargeback_sample",       "chargeback",   "T",  "bg-amber"),
    ("chargeback_template",     "chargeback",   "X",  "bg-slate"),
    # 챗봇 — 기획
    ("chatbot_one_pager",       "chatbot_plan", "1P", "bg-purple"),
    ("chatbot_system",          "chatbot_plan", "S",  "bg-purple"),
    ("chatbot_roadmap",         "chatbot_plan", "R",  "bg-purple"),
    ("chatbot_cost",            "chatbot_plan", "$",  "bg-purple"),
    ("chatbot_infographic",     "chatbot_plan", "I",  "bg-purple"),
    # 챗봇 — 운영
    ("chatbot_operations",      "chatbot_ops",  "M",  "bg-purple"),
    ("chatbot_cs_operator",     "chatbot_ops",  "G",  "bg-purple"),
    ("chatbot_training_test",   "chatbot_ops",  "Q",  "bg-purple"),
    ("chatbot_training",        "chatbot_ops",  "T",  "bg-purple"),
    ("chatbot_demo",            "chatbot_ops",  "D",  "bg-purple"),
    # 챗봇 — 플로우
    ("chatbot_flow_simple",     "chatbot_flow", "S",  "bg-purple"),
    ("chatbot_flow_diagram",    "chatbot_flow", "D",  "bg-purple"),
    ("chatbot_flow",            "chatbot_flow", "F",  "bg-purple"),
    ("chatbot_escalation",      "chatbot_flow", "E",  "bg-purple"),
    # IP 보호
    ("ip_ops",                  "ip_ops",       "M",  "bg-green"),
    # 주간 리포트
    ("chatbot_weekly",          "weekly",       "W",  "bg-cyan"),
    ("weekly_reports",          "weekly",       "A",  "bg-cyan"),
    # 개인정보 / 컴플라이언스 — 인덱스 제외 (EXCLUDED 참조)
    # ("personal_info",           "cs_manual",    "PI", "bg-green"),
    # 차지백 (대문자 시작 엑셀)
    ("Chargeback_Evidence",     "chargeback",   "T",  "bg-amber"),
    ("Chargeback_Explanation",  "chargeback",   "E",  "bg-amber"),
    # 대시보드
    ("ticket_dashboard_manual", "dashboard",    "M",  "bg-blue"),
    ("ticket_dashboard",        "dashboard",    "V",  "bg-blue"),
]


# ──────────────────────────────────────────────
# File scanning
# ──────────────────────────────────────────────

def extract_title(filepath):
    """HTML <title> 태그에서 문서 제목 추출."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            head = f.read(8000)
        m = re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S)
        if m:
            title = m.group(1).strip()
            # Remove common suffixes
            for suffix in [" | Toomics", " — Toomics", " - Toomics"]:
                if title.endswith(suffix):
                    title = title[: -len(suffix)]
            return title
    except Exception:
        pass
    name = os.path.splitext(os.path.basename(filepath))[0]
    return name.replace("_", " ").title()


def extract_description(filepath):
    """HTML meta description 추출."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            head = f.read(8000)
        m = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            head,
            re.I,
        )
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return ""


def detect_width(filepath):
    """파일 내 max-width 감지하여 960px/1280px 판별."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            head = f.read(15000)
        if "1280" in head or "max-w-wide" in head:
            return "1280px"
    except Exception:
        pass
    return "960px"


def classify_file(filename):
    """파일명을 prefix 규칙에 따라 분류. (section_id, icon, badge_class) 반환."""
    name = os.path.splitext(filename)[0]
    is_xlsx = filename.endswith(".xlsx")

    for prefix, section_id, icon, badge_class in PREFIX_RULES:
        if name.startswith(prefix):
            return section_id, icon, ("bg-slate" if is_xlsx else badge_class)

    return "other", "?", "bg-slate"


def scan_files(directory):
    """디렉토리에서 index.html 제외한 모든 산출물 파일 목록 반환. 중복 버전은 최신만 유지."""
    # 인덱스에서 완전히 제외할 파일
    EXCLUDED = {"personal_info_evidence_EA2_EA37_EA56_EA57.html"}

    raw = []
    for f in sorted(os.listdir(directory)):
        if f == "index.html" or f in EXCLUDED:
            continue
        if f.endswith(".html") or f.endswith(".xlsx"):
            raw.append(f)

    # 버전/날짜 중복 제거: 같은 base name에서 최신 버전만 유지
    groups = {}
    for f in raw:
        name = os.path.splitext(f)[0]
        ext = os.path.splitext(f)[1]

        # 주간보고는 w2w3, w4 등으로 다르므로 중복이 아님
        if re.search(r'_w\d', name, re.I):
            key = f
        else:
            # 1) _vN 버전 제거 (대소문자 모두)
            base = re.sub(r'_[vV]\d+$', '', name)
            # 2) _enhanced 접미사 제거
            base = re.sub(r'_enhanced$', '', base)
            # 3) 끝의 _YYYYMMDD 날짜 제거 (같은 문서의 날짜별 중복)
            #    단, 날짜 뒤에 _detail 같은 접미사가 있으면 별개 문서
            date_stripped = re.sub(r'_\d{8}$', '', base)
            # 4) 날짜 제거 후 남은 게 있으면 날짜 기반 그룹, 아니면 원본 유지
            if date_stripped != base:
                key = date_stripped + ext
            else:
                key = base + ext

        groups.setdefault(key, []).append(f)

    # 각 그룹에서 최신(마지막 정렬) 파일만 유지
    result = []
    for key, flist in groups.items():
        result.append(sorted(flist)[-1])

    return sorted(result)


def build_file_entries(directory, files):
    """파일 목록을 섹션별로 분류하여 엔트리 생성."""
    sections = {s["id"]: [] for s in SECTIONS}

    for fname in files:
        fpath = os.path.join(directory, fname)
        section_id, icon, badge_class = classify_file(fname)

        if fname.endswith(".xlsx"):
            title = fname.replace("_", " ").replace(".xlsx", "").title()
            desc = "Excel 다운로드"
            badge_text = "XLSX"
        else:
            title = extract_title(fpath)
            desc = extract_description(fpath)
            badge_text = detect_width(fpath)

        sections[section_id].append(
            {
                "filename": fname,
                "title": title,
                "desc": desc,
                "icon": icon,
                "badge_class": badge_class,
                "badge_text": badge_text,
            }
        )

    return sections


# ──────────────────────────────────────────────
# HTML Generation
# ──────────────────────────────────────────────

CSS = """\
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',-apple-system,sans-serif;
    background: #F8FAFC; color: #1E293B;
    font-size: 14px; line-height: 1.7;
    word-break: keep-all; overflow-wrap: break-word;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  .hero {
    background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 50%, #0EA5E9 100%);
    color: #fff; padding: 48px 24px; text-align: center;
  }
  .hero-badge {
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 20px;
    padding: 4px 14px; font-size: 12px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 14px;
  }
  .hero h1 { font-size: 32px; font-weight: 800; margin-bottom: 8px; }
  .hero .subtitle { font-size: 16px; opacity: 0.85; }
  .hero-meta {
    display: flex; justify-content: center; gap: 24px;
    margin-top: 20px; font-size: 12px; opacity: 0.75;
  }
  .container { max-width: 1280px; margin: 0 auto; padding: 32px 24px 64px; }
  .stats {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px; margin-bottom: 40px;
  }
  .stat-card {
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 20px; text-align: center;
    border-top: 3px solid #2563EB;
  }
  .stat-card .num { font-size: 28px; font-weight: 800; font-variant-numeric: tabular-nums; }
  .stat-card .lbl { font-size: 12px; color: #475569; margin-top: 4px; }
  .stat-card:nth-child(2) { border-top-color: #0EA5E9; }
  .stat-card:nth-child(3) { border-top-color: #10B981; }
  .stat-card:nth-child(4) { border-top-color: #F59E0B; }
  .stat-card:nth-child(5) { border-top-color: #7C3AED; }
  .section { margin-bottom: 36px; }
  .section-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 18px; font-weight: 800; margin-bottom: 16px;
    padding-bottom: 10px; border-bottom: 2px solid #E2E8F0;
  }
  .section-title .icon {
    width: 28px; height: 28px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: #fff; flex-shrink: 0;
  }
  .section-title .count {
    margin-left: auto; font-size: 12px; font-weight: 600;
    color: #94A3B8; background: #F1F5F9;
    padding: 2px 10px; border-radius: 12px;
  }
  .link-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 12px;
  }
  .link-card {
    display: flex; align-items: center; gap: 14px;
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 16px 18px;
    text-decoration: none; color: #1E293B;
    transition: border-color 0.15s, box-shadow 0.15s;
    border-left: 4px solid transparent;
  }
  .link-card:hover {
    border-color: #2563EB; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border-left-color: #2563EB;
  }
  .link-card .lc-icon {
    width: 36px; height: 36px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
  }
  .link-card .lc-body { flex: 1; min-width: 0; overflow: hidden; }
  .link-card .lc-title {
    font-size: 14px; font-weight: 700;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .link-card .lc-desc { font-size: 12px; color: #475569; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }
  .link-card .lc-badge {
    font-size: 10.5px; font-weight: 700; padding: 2px 8px;
    border-radius: 6px; white-space: nowrap;
  }
  .bg-blue   { background: #EFF6FF; color: #2563EB; }
  .bg-cyan   { background: #ECFEFF; color: #0891B2; }
  .bg-green  { background: #ECFDF5; color: #059669; }
  .bg-amber  { background: #FFFBEB; color: #D97706; }
  .bg-red    { background: #FEF2F2; color: #DC2626; }
  .bg-purple { background: #F5F3FF; color: #7C3AED; }
  .bg-slate  { background: #F1F5F9; color: #475569; }
  .ic-blue   { background: #2563EB; }
  .ic-cyan   { background: #0EA5E9; }
  .ic-green  { background: #10B981; }
  .ic-amber  { background: #F59E0B; }
  .ic-red    { background: #EF4444; }
  .ic-purple { background: #7C3AED; }
  .footer {
    text-align: center; padding: 24px; font-size: 12px;
    color: #94A3B8; border-top: 1px solid #E2E8F0; margin-top: 40px;
  }
  @media print {
    .hero { padding: 24px; }
    .link-card { break-inside: avoid; }
    .link-card::after { content: " (" attr(href) ")"; font-size: 10px; color: #94A3B8; }
  }
  @media (max-width: 600px) {
    .link-grid { grid-template-columns: 1fr; }
    .stats { grid-template-columns: repeat(2, 1fr); }
    .hero h1 { font-size: 24px; }
  }
"""


def escape(text):
    """HTML 이스케이프."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_html(sections_data, total_count, today_str):
    """전체 index.html 생성."""
    # Stat group counts
    stat_counts = {sg["id"]: 0 for sg in STAT_GROUPS}
    for sec in SECTIONS:
        count = len(sections_data.get(sec["id"], []))
        if sec["stat"] in stat_counts:
            stat_counts[sec["stat"]] += count

    lines = []
    lines.append("<!DOCTYPE html>")
    lines.append('<html lang="ko">')
    lines.append("<head>")
    lines.append('<meta charset="UTF-8">')
    lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append('<meta name="author" content="유종선">')
    lines.append('<meta name="description" content="Toomics Global BizOps — 산출물 인덱스">')
    lines.append("<title>BizOps 산출물 | Toomics Global</title>")
    lines.append("<style>")
    lines.append(CSS)
    lines.append("</style>")
    lines.append("</head>")
    lines.append("<body>")
    lines.append("")

    # Hero
    lines.append('<header class="hero">')
    lines.append('  <div class="hero-badge">Document Index</div>')
    lines.append("  <h1>BizOps 산출물</h1>")
    lines.append('  <div class="subtitle">Toomics Global · BizOps팀</div>')
    lines.append('  <div class="hero-meta">')
    lines.append("    <span>작성자: 유종선</span>")
    lines.append(f"    <span>최종 업데이트: {today_str}</span>")
    lines.append(f"    <span>문서 {total_count}건</span>")
    lines.append("  </div>")
    lines.append("</header>")
    lines.append("")

    # Stats
    lines.append('<div class="container">')
    lines.append('  <div class="stats">')
    for sg in STAT_GROUPS:
        cnt = stat_counts[sg["id"]]
        lines.append(
            f'    <div class="stat-card"><div class="num">{cnt}</div>'
            f'<div class="lbl">{escape(sg["label"])}</div></div>'
        )
    lines.append("  </div>")
    lines.append("")

    # Sections
    for sec in SECTIONS:
        entries = sections_data.get(sec["id"], [])
        if not entries:
            continue

        lines.append(f'  <div class="section">')
        lines.append(f'    <h2 class="section-title">')
        lines.append(
            f'      <span class="icon {sec["ic"]}">{escape(sec["icon"])}</span> {escape(sec["title"])}'
        )
        lines.append(f'      <span class="count">{len(entries)}건</span>')
        lines.append(f"    </h2>")
        lines.append(f'    <div class="link-grid">')

        for entry in entries:
            lines.append(f'      <a class="link-card" href="{escape(entry["filename"])}">')
            lines.append(
                f'        <span class="lc-icon {entry["badge_class"]}">{escape(entry["icon"])}</span>'
            )
            lines.append(f'        <span class="lc-body">')
            lines.append(f'          <span class="lc-title">{escape(entry["title"])}</span>')
            if entry["desc"]:
                lines.append(
                    f'          <span class="lc-desc">{escape(entry["desc"])}</span>'
                )
            lines.append(f"        </span>")
            lines.append(
                f'        <span class="lc-badge {entry["badge_class"]}">{escape(entry["badge_text"])}</span>'
            )
            lines.append(f"      </a>")

        lines.append(f"    </div>")
        lines.append(f"  </div>")
        lines.append("")

    # Footer
    lines.append("</div>")
    lines.append("")
    lines.append('<footer class="footer">')
    lines.append(f"  Toomics Global · BizOps Team · 유종선 · {today_str[:4]}")
    lines.append("</footer>")
    lines.append("")
    lines.append("</body>")
    lines.append("</html>")

    return "\n".join(lines) + "\n"


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────


def generate_weekly_archive(directory, today_str):
    """주간 리포트 아카이브 페이지 자동 생성."""
    weekly_files = []
    for f in sorted(os.listdir(directory), reverse=True):
        if f == "weekly_reports.html" or f == "index.html":
            continue
        if not (f.endswith(".html")):
            continue
        name = os.path.splitext(f)[0]
        if name.startswith("cs_weekly") or name.startswith("chatbot_weekly"):
            title = extract_title(os.path.join(directory, f))
            desc = extract_description(os.path.join(directory, f))
            # Extract date from filename
            dm = re.search(r'(\d{8})', name)
            date_str = dm.group(1) if dm else ""
            if date_str:
                date_fmt = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}"
            else:
                date_fmt = ""
            # Detect week label
            wm = re.search(r'_(w\d\w*)', name, re.I)
            week_label = wm.group(1).upper() if wm else ""
            weekly_files.append({
                "filename": f,
                "title": title,
                "desc": desc,
                "date": date_fmt,
                "week": week_label,
            })

    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append('<html lang="ko">')
    lines.append('<head>')
    lines.append('<meta charset="UTF-8">')
    lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append('<meta name="author" content="유종선">')
    lines.append('<meta name="description" content="Toomics Global BizOps — 주간 보고서 아카이브">')
    lines.append('<title>BizOps 주간 보고서 아카이브 | Toomics Global</title>')
    lines.append('<style>')
    lines.append('*{margin:0;padding:0;box-sizing:border-box}')
    lines.append("body{font-family:'Malgun Gothic','Noto Sans KR',sans-serif;background:#F8FAFC;color:#1E293B;font-size:14px;line-height:1.7}")
    lines.append('.hero{background:linear-gradient(135deg,#0F4C81 0%,#0EA5E9 50%,#38BDF8 100%);color:#fff;padding:48px 24px;text-align:center}')
    lines.append('.hero-badge{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);border-radius:20px;padding:4px 14px;font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px}')
    lines.append('.hero h1{font-size:28px;font-weight:800;margin-bottom:8px}.hero .subtitle{font-size:15px;opacity:.85}')
    lines.append('.container{max-width:960px;margin:0 auto;padding:32px 24px 64px}')
    lines.append('.back-link{display:inline-block;margin-bottom:24px;color:#2563EB;text-decoration:none;font-size:13px;font-weight:600}')
    lines.append('.back-link:hover{text-decoration:underline}')
    lines.append('.report-card{display:block;background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;margin-bottom:12px;text-decoration:none;color:#1E293B;transition:border-color .15s,box-shadow .15s;border-left:4px solid #0EA5E9}')
    lines.append('.report-card:hover{border-color:#2563EB;box-shadow:0 4px 12px rgba(0,0,0,.06);border-left-color:#2563EB}')
    lines.append('.report-card .rc-meta{display:flex;gap:12px;align-items:center;margin-bottom:6px}')
    lines.append('.report-card .rc-week{background:#EFF6FF;color:#2563EB;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:700}')
    lines.append('.report-card .rc-date{font-size:12px;color:#94A3B8}')
    lines.append('.report-card .rc-title{font-size:15px;font-weight:700}')
    lines.append('.report-card .rc-desc{font-size:12px;color:#475569;margin-top:4px}')
    lines.append('.footer{text-align:center;padding:24px;font-size:12px;color:#94A3B8;border-top:1px solid #E2E8F0;margin-top:40px}')
    lines.append('</style>')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('<header class="hero">')
    lines.append('  <div class="hero-badge">Weekly Report Archive</div>')
    lines.append('  <h1>주간 보고서 아카이브</h1>')
    lines.append(f'  <div class="subtitle">총 {len(weekly_files)}건 · 최종 업데이트 {today_str}</div>')
    lines.append('</header>')
    lines.append('<div class="container">')
    lines.append('<a class="back-link" href="index.html">← 산출물 인덱스로</a>')
    for entry in weekly_files:
        lines.append(f'<a class="report-card" href="{escape(entry["filename"])}">')
        lines.append(f'  <div class="rc-meta">')
        if entry["week"]:
            lines.append(f'    <span class="rc-week">{escape(entry["week"])}</span>')
        lines.append(f'    <span class="rc-date">{escape(entry["date"])}</span>')
        lines.append(f'  </div>')
        lines.append(f'  <div class="rc-title">{escape(entry["title"])}</div>')
        if entry["desc"]:
            lines.append(f'  <div class="rc-desc">{escape(entry["desc"])}</div>')
        lines.append(f'</a>')
    lines.append('</div>')
    lines.append(f'<footer class="footer">Toomics Global · BizOps Team · 유종선 · {today_str[:4]}</footer>')
    lines.append('</body>')
    lines.append('</html>')
    return "\n".join(lines) + "\n"


def main():
    dry_run = "--dry-run" in sys.argv

    # Determine repo root (script is in scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    os.chdir(repo_root)

    # Today (KST)
    kst = timezone(timedelta(hours=9))
    today_str = datetime.now(kst).strftime("%Y-%m-%d")

    # Generate weekly archive first
    archive_html = generate_weekly_archive(".", today_str)
    archive_path = os.path.join(repo_root, "weekly_reports.html")
    if not dry_run:
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(archive_html)
        print("weekly_reports.html updated.")

    # Scan files — weekly files excluded from main index (they go through archive)
    files = scan_files(".")
    if not files:
        print("No deliverable files found.", file=sys.stderr)
        sys.exit(1)

    # Remove individual weekly files from main index, keep only weekly_reports.html
    files = [f for f in files if not (
        (f.startswith("cs_weekly") or f.startswith("chatbot_weekly")) and f != "weekly_reports.html"
    )]

    # Build entries
    sections_data = build_file_entries(".", files)
    total = len(files)

    # Generate
    html = generate_html(sections_data, total, today_str)

    if dry_run:
        print(html)
        print(f"\n[DRY RUN] {total} files detected.", file=sys.stderr)
    else:
        # Check if changed
        index_path = os.path.join(repo_root, "index.html")
        old_content = ""
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                old_content = f.read()

        if html == old_content:
            print(f"index.html is up to date ({total} files).")
        else:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"index.html updated ({total} files).")


if __name__ == "__main__":
    main()
