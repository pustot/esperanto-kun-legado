import csv
import re

# TODO: （當前通過禁用-op-跳過，但沒解決比如別的詞根或真正用-op-者。比如可以限制-op- -on- 只用於數字前）
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

correlative_dict = {
    "kia": "何a", "kial": "何al", "kiam": "何am", "kie": "何e", "kiel": "何el", "kies": "何es", "kio": "何o", "kiom": "何om", "kiu": "何u",
	"tia": "彼a", "tial": "彼al", "tiam": "彼am", "tie": "彼e", "tiel": "彼el", "ties": "彼es", "tio": "彼o", "tiom": "彼om", "tiu": "彼u",
	"ia": "某a", "ial": "某al", "iam": "某am", "ie": "某e", "iel": "某el", "ies": "某es", "io": "某o", "iom": "某om", "iu": "某u",
	"ĉia": "每a", "ĉial": "每al", "ĉiam": "每am", "ĉie": "每e", "ĉiel": "每el", "ĉies": "每es", "ĉio": "每o", "ĉiom": "每om", "ĉiu": "每u",
	"nenia": "無a", "nenial": "無al", "neniam": "無am", "nenie": "無e", "neniel": "無el", "nenies": "無es", "nenio": "無o", "neniom": "無om", "neniu": "無u",
}


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

    # correlatives: -en → -
    if word in ["kien", "tien", "ien", "nenien", "ĉien"]:
        return word[:-2], 'en'

    # correlative roots
    if word in correlative_dict or (suffix and word + suffix[0] in correlative_dict):
        if suffix:
            word += suffix[0]
            suffix = suffix[1:]
        return correlative_dict[word], suffix
    
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
    elif word[-2:] in ['it', 'at', 'ot'] and word not in ['dat', 'frat', 'rilat', 'spirit', 'strat']:
        # 特殊情况于 dat- 等词
        suffix = word[-2:] + suffix
        word = word[:-2]

    # dissuffix = word[:-1]
    return word, suffix


# 定义一个函数，将世界语单词转换为汉字化的单词
def word_eo_to_han(eo_word, is_before_hyphen=False, is_sentence_begin=False):
    if not eo_word:
        return ''
    is_first_upper = False
    if eo_word[0].isupper():
        is_first_upper = True
    # 目前句首的先都小写，但没法应对句首出现未知词
    if is_sentence_begin:
        eo_word = eo_word.lower()

    # if it is before hyphen, it already has no grammatical suffix
    # 不过这种方案目前可以兼容一些连字符前带后缀者如 drako-reĝo -> 龍o-王o
    # eo 连字符合成词的规则究竟如何，还需了解。
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
            if eo_word[i:j + 1] in dictionary:
                current_root = eo_word[i:j + 1]
                valid_j = j
            j += 1

        # TODO: 暂时对 intern 特殊处理以应对 internacia 样单词
        if current_root == 'intern' and valid_j + 2 < len(eo_word):
            chinese_word += dictionary['inter']
            i = valid_j
            continue

        # 如果找到了词根，则将其替换为对应的汉字
        if current_root:
            # 有的词根的汉字化列置空，如此则还是保留拉丁字形式
            chinese_word += dictionary[current_root] if dictionary[current_root] != "" else current_root
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


def paragraph_eo_to_han(eo_paragraph):
    eo_word_list = re.findall(r"[\w]+|[.,!?;\:\-“„”\"«»\~\[\]\{\}\n]| ", eo_paragraph)
    return ''.join([word_eo_to_han(
        word, 
        i + 1 < len(eo_word_list) and eo_word_list[i + 1] == '-',
        # 判断是不是句首，情况太多了。。。
        (i == 0) or 
        (i == 1 and eo_word_list[0] == '\n') or 
        (i-2 >= 0 and eo_word_list[i-1] in [' ', '\n'] and eo_word_list[i-2]=='.') or 
        (i-3 >= 0 and eo_word_list[i-1] in [' ', '\n'] and eo_word_list[i-2] in [' ', '\n'] and eo_word_list[i-3]=='.')
        ) for (i, word) in enumerate(eo_word_list)])

if __name__ == "__main__":
    print("************vorta ekzemplo**********")
    print(word_eo_to_han("internacia"), word_eo_to_han("lernantoj"), word_eo_to_han("lerninto"))
    print(word_eo_to_han("interno"), word_eo_to_han("internajn"))
    print(word_eo_to_han("ideo"), word_eo_to_han("ideoj"), word_eo_to_han("hebreoj"))
    print(word_eo_to_han("Ĉiuj"))

    # hanize 'testa-teksto.txt' and export to 'testa-rezulto.py.txt'
    with open('testa-teksto.txt', 'r', encoding='utf-8') as reader:
        eo_text = reader.read()
    han_text = paragraph_eo_to_han(eo_text)
    with open('testa-rezulto.py.txt', 'w', encoding='utf-8') as writer:
        writer.write(han_text)
