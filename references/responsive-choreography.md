# Responsive choreography

Responsive design preserves narrative priority and interaction capability across widths. It does not preserve every desktop object or its exact geometry.

## Design three compositions

For substantial pages, reason about desktop, an intermediate state around 768px, and a narrow-mobile state around 390px. Define an independent reading order, compact interaction, and intentional information reduction during module planning—not as cleanup after desktop implementation.

## Responsive transformation verbs

For each module choose explicit transformations:

- **reorder** — change reading order to preserve the argument;
- **stack** — replace side-by-side comparison with a clear sequence;
- **focus** — show the most important rows or state and hide secondary detail;
- **summarize** — replace a dense panel with a compact equivalent;
- **scroll** — use deliberate local scrolling only when comparison requires it;
- **replace** — use a mobile-specific interaction or static proof when the desktop mechanism is unsuitable.

“Scale down” is rarely sufficient.

## Mobile equivalence test

For every substantial desktop panel ask:

1. What exact claim does it prove?
2. Can a mobile visitor understand the same claim without zooming or clipping?
3. Is the primary action reachable and comfortably tappable?
4. Does mobile retain meaningful interaction or provide an honest compact equivalent?
5. Does the first screen have intentional title wrapping and a visible next action?

Mobile may show fewer details, but it must not lose the page's core promise or proof.

## Runtime acceptance

At desktop, 768px, and 390px verify document overflow, clipping, focused elements, headline wrapping, first-screen hierarchy, navigation, dynamic-panel state, keyboard/touch equivalence, fixed-element footprint, portrait composition, and longer localized copy.
