# Multi-Signal Cross-Source Entity Correlation Framework

A college minor project for collecting publicly available OSINT data and identifying potential cross-source entity relationships using multiple independent correlation signals.

## Project Goal

The system aims to:

- Collect publicly available data from multiple online sources
- Extract cyber-relevant entities
- Normalize extracted entities
- Correlate entities across different sources
- Calculate explainable confidence scores
- Preserve source provenance
- Present investigation results through a web dashboard and REST API

## Technology Stack

- Python
- FastAPI
- SQLite (planned)
- HTML/CSS/JavaScript (planned)

## Current Status

Early development.

Currently implemented:

- FastAPI application
- Health-check endpoint
- Automatic API documentation

## Planned Data Sources

- X/Twitter
- Reddit
- Instagram public profiles
- Public forums
- Public paste sites

## Run Locally

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1