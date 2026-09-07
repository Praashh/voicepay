# VoicePay — Voice Payment Assistant

A voice AI agent that lets you manage payments through natural conversation.

Talk to VoicePay to:
- **Create payment links** - collect money from customers via SMS or email
- **Check payment status** — look up any payment's details
- **View transaction history** - see recent payments and settlements
- **Process refunds** - initiate refunds with confirmation safeguards
- **Manage orders** - create and track orders

Built on:
- [LiveKit Cloud](https://cloud.livekit.io/) for real-time voice infrastructure
- [LiveKit Inference](https://docs.livekit.io/agents/models/inference) for AI models (STT, LLM, TTS)
- [Razorpay MCP Server](https://github.com/razorpay/razorpay-mcp-server) for payment operations via Model Context Protocol

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- A [LiveKit Cloud](https://cloud.livekit.io/) account
- A [Razorpay](https://razorpay.com/) account with API access

### 1. Install dependencies

```console
uv sync
```

### 2. Configure environment

Copy `.env.example` to `.env.local` and fill in your credentials:

```bash
# LiveKit Cloud credentials (from cloud.livekit.io)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Razorpay MCP token (Base64-encoded key_id:key_secret)
RAZORPAY_MCP_TOKEN=your-base64-token
```


### 3. Run the agent

**Talk directly in your terminal:**

```console
uv run python src/agent.py console
```

**Run for use with a frontend or telephony:**

```console
uv run python src/agent.py dev
```

**Production:**

```console
uv run python src/agent.py start
```

## Demo Conversations

https://github.com/user-attachments/assets/Voicepay.mp4

## Architecture

```
┌─────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│   User      │◄───►│   LiveKit Cloud      │◄───►│   VoicePay Agent   │
│   (Voice)   │     │   (WebRTC/SIP)       │     │                    │
└─────────────┘     └──────────────────────┘     │  STT → LLM → TTS  │
                                                  │        │           │
                                                  │   MCPToolset       │
                                                  │        │           │
                                                  └────────┼───────────┘
                                                           │
                                                  ┌────────▼───────────┐
                                                  │  Razorpay MCP      │
                                                  │  Server (Remote)   │
                                                  │                    │
                                                  │  35+ payment tools │
                                                  └────────────────────┘
```

