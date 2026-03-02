# Top Shelf (tvOS)

Guidelines for the Apple TV Home Screen Top Shelf area, which showcases app content when selected in the Dock. **tvOS only.**

## Best Practices

- **Help people jump right into content.** Carousel layouts include two default buttons: a primary playback button and a More Info button.
- **Feature new content.** Showcase new releases/episodes, highlight upcoming content. Avoid promoting already-purchased/watched content.
- **Personalize content.** Show targeted recommendations, let people resume playback or jump back into gameplay.
- **Avoid advertisements or prices.** Showing purchasable content is fine, but focus on new/exciting content. Display prices only when people show interest.
- **Showcase dynamic content.** Prefer [layered images](/design/human-interface-guidelines/images#Layered-images) for a captivating experience. Static images are a fallback.
- **Avoid implying interactivity in static images.** Static Top Shelf images aren't focusable.

## Static Fallback Image

If full-screen content is unavailable, the system displays a static image (flipped and blurred to fit 1920px wide at 16:9).

| Image size |
| --- |
| 2320×720 pt (2320×720 px @1x, 4640×1440 px @2x) |

## Dynamic Layouts

### Carousel Actions

Full-screen video/images with minimal controls. Best for content people already know (user-generated content, franchise content).

- **Provide a title** (e.g., show/movie title, photo album). Optional brief subtitle (date range, show name).

### Carousel Details

Extends carousel actions with additional info (plot summary, cast list, metadata).

- **Provide a title** near top of screen identifying currently playing content.
- Optional succinct phrase or app attribution above title (e.g., "Featured on *My App*").

### Sectioned Content Row

Single labeled row of focusable content. Good for recently viewed, new, or favorites.

- **Provide enough content to span full screen width.**
- Include at least one label for context and consistency.
- Can configure multiple labels.

#### Image Sizes for Sectioned Content Row

**Poster (2:3)**

| Aspect | Image size |
| --- | --- |
| Actual size | 404×608 pt (808×1216 px @2x) |
| Focused/Safe zone | 380×570 pt (760×1140 px @2x) |
| Unfocused | 333×570 pt (666×1140 px @2x) |

**Square (1:1)**

| Aspect | Image size |
| --- | --- |
| Actual size | 608×608 pt (1216×1216 px @2x) |
| Focused/Safe zone | 570×570 pt (1140×1140 px @2x) |
| Unfocused | 500×500 pt (1000×1000 px @2x) |

**16:9**

| Aspect | Image size |
| --- | --- |
| Actual size | 908×512 pt (1816×1024 px @2x) |
| Focused/Safe zone | 852×479 pt (1704×958 px @2x) |
| Unfocused | 782×440 pt (1564×880 px @2x) |

**Note:** Mixed image sizes auto-scale to match the tallest image height. E.g., a 16:9 image scales to 500px high when in a row with poster or square images.

### Scrolling Inset Banner

Series of large images spanning nearly the full screen width. Auto-scrolls on timer, circles back after final image.

- **Provide 3–8 images.** Fewer than 3 feels sparse; more than 8 makes navigation difficult.
- **Embed text in the image** — this layout doesn't show labels. In layered images, place text on a dedicated top layer. Also add text to the accessibility label for VoiceOver.

| Aspect | Image size |
| --- | --- |
| Actual size | 1940×692 pt (3880×1384 px @2x) |
| Focused/Safe zone | 1740×620 pt (3480×1240 px @2x) |
| Unfocused | 1740×560 pt (3480×1120 px @2x) |