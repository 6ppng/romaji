"""wikipediaから記事の要約を取得する例."""
import sys

import wikipedia

# 言語を日本語に設定
wikipedia.set_lang("jp")
# テキストファイルを開く
f = open("data/wikipedia.txt", "a")

args = sys.argv
word = args[1]
# 検索ワードを用いて検索
words = wikipedia.search(word)

if not words:
    print("一致なし")
else:
    # 検索ワードがヒットすれば要約を取得
    line = str(wikipedia.summary(words[0]))
    f.write(word)
    f.write(line.rstrip())
    print("success!")

f.write("\n" + "EOS" + "\n")
f.close()
