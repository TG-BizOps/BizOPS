#!/usr/bin/env python3
"""Build index.html from docs.json — BizOps Portal build system."""
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# CSS (verbatim from original index.html lines 9-484)
# ---------------------------------------------------------------------------
CSS = """\
<style>
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

  /* Stat Cards */
  .stats {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px; margin-bottom: 40px;
  }
  .stat-card {
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 20px; text-align: center;
    border-top: 3px solid #2563EB;
    text-decoration: none; color: #1E293B;
    transition: box-shadow 0.15s, transform 0.15s;
    cursor: pointer;
  }
  .stat-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); transform: translateY(-2px); }
  .stat-card .num { font-size: 28px; font-weight: 800; font-variant-numeric: tabular-nums; }
  .stat-card .lbl { font-size: 12px; color: #475569; margin-top: 4px; }

  /* Accordion */
  .accordion { margin-bottom: 16px; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; }
  .accordion-header {
    display: flex; align-items: center; gap: 10px;
    padding: 16px 20px; background: #fff; cursor: pointer;
    font-size: 16px; font-weight: 800; user-select: none;
    transition: background 0.15s;
    border: none; width: 100%; text-align: left; color: #1E293B;
    font-family: inherit; line-height: 1.7;
  }
  .accordion-header:hover { background: #F8FAFC; }
  .accordion-header .icon {
    width: 28px; height: 28px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; color: #fff; flex-shrink: 0;
  }
  .accordion-header .count {
    font-size: 12px; font-weight: 600;
    color: #94A3B8; background: #F1F5F9;
    padding: 2px 10px; border-radius: 12px;
  }
  .accordion-header .chevron {
    width: 20px; height: 20px; flex-shrink: 0;
    transition: transform 0.25s ease;
    color: #94A3B8; margin-left: auto;
  }
  .accordion.open .accordion-header .chevron { transform: rotate(180deg); }
  .accordion-body {
    max-height: 0; overflow: hidden;
    transition: max-height 0.35s ease;
    background: #F8FAFC;
  }
  .accordion.open .accordion-body { max-height: 2000px; }
  .accordion-body-inner { padding: 8px 20px 20px; }

  /* Link Grid */
  .link-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 10px;
  }
  .link-card {
    display: flex; align-items: center; gap: 14px;
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 10px; padding: 14px 16px;
    text-decoration: none; color: #1E293B;
    transition: border-color 0.15s, box-shadow 0.15s;
    border-left: 4px solid transparent;
  }
  .link-card:hover {
    border-color: #2563EB; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border-left-color: #2563EB;
  }
  .link-card .lc-icon {
    width: 34px; height: 34px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; flex-shrink: 0;
  }
  .link-card .lc-body { flex: 1; min-width: 0; overflow: hidden; }
  .link-card .lc-title {
    font-size: 13px; font-weight: 700;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .link-card .lc-desc { font-size: 11px; color: #475569; margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }
  .link-card .lc-badge {
    font-size: 10px; font-weight: 700; padding: 2px 8px;
    border-radius: 6px; white-space: nowrap;
  }

  .link-card .lc-version {
    font-size: 10px; font-weight: 700; padding: 1px 6px;
    border-radius: 4px; white-space: nowrap; flex-shrink: 0;
    background: #F1F5F9; color: #64748B;
  }

  /* Color Tokens */
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
  .ic-slate  { background: #475569; }

  /* History */
  .history-details {
    margin-top: 48px; border-top: 1px solid #E2E8F0; padding-top: 20px;
  }
  .history-summary {
    font-size: 13px; font-weight: 600; color: #94A3B8;
    padding: 8px 0; display: flex; align-items: center; gap: 6px;
  }
  .history-summary .count {
    font-size: 11px; font-weight: 600; color: #94A3B8;
    background: #F1F5F9; padding: 1px 8px; border-radius: 10px;
  }
  .history-content { padding-top: 12px; }
  .history-list { list-style: none; }
  .history-item {
    display: flex; gap: 12px; padding: 10px 0;
    border-bottom: 1px solid #E2E8F0; font-size: 13px;
  }
  .history-item:last-child { border-bottom: none; }
  .history-date {
    flex-shrink: 0; font-weight: 700; color: #64748B;
    font-variant-numeric: tabular-nums; min-width: 90px;
  }
  .history-msg { color: #334155; }

  /* Search */
  .search-wrap {
    position: relative; margin-bottom: 24px;
  }
  .search-input {
    width: 100%; padding: 14px 16px 14px 44px;
    border: 1px solid #E2E8F0; border-radius: 12px;
    font-size: 14px; font-family: inherit; color: #1E293B;
    background: #fff; outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .search-input:focus {
    border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
  }
  .search-input::placeholder { color: #94A3B8; }
  .search-icon {
    position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
    width: 20px; height: 20px; color: #94A3B8; pointer-events: none;
  }
  .search-meta {
    position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
    font-size: 12px; color: #94A3B8; pointer-events: none;
  }
  .search-meta.hidden { display: none; }
  .no-results {
    text-align: center; padding: 40px 20px; color: #94A3B8;
    font-size: 14px; display: none;
  }
  .accordion.search-hidden, .link-card.search-hidden { display: none; }

  /* Filters */
  .filter-wrap { margin-top: -16px; margin-bottom: 20px; }
  .filter-toggle {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fff; border: 1px solid #E2E8F0; border-radius: 8px;
    padding: 7px 14px; font-size: 12px; font-weight: 600;
    color: #64748B; cursor: pointer; font-family: inherit;
    transition: all 0.15s;
  }
  .filter-toggle:hover { border-color: #CBD5E1; background: #F8FAFC; }
  .filter-toggle.has-filter { border-color: #2563EB; color: #2563EB; background: #EFF6FF; }
  .filter-active-count {
    font-size: 10px; background: #2563EB; color: #fff;
    padding: 1px 7px; border-radius: 10px; font-weight: 700; display: none;
  }
  .filter-toggle.has-filter .filter-active-count { display: inline; }
  .filter-chevron { width: 14px; height: 14px; transition: transform 0.2s; }
  .filter-wrap.open .filter-chevron { transform: rotate(180deg); }
  .filter-body {
    display: none; margin-top: 12px; padding: 16px 20px;
    background: #fff; border: 1px solid #E2E8F0; border-radius: 12px;
  }
  .filter-wrap.open .filter-body { display: block; }
  .filter-group { margin-bottom: 14px; }
  .filter-group:last-child { margin-bottom: 0; }
  .filter-label {
    font-size: 11px; font-weight: 700; color: #94A3B8;
    letter-spacing: 0.5px; margin-bottom: 8px;
  }
  .filter-pills { display: flex; flex-wrap: wrap; gap: 6px; }
  .filter-pill {
    padding: 4px 12px; border: 1px solid #E2E8F0; border-radius: 16px;
    background: #fff; color: #64748B; font-size: 11px; font-weight: 600;
    cursor: pointer; font-family: inherit; transition: all 0.15s;
    white-space: nowrap;
  }
  .filter-pill:hover { border-color: #CBD5E1; background: #F8FAFC; }
  .filter-pill.active { background: #1E293B; color: #fff; border-color: #1E293B; }

  /* Document Status Badges */
  .doc-status {
    font-size: 9px; font-weight: 700; padding: 1px 6px;
    border-radius: 4px; margin-left: 6px; letter-spacing: 0.3px;
    vertical-align: middle; white-space: nowrap;
  }
  .doc-status-published { background: #DCFCE7; color: #16A34A; }

  /* Version History */
  .version-toggle {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 6px;
    background: #F1F5F9; border: 1px solid #E2E8F0;
    color: #94A3B8; font-size: 11px; cursor: pointer;
    margin-left: 6px; flex-shrink: 0; transition: all 0.15s;
    vertical-align: middle; line-height: 1;
  }
  .version-toggle:hover { background: #E2E8F0; color: #475569; }
  .version-toggle.open { background: #EFF6FF; border-color: #BFDBFE; color: #2563EB; }
  .version-dropdown {
    display: none; margin-top: 4px; padding: 10px 14px;
    background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
    font-size: 12px; min-width: 280px; width: 100%; flex-basis: 100%;
  }
  .version-dropdown.open { display: block; }
  .version-entry {
    display: flex; align-items: baseline; gap: 10px;
    padding: 5px 0; border-bottom: 1px solid #E2E8F0;
    white-space: nowrap;
  }
  .version-entry:last-child { border-bottom: none; }
  .version-entry .ver-tag {
    font-weight: 800; color: #2563EB; font-size: 11px;
    min-width: 36px; flex-shrink: 0;
  }
  .version-entry .ver-date {
    font-size: 0.8rem; color: #888; min-width: 84px; flex-shrink: 0;
    font-variant-numeric: tabular-nums;
  }
  .version-entry .ver-summary { color: #475569; white-space: normal; }

  /* NEW / UPDATED badges */
  .badge-new {
    display: inline-block; background: #DCFCE7; color: #16A34A;
    font-size: 10px; font-weight: 700; padding: 1px 6px;
    border-radius: 4px; margin-left: 6px; letter-spacing: 0.5px;
    vertical-align: middle; animation: badgePulse 2s ease-in-out infinite;
  }
  .badge-updated {
    display: inline-block; background: #DBEAFE; color: #2563EB;
    font-size: 10px; font-weight: 700; padding: 1px 6px;
    border-radius: 4px; margin-left: 6px; letter-spacing: 0.5px;
    vertical-align: middle;
  }
  @keyframes badgePulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  /* Request System */
  .req-section {
    margin-top: 32px; margin-bottom: 24px;
  }
  .req-section-title {
    font-size: 15px; font-weight: 800; color: #0369A1;
    padding: 12px 16px; cursor: pointer; user-select: none;
    border: 1px solid #E0F2FE; border-radius: 10px;
    background: #F0F9FF; display: flex; align-items: center; justify-content: space-between;
    transition: background 0.15s;
  }
  .req-section-title:hover { background: #E0F2FE; }
  .req-section-title .chevron-req {
    font-size: 11px; color: #0369A1; transition: transform 0.2s;
  }
  .req-section-title.open .chevron-req { transform: rotate(90deg); }
  .req-section .req-card { display: none; margin-top: 12px; }
  .req-section.open .req-card { display: block; }
  .req-card {
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 20px 24px;
  }
  .req-status-bar {
    display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; align-items: center;
  }
  .req-refresh-btn {
    font-size: 11px; font-weight: 600; padding: 4px 10px;
    border-radius: 8px; border: 1px solid #CBD5E1; background: #F8FAFC;
    color: #475569; cursor: pointer; margin-left: auto;
    transition: background 0.15s, border-color 0.15s;
    display: inline-flex; align-items: center; gap: 4px;
  }
  .req-refresh-btn:hover { background: #E2E8F0; border-color: #94A3B8; }
  .req-refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .req-status-badge {
    font-size: 12px; font-weight: 700; padding: 4px 12px;
    border-radius: 8px; display: inline-flex; align-items: center; gap: 6px;
  }
  .req-badge-wait { background: #FEF9C3; color: #A16207; }
  .req-badge-progress { background: #DBEAFE; color: #1D4ED8; }
  .req-badge-done { background: #DCFCE7; color: #15803D; }
  .req-badge-all { background: #F1F5F9; color: #475569; }
  .req-status-badge { cursor: pointer; transition: box-shadow 0.15s, transform 0.15s; }
  .req-status-badge:hover { transform: translateY(-1px); }
  .req-status-badge.active { box-shadow: 0 0 0 2px #1E293B; }
  .req-pagination {
    display: flex; justify-content: center; align-items: center;
    gap: 4px; margin-top: 12px; padding-top: 12px;
    border-top: 1px solid #F1F5F9;
  }
  .req-pagination button {
    min-width: 32px; height: 32px; border: 1px solid #E2E8F0;
    border-radius: 6px; background: #fff; color: #475569;
    font-size: 12px; font-weight: 600; cursor: pointer;
    font-family: inherit; transition: all 0.15s;
  }
  .req-pagination button:hover { background: #F1F5F9; border-color: #CBD5E1; }
  .req-pagination button.active { background: #2563EB; color: #fff; border-color: #2563EB; }
  .req-pagination button:disabled { opacity: 0.4; cursor: default; }
  .req-table {
    width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px;
  }
  .req-table th {
    background: #F8FAFC; padding: 8px 10px; text-align: left;
    font-weight: 700; color: #475569; border-bottom: 2px solid #E2E8F0;
    white-space: nowrap;
  }
  .req-table td {
    padding: 8px 10px; border-bottom: 1px solid #F1F5F9; color: #334155;
  }
  .req-table tr:hover td { background: #F8FAFC; }
  .req-table .td-status {
    font-size: 11px; font-weight: 700; padding: 2px 8px;
    border-radius: 6px; display: inline-block; white-space: nowrap;
  }
  .req-table .td-pri {
    font-size: 11px; white-space: nowrap;
  }
  .req-empty {
    text-align: center; padding: 24px; color: #94A3B8; font-size: 13px;
  }

  .req-form { display: flex; flex-direction: column; gap: 14px; }
  .req-field label {
    display: block; font-size: 12px; font-weight: 700;
    color: #475569; margin-bottom: 4px;
  }
  .req-field input[type="text"],
  .req-field select,
  .req-field textarea {
    width: 100%; padding: 8px 12px; border: 1px solid #E2E8F0;
    border-radius: 8px; font-size: 13px; font-family: inherit;
    background: #F8FAFC; color: #1E293B;
    transition: border-color 0.15s;
  }
  .req-field input:focus,
  .req-field select:focus,
  .req-field textarea:focus {
    outline: none; border-color: #0EA5E9; background: #fff;
  }
  .req-field textarea { min-height: 80px; resize: vertical; }
  .req-field .field-error { border-color: #DC2626 !important; background: #FEF2F2 !important; }
  .req-field .field-error-msg { font-size: 11px; color: #DC2626; margin-top: 3px; }
  .req-radio-group {
    display: flex; gap: 16px; margin-top: 4px;
  }
  .req-radio-group label {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 13px; font-weight: 600; cursor: pointer; color: #334155;
  }
  .req-radio-group input[type="radio"] { accent-color: #0EA5E9; }
  .req-submit {
    align-self: flex-start; padding: 10px 28px;
    background: linear-gradient(135deg, #0C4A6E, #0EA5E9);
    color: #fff; border: none; border-radius: 8px;
    font-size: 13px; font-weight: 700; cursor: pointer;
    transition: opacity 0.15s;
  }
  .req-submit:hover { opacity: 0.9; }
  .req-submit:disabled { opacity: 0.5; cursor: not-allowed; }
  .req-toast {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: #0C4A6E; color: #fff; padding: 12px 28px;
    border-radius: 10px; font-size: 13px; font-weight: 700;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    opacity: 0; transition: opacity 0.3s;
    z-index: 9999; pointer-events: none;
  }
  .req-toast.show { opacity: 1; }

  /* Recent Updates */
  .recent-panel {
    background: #fff; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;
  }
  .recent-panel-header {
    font-size: 13px; font-weight: 700; color: #475569; margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px;
  }
  .recent-item {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0; font-size: 12px;
    border-bottom: 1px solid #F1F5F9;
  }
  .recent-item:last-child { border-bottom: none; }
  .recent-dot {
    width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
  }
  .recent-title {
    flex: 1; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; color: #334155; font-weight: 600;
  }
  .recent-version {
    font-size: 11px; font-weight: 800; color: #2563EB;
    flex-shrink: 0; font-variant-numeric: tabular-nums;
  }
  .recent-type {
    font-size: 10px; font-weight: 700; padding: 2px 8px;
    border-radius: 6px; background: #F1F5F9; color: #64748B;
    flex-shrink: 0; white-space: nowrap;
  }

  .footer {
    text-align: center; padding: 24px; font-size: 12px;
    color: #94A3B8; border-top: 1px solid #E2E8F0; margin-top: 40px;
  }
  @media print {
    .hero { padding: 24px; }
    .accordion-body { max-height: none !important; }
    .chevron { display: none; }
    .search-wrap, .badge-new, .badge-updated, .req-section, .req-toast, .history-toggle, .recent-panel { display: none; }
  }
  @media (max-width: 600px) {
    .link-grid { grid-template-columns: 1fr; }
    .stats { grid-template-columns: repeat(2, 1fr); }
    .hero h1 { font-size: 24px; }
    .filter-pills { gap: 4px; }
    .filter-pill { padding: 3px 8px; font-size: 10px; }
  }
</style>"""

