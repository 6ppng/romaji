"""ローマ字化処理モジュール."""
from json import loads
from logging import DEBUG, basicConfig, exception
from os import getcwd
from pathlib import Path
from re import sub
from typing import Dict, Iterator

from pykakasi import kakasi

wd = Path(getcwd())
RAW_DATA = wd / "data" / "raw.txt"
ROMAJI_DATA = wd / "data" / "romaji.txt"
NIHONSIKI_TABLE = wd / "data" / "nihonsiki.json"
LOG_PATH = wd / "log" / "compile.log"

basicConfig(filename=LOG_PATH, level=DEBUG)
kks = kakasi()

with NIHONSIKI_TABLE.open() as f:
    nihonsiki_table: Dict[str, str] = loads(f.read())


def itter_line() -> Iterator[str]:
    """生データから1行ずつテキストを読みだす.

    Yields:
        Iterator[str]: 生データのテキスト
    """
    with RAW_DATA.open() as f:
        while (line := f.readline()) != "":
            yield line


def compile_to_romaji(raw: str) -> str:
    """Pykakasiでローマ字化する.

    Args:
        raw (str): 生データテキスト

    Returns:
        str: ローマ字テキスト
    """
    return " ".join([token["hepburn"] for token in kks.convert(raw)])


def filter_char(romaji: str) -> str:
    r"""a-zおよび句点・読点・空白文字のみにフィルタする.

    Args:
        romaji (str): ローマ字テキスト

    Returns:
        str: a-zおよび句点(,)・読点(.)・空白文字( )のみのローマ字テキスト
    """
    filtered = sub(r"[^a-z,.\s]", "", romaji)
    return sub(r"\s{2,}", " ", filtered).strip()


def hepburn_to_nihonsiki(text: str) -> str:
    """ヘボン式ローマ字を日本式に変換する.

    Args:
        text (str): ヘボン式ローマ字テキスト

    Returns:
        str: 日本式ローマ字テキスト
    """
    for h, n in nihonsiki_table.items():
        text = sub(h, n, text)

    return text


def main() -> None:
    """ローマ字化処理."""
    with ROMAJI_DATA.open("a") as f:

        lines = (compile_to_romaji(line) for line in itter_line())
        lines = (
            filtered for line in lines if (filtered := filter_char(line)) != ""
        )
        lines = (hepburn_to_nihonsiki(line) + "\n" for line in lines)

        f.writelines(lines)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exception(e)
