# Document-Boundary Packing Masks (Flash-Decoding)

## Overview
Profile: Slashes pre-training compute waste. To maximize token-per-second processing efficiency, engineers pack multiple short, completely separate user documents into a single massive 8k or 32k token context window chunk.

## Diagram
```mermaid
graph TD
  A[Document-Boundary Packing Masks (Flash-Decoding)] --> B(Detailed Implementation)
  B --> C{Optimizations}
```

## Meta
- **Year**: 2023
- **Paper**: [Link](https://arxiv.org/abs/2308.16137)

[Back to README](../../README.md)