CHEVRON_SVG = '<svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"/></svg>'

SEARCH_ICON_SVG = '<svg class="search-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"/></svg>'

FILTER_ICON_SVG = '<svg width="14" height="14" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"/></svg>'

FILTER_CHEVRON_SVG = '<svg class="filter-chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"/></svg>'

PORTAL_MANUAL_ICON_SVG = '<svg width="14" height="14" viewBox="0 0 20 20" fill="currentColor"><path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/></svg>'


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_hero(meta: dict, total_docs: int, total_cats: int) -> str:
    pm = meta['portal_manual']
    return (
        '<header class="hero">\n'
        '  <div class="hero-badge">Document Portal</div>\n'
        f'  <h1>{meta["title"]}</h1>\n'
        f'  <div class="subtitle">{meta["subtitle"]}</div>\n'
        '  <div class="hero-meta">\n'
        f'    <span>작성자: {meta["author"]}</span>\n'
        f'    <span>문서 {total_docs}건 &middot; {total_cats}개 카테고리</span>\n'
        '  </div>\n'
        f'  <a href="{pm["href"]}" style="display:inline-flex;align-items:center;gap:6px;margin-top:16px;'
        'background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:8px;'
        'padding:6px 14px;font-size:12px;font-weight:600;color:#fff;text-decoration:none;transition:.2s;" '
        'onmouseover="this.style.background=\'rgba(255,255,255,0.22)\'" '
        'onmouseout="this.style.background=\'rgba(255,255,255,0.12)\'">\n'
        f'    {PORTAL_MANUAL_ICON_SVG}\n'
        f'    {pm["label"]}\n'
        '  </a>\n'
        '</header>\n'
    )


