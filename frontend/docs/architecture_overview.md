# Frontend Technical Architecture

> [!IMPORTANT]
> **Compatibility Note**: Due to the current environment using **Node.js v14.21.3**, the project requires specific versions of build tools to avoid syntax errors.

## Overview
The frontend of VulnScanC is a Single Page Application (SPA) built with **React**. It provides a web-based interface for interacting with security scanning data, managing projects, and utilizing AI-driven analysis tools.

## Tech Stack
- **Core Library**: React
- **Routing**: React Router DOM
- **Bundler**: Webpack
- **Styling**: CSS (Modular approach with CSS files per component and global theme support)
- **Icons**: SVG

### Build Tooling (Node.js v14 Compatibility)
To ensure stability in the current environment, the following versions are used:
- **webpack**: `5.75.0`
- **webpack-dev-server**: `4.15.1`
- **copy-webpack-plugin**: `11.0.0`
