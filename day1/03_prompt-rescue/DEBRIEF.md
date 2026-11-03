# Prompt Rescue: What We Fixed

We went from **6 out of 21** test tickets passing to **20 out of 21**. We kept the same model (Claude Haiku) and still make just one API call per ticket.

**1. The model made up details.**
The old prompt said "always include all fields", so whenever a ticket didn't say something, Claude filled the gap with a guess. For example, it turned "our CRM tool" into "CRM Platform" and invented error codes that weren't in the ticket. Now the prompt tells Claude to copy values word for word from the ticket, and to leave a field empty (null) when the ticket doesn't mention it.

**2. Angry tickets got high priority.**
An all-caps "CRITICAL" request for a new feature (SSO) was rated P1, the top priority. The old prompt described each level in a single short line, so Claude had little to go on besides the customer's tone. We rewrote each level with a fuller description and concrete examples, and told Claude to ignore the tone:

- **P1:** the system is down, data is lost, or there's a security or privacy issue (for example, other users' personal data showing up). This stays P1 even if only one person reported it.
- **P2:** an existing feature is broken for a team, with no workaround (for example, wrong search results after an update, a failing webhook, a dashboard showing old data). Slow but still working is P2, not P1.
- **P3:** small or cosmetic bugs (for example, a cut-off tooltip), problems that go away when you retry, and vague tickets that don't say what's actually broken.
- **P4:** feature requests (for example, dark mode, SSO, a calendar view), however urgent they sound.

We also added a rule for tickets with several issues: use the highest priority among them.

**3. The JSON could break.**
The old prompt only asked Claude to reply in JSON, so nothing guaranteed a valid result. Now we use the API's structured outputs (`client.messages.parse()` with a Pydantic schema), which forces every reply into the exact format our pipeline expects.

**4. The reply didn't match the rating.**
Claude sometimes promised to "fix" a feature request. Now each type of ticket has its own reply rules: feature requests are logged for the product team with no fix promised, and vague tickets get follow-up questions.

**Still open:** One borderline ticket, where the issue comes and goes and a retry works, still flips between P2 and P3. We didn't add a special rule just for that one test case, because then we'd be tuning to the test instead of fixing the real problem.