def build_stats(categories: list) -> str:
    lines = ['  <!-- Stats -->\n  <div class="stats">']
    for cat in categories:
        lbl = cat.get('stat_label') or cat['label']
        n = len(cat['docs'])
        lines.append(
            f'    <div class="stat-card" data-target="{cat["id"]}" '
            f'style="border-top-color:{cat["color"]}">\n'
            f'      <div class="num">{n}</div><div class="lbl">{lbl}</div>\n'
            f'    </div>'
        )
    lines.append('  </div>')
    return '\n'.join(lines) + '\n'


def build_search() -> str:
    return (
        '\n  <!-- Search -->\n'
        '  <div class="search-wrap">\n'
        f'    {SEARCH_ICON_SVG}\n'
        '    <input class="search-input" type="text" id="searchInput" '
        'placeholder="문서 검색 (제목, 유형, 키워드)">\n'
        '    <span class="search-meta hidden" id="searchMeta"></span>\n'
        '  </div>\n'
    )


def build_filters(categories: list, filter_types: list, filter_statuses: list) -> str:
    lines = [
        '\n  <!-- Filters -->',
        '  <div class="filter-wrap" id="filterWrap">',
        '    <button class="filter-toggle" id="filterToggle" type="button">',
        f'      {FILTER_ICON_SVG}',
        '      필터',
        '      <span class="filter-active-count" id="filterActiveCount">0</span>',
        f'      {FILTER_CHEVRON_SVG}',
        '    </button>',
        '    <div class="filter-body" id="filterBody">',
        # Category pills
        '      <div class="filter-group">',
        '        <div class="filter-label">카테고리</div>',
        '        <div class="filter-pills" data-group="cat">',
        '          <button class="filter-pill active" data-value="all" type="button">All</button>',
    ]
    for cat in categories:
        lbl = cat.get('stat_label') or cat['label']
        lines.append(f'          <button class="filter-pill" data-value="{cat["id"]}" type="button">{lbl}</button>')
    lines += [
        '        </div>',
        '      </div>',
        # Type pills
        '      <div class="filter-group">',
        '        <div class="filter-label">문서 타입</div>',
        '        <div class="filter-pills" data-group="type">',
        '          <button class="filter-pill active" data-value="all" type="button">All</button>',
    ]
    for t in filter_types:
        lines.append(f'          <button class="filter-pill" data-value="{t}" type="button">{t}</button>')
    lines += [
        '        </div>',
        '      </div>',
        # Status pills
        '      <div class="filter-group">',
        '        <div class="filter-label">상태</div>',
        '        <div class="filter-pills" data-group="status">',
        '          <button class="filter-pill active" data-value="all" type="button">All</button>',
    ]
    for s in filter_statuses:
        lines.append(f'          <button class="filter-pill" data-value="{s}" type="button">{s}</button>')
    lines += [
        '        </div>',
        '      </div>',
        '    </div>',
        '  </div>',
    ]
    return '\n'.join(lines) + '\n'


