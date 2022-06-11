"""取得・前処理モジュール."""
from logging import DEBUG, basicConfig, debug, exception, info
from os import getcwd
from pathlib import Path
from re import sub
from typing import List

from wikipedia import page, random, search, set_lang
from wikipedia.exceptions import (
    DisambiguationError,
    PageError,
    WikipediaException,
)

ARTICLES_NUM = 100
RAW_DATA = Path(getcwd()) / "data" / "raw.txt"
LOG_PATH = Path(getcwd()) / "log" / "fetch.log"

basicConfig(filename=LOG_PATH, level=DEBUG)


def get_page_content(title: str) -> str:
    """指定された記事のテキストを取得する.

    * 与えられたタイトルから記事が一意に定まらない場合、
    * クエリが参照するタイトルの中で最長のタイトルで再検索する。

    Args:
        title (str): 記事のタイトル

    Returns:
        str: 記事のテキスト
    """
    while True:
        try:
            content: str = page(title).content

        except DisambiguationError as e:
            title = max(
                filter(lambda o: o != title, e.options),
                key=lambda o: len(o),
                default="",
            )
            debug(f"取得対象記事変更: 「{title}」...")

        except (PageError, WikipediaException):
            return ""

        else:
            return content


def main() -> None:
    """Wikipediaから記事を取得する.

    * Wikipediaから日本語のランダムな記事を取得する。
    * 空行・英字を除去した後、生データとしてファイルに格納する。
    """
    info("取得処理開始")
    set_lang("ja")
    texts: List[str] = []
    for _ in range(ARTICLES_NUM):

        debug("記事名取得開始")
        title = search(random())[0]
        debug("記事名取得完了")

        debug(f"取得開始: 記事「{title}」...")
        texts.append(get_page_content(title))
        debug(f"取得完了: 記事「{title}」")

    info("取得処理完了")

    info("前処理開始")
    texts = list(map(lambda text: sub("[a-zA-Z]", "", text), texts))
    texts = list(map(lambda text: sub(r"\n\s*\n", "\n", text + "\n"), texts))
    info("前処理完了")

    info("ファイル格納開始")
    with RAW_DATA.open("a") as f:
        f.writelines(texts)
    info("ファイル格納完了")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exception(e)
