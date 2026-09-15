# From copy to modules

Choose modules after the product argument is clear and before detailed layout or motion work. A module is justified by a narrative job, not by a fashionable component category.

## Claim map

| Narrative step | Claim or question | Evidence | Best proof form | Needed interaction/state |
|---|---|---|---|---|
| Arrival | What is this and why care? | product definition | headline + concise visual | optional state preview |
| Trust | Is the capability real? | source/runtime fact | dynamic mock, screenshot, command, diagram | inspect, replay, compare |
| Mechanism | How does it work? | architecture/workflow | flow, annotated panel, sequence | step, hover, scrub |
| Action | What do I do next? | install/open/docs route | contextual action | copy, open, confirm |

Use the smallest proof form that communicates the claim. Not every feature needs a card, not every workflow needs animation, and not every page needs a dashboard recreation.

## Module contract

Complete this for every substantial module:

```md
### Module: <name>

Narrative job:
Claim or visitor question:
Evidence source:
Visible copy and data:
Default state:
User action:
State transitions:
Entry:
Exit and re-entry:
Replay or loop policy:
Desktop composition:
768px composition:
390px composition:
Reduced-motion behavior:
No-JavaScript or failure state:
Acceptance proof:
```

## Selection tests

Keep a module only if it makes an important claim easier to understand, provides efficient evidence, lets the visitor rehearse a real action, resolves a trust objection, or provides necessary navigation/conversion.

Combine or remove modules that repeat the same job. If a module has animation but no state or narrative change, reconsider it as decoration.

## Approval artifact

In guided mode, present a short table showing module, job, proof form, interaction, and mobile equivalent. Approval concerns argument and behavior, not pixel details; typography, spacing, easing, and ornamental choices remain design decisions unless the user asks to control them.
