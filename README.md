pdf2ref
=======
使い方
------
### `pdf2ref.py`
    メインプログラム。

    Usage: $ python3 level1.py "Amount" "50yen" "100yen" "500yen"

 pdf2ref.pyの詳細
----------------
    pdfファイルのReferenceリストを取ってくる
    ReferenceリストのTitleからGoogleScholarに投げて、ちゃんとしたTitle, Author, Conf, Pdfのリストを取ってくる
    ......ここから妄想......
    これをリカーシブに動かして、論文毎のReferenceグラフを作成。可視化。自動で重要な論文取ってくるなんてできたらムフフ....
    で、動かそうとした所、少しのReferenceなら大丈夫だけど、20個めくらいからGoogleScholarのRecaptchに引っかかってどうもならん。死んだ。

関連情報
--------
### PDFからテキストを抽出する
1. [リンク1](http://blog.mwsoft.jp/article/93796981.html)
 
###  scholar.py
2. [リンク2](https://github.com/ckreibich/scholar.py)

ライセンス
----------
Copyright &copy; 2014 @higitune
