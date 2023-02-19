from pathlib import Path
import re


def get_save_dir(parent: str | None, album_title: str, override: bool) -> Path:
    save_dir = Path(parent or Path.cwd(), album_title)
    if save_dir.exists() and not override:
        save_dir = _incremented_save_dir(save_dir)
    save_dir.mkdir(exist_ok=True)
    return save_dir


def _incremented_save_dir(save_dir: Path) -> Path:
    incremented_dir = Path(save_dir.parent, _incremented_path_name(save_dir.name))
    return _incremented_save_dir(incremented_dir) if incremented_dir.exists() else incremented_dir


def _incremented_path_name(dir_name: str) -> str:
    incremented_ordinal = _incremented_ordinal(dir_name)
    return f"{dir_name}{_ordinal_identifier(incremented_ordinal)}" if incremented_ordinal == 1 else dir_name.replace(
        _ordinal_identifier(incremented_ordinal - 1), _ordinal_identifier(incremented_ordinal))


def _ordinal_identifier(ordinal: int) -> str:
    return f"({ordinal})"


def _incremented_ordinal(dir_name: str) -> int:
    ordinal_identifier = re.search(r"\([1-9]\d*\)$", dir_name)
    if ordinal_identifier is not None:
        return int(ordinal_identifier.group(0)[1:-1]) + 1
    return 1
