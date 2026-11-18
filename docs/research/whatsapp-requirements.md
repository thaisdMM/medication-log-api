# What a WhatsApp bot would need

Research for a later-release WhatsApp integration. Facts only; no decision.
Sources were read on 2026-11-18. Anything a source does not state is marked
**unverified**.

## Sources

- [NUMBERS] Business phone numbers — https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers.md
- [START] Get started — https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started.md
- [PRICING] Pricing — https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md
- [FAQ] Unofficial apps — https://faq.whatsapp.com/1217634902127718
- [TWILIO] Twilio WhatsApp pricing — https://www.twilio.com/en-us/whatsapp/pricing

## Phone number

- "Numbers already in use with WhatsApp cannot be registered unless they are
  deleted first" [NUMBERS]. A number in daily use stays out unless it leaves
  the WhatsApp app.
- Completing the get-started steps generates and registers a test business
  phone number automatically [NUMBERS]. How many recipients it accepts, and
  whether it can be used for good, are **unverified**.

## What has to exist before the first message

- A Facebook or managed Meta account, registered as a developer [START].
- A business portfolio, chosen or created while creating the app [START].
- A Meta app with the WhatsApp use case [START].
- An access token. The temporary one "expires quickly and is not suitable for
  development purposes"; a permanent one comes from a system user in Business
  Settings [START].
- A webhook endpoint for message notifications [START].
- Whether business verification is required is **unverified**: the
  get-started page does not mention it.

## Cost when the person writes first

- When a person writes, a 24-hour customer service window opens; inside it the
  business can send non-template messages [PRICING].
- Each business phone number has "one free tier of 1,000 delivered service
  messages per month", from October 1, 2026; unused messages do not roll over
  [PRICING].
- After the free tier, service messages are charged per message. Without a
  payment method, Meta "will deliver service messages within the free tier but
  not deliver them after the free tier has been used" [PRICING].
- A message the server starts (a reminder) needs a template. The pricing page
  compares utility messages to users in Brazil at "0.68 ¢ per message"; the
  currency is not stated there [PRICING].

## Unofficial libraries

- Unofficial apps are versions built by third parties without WhatsApp's
  approval; using them, or connecting an account to them, violates the Terms
  of Service, and the account can be banned temporarily or permanently [FAQ].

## Through a provider

- Twilio charges "$0.005 per message", inbound or outbound, plus Meta's fee,
  which it passes through [TWILIO].