def build_link_card(doc: dict) -> str:
    """Build a single link-card element."""
    # Icon: class or inline style
    if doc.get('icon_style'):
        icon_span = '<span class="lc-icon" style="{}">{}</span>'.format(
            doc['icon_style'], doc['icon_text'])
    else:
        icon_span = '<span class="lc-icon {}">{}</span>'.format(
            doc.get('icon_class', ''), doc['icon_text'])

    # Body
    title = f'<span class="lc-title">{doc["title"]}</span>'
    desc = f'<span class="lc-desc">{doc["desc"]}</span>' if doc.get('desc') else ''
    body = f'<span class="lc-body">{title}{desc}</span>'

    # Version
    version = f'<span class="lc-version">{doc["version"]}</span>'

    # Badge: class or inline style
    if doc.get('badge_style'):
        badge = f'<span class="lc-badge" style="{doc["badge_style"]}">{doc["badge_text"]}</span>'
    else:
        badge = f'<span class="lc-badge {doc.get("badge_class", "")}">{doc["badge_text"]}</span>'

    return (
        f'        <a class="link-card" href="{doc["href"]}" '
        f'data-updated="{doc["updated"]}">'
        f'{icon_span}{body}{version}{badge}</a>'
    )


def build_accordion(cat: dict) -> str:
    """Build one accordion section."""
    n = len(cat['docs'])
    # Header icon: class or inline style
    if cat.get('icon_style'):
        icon = f'<span class="icon" style="{cat["icon_style"]}">{cat["icon_text"]}</span>'
    else:
        icon = f'<span class="icon {cat.get("icon_class", "")}">{cat["icon_text"]}</span>'

    lines = [
        f'  <!-- {cat["label"]} -->',
        f'  <div class="accordion" id="{cat["id"]}">',
        f'    <button class="accordion-header" aria-expanded="false">',
        f'      {icon} {cat["label"]}',
        f'      <span class="count">{n}건</span>',
        f'      {CHEVRON_SVG}',
        f'    </button>',
        f'    <div class="accordion-body"><div class="accordion-body-inner">',
        f'      <div class="link-grid">',
    ]
    for doc in cat['docs']:
        lines.append(build_link_card(doc))
    lines += [
        '      </div>',
        '    </div></div>',
        '  </div>',
        '',
    ]
    return '\n'.join(lines)


def build_request_status() -> str:
    return (
        '  <!-- 요청 현황 -->\n'
        '  <div class="req-section">\n'
        '    <div class="req-section-title" onclick="this.classList.toggle(\'open\');'
        'this.closest(\'.req-section\').classList.toggle(\'open\')">'
        '\U0001f4ca 요청 현황<span class="chevron-req">\u25b6</span></div>\n'
        '    <div class="req-card">\n'
        '      <div class="req-status-bar" id="reqStatusBar">\n'
        '        <span class="req-status-badge req-badge-wait">대기중 <strong>-</strong></span>\n'
        '        <span class="req-status-badge req-badge-progress">진행중 <strong>-</strong></span>\n'
        '        <span class="req-status-badge req-badge-done">완료 <strong>-</strong></span>\n'
        '        <button type="button" class="req-refresh-btn" id="reqRefreshBtn" '
        'onclick="refreshRequests()">\U0001f504 새로고침</button>\n'
        '      </div>\n'
        '      <table class="req-table">\n'
        '        <thead><tr><th>ID</th><th>요청자</th><th>대상 문서</th><th>유형</th>'
        '<th>우선순위</th><th>상태</th><th>등록일</th><th>완료일</th></tr></thead>\n'
        '        <tbody id="reqTableBody">\n'
        '          <tr><td colspan="8" class="req-empty">데이터를 불러오는 중...</td></tr>\n'
        '        </tbody>\n'
        '      </table>\n'
        '      <div class="req-pagination" id="reqPagination" style="display:none;"></div>\n'
        '    </div>\n'
        '  </div>\n'
    )


def build_request_form(categories: list, request_types: list) -> str:
    # Build optgroup options from categories' request_options
    optgroups = ''
    for cat in categories:
        opts = cat.get('request_options', [])
        if not opts:
            continue
        optgroups += f'            <optgroup label="{cat["label"]}">\n'
        for opt in opts:
            optgroups += f'              <option>{opt}</option>\n'
        optgroups += '            </optgroup>\n'

    # Request type options
    type_opts = '\n'.join(
        f'            <option value="{t}">{t}</option>' for t in request_types
    )

    return (
        '\n  <!-- 문서 업데이트 요청 -->\n'
        '  <div class="req-section">\n'
        '    <div class="req-section-title" onclick="this.classList.toggle(\'open\');'
        'this.closest(\'.req-section\').classList.toggle(\'open\')">'
        '\U0001f4cb 문서 업데이트 요청<span class="chevron-req">\u25b6</span></div>\n'
        '    <div class="req-card">\n'
        '      <form class="req-form" id="reqForm">\n'
        '        <div class="req-field">\n'
        '          <label for="reqName">요청자 이름</label>\n'
        '          <input type="text" id="reqName" placeholder="이름을 입력하세요" required>\n'
        '        </div>\n'
        '        <div class="req-field">\n'
        '          <label for="reqDoc">대상 문서</label>\n'
        '          <select id="reqDoc" required>\n'
        '            <option value="">문서를 선택하세요</option>\n'
        f'{optgroups}'
        '          </select>\n'
        '        </div>\n'
        '        <div class="req-field">\n'
        '          <label for="reqType">요청 유형</label>\n'
        '          <select id="reqType" required>\n'
        '            <option value="">유형을 선택하세요</option>\n'
        f'{type_opts}\n'
        '          </select>\n'
        '        </div>\n'
        '        <div class="req-field">\n'
        '          <label for="reqContent">요청 내용</label>\n'
        '          <textarea id="reqContent" placeholder="수정/추가/삭제할 내용을 상세히 작성해주세요" required></textarea>\n'
        '        </div>\n'
        '        <div class="req-field">\n'
        '          <label>우선순위</label>\n'
        '          <div class="req-radio-group">\n'
        '            <label><input type="radio" name="reqPriority" value="높음" required> \U0001f534 높음</label>\n'
        '            <label><input type="radio" name="reqPriority" value="보통" checked> \U0001f7e1 보통</label>\n'
        '            <label><input type="radio" name="reqPriority" value="낮음"> \U0001f7e2 낮음</label>\n'
        '          </div>\n'
        '        </div>\n'
        '        <button type="submit" class="req-submit" id="reqSubmitBtn">요청 제출</button>\n'
        '      </form>\n'
        '    </div>\n'
        '  </div>\n'
    )


