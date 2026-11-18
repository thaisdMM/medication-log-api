# Slice 7, task 7.1 — done

# Telegram decisions recorded

- No code changed in the repository
- `docs/adr/0020-telegram-linking-by-deep-link.md`: account linking by deep
  link with a one-time code issued by the API
- `docs/adr/0021-bot-replies-inside-the-webhook-response.md`: the bot replies
  inside the webhook response
- `docs/open-questions.md`: the account linking question removed; the
  hibernation question stays open until 7.2
- `docs/domain-model.md`: the conversation id is linked by deep link, in a
  table of its own
- `docs/task-slices/0001-roadmap.md`: a WhatsApp Cloud API integration kept
  for the later release
- `docs/research/whatsapp-requirements.md`, on branch
  `research/whatsapp-requirements`: phone number, setup steps, cost when the
  person writes first, unofficial libraries and a provider's fee, each with
  its source. Not merged, like the other research documents
- The linking question on the first release map is closed, and the map lists
  the new decisions and the WhatsApp follow-up

**Deviations from the task text:** none.

**What this locks in for the rest of the slice:** 7.3 to 7.5 build the link
code, the link and the bot commands on ADR 0020 and ADR 0021. No outgoing
call to Telegram is written in this slice.
