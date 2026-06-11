# Using This Skill in Antigravity

This is a port of the original Claude Code skill modified to work seamlessly inside [Antigravity](https://github.com/google-deepmind/antigravity).

## Setup

### 1. Copy the skill to your app project (Optional)

You can copy this repository's folder into your system's skills directory, or simply load it directly in the workspace. Since the instruction file `SKILL.md` is in the root, Antigravity will automatically recognize it as a skill for current or target workspaces.

### 2. Install Python Dependencies

The screenshot generation and compositing scripts require **Pillow** (PIL):

```powershell
pip install Pillow
```

### 3. Font Requirement

The scaffold generator will automatically look for standard sans-serif bold fonts on your OS:
- **Windows**: `SF-Pro-Display-Black.otf`, `Arial Black` (`ariblk.ttf`), `Segoe UI Black` (`seguibl.ttf`), or `Arial Bold` (`arialbd.ttf`).
- **macOS**: `SF-Pro-Display-Black.otf`, `Arial Bold`, `Helvetica`, or system sans-serif fonts.
- **Linux**: standard `DejaVu Sans Bold` or `Liberation Sans Bold`.

If you have a preferred high-converting font, install it on your system or place it in the skill directory as `SF-Pro-Display-Black.otf`.

### 4. Image Generation Setup

**No setup required!** Unlike the original Claude Code and Kiro versions (which require installing `gemini-mcp` and setting up API keys), Antigravity uses its native, built-in `generate_image` tool directly for AI-based screenshot enhancement and pop-out card generation.

---

## State Files

All workflow state is saved as markdown files inside a `.aso/` folder in the user's **app project directory** (not this skill directory). Check for these files at the start of every conversation:

| File | Contents |
|------|----------|
| `.aso/benefits.md` | Confirmed benefit headlines, target audience, app context, brand colour |
| `.aso/screenshot-pairings.md` | Screenshot file paths, ratings, confirmed pairings |
| `.aso/generation-state.md` | Brand colour, generated screenshot paths, approval status |

These persist state across conversations — never delete them unless the user explicitly asks to start over.

---

## Usage

In your chat with Antigravity, just mention the skill or prompt:

```
Run the ASO screenshot workflow
```

Antigravity will load the `SKILL.md` instructions and guide you through the 4-phase process:

1. **Benefit Discovery** — analyzes your codebase to find the 3-5 core benefits.
2. **Screenshot Pairing** — reviews your simulator screenshots and pairs them with benefits.
3. **Generation** — creates scaffold PNGs via `compose.py`, enhances with Antigravity's native `generate_image` tool, and crops/resizes them using `resize.py`.
4. **Showcase** — generates a side-by-side preview of the final set.

---

## Python Scripts

All three Python scripts have been optimized for Windows, macOS, and Linux:

- **`compose.py`** — generates deterministic scaffold PNGs (updated with robust cross-platform font lookup).
- **`resize.py`** — crops and resizes screenshots to exact App Store Connect display dimensions (replacing macOS-only `sips`).
- **`generate_frame.py`** — regenerates the iPhone device frame template if needed.
- **`showcase.py`** — generates the final side-by-side showcase image.
