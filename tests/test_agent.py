import textwrap

import pytest
from livekit.agents import AgentSession, inference, llm

from agent import PaymentAssistant


def _judge_llm() -> llm.LLM:
    return inference.LLM(model="openai/gpt-4.1-mini")


@pytest.mark.asyncio
async def test_greeting_offers_payment_help() -> None:
    """The agent should greet the user and offer payment-related assistance."""
    async with (
        _judge_llm() as judge_llm,
        AgentSession() as session,
    ):
        await session.start(PaymentAssistant())

        result = await session.run(user_input="Hello")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                judge_llm,
                intent=textwrap.dedent(
                    """\
                    Greets the user in a friendly manner and offers to help with
                    payment-related tasks. Should mention payments, transactions,
                    or something related to its payment capabilities.

                    The response should be brief (one to three sentences), in plain
                    spoken prose with no lists, markdown, or emojis.
                    """
                ),
            )
        )

        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_declines_non_payment_request() -> None:
    """The agent should politely decline requests outside its payment scope."""
    async with (
        _judge_llm() as judge_llm,
        AgentSession() as session,
    ):
        await session.start(PaymentAssistant())

        result = await session.run(user_input="What's the weather like today?")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                judge_llm,
                intent=textwrap.dedent(
                    """\
                    Politely declines the weather request, explaining that it
                    can only help with payment-related tasks. May offer to help
                    with payments instead. Does not attempt to answer the weather
                    question.
                    """
                ),
            )
        )

        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_collects_info_for_payment_link() -> None:
    """When asked to create a payment link, the agent should collect required details."""
    async with (
        _judge_llm() as judge_llm,
        AgentSession() as session,
    ):
        await session.start(PaymentAssistant())

        result = await session.run(
            user_input="I need to collect money from a customer"
        )

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                judge_llm,
                intent=textwrap.dedent(
                    """\
                    Asks the user for details needed to create a payment link,
                    such as the amount, or the customer's name/email/phone number.
                    Does NOT immediately try to create a payment link without
                    having the required information first. Asks one question at a time.
                    """
                ),
            )
        )

        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_confirms_before_refund() -> None:
    """The agent should ask for confirmation before initiating a refund."""
    async with (
        _judge_llm() as judge_llm,
        AgentSession() as session,
    ):
        await session.start(PaymentAssistant())

        result = await session.run(
            user_input="I want to refund the last payment of 500 rupees"
        )

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                judge_llm,
                intent=textwrap.dedent(
                    """\
                    Does NOT immediately execute a refund. Instead, asks for
                    confirmation or clarification before proceeding. This could
                    include asking for the payment reference, confirming the
                    amount, or asking "are you sure?" type questions. The agent
                    treats refunds as sensitive operations requiring explicit
                    confirmation.
                    """
                ),
            )
        )

        result.expect.no_more_events()
