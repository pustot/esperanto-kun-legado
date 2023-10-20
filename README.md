# esperanto-kun-legado

Kun-legado / ĉin-skribigo por Esperanto. 世界语训读/汉字化。 Kun'yomi / Chinese script writing for Esperanto.

Listo de facilaj vortoj laŭ `UEA.facila`: https://uea.facila.org/vortlisto/#listo

Dankon al https://zhuanlan.zhihu.com/p/349645051 (sed multaj enskriboj estas malĝustaj)

更新計劃：沿 https://esperanto12.net/zh/ ，已更新至第 5 課

參見學習筆記 https://github.com/twaqngu/TwaqNoto/blob/master/400-Lingvo/400-eo-Esperanto.md

# Python Usage

```py
>>>  from cxinskribigilo import sentence_eo_to_han

>>> # frazojn traduki
>>> sentence_eo_to_han("Ni ĉiuj naskiĝis liberaj kaj egalaj laŭ digno kaj rajtoj. Ni ĉiuj havas niajn proprajn pensojn kaj ideojn. Ni ĉiuj devas agi unuj kun aliaj laŭ spirito de frateco.")
'咱 ĉiuj 誕成is 閒aj 與 等aj 沿 digno 與 權oj. 咱 ĉiuj 有as 咱ajn 擁ajn 思ojn 與 想ojn. 咱 ĉiuj 須as 行i unuj 共 另aj 沿 魂o de 兄性o.'
```

# 一些小原則

- 優先漢字化那些意義強的、常用的詞根
- 儘量不漢字化那些弱語義的（如 -um-）或用途少的（如 ge-）詞綴、語義不單純的獨立詞（如 je）
- 儘量用單個漢字、通用的繁體字，並儘可能不重複（重複的情況，計劃漸次清理）
- 現代從某外語借的詞儘量不漢字化，如blogo

# 一些難題

- vid-見, rigard-看; aŭd-聞, aŭskult-聽
    - 都是一個描述狀態（看見、聽見）一個描述動作（看、聽）
- bezon- dev- neces- nepr-; -end-
    - 需 須 必 定？ 應
    - -end- 是應當、需要的意思，但不知道哪個字專門用給這個後綴
    - dev- 最好用「應」對應should，不過也可以用「須」對應必須must
- agrabl- gaj- ĝoj- plezur-, amuz- feliĉ- plaĉ-, afabl- ĝu- komfort- kontent-
    - 樂 嬉 歡 愉 快 欣
    - 好像一般的快樂開心就是 feliĉ- plezur- ĝoj-, plaĉ- (喜歡)
    - agrabl- 快 快い（こころよい）？快適？來自agréer，除了agree也有稱心滿意喜歡。否定義也很符合「不快」。不在基本詞里，可能偏一點點
    - gaj- 歡 好像有活潑開朗？不在基本詞里，可能偏一點點
    - ĝoj- 喜 嬉しい？喜ぶ？（）不在基本詞里，可能偏一點點
    - plezur- 樂 快樂？愉快な、楽しい？
    - amuz- 娛 （稍不那麼棘手）因爲有娛樂這個派生詞
    - feliĉ- 幸 （稍不那麼棘手）因爲有幸福的意思
    - plaĉ- 悅 （稍不那麼棘手）因爲有讓人喜歡的意思，構成喜歡的結構，聯想「悅己者」
    - afabl- 善 （不難區分，就是 nice，友善，和藹，但不知道用 慈 或 善 這個字好不好）
    - ĝu- 享
    - komfort- 舒 （不難區分）
    - kontent- 滿足 （不難區分，但沒找到單個字描述）
- inteligent- mens- saĝ- sci-
    - 智 慧 賢 知
- pet- postul-
    - 請 求
- pens-思 konsider-慮 ide-想 ideal-理想 imag-想象 opini-意見 senc-意 signif-謂 propon-建議
    - ide-想 是想法，但不知道怎麽縮合適
    - 想念大概是 sopiri- 但不在基本詞的角逐中，或者用 mank-缺 來構成
- hom-人 person-個 -ul-佬 -ist-者 popol-民 -an-士 amas-衆 gast-客 membr-員
    - popol-民 應該是人民，不知道一個漢字怎麽縮
    - person-個 個人，個體
    - -an- 是國民，所以用「民」好點，但是 popol- 佔之；思及「人士」，用了「士」；參見 兵 soldat-
- lok-位 ter-地 -ej-所 -uj-鄉 rang-地位
- hejm-厝 famili-家 naci-族 land-國 ŝtat-邦
    - hejm-厝, dom-屋
    - famili-家, ĝarden-庭
- kaj與 aŭ或 ne不/非 mal-否
    - 想要與計算機的 與、或、非 對應，不過 ne 還是寫作「不」順眼。。。
    - mal- 表示的是反義，自然語言很難有這個詞根。我用了不太口語的「否」防止malbona讀起來像「不好」
- supr- super sur, sub
- afer-事 okaz-起 ek-開 kaz-案
    - okaz-起 想找個發生之類的字，沒找到，遂參考 起こる
    - ek-開 本來用的起，現在用開吧，其實也合適，「開搞」
- fakt-事實 real-現實 efektiv-實際 ver-真
- daŭr-續 -ad-久
- ĝeneral-普 ordinar-凡
- kalkul-算 komput-計
    - komput-計 好像只用於計算機。。。
- ĉar因 pro由？ kaŭz-致
- al往 pri關 koncern-涉
    - pri 關？對？就？
- korekt-矯 prav-對 ĝust-正
- ke,曰
    - 是不是很機智
- rilat-聯 lig-綁
- 大數系統參考國際單位制的字頭，是以 mil千 milion-兆 miliard-吉
    - milion- 在百萬和兆中選擇兆。因爲它是單個漢字，而且其大數不優先兼容東亞古代系統（其實都不一定會用「萬」）
- rimed-手段 metod-方法 manier-方式
- grand-大 -eg-巨 -et-小
    - 因爲grand太長常用，不想叫它巨，所以叫-eg-巨。-et-呢，到底是把常用詞根「小」用起來，還是跟巨對應用「微」？沒想好
- 人稱代詞
    - 第二人稱，單數ci漢字化爲汝，複數且今替代單數的vi漢字化爲恁，因爲恁字確實也是單複通用。
- 性別問題
    - 中性第三人稱代詞。其實對漢字來說也是無奈，本來「他」就是中性的，非要造個「她」強行對立。考慮到ŝli是派生自ŝi li，所以用了同帶人字旁的「佢」，ri用不帶人字旁的「渠」
    - 目前兼容-iĉ-「男」，-in-「女」
        - 相關詞彙 vir-「夫」（夫妻之義給了edz-「婚」），patr-「親」（參考日語），av-「祖」，fil-「子」，nep-「孫」，frat-「兄」，onkl-「叔」，kuz-「堂表兄」（不知道怎麽縮，「表」字給了esprim-，雖然後者也能用「傳」），nev-「侄」
- dir-言 parol-講 diskut-議 komunik-談 teori-論 anonc-宣 rakont-述 ordon-令 instrukci-指令 las-讓 permes-許
    - konvink-說服 roman-小說 kongres-會議 propon-建議
    - dir- 從「說」改到「言」，因爲想把這個常用漢字構件用上。但同爲常用字的「說」就空出來了
- viv-生 fart-生活 aktiv-活
    - stud-學 student-徒
- instru-授 eduk-教
    - religi-宗教
