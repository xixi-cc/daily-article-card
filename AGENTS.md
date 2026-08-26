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
