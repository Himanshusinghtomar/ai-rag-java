# Java Codebase RAG System

## Overview
A generic, low-cost Retrieval-Augmented Generation (RAG) system for large Java microservice architectures.

## Features
- AST-based Java parsing
- Method-level semantic chunking
- Dependency-aware indexing
- Zero fine-tuning
- Local LLM support (Ollama)

## Architecture
Codebase → Chunking → Embeddings → Vector Store → LLM

## Why RAG?
Fine-tuning is expensive and stale. RAG enables live, precise, project-aware assistance.

## Supported Use Cases
- Code navigation
- Bug root cause analysis
- Dependency tracing
- Configuration understanding
