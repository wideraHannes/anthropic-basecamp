**To:** Priya Anand, VP Customer Operations, Meridian
**Subject:** Re: Honestly not sure this is going to work

Hi Priya,

Yes, it's fixable, and it's not the model.

**What was wrong:** The agent's instructions told it to handle only one issue per ticket and to always close tickets as "resolved". In T-4471, that meant SSO got fixed, the $1,200 refund was ignored, and the ticket was still marked "resolved".

**What we changed:** Only the instructions, no code and no model change. Every issue now gets handled, "resolved" is only allowed when everything is actually fixed, and anything the system can't decide goes to a person.

**Proof:** We ran each ticket 5 times, including two tickets the fix was never tuned on.
- Before: 1 of 9 resolved. After: **14 of 15**, at $0.15 per ticket (was $0.13).
- A bigger model resolved **0 of 5** at twice the cost. A better model wouldn't have helped.

**One open point:** In 1 run, the agent handed a ticket to a human instead of resetting 2FA itself first. That's not harmful, just slower, and we have the fix ready to test.

Happy to walk your leadership through it.

Best,
Hannes