def build_changelog(changelog: list) -> str:
    total = len(changelog)
    items = '\n'.join(
        f'        <li class="history-item"><span class="history-date">{c["date"]}</span>'
        f'<span class="history-msg">{c["message"]}</span></li>'
        for c in changelog
    )
    return (
        f'\n  <!-- 변경 히스토리 -->\n'
        f'  <div class="history-details" id="sec-history" style="display:block;">\n'
        f'    <div class="history-summary" style="cursor:default;">\n'
        f'      변경 히스토리 <span class="count">전체 {total}건</span>\n'
        f'    </div>\n'
        f'    <div class="history-content" style="display:block;">\n'
        f'      <ul class="history-list">\n'
        f'{items}\n'
        f'      </ul>\n'
        f'      <button class="history-toggle" id="historyToggle" '
        f'style="display:none;margin-top:12px;background:#F1F5F9;border:1px solid #E2E8F0;'
        f'border-radius:8px;padding:6px 16px;font-size:12px;font-weight:600;color:#475569;'
        f'cursor:pointer;width:100%;transition:background 0.15s;" '
        f'onmouseover="this.style.background=\'#E2E8F0\'" '
        f'onmouseout="this.style.background=\'#F1F5F9\'"></button>\n'
        f'    </div>\n'
        f'  </div>\n'
    )


def build_footer(meta: dict) -> str:
    return (
        f'<footer class="footer">\n'
        f'  Toomics Global &middot; BizOps Team &middot; {meta["author"]} &middot; 2026\n'
        f'</footer>\n'
    )


