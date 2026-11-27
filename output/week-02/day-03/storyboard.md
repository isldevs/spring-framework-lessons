# Timed storyboard — Optional dependencies

- 0.000–1.993s: Complete cover plus immediate hook and moving lookup; transition1–2s.
- 1.993–6.865s: Required AuditPublisher lookup: zero candidates; refresh fails.
- 6.865–12.459s: Constructor parameter becomes Optional<AuditPublisher>; nested-type resolution can return empty.
- 12.459–17.755s: One matching managed publisher: wrap the same reference and supply through constructor.
- 17.755–23.854s: Separate fresh absent context: empty Optional, service skips extra notification, context ready.
- 23.854–34.839s: Actual four-test proof; absence versus ambiguity qualification; app→Spring→Optional→service recap.
- 34.839–36.180s: Separate spoken Thanks after the full two-second recap hold.

Complete recap reading hold: 32.839208–34.839208s. Edit timing is illustrative, not framework execution performance.
