import csv
import re

# TODO:
# ĉiopovan 每op蛋an

# 创建一个空字典来存储字典信息
dictionary = {
    # TODO: 如何正确处理不在一词之末的语法后缀，如 loĝantaro
    "ant": "", "int": "", "ont": "",
    "at": "", "it": "", "ot": "",
}

roots = ["ĉar", "ĉi", "ĉu", "kaj", "ke", "la", "minus", "plus",
	"se", "ĉe", "da", "de", "el", "ekster", "en", "ĝis", "je", "kun", "na",
	"po", "pri", "pro", "sen", "tra", "ajn", "do", "ja", "jen", "ju", "ne",
	"pli", "tamen", "tre", "tro", "ci", "ĝi", "ili", "li", "mi", "ni", "oni",
	"ri", "si", "ŝi", "ŝli", "vi", "unu", "du", "tri", "kvin", "ĵus", "nun", "plu",
	"tuj", "amen", "bis", "boj", "fi", "ha", "he", "ho", "hu", "hura", "nu", "ve",
	#  "esperanto", 
    "plej"
]

# TODO: 表解词应该单独处理，而不是词根找译。不然 kiam 就成了 何爱
correlatives = [
	"kia", "kial", "kiam", "kie", "kiel", "kies", "kio", "kiom", "kiu",
	"tia", "tial", "tiam", "tie", "tiel", "ties", "tio", "tiom", "tiu",
	"ia", "ial", "iam", "ie", "iel", "ies", "io", "iom", "iu",
	"ĉia", "ĉial", "ĉiam", "ĉie", "ĉiel", "ĉies", "ĉio", "ĉiom", "ĉiu",
	"nenia", "nenial", "neniam", "nenie", "neniel", "nenies", "nenio", "neniom", "neniu",
]


# 你的 CSV 文件列表
# 注意，加入映射词典的不包含 "gramatikaj-finaĵoj.csv"，因为有专门的去语法后缀的函数
csv_files = ["pronomoj-kaj-tabelvortoj.csv", "afiksoj.csv", "alioj-de-facila.csv", "facilaj-vortoj.csv"]

# 循环遍历每个 CSV 文件
for csv_file in csv_files:
    # UTF-8 with BOM, kun `\ufeff`, do uzas 'utf-8-sig'
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        # 假设 CSV 文件的第一行是标题，包含 'eo' 和 'han' 列
        headers = next(csv_reader)
        for row in csv_reader:
            # 获取 'eo' 和 'han' 列的值
            # 直接無視表里世界語詞根的橫槓
            eo_word = row[headers.index('eo')].strip('-')
            han_word = row[headers.index('han')]
            
            # 将字典信息存储在字典中，使用 Esperanto 词作为键，汉字作为值
            dictionary[eo_word] = han_word


# The process refers to https://github.com/abadojack/stemmer/blob/master/stemmer.go
def split_suffix(word):
    word = word.lower()
    # standalone roots
    if word in roots:
        return word, ''
    
    suffix = ''

    if not word[-1].isalpha():
        if len(word) == 1:
            return word, ''
        suffix = word[-1]
        word = word[:-1]

    non_verb = False
    # nouns, adjectives, -u correlatives:
    # -oj -on -ojn → -
    # -aj -an -ajn → -
    # -uj -un -ujn → -
    if word[-2:] in ['oj', 'on', 'aj', 'an', 'uj', 'un']:
        suffix = word[-2:] + suffix
        word = word[:-2]
        non_verb = True
    elif word[-3:] in ['ojn', 'ajn', 'ujn']:
        suffix = word[-3:] + suffix
        word = word[:-3]
        non_verb = True

    # correlatives: -en → 
    if word in ["kien", "tien", "ien", "nenien", "ĉien"]:
        return word[:-2], 'en'

    # correlative roots
    if word in roots:
        return word, suffix
    
    # nur se ne stemmita.
    # 否则会错： ideoj, hebreoj
    if not non_verb and word[-1] in ['a', 'o', 'e']:
        suffix = word[-1]
        word = word[:-1]
        non_verb = True
    
    # accusative pronouns: -in → 
    if word[-2:] == 'in' and word[:-1] in ["ci", "ĝi", "ili", "li", "mi", "ni", "oni",
	                                        "ri", "si", "ŝi", "ŝli", "vi"]:
        return word[:-1], 'n'

    # accusative adverbs: -en → -
    if word[-2:] == 'en':
        suffix = 'en'
        word = word[:-2]
        non_verb = True
    
    # verbs: -is -as -os -us -u → -
    if not non_verb:
        if word[-1] == 'i':
            suffix = 'i'
            word = word[:-1]
        elif word[-2:] in ['is', 'as', 'os', 'us']:
            suffix = word[-2:] + suffix
            word = word[:-2]
        elif word[-1:] in ['u']:
            suffix = word[-1:] + suffix
            word = word[:-1]

    # lexical aspect: ek- el-

    # note: not enabled. -ad- 暫時視爲有實意的詞根
    # imperfective verbs & action nouns: -adi -ado → -i

    # compound verbs:
	# -inti -anti -onti -iti -ati -oti → -i
	# -inte -ante -onte -ite -ate -ote → -i
	# -inta -anta -onta -ita -ata -ota → -i
    # participle nouns:
	# -into -anto -onto → -anto → o
	# -ito  -ato  -oto  → -ato → o
    if word[-3:] in ['int', 'ant', 'ont']:
        suffix = word[-3:] + suffix
        word = word[:-3]
    elif word[-2:] in ['it', 'at', 'ot'] and word not in ['dat', 'frat', 'rilat']:
        # 特殊情况于 dat- 等词
        suffix = word[-2:] + suffix
        word = word[:-2]

    # dissuffix = word[:-1]
    return word, suffix


