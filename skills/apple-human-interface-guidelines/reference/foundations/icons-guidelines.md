# Icons Guidelines

Guidelines for designing interface icons (glyphs) across Apple platforms, including best practices, standard SF Symbol mappings, and macOS document icon specifications.

## Best Practices

- **Create recognizable, simplified designs.** Use familiar visual metaphors directly related to the actions or content they represent.
- **Maintain visual consistency** across all interface icons — consistent size, detail level, stroke weight, and perspective. Adjust individual icon dimensions as needed to match visual weight.
- **Match weights of interface icons and adjacent text** for consistent appearance, unless deliberately emphasizing one over the other.
- **Add padding for optical alignment** on asymmetric icons. Include adjustment pixels as padding around the icon so geometric centering of the asset produces optical centering.
- **Selected-state versions are usually unnecessary** — standard system components (toolbars, tab bars, buttons) automatically update selected appearance.
- **Use inclusive images** — gender-neutral human figures; avoid culture/language-specific imagery.
- **Text in icons:** Only include text when essential for meaning. Localize individual characters. For text passages, use abstract representations with RTL-flipped versions.
- **Use vector formats (PDF or SVG)** for custom interface icons — they auto-scale for high-res displays. Avoid PNG for interface icons.
- **Provide alternative text labels** (accessibility descriptions) for all custom interface icons.
- **Avoid replicas of Apple hardware** — use only images from Apple Design Resources or SF Symbols representing Apple products.

## Standard Icons (SF Symbols)

### Editing

| Action | Symbol name |
|---|---|
| Cut | `scissors` |
| Copy | `document.on.document` |
| Paste | `document.on.clipboard` |
| Done / Save | `checkmark` |
| Cancel / Close | `xmark` |
| Delete | `trash` |
| Undo | `arrow.uturn.backward` |
| Redo | `arrow.uturn.forward` |
| Compose | `square.and.pencil` |
| Duplicate | `plus.square.on.square` |
| Rename | `pencil` |
| Move to / Folder | `folder` |
| Attach | `paperclip` |
| Add | `plus` |
| More | `ellipsis` |

### Selection

| Action | Symbol name |
|---|---|
| Select | `checkmark.circle` |
| Deselect / Close | `xmark` |
| Delete | `trash` |

### Text Formatting

| Action | Symbol name |
|---|---|
| Superscript | `textformat.superscript` |
| Subscript | `textformat.subscript` |
| Bold | `bold` |
| Italic | `italic` |
| Underline | `underline` |
| Align Left | `text.alignleft` |
| Center | `text.aligncenter` |
| Justified | `text.justify` |
| Align Right | `text.alignright` |

### Search

| Action | Symbol name |
|---|---|
| Search | `magnifyingglass` |
| Find / Find and Replace / Find Next / Find Previous / Use Selection for Find | `text.page.badge.magnifyingglass` |
| Filter | `line.3.horizontal.decrease` |

### Sharing and Exporting

| Action | Symbol name |
|---|---|
| Share / Export | `square.and.arrow.up` |
| Print | `printer` |

### Users and Accounts

| Action | Symbol name |
|---|---|
| Account / User / Profile | `person.crop.circle` |

### Ratings

| Action | Symbol name |
|---|---|
| Dislike | `hand.thumbsdown` |
| Like | `hand.thumbsup` |

### Layer Ordering

| Action | Symbol name |
|---|---|
| Bring to Front | `square.3.layers.3d.top.filled` |
| Send to Back | `square.3.layers.3d.bottom.filled` |
| Bring Forward | `square.2.layers.3d.top.filled` |
| Send Backward | `square.2.layers.3d.bottom.filled` |

### Other

| Action | Symbol name |
|---|---|
| Alarm | `alarm` |
| Archive | `archivebox` |
| Calendar | `calendar` |

## macOS Document Icons

Custom document icons represent custom document types. They use the traditional folded-corner paper appearance.

If no custom icon is supplied, macOS composites your app icon with the file extension onto the canvas.

### Composition Elements

You can supply any combination of:
- **Background fill** — masked to document icon shape with white folded corner drawn on top
- **Center image** — measures half the size of the overall document icon canvas
- **Text** — succinct term displayed at bottom edge (defaults to file extension, auto-capitalized)

### Background Fill Sizes

| Size | Retina |
|---|---|
| 512×512 px | 1024×1024 px |
| 256×256 px | 512×512 px |
| 128×128 px | 256×256 px |
| 32×32 px | 64×64 px |
| 16×16 px | 32×32 px |

### Center Image Sizes

| Size | Retina |
|---|---|
| 256×256 px | 512×512 px |
| 128×128 px | 256×256 px |
| 32×32 px | 64×64 px |
| 16×16 px | 32×32 px |

### Document Icon Guidelines

- Design simple images clearly communicating the document type.
- A single expressive background fill image can be sufficient (no center image needed).
- **Reduce complexity at small sizes** — fewer lines, thicker strokes aligned to pixel grid; remove fine details at 16×16.
- **Avoid important content in top-right corner** of background fill (folded corner covers it).
- Center image margin: ~10% of canvas; image should occupy ~80% of canvas.
- Text should be short enough to be legible at small sizes.