# Ollive AI Lab — AI Observability & Risk Intelligence Platform

Production-style AI evaluation platform comparing Open Source and Frontier LLM assistants across safety, hallucination risk, latency, and conversational reliability.

---

# Features

## Open Source Assistant
- Qwen2.5 OSS model from Hugging Face
- Multi-turn conversational memory
- Local inference

## Frontier Assistant
- OpenAI GPT-based assistant
- Hosted inference via API
- Same assistant experience for fair comparison

## Evaluation Framework
Benchmarks both assistants on:

- Hallucination tendencies
- Jailbreak robustness
- Harmful response resistance
- Bias & sensitive outputs
- Latency behavior
- Conversational memory

## Safety Guardrails
Custom safety filtering layer blocks:

- Malware generation
- Hacking prompts
- Harmful requests
- Unsafe instructions

## Dashboard
Interactive Streamlit dashboard with:

- Benchmark metrics
- Latency graphs
- Hallucination visualizations
- Category analysis
- Evaluation tables

---

# Architecture

```text
User Prompt
     ↓
Guardrails / Safety Layer
     ↓
Selected Assistant
 ┌──────────────┬──────────────┐
 │ OSS Model    │ Frontier API │
 └──────────────┴──────────────┘
     ↓
Evaluation Engine
     ↓
Metrics + Visual Dashboard
