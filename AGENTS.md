# Repository publishing invariant

Every completed website update must be pushed to GitHub. This applies to card
content, data, figures, rendering, styles, documentation, automation, and build
or deployment configuration.

An update is not complete until all of the following hold:

1. Run the relevant validation and production build.
2. Commit only the intended repository changes.
3. Push the current branch to the configured GitHub `origin` without force.
4. Verify that `git rev-parse HEAD` equals the corresponding branch SHA from
   `git ls-remote origin`.
5. Verify the GitHub Actions / GitHub Pages result when the update affects the
   published site.
6. When OpenAI Sites is also published, deploy the same validated source tree;
   GitHub synchronization remains mandatory and is never replaced by a Sites
   source push.

If credentials, the push, CI, Pages, or Sites deployment are ambiguous, stop
and report the exact boundary. Do not claim publication or synchronization.

## Independent Paper Card batches

For a multi-paper campaign or long Goal, read `docs/CARD_CONTEXT.md` and use
`python3 scripts/card_batch.py context` for compact controller checkpoints and
single-paper handoffs. Delegate independent paper units to fresh subagents
with `fork_context=false`; keep one paper per agent by default and preserve
the campaign's authorized concurrency (currently two). Do not reuse a paper
agent for unrelated papers. Keep detailed evidence and logs in that unit's
files; return a short outcome and artifact pointers. The parent is the sole
ledger writer and integrator, with risk-routed scientific review and the full
existing publication gates. Context packaging does not authorize resuming
stopped work, publishing, lowering review standards or changing Goal status.

For controller-owned incremental logistics and measured stage usage, read
`docs/CARD_WORKFLOW.md` and use `card_batch.py workflow`. Keep scope authority
immutable, record interval usage deltas (unknown values remain null), and emit
summaries at batch boundaries. This tool never resumes unstarted work or
replaces the context handoff, scientific acceptance or publication gates.
