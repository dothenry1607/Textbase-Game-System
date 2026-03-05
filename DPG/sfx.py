"""Sound effects wrapper around ``pygame.mixer``.

If pygame is not available or the mixer fails to initialise, all functions
become no‑ops so that the rest of the game can run without sound.
"""

try:
    from pygame import mixer
    from pygame.time import Clock
    mixer.init()
    _MIXER_AVAILABLE = True
except Exception:
    _MIXER_AVAILABLE = False


def play_sfx(filepath: str, wait: bool = False, volume: float | None = None) -> None:
    """Play a sound effect from ``filepath``.

    ``volume`` (0.0–1.0) may be provided to override the current mixer
    volume.  If ``wait`` is True the function blocks until the sound finishes.
    """
    if not _MIXER_AVAILABLE:
        return
    try:
        sound = mixer.Sound(filepath)
        if volume is not None:
            sound.set_volume(volume)
        sound.play()
        if wait:
            while mixer.get_busy():
                Clock().tick(10)
    except Exception:
        # ignore any playback errors
        pass

