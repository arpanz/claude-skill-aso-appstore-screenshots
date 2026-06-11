# Using This Skill in Kiro

This is a port of the original Claude Code skill to work with [Kiro](https://kiro.dev).

## Setup

### 1. Copy the steering file to your app project

Copy `.kiro/steering/aso-appstore-screenshots.md` into your app project's `.kiro/steering/` folder:

```powershell
# Windows
Copy-Item ".kiro\steering\aso-appstore-screenshots.md" "C:\path\to\your-app\.kiro\steering\"

# macOS/Linux
cp .kiro/steering/aso-appstore-screenshots.md /path/to/your-app/.kiro/steering/
```

The steering file has `inclusion: manual` — it only loads when you explicitly reference it in chat, so it won't clutter every conversation.

### 2. Install Python dependencies

```bash
pip install Pillow
```

### 3. Font requirement

The scaffold generator uses **SF Pro Display Black**. Install from [Apple's developer fonts](https://developer.apple.com/fonts/). Expected path:

```
/Library/Fonts/SF-Pro-Display-Black.otf       # macOS
C:\Windows\Fonts\SF-Pro-Display-Black.otf     # Windows (after manual install)
```

### 4. Set up Gemini MCP (for AI enhancement)

The generation phase requires the Gemini MCP server for `edit_image` calls.

```bash
npm install -g @houtini/gemini-mcp
```

Add to your Kiro MCP config at `.kiro/settings/mcp.json` or `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "gemini-mcp",
      "args": [],
      "env": {
        "GEMINI_API_KEY": "your-key-here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Reconnect MCP servers from the Kiro MCP panel after saving.

## Usage

Open your app project in Kiro. In chat, reference the steering file and start:

```
#aso-appstore-screenshots let's create App Store screenshots for my app
```

Or just say:
```
Run the ASO screenshot workflow
```

(after referencing the steering file once, Kiro will load the full instructions)

The workflow will guide you through:
1. **Benefit Discovery** — analyzes your codebase to find the 3-5 core benefits
2. **Screenshot Pairing** — reviews your simulator screenshots and pairs them with benefits
3. **Generation** — creates scaffold PNGs via `compose.py`, then enhances with Nano Banana Pro
4. **Showcase** — generates a side-by-side preview of the final set

## State Files

Unlike the Claude Code version (which uses a built-in memory system), state is saved as markdown files in a `.aso/` folder inside your app project:

| File | What's saved |
|------|-------------|
| `.aso/benefits.md` | Confirmed benefits, target audience, brand colour |
| `.aso/screenshot-pairings.md` | Screenshot ratings and confirmed pairings |
| `.aso/generation-state.md` | Generated file paths, approval status |

These persist across conversations. Start a new chat, reference the steering file, and Kiro will read these files and resume where you left off.

## Key Differences from Claude Code Version

| Claude Code | Kiro |
|---|---|
| `/aso-appstore-screenshots` slash command | Reference steering file in chat: `#aso-appstore-screenshots` |
| Built-in memory system | `.aso/*.md` files in your project |
| `~/.claude/skills/` path | Path to wherever you cloned this repo |
| `sips` for crop/resize (macOS only) | Python + Pillow (cross-platform) |
| `bash` commands | PowerShell or bash depending on OS |

## Python Scripts

All three Python scripts work unchanged — no modifications needed:

- **`compose.py`** — generates deterministic scaffold PNGs
- **`generate_frame.py`** — regenerates the device frame template if needed
- **`showcase.py`** — generates the final side-by-side showcase image

When running compose.py, pass the full path to the script since it won't be in `~/.claude/skills/` anymore:

```powershell
# Windows
python "E:\path\to\claude-skill-aso-appstore-screenshots\compose.py" --bg "#E31837" --verb "TRACK" --desc "TRADING CARD PRICES" --screenshot .\simulator.png --output .\scaffold.png

# macOS/Linux
python3 /path/to/claude-skill-aso-appstore-screenshots/compose.py --bg "#E31837" --verb "TRACK" --desc "TRADING CARD PRICES" --screenshot ./simulator.png --output ./scaffold.png
```
