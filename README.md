<a href="https://livekit.io/">
  <img src="./.github/assets/livekit-mark.png" alt="LiveKit logo" width="100" height="100">
</a>

# VoicePay — Voice Payment Assistant

A voice AI agent that lets you manage payments through natural conversation, powered by [LiveKit Agents](https://github.com/livekit/agents) and [Razorpay](https://razorpay.com/).

Talk to VoicePay to:
- **Create payment links** — collect money from customers via SMS or email
- **Check payment status** — look up any payment's details
- **View transaction history** — see recent payments and settlements
- **Process refunds** — initiate refunds with confirmation safeguards
- **Manage orders** — create and track orders

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

**Generate your Razorpay MCP token:**

1. Log in to your [Razorpay Dashboard](https://razorpay.com/) → Account & Settings → API Keys
2. Generate (or copy) your Key ID and Key Secret
3. Encode them:
   ```bash
   echo -n "rzp_test_YOUR_KEY_ID:YOUR_KEY_SECRET" | base64
   ```
4. Paste the output as `RAZORPAY_MCP_TOKEN` in `.env.local`

> **Note:** Use Test Mode keys (`rzp_test_...`) for development. No real money will be transacted.

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

## Example Conversations

> **You:** "I need to collect five hundred rupees from Rahul."
>
> **VoicePay:** "Sure! I'll create a payment link for five hundred rupees. What's Rahul's email address or phone number?"
>
> **You:** "His email is rahul@example.com."
>
> **VoicePay:** "Got it. Just to confirm — a payment link for five hundred rupees to Rahul at rahul@example.com. Shall I go ahead?"
>
> **You:** "Yes, send it."
>
> **VoicePay:** "Done! The payment link has been sent to Rahul's email. He'll receive it shortly."

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

## Testing

### In-process tests

```console
uv run pytest tests/test_agent.py -v
```

### Simulation scenarios

Full multi-turn conversations against the live agent:

```console
lk agent simulate --scenarios scenarios.yaml
```

## Frontend & Telephony

Connect any LiveKit frontend to VoicePay:

| Platform | Link |
|----------|------|
| **Web** | [`livekit-examples/agent-starter-react`](https://github.com/livekit-examples/agent-starter-react) |
| **iOS/macOS** | [`livekit-examples/agent-starter-swift`](https://github.com/livekit-examples/agent-starter-swift) |
| **Flutter** | [`livekit-examples/agent-starter-flutter`](https://github.com/livekit-examples/agent-starter-flutter) |
| **Telephony** | [Documentation](https://docs.livekit.io/telephony/) |

## Deploying to Production

This project includes a `Dockerfile` ready for deployment. See the [LiveKit deployment guide](https://docs.livekit.io/deploy/agents/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
