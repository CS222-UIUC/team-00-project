# Team 0 Project – Spring 2025

## Introduction

The AI-Powered LaTeX Editor is a fully open-sourced, privacy-focused tool designed to streamline LaTeX editing for students in technical fields. It runs locally and supports natural language, handwriting, and image-based inputs through AI. The editor provides a modern UI, real-time preview, and fast PDF rendering — all without needing cloud access or subscriptions.

It includes the following features:

Natural Language to LaTeX: Powered by fine-tuned LLMs , your plain English is instantly translated into LaTeX.

Handwriting Recognition: Upload math photos or write directly — our ResNet-based recognizer turns it into clean LaTeX.

Tectonic-Based Rendering: Generates PDF previews on the fly using a self-contained LaTeX engine.

Document Management: Create and edit multiple LaTeX documents linked to your account.

See more details in: [proposal](https://docs.google.com/document/d/1Ipx34Mwvf48kuJAU6oV9qhhJl3--2rnNl3wdk8bEcwY/edit?tab=t.0#heading=h.qougbnz1fcec)

## Technical Architecture

![Technical Architecture](https://github.com/user-attachments/assets/c52569b5-3924-49cc-818f-13c505c43c45)

## Environment Setup

### Clone the Repository

```bash
git clone https://github.com/CS222-UIUC/team-00-project.git
cd team-00-project
```

### Initial Environment Installation

```bash
pip install -r requirements.txt
```

### Start the Application

```bash
# For Windows users
./start_servers.bat

# For Linux/MacOS users
./start_servers.sh
```
Please access localhost/8000 port for interactive UI when servers are successfully started.

## Group Members and Their Roles

Hezi Jiang: Develop Handwriting Recognition AI model, including finding data, comparing efficiency of different models, training Restnet model, and combining Connected Component with Restnet.

Kexin Hu:Develop DJANGO & SQLITE, Develop Document List, Develop LaTex Editor, Develop Tectonic LaTeX Renderer

Xinyang Li: Develop DJANGO & SQLITE, design the Login Page, Develop Document List, Develop LaTex Editor, Develop LLM AI Helper
