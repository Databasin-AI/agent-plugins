---
name: databasin-brand-guidelines
description: Applies Databasin's official brand colors and typography to any sort of artifact that may benefit from having Databasin's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
---

# Databasin Brand Styling

## Overview

To access Databasin's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Databasin brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Primary: `#ffbf00` - Primary actions and emphasis (amber/gold)
- Primary Hover: `#e8ae01` - Interactive hover states
- Secondary: `#525f7a` - Secondary elements and backgrounds
- Contrast: `#181c25` - High contrast text and dark backgrounds

**Accent Colors:**

- Success: `#62af9a` (light) / `#1d6a54` (dark) - Success states
- Error: `#ce7e7b` (light) / `#883935` (dark) - Error and danger states
- Warning: `#f59e0b` - Warning states
- Info: `#06b6d4` - Informational elements

### Typography

- **Headings**: Roboto, font-weight 300 (light)
- **Body Text**: Roboto, font-weight 400
- **Note**: Uses system font stack optimized for each OS

## Features

### Smart Color Application

- Uses Pico CSS Amber theme as foundation
- Primary amber/gold color for actions and links
- Secondary blue-gray for navigation and sidebars
- Success/error states with proper contrast ratios

### Text Styling

- Headings: Light weight (300) for modern appearance
- Body text: Standard weight (400)
- Status colors for success, error, warning states
- Responsive typography that scales with viewport

### Component Colors

- Cards use subtle borders with muted gray (`#e7eaf0`)
- Buttons have amber primary, blue-gray secondary
- Status indicators cycle through success (green), error (red), warning (amber)

## Technical Details

### Font Management

- Uses Roboto from system or CDN
- Falls back to Oxygen, Ubuntu, Cantarell, Helvetica, Arial
- Emoji support via Apple/Segoe UI emoji fonts
- Font-weight 300 for headings, 400 for body

### Color Application

- Primary: `#ffbf00` (RGB: 255, 191, 0)
- Primary Hover: `#e8ae01` (RGB: 232, 174, 1)
- Secondary: `#525f7a` (RGB: 82, 95, 122)
- Success: `#62af9a` (RGB: 98, 175, 154)
- Error: `#ce7e7b` (RGB: 206, 126, 123)
- Applied via CSS custom properties (`--pico-primary`, `--status-success`, etc.)
- Maintains color fidelity across light and dark themes
