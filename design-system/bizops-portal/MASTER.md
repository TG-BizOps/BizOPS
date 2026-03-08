# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** BizOPS Portal
**Updated:** 2026-03-08
**Category:** Analytics Dashboard / Document Portal

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#1E40AF` | `--color-primary` |
| Primary Dark | `#1E3A8A` | `--color-primary-dark` |
| Secondary | `#3B82F6` | `--color-secondary` |
| CTA/Accent | `#F59E0B` | `--color-cta` |
| CTA Hover | `#D97706` | `--color-cta-hover` |
| Background | `#F1F5F9` | `--color-background` |
| Surface | `#FFFFFF` | `--color-surface` |
| Text | `#0F172A` | `--color-text` |
| Text Muted | `#64748B` | `--color-text-muted` |
| Text Subtle | `#94A3B8` | `--color-text-subtle` |
| Border | `#E2E8F0` | `--color-border` |

**Color Notes:** Blue data + amber highlights. Dark navbar (`#0F172A`).

#### Category Colors (Stat Cards / Accordion Borders)

| Category | Hex | Usage |
|----------|-----|-------|
| CS 운영 | `#2563EB` | Blue |
| FAQ | `#0891B2` | Cyan |
| AI 챗봇 | `#7C3AED` | Purple |
| 차지백 | `#F59E0B` | Amber |
| IP 보호 | `#10B981` | Green |
| CS Dashboard | `#6366F1` | Indigo |
| 대시보드 | `#EF4444` | Red |
| 정책/약관 | `#0F766E` | Teal |
| 기타 | `#475569` | Slate |

### Typography

- **Heading Font:** Fira Code (`'Fira Code', 'Malgun Gothic', monospace`)
- **Body Font:** Fira Sans (`'Fira Sans', 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', -apple-system, sans-serif`)
- **Mood:** dashboard, data, analytics, code, technical, precise
- **Google Fonts:** [Fira Code + Fira Sans](https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap)

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` | Tight gaps |
| `--space-sm` | `8px` | Icon gaps, inline spacing |
| `--space-md` | `16px` | Standard padding |
| `--space-lg` | `24px` | Section padding |
| `--space-xl` | `32px` | Large gaps |
| `--space-2xl` | `48px` | Section margins |
| `--space-3xl` | `64px` | Hero padding |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Cards, buttons |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Hero images, featured cards |

### Border Radius

| Token | Value |
|-------|-------|
| `--radius-sm` | `8px` |
| `--radius-md` | `12px` |
| `--radius-pill` | `20px` |

### Transitions

All interactive elements: `200ms ease` (`--transition`)

---

## Component Specs

### Navbar

```css
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  height: 52px;
  background: #0F172A;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  /* Logo (left) | Status badge + Avatar (right) */
}
```

### Hero Section

```css
.hero {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
  padding: 28px 32px 20px;
  color: white;
  /* Left: Title + Subtitle + Metadata */
  /* Right: CTA + Link buttons */
}
```

**Hero Stat Strip:** Horizontal flex, 8px gap, 9 category cards.
```css
.stat-card {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-top: 3px solid [category-color];
  padding: 10px 4px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
.stat-card:hover {
  background: rgba(255,255,255,0.14);
}
```

### Buttons

```css
/* Primary CTA (Amber) */
.hero-cta {
  background: var(--color-cta);
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  transition: all 200ms ease;
}
.hero-cta:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
}
```

### Search + Filter

```css
.search-filter-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.search-input {
  height: 40px;
  padding: 0 14px 0 38px;  /* left padding for icon */
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
}
.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(30,64,175,0.12);
}
```

### Cards (Link Cards)

```css
.link-card {
  display: flex;
  gap: 14px;
  padding: 16px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  min-width: 340px;
  transition: all 200ms ease;
}
.link-card:hover {
  background: #F8FAFC;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
```

### Accordion Sections

```css
.accordion {
  border-left: 4px solid [category-color];
  border-radius: var(--radius-md);
  background: white;
  margin-bottom: 8px;
}
.accordion-header {
  /* Icon (32x32 circle) + Title (Fira Code 15px 700) + Count badge + Chevron */
  padding: 14px 20px;
  cursor: pointer;
}
.accordion-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.35s ease;
  background: #FAFBFC;
}
```

### Modals

```css
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}
.modal {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
}
```

---

## Layout

### Container

```css
.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 16px 24px 64px;
}
```

### Link Grid

```css
.link-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 12px;
}
```

### Footer

```css
.footer {
  background: #0F172A;
  color: rgba(255,255,255,0.5);
  padding: 24px;
  margin-top: 40px;
}
```

---

## Style Guidelines

**Style:** Data-Dense Dashboard / Document Portal

**Keywords:** Multiple charts/widgets, data tables, KPI cards, minimal padding, grid layout, space-efficient, maximum data visibility

**Best For:** Business intelligence dashboards, operational document portals, enterprise reporting

**Key Effects:** Hover tooltips, chart zoom on click, row highlighting on hover, smooth filter animations, data loading spinners

### Page Pattern

**Pattern Name:** Document Portal with Hero KPI Strip

- **Information Architecture:** Hero with KPI stat strip → Search/Filter → Accordion sections with link cards
- **Navigation:** Sticky navbar + accordion expand/collapse + in-page anchors
- **Stat Cards:** Single horizontal row in hero, clickable to scroll to section
- **Content:** Grid of link cards per category, with icon, title, description, version badge, type badge

---

## Responsive Breakpoints

| Breakpoint | Key Changes |
|-----------|-------------|
| `1024px` | Container padding reduced |
| `768px` | Stat cards horizontal scroll, link grid single column, hero padding reduced |
| `375px` | Search/filter stacked, CTA full width |

`prefers-reduced-motion`: All animations/transitions → 0.01ms

---

## Anti-Patterns (Do NOT Use)

- ❌ Ornate design
- ❌ No filtering
- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y
- ❌ **Dark mode** — Light mode only (라이트모드만)

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile

---

## Shared with CS Dashboard

The CS AI Dashboard (`toomics-ai-agent/dashboard/`) shares the same design system foundation:

| Token | Portal | CS Dashboard | Match |
|-------|--------|--------------|-------|
| `--color-primary` | `#1E40AF` | `#1E40AF` | ✅ |
| `--color-primary-dark` | `#1E3A8A` | `#1E3A8A` | ✅ |
| `--color-secondary` | `#3B82F6` | `#3B82F6` | ✅ |
| `--color-cta` | `#F59E0B` | `#F59E0B` | ✅ |
| `--color-background` | `#F1F5F9` | `#F1F5F9` | ✅ |
| `--color-text` | `#0F172A` | `#0F172A` | ✅ |
| `--color-border` | `#E2E8F0` | `#E2E8F0` | ✅ |
| `--font-heading` | Fira Code | Fira Code | ✅ |
| `--font-body` | Fira Sans | Fira Sans | ✅ |
| `--radius-sm/md/pill` | 8/12/20px | 8/12/20px | ✅ |
| `--shadow-sm/md/lg` | Same values | Same values | ✅ |
| `--transition` | 200ms ease | 200ms ease | ✅ |

**Differences (intentional):**
- CS Dashboard adds semantic colors: `--color-success`, `--color-danger`, `--color-warning`, `--color-info`, `--color-purple`, `--color-cyan`
- CS Dashboard uses `--color-bg` (alias for `--color-background`), `--color-card` (alias for `--color-surface`)