# 定义一个字典，将世界语词根映射到对应的汉字
root_to_chinese = dictionary


# 定义一个函数，将世界语单词转换为汉字化的单词
def word_eo_to_han(eo_word, is_before_hyphen=False):
    if not eo_word:
        return ''
    is_first_upper = False
    if eo_word[0].isupper():
        is_first_upper = True
    # 目前先都小写
    eo_word = eo_word.lower()

    # if it is before hyphen, it already has no grammatical suffix
    if is_before_hyphen:
        suffix = ''
    else:
        # TODO: 仅为避混于「每」之紧急措施。
        if eo_word == 'ĉi':
            return '此'
        eo_word, suffix = split_suffix(eo_word)
    
    # 初始化汉字化后的单词
    chinese_word = ""

    # 遍历世界语单词的每个字母
    i = 0
    while i < len(eo_word):
        # 从当前位置开始查找最长的词根
        current_root = ""
        j = i
        valid_j = i
        while j < len(eo_word):
            if eo_word[i:j + 1] in root_to_chinese:
                current_root = eo_word[i:j + 1]
                valid_j = j
            j += 1

        # TODO: 暂时对 intern 特殊处理以应对 internacia 样单词
        if current_root == 'intern' and valid_j + 2 < len(eo_word):
            chinese_word += root_to_chinese['inter']
            i = valid_j
            continue

        # 如果找到了词根，则将其替换为对应的汉字
        if current_root:
            # 有的词根的汉字化列置空，如此则还是保留拉丁字形式
            chinese_word += root_to_chinese[current_root] if root_to_chinese[current_root] != "" else current_root
            i = valid_j + 1
        else:
            # 如果未找到词根，则保留原始字符
            chinese_word += eo_word[i]
            # i += 1
            # TODO: 在只有部分词根有记录时，如何处理，以使例如 `cenzuran` 不变成 `c入zur民`。暂时全词皆删
            chinese_word = eo_word
            break

    if is_first_upper:
        chinese_word = chinese_word[0].upper() + chinese_word[1:]

    return chinese_word + suffix


def sentence_eo_to_han(eo_sentence):
    eo_word_list = re.findall(r"[\w]+|[.,!?;\-“„”\"«»\~\[\]\{\}]| ", eo_sentence)
    return ''.join([word_eo_to_han(word, i + 1 >= len(eo_word_list) or eo_word_list[i + 1] == '-') for (i, word) in enumerate(eo_word_list)])

# word_eo_to_han 使用示例
eo_word = "naskiĝtago"
han_word = word_eo_to_han(eo_word)
print("************vorta ekzemplo**********")
print(han_word)  
print(word_eo_to_han("internacia"))
print(word_eo_to_han("interno"), word_eo_to_han("internajn"))
print(word_eo_to_han("lernantoj"), word_eo_to_han("lerninto"))
print(word_eo_to_han("ideo"), word_eo_to_han("ideoj"), word_eo_to_han("hebreoj"))
# 输出：
"""
誕成日o
"""

