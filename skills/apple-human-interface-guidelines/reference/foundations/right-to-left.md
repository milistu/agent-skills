# Right to Left (RTL) Design Guidelines

Guidelines for supporting right-to-left languages (Arabic, Hebrew, etc.) by reversing interface elements to match reading direction. System-provided UI frameworks support RTL by default and flip components automatically.

## Text Alignment

- **Adjust text alignment to match interface direction** if the system doesn't do so automatically. Left-aligned text in LTR → right-aligned in RTL.
- **Align paragraphs (3+ lines) based on their language, not the current context.** A left-to-right paragraph should remain left-aligned even in an RTL context. For 1-2 line text blocks, align to match the current reading direction.
- **Use consistent alignment for all items in a list.** Reverse alignment for the entire list in RTL, including items displayed in a different script.

## Numbers and Characters

- Different RTL languages use different number systems: Hebrew uses Western Arabic numerals; Arabic may use Western or Eastern Arabic numerals (varies by region).
- Apps covering mathematical/number-centric topics should identify the appropriate numeral display for each locale. Other apps can rely on system-provided number representations.
- **Never reverse the order of digits within a specific number.** Phone numbers, credit card numbers, etc. always appear in the same digit order regardless of language.
- **Reverse the order of numerals that show progress or counting direction** (e.g., labels under a rating control), but never flip the numerals themselves.

## Controls

- **Flip controls showing progress from one value to another** (sliders, progress indicators). Also reverse positions of accompanying glyphs depicting start/end values (e.g., volume speaker icons).
- **Flip navigation controls** (back buttons, next/previous) so flow matches RTL reading order. Back button should point right in RTL.
- **Preserve direction of controls referring to actual directions** or pointing to specific onscreen areas. A "to the right" control always points right.
- **Visually balance adjacent Latin and RTL scripts.** Arabic/Hebrew text can look too small next to uppercased Latin text because they lack uppercase letters. Increase RTL font size by ~2 points to balance.

## Images

- **Don't flip photographs, illustrations, or general artwork.** Flipping changes meaning and may violate copyright. Create a new version if content is tied to reading direction.
- **Reverse positions of images when their order is meaningful** (chronological, alphabetical, etc.) to preserve meaning in RTL.

## Interface Icons

SF Symbols provides RTL variants and localized symbols for Arabic and Hebrew. Custom symbols can specify directionality.

### When to Flip

- **Flip icons representing text or reading direction.** Left-aligned text bars → right-aligned in RTL.
- **Flip icons showing forward/backward motion.** Forward motion follows reading direction. Speaker with sound waves should flip so waves emanate in the reading direction.

### When NOT to Flip

- **Never flip logos or universal signs/marks** (checkmarks, etc.). Always display logos in original form.
- **Generally don't flip icons depicting real-world objects** (clocks, game controllers) unless used to indicate directionality. Right-handed tool icons don't need flipping.

### Complex Icons

- **Consider individual components and visual balance** before flipping complex custom icons.
- Maintain consistent visual design language elements (e.g., the backslash for prohibition/negation stays the same direction in both LTR and RTL).
- Flip badge positions if needed to maintain visual balance (e.g., a plus badge on a shopping cart should move from top-right to top-left when the cart flips).
- For icons containing tools (magnifying glass, pencil), preserve tool orientation while flipping the base image.

### Localized Icons

- **Create localized versions of icons displaying text** (e.g., signature, rich-text, I-beam pointer). SF Symbols offers Latin, Hebrew, and Arabic versions.
- For icons using letters to communicate concepts unrelated to reading/writing, consider designing alternatives that don't use text.