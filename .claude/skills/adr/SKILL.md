---
name: adr
description: The rules for turning a project decision into an Architecture Decision Record — the criterion that separates an ADR from a spec, the MADR sections in use, and seven rules that exist because each was broken once.
disable-model-invocation: true
---

# Writing an ADR

**No decision of this project is written in this file, on purpose.** What the
project decided lives in `docs/`; what an archive file says lives in the archive.
This file says *how a record is written*, never *what is true about the system*.
A decision copied here would become a second source competing with the record
that owns it.

## What an ADR is, and what it is not

An ADR answers *why did we choose this and not that*. What is true about the
system is spec, and belongs under `docs/`.

Two tests settle which one a piece of text is:

1. Could a competent engineer, holding the same information, reasonably have
   chosen differently? Yes → ADR. No → spec.
2. When it changes, does a new record supersede it while the old one survives
   marked `Superseded`? → ADR. Do you edit it in place because the old text is
   worthless? → spec.

## The template

MADR. Front matter: `status`, `date`, `decision-makers` — and `consulted` or
`informed` only when they have content.

| Section | Required |
|---|---|
| Context and Problem Statement | yes |
| Considered Options | yes |
| Decision Outcome | yes |
| Decision Drivers, Consequences, Confirmation, Pros and Cons, More Information | no |

Target length is one screen. A record that does not fit is carrying narrative,
or it is two decisions wearing one title.

## Seven rules

1. **Nothing enters that is not written.** Every sentence comes from the source
   or from a document that already exists. A framing that *follows from* the
   decision is inference, and inference is what this file exists to stop.

2. **Ask before writing a negative consequence**, and ask whether there is a
   positive the source never wrote down. A record listing three costs and no
   benefit misrepresents a decision its author considers a good one.

3. **No motive in the source, no motive in the record.** State the choice and
   stop. A constructed motive is worse than an absent one: nobody who was not in
   the original conversation can tell it apart from a real one.

4. **Use only the sections the source fills.** MADR has a full form and a
   minimal one, and most records are the minimal one. An empty heading is not
   fidelity to the template.

5. **A decided value is written only in the record that decides it.** A status
   code, a library or a field name repeated in a record that does not decide it
   is how a superseded value survives a rewrite.

6. **The rejected option travels; the account of rejecting it does not.** An
   alternative enters as a Considered Option with the technical reason it lost.
   Who proposed it, who withdrew it and on which day never enter. Attribution is
   the `decision-makers` field, never a quotation in the body.

7. **Ask instead of inferring — and when a draft carries inference anyway, mark
   the exact sentence.** The question costs one round. An invented sentence
   costs the reader the work of finding it, and it is found only by someone who
   knows the source by heart. A draft that carries inference names it: which
   sentence, and what it was built from, separated from what the source writes.
   A less complete record is preferred to a complete one holding something the
   source does not say.

## When something is missing

A gap in the source is a gap in the record, declared as such — never filled.

Stop and ask when: the source gives no motive, the source gives only costs, the
source names no alternative where Considered Options is required, the date of
the decision is not recorded anywhere, or two sources disagree. One question at
a time.

## Before it becomes a file

The draft is written in the conversation. It becomes a file after Thaís
approves it, never before.