# sentence_eo_to_han 使用示例
# TODO: 语尾如 -on -an -i 被错误汉字化
print("************fraza ekzemplo**********")
print(sentence_eo_to_han("""
Esperanto, origine la Lingvo Internacia, estas la plej disvastiĝinta internacia planlingvo. 
La nomo de la lingvo venas de la kaŝnomo “D-ro Esperanto„ sub kiu la varsovia okul-kuracisto 
Ludoviko Lazaro Zamenhofo en la jaro 1887 publikigis la bazon de la lingvo. 
La unua versio, la rusa, ricevis la cenzuran permeson disvastiĝi en la 26-a de julio; 
ĉi tiun daton oni konsideras la naskiĝtago de Esperanto. 
Li celis kaj sukcesis krei facile lerneblan neŭtralan lingvon, taŭgan por uzo en la internacia komunikado; 
la celo tamen ne estas anstataŭigi aliajn, naciajn lingvojn.
"""))
# 输出：
"""
冀anto, 原e la 語o 間族a, 是as la 最 散廣成inta 間族a 謀語o. La 名o de la 語o 來as de la 隱名o “D-ro 冀anto„ 
下 何u la varsovia 眼-醫者o Ludoviko Lazaro Zamenhofo 入 la 年o 1887 公化is la 基on de la 語o. La 一a 版o, la rusa, 
獲is la cenzuran 許on 散廣成i 入 la 26-a de julio; 此 彼un 期on oni 慮as la 誕成日o de 冀anto. 
他 的is 與 昌is 創i 易e 習能an 中立an 語on, 適an 爲 使o 入 la 間族a 談久o; la 的o 然而 不 是as 替化i 另ajn, 族ajn 語ojn.
"""

print("************又一个 fraza ekzemplo**********")
print(sentence_eo_to_han("""
Mi naskiĝis en Bjelostoko, gubernio de Grodno. Tiu ĉi loko de mia naskiĝo kaj de miaj infanaj jaroj donis la direkton 
al ĉiuj miaj estontaj celadoj. En Bjelostoko la loĝantaro konsistas el kvar diversaj elementoj: rusoj, poloj, 
germanoj kaj hebreoj; ĉiuj el tiuj ĉi elementoj parolas apartan lingvon kaj neamike rilatas la aliajn elementojn. 
En tia urbo pli ol ie la impresema naturo sentas la multepezan malfeliĉon de diverslingveco kaj konvinkiĝas ĉe ĉiu paŝo, 
ke la diverseco de lingvoj estas la sola, aŭ almenaŭ la ĉefa, kaŭzo, kiu disigas la homan familion kaj dividas ĝin en 
malamikaj partoj. Oni edukadis min kiel idealiston; oni min instruis, ke ĉiuj homoj estas fratoj, kaj dume sur la strato 
kaj sur la korto, ĉio ĉe ĉiu paŝo igis min senti, ke homoj ne ekzistas: ekzistas sole rusoj, poloj, germanoj, hebreoj k.t.p. 
Tio ĉi ĉiam forte turmentis mian infanan animon, kvankam multaj eble ridetos pri tiu ĉi „doloro pro la mondo“ ĉe la infano. 
Ĉar al mi tiam ŝajnis, ke la „grandaĝaj“ posedas ian ĉiopovan forton, mi ripetadis al mi, ke kiam mi estos grandaĝa, 
mi nepre forigos tiun ĉi malbonon.
"""))
# 输出：
"""
吾 誕成is 入 Bjelostoko, gubernio de Grodno. 彼u 此 位o de 吾a 誕成o 與 de 吾aj 童aj 年oj 予is la 向on 往 ĉiuj 吾aj 是ontaj 的久oj. 
入 Bjelostoko la 住ant集o 組成as 出 四 繽aj elementoj rusoj, poloj, germanoj 與 hebreoj; ĉiuj 出 彼uj 此 elementoj 講as 別an 語on 
與 不友e 聯as la 另ajn elementojn. 入 彼a 城o 更 比 某e la impresema 自然o 感as la 多e重an 否幸on de 繽語性o 與 說服成as 在 ĉiu 步o, 
曰 la 繽性o de 語oj 是as la 獨a, 或 almenaŭ la 主a, 致o, 何u 散化as la 人an 家on 與 割as 它n 入 否友aj 部oj. Oni 教久is 吾n 何出 理想者on; 
oni 吾n 授is, 曰 ĉiuj 人oj 是as 兄oj, 與 當e sur la strato 與 sur la 院o, ĉio 在 ĉiu 步o 化is 吾n 感i, 曰 人oj 不 存as 存as 獨e rusoj, 
poloj, germanoj, hebreoj k.t.p. 彼o 此 ĉi愛 力e turmentis 吾an 童an 靈on, 雖 多aj 能e 笑小os 關 彼u 此 „痛o 由 la 世o“ 在 la 童o. 
因 往 吾 彼愛 似is, 曰 la „大齡aj“ 占as  某an ĉiop蛋an 力on, 吾 重複久is 往 吾, 曰 何愛 吾 是os 大齡a, 吾 定e 離化os 彼un 此 否良on.
"""
