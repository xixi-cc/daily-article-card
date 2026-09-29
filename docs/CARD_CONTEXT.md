# Context isolation for independent Paper Cards

The main Goal chat schedules and integrates work. Detailed reading belongs to
a fresh per-paper subagent; unrelated papers must not inherit each other's
history. This changes information routing, not the scientific standard.

## Controller: retain only scheduling state

At a batch boundary or after compaction, read the latest `controller.md` and
the current small batch's receipts. Do not dump the full run manifest, all old
overlays, every source hash, full PDF text, derivations or browser output into
the parent chat. The full ledger remains on disk and tools query it internally.

Generate a checkpoint from the authoritative manifest:

```bash
python3 scripts/card_batch.py context brief \
  --manifest /absolute/current-manifest.json \
  --out /absolute/new-checkpoint --limit 5
```

This produces `controller.md` and `controller.json`: counts, production paths,
baselines, at most five routing candidates, preserved boundaries and pointers.
It never starts work. Optional `--runtime /absolute/runtime.json` records the
parent-maintained active-unit registry in this view. Its `active_units` list
contains only `key`, actual `agent_id`, `packet_path`, and `stage`. At most two
paper workers may be active under the present campaign policy. A missing
registry means unknown runtime state, not zero running agents. Before a
recovery, check both agent/process identity and artifact state; a quiet log is
not proof that a writer is gone.

Optional `--receipts /absolute/current-receipts` reads short `*.receipt.json`
files and shows only counts plus a bounded preview. Reported items are excluded
from the unreported preview and remain **awaiting parent decision**, never
automatically accepted. Keep one current receipt per paper in that directory;
archive prior revisions separately. This view verifies packet/result hashes,
not the scientific evidence again. After a real acceptance decision, the sole
parent writer updates the new run's mutable authority, preserving historical
campaign snapshots. Generate the next checkpoint from that new authority.

## Worker: one paper, fresh history

```bash
python3 scripts/card_batch.py context packet \
  --manifest /absolute/current-manifest.json --key Daily:2609.00399 \
  --intake /absolute/one-paper-intake.json \
  --role worker --out /absolute/new-unit
```

The packet includes only that paper's identity, source version if known,
eligibility boundary, instruction references and existing evidence pointers.
It defines a unique writable `work/` directory and a bounded result contract.
It does not embed card prose or source reports, and does not claim the item.
For pending Daily candidates, use `scripts/prepare_card_intakes.py` to extract
only that paper from the hash-pinned frozen queue. The optional `--intake` binds
the paper nomination and queue hash to the packet; it remains an abstract
prescreen, not a final grade or a substitute for exact-version PDF review.

After the user's actual batch-resume authorization and ownership check, spawn
with `fork_context=false` and an initial prompt pointing to `worker-prompt.txt`.
Do not fork the parent history. Inherit the model and reasoning settings unless
the user asks for a change. The dispatch message must state the authorized
operation and the exact unit. In the current runtime, use the subagent tool,
not `create_thread`; do not manufacture hundreds of user-owned sidebar chats.

Use one paper per worker by default. Only closely related small papers with
shared source evidence justify a bounded two/three-paper unit. Do not increase
concurrency to compensate for long context. The earlier two-worker policy and
single parent integrator remain in force. Extraction/API concurrency is a
separate limit and does not change here.

Keep an agent for targeted corrections to the **same** paper when useful. Once
its deliverable is durable and accepted (or its exception is recorded), close
it; do not send the next unrelated paper to that agent. Do not close a running
worker just to free a slot without securing its checkpoint.

## Evidence is complete; the return message is short

Keep the full official PDF/version, physical-page evidence, all needed equation
and figure checks, full report and review receipts inside the paper's durable
evidence flow. No evidence is discarded to meet a token or summary quota.
Read core evidence first and follow required source pointers as needed.

The worker writes `work/result.json`, using the contract in its prompt:

- `key`, `packet_sha256`, `source_version`, `outcome`;
- `summary` at most 400 characters, at most eight short `risk_flags`;
- short `next_action`, `full_report` path/hash;
- at most six `artifacts` path/hash pointers; large evidence sets use a manifest.

Its final chat message contains only the key, outcome, result path and blocker,
at most 600 characters. Do not return full derivations, manuscript prose, giant
JSON arrays, screenshots or command logs. These limits govern the routing
envelope, not what must be scientifically checked.

```bash
python3 scripts/card_batch.py context receipt \
  --packet /absolute/new-unit/packet.json \
  --result /absolute/new-unit/work/result.json \
  --out /absolute/current-receipts/paper.receipt.json
```

The receipt verifies key, packet/input/authority versions, bounded fields and
artifact hashes/scope. Oversized returns are rejected for a corrected envelope,
not silently truncated. A receipt is explicitly **not** scientific acceptance,
installation or publication. `card_staged` needs a card plus evidence-manifest
pointer. Daily/Collection eligibility and full scientific checks still apply.

## Review and integration

The parent reads the short receipt, runs `delivery`, and routes central theorems,
complex equations, quantitative comparisons or source conflicts to a fresh
reviewer when needed. Give the reviewer the exact paper/artifact/claim scope,
not all prior batches. It can open the complete source evidence. The parent
does not repeat the full worker proof simply to regenerate another summary.

An unresolved source exception is a valid terminal outcome for the ordinary
queue. Preserve evidence and the exact reopening condition; open-ended proof
repair or external-reference archaeology is separate work, not an unlimited
continuation of every card. Never convert missing evidence into a positive grade.

Install/build through the sole parent writer. Accumulate at most ten accepted
cards per full validation batch; the context unit and release batch are distinct.
Only new/changed artifacts invalidate acceptance. Avoid dumping passing logs;
record their paths and summarize failures relevant to the current decision.

## Long Goal continuity

Every continuation should finish a work unit, record an exception, accept an
artifact or advance a batch. While agents run, do independent useful work;
otherwise use a bounded event wait. Do not repeatedly print unchanged status,
rewrite a cumulative history, or force another turn with a Stop hook.

After compaction, resume from the latest checkpoint and active job identities.
There is no supported operation in this workflow to erase already accumulated
parent chat history, nor does writing a checkpoint reset the model's context.
Fresh worker context prevents unrelated paper histories from spreading; parent
history growth is reduced by short receipts. A genuinely new parent chat is a
separate explicit user choice, never created automatically by these tools.

## Measure before claiming savings

Record controller/packet/result sizes, rework and acceptance outcomes. A reduced
file size is not a measured reduction in token cost or account allowance. When
the runtime exposes it, compare input, cached input, uncached input, output,
elapsed time, acceptance rate and repeated reading over comparable small batches.
Leave unavailable usage fields null. Do not lower model/reasoning or scientific
checks merely to make a token count smaller.

Official background: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
describes keeping intermediate work outside the main chat and returning
summaries. The exact `fork_context=false` field is verified against this
session's callable spawn tool; other runtimes must use their supported schema.
