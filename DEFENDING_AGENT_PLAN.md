# Defending Agent Design Plan

This document outlines a potential architecture for a **Defending Agent** built on the LiteLLM framework. The goal of the agent is to analyze code and interaction traces produced by other agents in order to identify and help mitigate risks of prompt injection.

## 1. Overview

The Defending Agent operates in an offline or semi-offline setting. It processes log files, source code, and interaction traces for victim agents and looks for patterns that may enable adversaries to inject malicious prompts or code. The agent does not execute or modify the victim agent's code; instead it provides analyses and suggested defenses.

## 2. Key Features

1. **File Reading**
   - The agent ingests files from predefined directories (e.g., `trajectories/` for trace logs or `src/` for code).
   - Use standard Python file IO to load content. For large files, stream reading can be used.

2. **Content Organization & Analysis**
   - Parse text files and code to extract commands, prompts, and user inputs.
   - For structured data (e.g., JSON logs), load using Python's `json` module.
   - Identify commands that pass user input directly into LLM calls or shell commands.

3. **Injection Point Detection**
   - Search for patterns where external input is concatenated with system prompts or forwarded to the LLM without sanitization.
   - Maintain a list of high-risk lines or files. Provide context snippets so developers can quickly inspect them.

4. **Defensive Suggestions**
   - Recommend checking input boundaries, applying prompt sanitization, or restructuring prompts to minimize injection risk.
   - Provide example mitigation patterns, such as separating user-provided text from system prompts and validating content before use.

## 3. Implementation Steps

1. **Set Up LiteLLM**
   - Install the LiteLLM package (`pip install litellm`).
   - Configure the agent to use a local or remote model for analysis. Since the agent only analyzes text and code, a smaller model may suffice.

2. **Develop File Loaders**
   - Write utilities in Python to crawl directories, read files, and store them in memory for analysis. Maintain a configuration file listing the paths to inspect.

3. **Static Analysis Module**
   - Implement functions that scan for specific patterns: unsanitized user input, direct string concatenation with prompts, or shell command injections.
   - Consider using a simple rule-based approach or pattern matching to keep the logic transparent.

4. **Reporting**
   - Summarize findings in a structured report (e.g., markdown or JSON). Include file names, line numbers, and recommended mitigations.
   - Provide a final summary that can be manually reviewed before applying any changes.

## 4. Usage

Developers run the Defending Agent after collecting logs or when reviewing code updates. The agent outputs a list of potential injection points and recommended fixes, assisting developers in hardening their agent-based systems.


## 5. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Defending Agent                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ File Reader │  │  Analyzer   │  │ Defense Engine  │  │
│  │   Module    │  │   Module    │  │     Module      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                  LiteLLM Framework                      │
├─────────────────────────────────────────────────────────┤
│           External Systems & File Storage               │
└─────────────────────────────────────────────────────────┘
```

### 5.1 File Reader Module
- **FileWatcher**: monitors the `trajectories/` folder for new or updated files.
- **TraceCollector**: loads interaction traces from JSON logs.
- **CodeAnalyzer**: parses source files for structural information.

### 5.2 Analyzer Module
- **ContentProcessor**: cleans and normalizes text.
- **VulnerabilityScanner**: detects potential injection points.
- **RiskAssessment**: assigns a risk level to each finding.

### 5.3 Defense Engine Module
- **AttackSimulator**: explores how an attacker might exploit a vulnerability.
- **DefenseGenerator**: proposes mitigations and best practices.
- **ResponseCoordinator**: coordinates alerting and reporting.

## 6. Data Flow

```
[Victim Agent Files]
        ↓
[File Reader Module]
        ↓
[Raw Data Processing]
        ↓
[Analyzer Module]
        ↓
[Vulnerability Assessment]
        ↓
[Defense Engine Module]
        ↓
[Protection Strategies & Alerts]
```

## 7. Monitoring Trajectories

A simple Python script (`trajectory_monitor.py`) demonstrates how to watch the
`trajectories/` directory for new JSON files. It uses the `watchdog` package when
available and falls back to periodic polling otherwise. Each new file is parsed
and inspected for suspicious patterns in user messages. See the script for
implementation details.
