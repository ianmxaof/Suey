# Suey, local installation

Double-click **Launch-Suey.cmd** to run the transparent desktop sprite with the finished blank-faced Suey artwork. It uses your existing Python 3.14 and its built-in Tkinter library, so no package download is needed. Drag her to place her; right-click for **Wander**, **Stay here**, or **Quit Suey**. Escape also closes her.

This local source snapshot comes from `ianmxaof/Suey` commit `06adb24de9d6f047c16779635eaea56b88d23b6f`. The original PyQt sprite loader now resolves assets relative to its source file and uses the full 192 x 208 frame size. `desktop_suey.pyw` provides the same wandering and idle behavior without the PyQt dependency. The original source is backed up as `sprite_walker.original.py`. The separate legacy watcher modules are preserved for future work. The launcher starts only the sprite, without activating those monitoring and Telegram prototypes.

- `codex-pet/`: local Codex v2 package, with `pet.json` and `spritesheet.png`.
- `codex-pet-compat/`: nine-row compatibility package for older clients.
- `chatgpt-pet/v2/`: full artwork, editable sources, previews and QA reports.
- `kantekiFemale/wandering_sprite_full_package/assets/`: all nine transparent state animations plus `walk1.gif`, `walk2.gif`, and `sit.gif` aliases used by the original app.
- `local-assets-validation.json`: local asset checks.

Suey retains her blank face, straight black hair, Alice-like apron dress and little bag with a key and scroll. No cape.