def build_js(meta: dict, version_history: dict, categories: list) -> str:
    """Build the entire <script> block."""
    vh_json = json.dumps(version_history, indent=2, ensure_ascii=False)
    cats_js = json.dumps(
        [{'id': c['id'], 'name': c.get('stat_label') or c['label'], 'color': c['color']}
         for c in categories],
        ensure_ascii=False
    )

    return f"""\
<script>
var APPS_SCRIPT_URL = '{meta["apps_script_url"]}';

// Accordion toggle
document.querySelectorAll('.accordion-header').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const acc = btn.parentElement;
    const isOpen = acc.classList.contains('open');
    acc.classList.toggle('open');
    btn.setAttribute('aria-expanded', !isOpen);
  }});
}});

// Stat card → scroll to accordion & open it
document.querySelectorAll('.stat-card[data-target]').forEach(card => {{
  card.addEventListener('click', () => {{
    const target = document.getElementById(card.dataset.target);
    if (!target) return;
    if (!target.classList.contains('open')) {{
      target.classList.add('open');
      target.querySelector('.accordion-header').setAttribute('aria-expanded', 'true');
    }}
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }});
}});

// Document Status Data (key = filename from href)
var DOC_STATUS = {{}};
(function() {{
  document.querySelectorAll('.link-card').forEach(function(card) {{
    var href = card.getAttribute('href') || '';
    var status = DOC_STATUS[href.split('/').pop()] || 'Published';
    card.dataset.status = status;
    var typeBadge = card.querySelector('.lc-badge');
    if (typeBadge) {{
      typeBadge.insertAdjacentHTML('afterend',
        '<span class="doc-status doc-status-published">' + status + '</span>');
    }}
  }});
}})();

// Version History Data
var VERSION_HISTORY = {vh_json};

// Inject version history toggles
(function() {{
  document.querySelectorAll('.link-card').forEach(function(card) {{
    var href = card.getAttribute('href') || '';
    var fname = href.split('/').pop();
    var vData = VERSION_HISTORY[fname];
    if (!vData || !vData.history || vData.history.length === 0) return;

    // Add toggle button after doc-status badge (or after lc-badge)
    var statusBadge = card.querySelector('.doc-status');
    var insertAfter = statusBadge || card.querySelector('.lc-badge');
    if (!insertAfter) return;

    var toggleBtn = document.createElement('button');
    toggleBtn.className = 'version-toggle';
    toggleBtn.type = 'button';
    toggleBtn.textContent = '\\uD83D\\uDD50';
    toggleBtn.title = '버전 히스토리 (' + vData.history.length + '건)';
    insertAfter.insertAdjacentElement('afterend', toggleBtn);

    // Build dropdown
    var dropdown = document.createElement('div');
    dropdown.className = 'version-dropdown';
    var html = '';
    vData.history.forEach(function(h) {{
      html += '<div class="version-entry">';
      html += '<span class="ver-tag">' + h.version + '</span>';
      html += '<span class="ver-date">' + h.date + '</span>';
      html += '<span class="ver-summary">' + h.summary + '</span>';
      html += '</div>';
    }});
    dropdown.innerHTML = html;

    // Append dropdown to card itself (not lc-body, to avoid overflow:hidden clipping)
    card.style.flexWrap = 'wrap';
    card.appendChild(dropdown);

    // Toggle behavior
    toggleBtn.addEventListener('click', function(e) {{
      e.preventDefault();
      e.stopPropagation();
      var isOpen = dropdown.classList.contains('open');
      // Close all others first
      document.querySelectorAll('.version-dropdown.open').forEach(function(d) {{
        d.classList.remove('open');
      }});
      document.querySelectorAll('.version-toggle.open').forEach(function(t) {{
        t.classList.remove('open');
      }});
      if (!isOpen) {{
        dropdown.classList.add('open');
        toggleBtn.classList.add('open');
      }}
    }});
  }});
}})();


// Unified Search + Filter
(function() {{
  var input = document.getElementById('searchInput');
  var meta = document.getElementById('searchMeta');
  var noResults = document.getElementById('noResults');
  var filterWrap = document.getElementById('filterWrap');
  var filterToggle = document.getElementById('filterToggle');
  var filterCountEl = document.getElementById('filterActiveCount');
  if (!input) return;

  var accordions = document.querySelectorAll('.accordion');
  var allCards = document.querySelectorAll('.link-card');

  // Filter state
  var activeCats = new Set();
  var activeTypes = new Set();
  var activeStatuses = new Set();

  // Toggle filter panel
  filterToggle.addEventListener('click', function() {{
    filterWrap.classList.toggle('open');
  }});

  // Filter pill click
  document.querySelectorAll('.filter-pills').forEach(function(group) {{
    group.addEventListener('click', function(e) {{
      var pill = e.target.closest('.filter-pill');
      if (!pill) return;
      var val = pill.dataset.value;
      var gName = group.dataset.group;
      var stateSet = gName === 'cat' ? activeCats : gName === 'type' ? activeTypes : activeStatuses;

      if (val === 'all') {{
        stateSet.clear();
        group.querySelectorAll('.filter-pill').forEach(function(p) {{
          p.classList.toggle('active', p.dataset.value === 'all');
        }});
      }} else {{
        var allBtn = group.querySelector('[data-value="all"]');
        if (pill.classList.contains('active')) {{
          pill.classList.remove('active');
          stateSet.delete(val);
          if (stateSet.size === 0) allBtn.classList.add('active');
        }} else {{
          pill.classList.add('active');
          stateSet.add(val);
          allBtn.classList.remove('active');
        }}
      }}
      updateFilterUI();
      applyFilters();
    }});
  }});

  function updateFilterUI() {{
    var count = activeCats.size + activeTypes.size + activeStatuses.size;
    if (count > 0) {{
      filterToggle.classList.add('has-filter');
      filterCountEl.textContent = count;
      filterCountEl.style.display = 'inline';
    }} else {{
      filterToggle.classList.remove('has-filter');
      filterCountEl.style.display = 'none';
    }}
  }}

  input.addEventListener('input', applyFilters);

  window._applyFilters = applyFilters; // expose for other modules

  function applyFilters() {{
    var q = input.value.trim().toLowerCase();
    var hasQuery = q.length > 0;
    var hasCat = activeCats.size > 0;
    var hasType = activeTypes.size > 0;
    var hasStatus = activeStatuses.size > 0;
    var hasAny = hasQuery || hasCat || hasType || hasStatus;

    if (!hasAny) {{
      allCards.forEach(function(c) {{ c.classList.remove('search-hidden'); }});
      accordions.forEach(function(a) {{
        a.classList.remove('search-hidden');
        a.classList.remove('open');
        a.querySelector('.accordion-header').setAttribute('aria-expanded', 'false');
      }});
      meta.classList.add('hidden');
      noResults.style.display = 'none';
      return;
    }}

    var totalMatch = 0;

    accordions.forEach(function(acc) {{
      var catId = acc.id;
      var catOk = !hasCat || activeCats.has(catId);
      var cards = acc.querySelectorAll('.link-card');
      var accMatch = 0;

      cards.forEach(function(card) {{
        var show = true;
        if (!catOk) show = false;
        if (show && hasType) {{
          var badge = (card.querySelector('.lc-badge')?.textContent || '').trim();
          if (!activeTypes.has(badge)) show = false;
        }}
        if (show && hasStatus) {{
          var st = card.dataset.status || 'Published';
          if (!activeStatuses.has(st)) show = false;
        }}
        if (show && hasQuery) {{
          var title = (card.querySelector('.lc-title')?.textContent || '').toLowerCase();
          var desc = (card.querySelector('.lc-desc')?.textContent || '').toLowerCase();
          var bdg = (card.querySelector('.lc-badge')?.textContent || '').toLowerCase();
          if (!title.includes(q) && !desc.includes(q) && !bdg.includes(q)) show = false;
        }}
        card.classList.toggle('search-hidden', !show);
        if (show) accMatch++;
      }});
      totalMatch += accMatch;

      if (accMatch > 0) {{
        acc.classList.remove('search-hidden');
        acc.classList.add('open');
        acc.querySelector('.accordion-header').setAttribute('aria-expanded', 'true');
      }} else {{
        acc.classList.add('search-hidden');
      }}
    }});

    if (totalMatch > 0) {{
      meta.textContent = totalMatch + '건 일치';
      meta.classList.remove('hidden');
      noResults.style.display = 'none';
    }} else {{
      meta.classList.add('hidden');
      noResults.style.display = 'block';
    }}
  }}
}})();

// Recent Updates Panel (최근 5개 문서)
(function() {{
  var categories = {cats_js};
  var DAY = 86400000;
  var now = new Date();
  var updates = [];
  document.querySelectorAll('.link-card[data-updated]').forEach(function(card) {{
    var d = new Date(card.dataset.updated + 'T00:00:00');
    var diff = Math.floor((now - d) / DAY);
    var title = (card.querySelector('.lc-title')?.textContent || '').replace(/Updated/g, '').trim();
    var badge = (card.querySelector('.lc-badge')?.textContent || '').trim();
    var version = (card.querySelector('.lc-version')?.textContent || '').trim();
    var acc = card.closest('.accordion');
    var cat = acc ? acc.id : '';
    updates.push({{ diff: diff, title: title, badge: badge, version: version, cat: cat }});
  }});
  var recent = updates.slice().sort(function(a, b) {{ return a.diff - b.diff; }}).slice(0, 5);
  var panel = document.getElementById('recentPanel');
  if (!panel || recent.length === 0) return;
  var h = '<div class="recent-panel-header">최근 업데이트 (최근 5개 문서)</div>';
  recent.forEach(function(u) {{
    var catData = categories.find(function(c) {{ return c.id === u.cat; }});
    var color = catData ? catData.color : '#94A3B8';
    h += '<div class="recent-item">';
    h += '<span class="recent-dot" style="background:' + color + ';"></span>';
    h += '<span class="recent-title">' + u.title + '</span>';
    if (u.version) h += '<span class="recent-version">' + u.version + '</span>';
    h += '<span class="recent-type">' + u.badge + '</span>';
    h += '</div>';
  }});
  panel.innerHTML = h;
}})();

// History: show first 5, toggle rest
(function() {{
  var items = document.querySelectorAll('#sec-history .history-item');
  var btn = document.getElementById('historyToggle');
  if (!btn || items.length <= 5) return;
  var expanded = false;
  var hiddenCount = items.length - 5;
  items.forEach(function(item, i) {{
    if (i >= 5) item.style.display = 'none';
  }});
  btn.style.display = 'block';
  btn.textContent = '더보기 (' + hiddenCount + '건)';
  btn.addEventListener('click', function() {{
    expanded = !expanded;
    items.forEach(function(item, i) {{
      if (i >= 5) item.style.display = expanded ? '' : 'none';
    }});
    btn.textContent = expanded ? '접기' : '더보기 (' + hiddenCount + '건)';
  }});
}})();

// Document Request System
(function() {{
  // Toast
  function showToast(msg, isError) {{
    var toast = document.getElementById('reqToast');
    toast.textContent = msg;
    toast.style.background = isError ? '#DC2626' : '#0C4A6E';
    toast.classList.add('show');
    setTimeout(function() {{ toast.classList.remove('show'); }}, 3000);
  }}

  // Status color map & shared constants
  var statusClass = {{ '대기중': 'req-badge-wait', '진행중': 'req-badge-progress', '완료': 'req-badge-done' }};
  function fmtDate(v) {{ return v ? String(v).substring(0, 10) : '-'; }}
  var REFRESH_BTN = '<button type="button" class="req-refresh-btn" id="reqRefreshBtn" onclick="refreshRequests()">\\uD83D\\uDD04 새로고침</button>';
  var PER_PAGE = 5;
  var allRequests = [];
  var activeFilter = '';
  var currentPage = 1;

  function statusBarHtml(counts, filter) {{
    var f = filter || '';
    return '<span class="req-status-badge req-badge-all' + (f === '' ? ' active' : '') + '" data-filter="">전체 <strong>' + ((counts['대기중'] || 0) + (counts['진행중'] || 0) + (counts['완료'] || 0)) + '</strong></span>' +
      '<span class="req-status-badge req-badge-wait' + (f === '대기중' ? ' active' : '') + '" data-filter="대기중">대기중 <strong>' + (counts['대기중'] || 0) + '</strong></span>' +
      '<span class="req-status-badge req-badge-progress' + (f === '진행중' ? ' active' : '') + '" data-filter="진행중">진행중 <strong>' + (counts['진행중'] || 0) + '</strong></span>' +
      '<span class="req-status-badge req-badge-done' + (f === '완료' ? ' active' : '') + '" data-filter="완료">완료 <strong>' + (counts['완료'] || 0) + '</strong></span>' + REFRESH_BTN;
  }}

  function getFiltered() {{
    if (!activeFilter) return allRequests;
    return allRequests.filter(function(r) {{ return r.status === activeFilter; }});
  }}

  function renderTable() {{
    var tbody = document.getElementById('reqTableBody');
    var pgDiv = document.getElementById('reqPagination');
    var filtered = getFiltered();
    var totalPages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
    if (currentPage > totalPages) currentPage = totalPages;
    var start = (currentPage - 1) * PER_PAGE;
    var page = filtered.slice(start, start + PER_PAGE);

    if (page.length === 0) {{
      tbody.innerHTML = '<tr><td colspan="8" class="req-empty">등록된 요청이 없습니다.</td></tr>';
      pgDiv.style.display = 'none';
      return;
    }}
    var html = '';
    page.forEach(function(r) {{
      var sc = statusClass[r.status] || 'req-badge-wait';
      var pri = r.priority === '높음' ? '\\uD83D\\uDD34 높음' : r.priority === '낮음' ? '\\uD83D\\uDFE2 낮음' : '\\uD83D\\uDFE1 보통';
      html += '<tr><td>' + (r.id || '-') + '</td><td>' + (r.requester || '-') + '</td><td>' + (r.document || '-') + '</td><td>' + (r.type || '-') + '</td><td class="td-pri">' + pri + '</td><td><span class="td-status ' + sc + '">' + (r.status || '-') + '</span></td><td>' + fmtDate(r.timestamp) + '</td><td>' + fmtDate(r.completed_at) + '</td></tr>';
    }});
    tbody.innerHTML = html;

    // Pagination
    if (totalPages <= 1) {{ pgDiv.style.display = 'none'; return; }}
    pgDiv.style.display = 'flex';
    var ph = '<button' + (currentPage === 1 ? ' disabled' : '') + ' data-pg="' + (currentPage - 1) + '">&lsaquo;</button>';
    for (var p = 1; p <= totalPages; p++) {{
      ph += '<button class="' + (p === currentPage ? 'active' : '') + '" data-pg="' + p + '">' + p + '</button>';
    }}
    ph += '<button' + (currentPage === totalPages ? ' disabled' : '') + ' data-pg="' + (currentPage + 1) + '">&rsaquo;</button>';
    pgDiv.innerHTML = ph;
  }}

  function bindStatusBar() {{
    var bar = document.getElementById('reqStatusBar');
    bar.addEventListener('click', function(e) {{
      var badge = e.target.closest('.req-status-badge');
      if (!badge || badge.classList.contains('active')) return;
      activeFilter = badge.dataset.filter || '';
      currentPage = 1;
      bar.querySelectorAll('.req-status-badge').forEach(function(b) {{ b.classList.remove('active'); }});
      badge.classList.add('active');
      renderTable();
    }});
  }}

  function bindPagination() {{
    document.getElementById('reqPagination').addEventListener('click', function(e) {{
      var btn = e.target.closest('button');
      if (!btn || btn.disabled) return;
      currentPage = parseInt(btn.dataset.pg);
      renderTable();
    }});
  }}

  // Fetch request status
  function loadRequests() {{
    var tbody = document.getElementById('reqTableBody');
    var bar = document.getElementById('reqStatusBar');
    var btn = document.getElementById('reqRefreshBtn');
    if (btn) {{ btn.disabled = true; btn.textContent = '로딩중...'; }}
    tbody.innerHTML = '<tr><td colspan="8" class="req-empty">데이터를 불러오는 중...</td></tr>';
    document.getElementById('reqPagination').style.display = 'none';

    fetch(APPS_SCRIPT_URL, {{ mode: 'cors', redirect: 'follow' }})
      .then(function(r) {{ return r.json(); }})
      .then(function(data) {{
        allRequests = Array.isArray(data) ? data : [];
        allRequests.sort(function(a, b) {{
          var da = a.timestamp ? new Date(a.timestamp) : new Date(0);
          var db = b.timestamp ? new Date(b.timestamp) : new Date(0);
          return db - da;
        }});
        console.log('[BizOPS] 요청 데이터 수신:', allRequests.length, '건 (최신순)');

        var counts = {{ '대기중': 0, '진행중': 0, '완료': 0 }};
        allRequests.forEach(function(r) {{
          if (counts.hasOwnProperty(r.status)) counts[r.status]++;
        }});
        activeFilter = '';
        currentPage = 1;
        bar.innerHTML = statusBarHtml(counts, '');
        bindStatusBar();
        renderTable();
      }})
      .catch(function(err) {{
        console.error('[BizOPS] loadRequests 에러:', err);
        allRequests = [];
        tbody.innerHTML = '<tr><td colspan="8" class="req-empty">현황 데이터를 불러올 수 없습니다.</td></tr>';
        bar.innerHTML = statusBarHtml({{ '대기중': '-', '진행중': '-', '완료': '-' }}, '');
        bindStatusBar();
      }});
  }}

  // Refresh: 시각적 초기화 후 300ms 딜레이
  window.refreshRequests = function() {{
    var btn = document.getElementById('reqRefreshBtn');
    if (btn) {{ btn.disabled = true; btn.textContent = '로딩중...'; }}
    document.getElementById('reqTableBody').innerHTML = '<tr><td colspan="8" class="req-empty">데이터를 불러오는 중...</td></tr>';
    document.getElementById('reqStatusBar').innerHTML = statusBarHtml({{ '대기중': 0, '진행중': 0, '완료': 0 }}, '');
    document.getElementById('reqPagination').style.display = 'none';
    var nb = document.getElementById('reqRefreshBtn');
    if (nb) {{ nb.disabled = true; nb.textContent = '로딩중...'; }}
    bindStatusBar();
    setTimeout(loadRequests, 300);
  }};

  // Bind pagination click (persistent, no re-bind needed)
  bindPagination();

  // Load on page init
  loadRequests();

  // Form submit
  var form = document.getElementById('reqForm');
  var submitBtn = document.getElementById('reqSubmitBtn');
  if (form) {{
    form.addEventListener('submit', function(e) {{
      e.preventDefault();

      var fields = [
        {{ el: document.getElementById('reqName'), val: function(e) {{ return e.value.trim(); }} }},
        {{ el: document.getElementById('reqDoc'), val: function(e) {{ return e.value; }} }},
        {{ el: document.getElementById('reqType'), val: function(e) {{ return e.value; }} }},
        {{ el: document.getElementById('reqContent'), val: function(e) {{ return e.value.trim(); }} }}
      ];
      var hasError = false;
      fields.forEach(function(f) {{
        var msg = f.el.parentElement.querySelector('.field-error-msg');
        if (msg) msg.remove();
        f.el.classList.remove('field-error');
        if (!f.val(f.el)) {{
          hasError = true;
          f.el.classList.add('field-error');
          var em = document.createElement('div');
          em.className = 'field-error-msg';
          em.textContent = '필수 입력 항목입니다';
          f.el.parentElement.appendChild(em);
        }}
      }});
      if (hasError) return;

      var reqName = fields[0].val(fields[0].el);
      var reqDoc = fields[1].val(fields[1].el);
      var reqType = fields[2].val(fields[2].el);
      var reqContent = fields[3].val(fields[3].el);
      var priority = '';
      document.querySelectorAll('input[name="reqPriority"]').forEach(function(r) {{
        if (r.checked) priority = r.value;
      }});

      submitBtn.disabled = true;
      submitBtn.textContent = '제출 중...';

      var payload = {{
        action: 'submit',
        requester: reqName,
        document: reqDoc,
        type: reqType,
        content: reqContent,
        priority: priority
      }};
      console.log('[BizOPS] 요청 제출 데이터:', JSON.stringify(payload));

      fetch(APPS_SCRIPT_URL, {{
        method: 'POST',
        mode: 'cors',
        headers: {{ 'Content-Type': 'text/plain' }},
        body: JSON.stringify(payload)
      }})
      .then(function(r) {{ return r.json(); }})
      .then(function(data) {{
        if (data.success) {{
          showToast('요청이 등록되었습니다');
          form.reset();
          document.querySelector('input[name="reqPriority"][value="보통"]').checked = true;
          loadRequests();
        }} else {{
          showToast(data.error || '등록에 실패했습니다', true);
        }}
      }})
      .catch(function() {{
        showToast('서버 연결에 실패했습니다', true);
      }})
      .finally(function() {{
        submitBtn.disabled = false;
        submitBtn.textContent = '요청 제출';
      }});
    }});

    // Clear error on input/change
    ['reqName', 'reqDoc', 'reqType', 'reqContent'].forEach(function(id) {{
      var el = document.getElementById(id);
      if (!el) return;
      var evt = el.tagName === 'SELECT' ? 'change' : 'input';
      el.addEventListener(evt, function() {{
        el.classList.remove('field-error');
        var msg = el.parentElement.querySelector('.field-error-msg');
        if (msg) msg.remove();
      }});
    }});
  }}
}})();
</script>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).resolve().parent.parent  # /Claude/BizOPS
    data = json.loads((root / 'docs.json').read_text('utf-8'))

    cats = data['categories']
    total_docs = sum(len(c['docs']) for c in cats)
    total_cats = len(cats)

    html = '<!DOCTYPE html>\n<html lang="ko">\n<head>\n'
    html += '<meta charset="UTF-8">\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += f'<meta name="author" content="{data["meta"]["author"]}">\n'
    html += '<meta name="description" content="Toomics Global BizOps — 산출물 포탈">\n'
    html += '<title>BizOps Portal | Toomics Global</title>\n'
    html += CSS + '\n'
    html += '</head>\n<body>\n\n'
    html += build_hero(data['meta'], total_docs, total_cats)
    html += '\n<div class="container">\n\n'
    html += build_stats(cats)
    html += build_search()
    html += build_filters(cats, data['filter_types'], data['filter_statuses'])
    html += '\n  <div class="no-results" id="noResults">검색 결과가 없습니다.</div>\n\n'
    html += '  <!-- 최근 업데이트 문서 -->\n  <div class="recent-panel" id="recentPanel"></div>\n\n'
    for cat in cats:
        html += build_accordion(cat)
    html += build_request_status()
    html += build_request_form(cats, data['request_types'])
    html += '\n  <div class="req-toast" id="reqToast"></div>\n'
    html += build_changelog(data['changelog'])
    html += '\n</div>\n\n'
    html += build_footer(data['meta'])
    html += '\n'
    html += build_js(data['meta'], data['version_history'], cats)
    html += '\n\n</body>\n</html>\n'

    out = root / 'index.html'
    out.write_text(html, encoding='utf-8')
    print(f'[build] Generated {out} ({len(html):,} bytes, {total_docs} docs, {total_cats} categories)')


if __name__ == '__main__':
    main()
