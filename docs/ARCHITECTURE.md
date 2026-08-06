# Fondazione Semplice 3.10 Architecture

## Overview

Fondazione Semplice is a dedicated AI trading research platform.

Core stack:

- OpenClaw Master (U50)
- OpenClaw Node (remote VPS)
- OctoBot
- Kronos-base
- NVIDIA Nemotron Nano 9B v2
- SGLang
- Deterministic Risk Engine
- Arena Manager

## Deployment

Master:

U50 Ubuntu machine running OpenClaw.

Node:

GCP VPS `fondazione`.

Target hardware:

- g2-standard-8
- 8 vCPU
- 32 GB RAM
- NVIDIA L4 24GB

## Trading Flow

Coinbase market data

-> OctoBot

-> Arena Manager

-> Kronos forecast

-> Nemotron decision engine

-> Risk Engine

-> Paper portfolio execution

## Safety

Default mode:

TRADING_MODE=PAPER

No AI component can bypass the Risk Engine.
