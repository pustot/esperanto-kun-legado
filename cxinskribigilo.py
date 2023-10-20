import csv
import re

# 创建一个空字典来存储字典信息
dictionary = {}

# 你的 CSV 文件列表
csv_files = ["gramatikaj-finaĵoj.csv", "afiksoj.csv", "facilaj-vortoj.csv", "pronomoj-kaj-tabelvortoj.csv", "alioj-de-facila.csv"]

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

# 定义一个字典，将世界语词根映射到对应的汉字
root_to_chinese = dictionary


# 定义一个函数，将世界语单词转换为汉字化的单词
def word_eo_to_han(eo_word):
    # 目前先都小写
    eo_word = eo_word.lower()

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
        if current_root == 'intern' and eo_word[valid_j + 1:] not in ['o', 'a', 'oj', 'aj', 'ojn', 'ajn']:
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

    return chinese_word


def sentence_eo_to_han(eo_sentence):
    eo_word_list = re.findall(r"[\w]+|[.,!?;\-“„]| ", eo_sentence)
    return ''.join([word_eo_to_han(word) for word in eo_word_list])

# word_eo_to_han 使用示例
eo_word = "naskiĝtago"
han_word = word_eo_to_han(eo_word)
print(han_word)  
# 输出：
"""
誕成日o
"""

# sentence_eo_to_han 使用示例
# TODO: 语尾如 -on -an -i 被错误汉字化
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
冀anto, 原e la 語o 間族a, 是as la 最 散廣成inta 間族a 謀語o. la 名o de la 語o 來as de la 隱名o “d-ro 冀anto„ 
下 何u la varsovia 眼-醫者o ludoviko lazaro zamenhofo 入 la 年o 1887 公化is la 基分 de la 語o. la 一a 版o, la rusa, 
獲is la cenzuran 許分 散廣成某 入 la 26-a de j佬某o; 每 彼un 期分 oni 慮as la 誕成日o de 冀anto. 
他 的is 和 昌is 創某 易e 習能士 中立士 語分, 適士 爲 使o 入 la 間族a 談久o; la 的o 然而 不 是as 替化某 另ajn, 族ajn 語ojn.
"""
