"""Background music helper wrapping ``pygame.mixer.music``.

Content is optional; failure to import pygame results in no-op functions.
"""

try:
    from pygame.mixer import music, init
    from pygame.time import Clock
    init()
    _MIXER_AVAILABLE = True
except Exception:
    _MIXER_AVAILABLE = False


def play_music(filepath: str, wait: bool = False, loop: bool = False,
               volume: float | None = None) -> None:
    """Start playing a music track from ``filepath``.

    ``loop`` will repeat indefinitely if true.  ``volume`` may be set
    between 0.0 and 1.0.
    """
    if not _MIXER_AVAILABLE:
        return
    try:
        music.load(filepath)
        if volume is not None:
            music.set_volume(volume)
        music.play(-1 if loop else 0)
        if wait:
            while music.get_busy():
                Clock().tick(10)
    except Exception:
        pass


def stop_music() -> None:
    """Stop any currently playing music."""
    if not _MIXER_AVAILABLE:
        return
    try:
        music.stop()
    except Exception:
        pass


