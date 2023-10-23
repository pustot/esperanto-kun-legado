#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <unordered_map>
#include <vector>
#include <string>
#include <algorithm>
#include <regex>
#include <locale>
#include <codecvt>

// TODO: this c++ implementation is not finished

// TODO: （當前通過禁用-op-跳過，但沒解決比如別的詞根或真正用-op-者。比如可以限制-op- -on- 只用於數字前）
// ĉiopovan 每op蛋an

// 多字符字符常量，它们不是标准C++的一部分，所以从char改成string
std::map<std::string, std::string> special_upper_to_lower = {
    {"Ĉ", "ĉ"}, {"Ĝ", "ĝ"}, {"Ĥ", "ĥ"}, {"Ĵ", "ĵ"}, {"Ŝ", "ŝ"}, {"Ŭ", "ŭ"}
};

// 创建一个空字典来存储字典信息
std::unordered_map<std::string, std::string> dictionary = {
    // TODO: 如何正确处理不在一词之末的语法后缀，如 loĝantaro
        {"ant", ""}, {"int", ""}, {"ont", ""},
        {"at", ""}, {"it", ""}, {"ot", ""}
};

// standalone roots
std::vector<std::string> roots = {
    "ĉar", "ĉi", "ĉu", "kaj", "ke", "la", "minus", "plus",
    "se", "ĉe", "da", "de", "el", "ekster", "en", "ĝis", "je", "kun", "na",
    "po", "pri", "pro", "sen", "tra", "ajn", "do", "ja", "jen", "ju", "ne",
    "pli", "tamen", "tre", "tro", "ci", "ĝi", "ili", "li", "mi", "ni", "oni",
    "ri", "si", "ŝi", "ŝli", "vi", "unu", "du", "tri", "kvin", "ĵus", "nun", "plu",
    "tuj", "amen", "bis", "boj", "fi", "ha", "he", "ho", "hu", "hura", "nu", "ve",
    // "esperanto", 
    "plej"
};

std::unordered_map<std::string, std::string> correlative_dict = {
    {"kia", "何a"}, {"kial", "何al"}, {"kiam", "何am"}, {"kie", "何e"}, {"kiel", "何el"}, {"kies", "何es"}, {"kio", "何o"}, {"kiom", "何om"}, {"kiu", "何u"},
    {"tia", "彼a"}, {"tial", "彼al"}, {"tiam", "彼am"}, {"tie", "彼e"}, {"tiel", "彼el"}, {"ties", "彼es"}, {"tio", "彼o"}, {"tiom", "彼om"}, {"tiu", "彼u"},
    {"ia", "某a"}, {"ial", "某al"}, {"iam", "某am"}, {"ie", "某e"}, {"iel", "某el"}, {"ies", "某es"}, {"io", "某o"}, {"iom", "某om"}, {"iu", "某u"},
    {"ĉia", "每a"}, {"ĉial", "每al"}, {"ĉiam", "每am"}, {"ĉie", "每e"}, {"ĉiel", "每el"}, {"ĉies", "每es"}, {"ĉio", "每o"}, {"ĉiom", "每om"}, {"ĉiu", "每u"},
    {"nenia", "無a"}, {"nenial", "無al"}, {"neniam", "無am"}, {"nenie", "無e"}, {"neniel", "無el"}, {"nenies", "無es"}, {"nenio", "無o"}, {"neniom", "無om"}, {"neniu", "無u"}
};

// 你的 CSV 文件列表
// 注意，加入映射词典的不包含 "gramatikaj-finaĵoj.csv"，因为有专门的去语法后缀的函数
std::vector<std::string> csv_files = {"pronomoj-kaj-tabelvortoj.csv", "afiksoj.csv", "alioj-de-facila.csv", "facilaj-vortoj.csv"};

// 去除字符串前后的连字符
// python 里面就直接 strip() 了。cpp有没有？
std::string trimHyphens(const std::string& str) {
    size_t start = str.find_first_not_of('-');
    size_t end = str.find_last_not_of('-');
    
    if (start == std::string::npos) {
        return "";
    }

    return str.substr(start, end - start + 1);
}

// 分离后缀的函数
std::pair<std::string, std::string> splitSuffix(const std::string& eo_word) {
    std::string word = eo_word;
    std::string suffix = "";

    // 如果单词为空，直接返回
    if (word.empty()) {
        return std::make_pair("", "");
    }

    
    if (std::find(roots.begin(), roots.end(), word) != roots.end()) {
        return std::make_pair(word, "");
    }

    // isalpha 只能应对26个拉丁字母。ux等特殊处理

    if (!std::isalpha(word.back())) {
        if (word.size() == 1) {
            return std::make_pair(word, "");
        }
        bool last_is_special_letter = false;
        for (const auto& [upper, lower] : special_upper_to_lower) {
            if (word.substr(word.length() - lower.length()) == lower)
                last_is_special_letter = true;
        }
        if (!last_is_special_letter) {
            suffix = std::string(1, word.back());
            word = word.substr(0, word.size() - 1);
        }
    }

    bool non_verb = false;

    // nouns, adjectives, -u correlatives:
    // -oj -on -ojn → -
    // -aj -an -ajn → -
    // -uj -un -ujn → -
    std::vector<std::string> suffixes = {"oj", "on", "aj", "an", "uj", "un", "ojn", "ajn", "ujn"};
    // Check for suffixes
    for (const std::string& s : suffixes) {
        size_t pos = word.rfind(s);
        if (pos != std::string::npos && pos == word.length() - s.length()) {
            suffix = s + suffix;
            word = word.substr(0, word.size() - s.length());
            non_verb = true;
            break; // Exit the loop after finding a matching suffix
        }
    }
    
    // correlatives: -en → -
    std::vector<std::string> cor_ens = {"kien", "tien", "ien", "nenien", "ĉien"};
    if (std::find(cor_ens.begin(), cor_ens.end(), word) != cor_ens.end()) {
        return std::make_pair(word.substr(0, word.size() - 2), "en");
    }

    // correlative roots
    if (correlative_dict.count(word) || (
        suffix.size() && correlative_dict.count(word + suffix[0])
    )) {
        if (suffix.size()) {
            word += suffix[0];
            suffix = suffix.substr(1);
        }
        return std::make_pair(correlative_dict[word], suffix);
    }

    // nur se ne stemmita.
    // 否则会错： ideoj, hebreoj
    if (!non_verb && (word.back() == 'a' || word.back() == 'o' || word.back() == 'e')) {
        suffix = word.back();
        word.pop_back();
        non_verb = true;
    }

    // accusative pronouns: -in → 
    std::vector<std::string> prons = {"ci", "ĝi", "ili", "li", "mi", "ni", "oni",
	                                        "ri", "si", "ŝi", "ŝli", "vi"};
    if (word.size() >= 2 && word.substr(word.size() - 2) == "in" &&
        std::find(prons.begin(), prons.end(), word.substr(0, word.size() - 1))!=prons.end()) {
            return std::make_pair(word.substr(0, word.size() - 1), "n");
    }

    // accusative adverbs: -en → -
    if (word.size() >= 2 && word.substr(word.size() - 2) == "en") {
        suffix = "en";
        word = word.substr(0, word.size() - 2);
        non_verb = true;
    }

    // verbs: -is -as -os -us -u → -
    if (!non_verb) {
        if (word.back() == 'i' || word.back() == 'u') {
            suffix = std::string(1, word.back());
            word.pop_back();
        } else if (word.size() > 2 && (
            word.substr(word.size() - 2) == "is" ||
            word.substr(word.size() - 2) == "as" ||
            word.substr(word.size() - 2) == "os" ||
            word.substr(word.size() - 2) == "us" 
        )) {
            suffix = word.substr(word.size() - 2) + suffix;
            word = word.substr(0, word.size() - 2);
        }
    }

    // lexical aspect: ek- el-

    // note: not enabled. -ad- 暫時視爲有實意的詞根
    // imperfective verbs & action nouns: -adi -ado → -i

    // compound verbs:
	    // -inti -anti -onti -iti -ati -oti → -i
	    // -inte -ante -onte -ite -ate -ote → -i
	    // -inta -anta -onta -ita -ata -ota → -i
    // participle nouns:
	    // -into -anto -onto → -anto → o
	    // -ito  -ato  -oto  → -ato → o
    // 特殊情况于 dat- 等词
    std::vector<std::string> special_roots_with_xt = {"dat", "frat", "rilat", "spirit", "strat"};
    if (word.size() > 3 && (
            word.substr(word.size() - 3) == "int" ||
            word.substr(word.size() - 3) == "ant" ||
            word.substr(word.size() - 3) == "ont"
    )) {
        suffix = word.substr(word.size() - 3) + suffix;
        word = word.substr(0, word.size() - 3);
    } else if (word.size() > 2 && (
            word.substr(word.size() - 2) == "it" ||
            word.substr(word.size() - 2) == "at" ||
            word.substr(word.size() - 2) == "ot"
    ) && !std::count(special_roots_with_xt.begin(), special_roots_with_xt.end(), word)) {
        suffix = word.substr(word.size() - 2) + suffix;
        word = word.substr(0, word.size() - 2);
    }

    return std::make_pair(word, suffix);
}

std::string word_eo_to_han(const std::string& eo_word, bool is_before_hyphen=false, bool is_sentence_begin=false) {
    std::string word = eo_word;
    // 如果单词为空，直接返回
    if (word.empty()) {
        return "";
    }

    bool is_first_upper = false;
    // 目前句首的先都小写，但没法应对句首出现未知词
    if (is_sentence_begin) {
        if (std::isupper(word[0])) {
            is_first_upper = true;
            word[0] = std::tolower(word[0]);
        }
        for (const auto& [upper, lower] : special_upper_to_lower)
            if (word.find(upper) == 0) { 
                is_first_upper = true;
                word.replace(0, upper.length(), lower);
            }
    }

    // if it is before hyphen, it already has no grammatical suffix
    // 不过这种方案目前可以兼容一些连字符前带后缀者如 drako-reĝo -> 龍o-王o
    // eo 连字符合成词的规则究竟如何，还需了解。
    std::string suffix;
    if (is_before_hyphen) {
        suffix = "";
    } else {
        // TODO: 仅为避混于「每」之紧急措施。
        if (word == "ĉi")
            return "此";
        // C++ 17 中的结构化绑定（Structured Binding）
        std::pair<std::string, std::string> p = splitSuffix(word);
        word = p.first;
        suffix = p.second;
    }

    // 初始化汉字化后的单词
    std::string chinese_word = "";

    // 遍历世界语单词的每个字母
    int i = 0;
    while (i < word.size()) {
        // 从当前位置开始查找最长的词根
        std::string current_root = "";
        int j = i;
        int valid_j = i;
        while (j < word.size()) {
            std::string substring = word.substr(i, j - i + 1);
            if (dictionary.find(substring) != dictionary.end()) {
                current_root = substring;
                valid_j = j;
            }
            j++;
        }

        // TODO: 暂时对 intern 特殊处理以应对 internacia 样单词
        if (current_root == "intern" && valid_j + 2 < word.size()) {
            chinese_word += dictionary["inter"];
            i = valid_j;
            continue;
        }

        // 如果找到了词根，则将其替换为对应的汉字
        if (!current_root.empty()) {
            // 有的词根的汉字化列置空，如此则还是保留拉丁字形式
            chinese_word += dictionary[current_root] != "" ? dictionary[current_root] : current_root;
            i = valid_j + 1;
        } else {
            // 如果未找到词根，则保留原始字符
            // chinese_word += word[i];
            // i += 1
            // TODO: 在只有部分词根有记录时，如何处理，以使例如 `cenzuran` 不变成 `c入zur民`。暂时全词皆删
            chinese_word = word;
            break;
        }
    }

    if (is_first_upper) {
        if (std::islower(chinese_word[0])) {
            chinese_word[0] = std::toupper(chinese_word[0]);
        }
        for (const auto& [upper, lower] : special_upper_to_lower)
            if (chinese_word.find(lower) == 0) { 
                chinese_word.replace(0, lower.length(), upper);
            }
    }
    

    return chinese_word + suffix;
}

// std::wstring stringToWstring(const std::string& str) {
//     std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
//     return converter.from_bytes(str);
// }

// std::string wstringToString(const std::wstring& wstr) {
//     std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
//     return converter.to_bytes(wstr);
// }

std::string paragraph_eo_to_han(const std::string& eo_paragraph) {
    // std::wstring w_eo_paragraph = stringToWstring(eo_paragraph);
    // std::cout << w_eo_paragraph << std::endl;
    std::vector<std::string> eo_word_list;
    // 尝试了用 wregex 使 \w 可以自动匹配帽子字母，但引入的问题太多，还是改成直接写一遍吧，即 [\wĉĝĥĵŝŭĈĜĤĴŜŬ]+
    // std::wregex words_regex(LR"([\w]+|[.,!?;\:\-“„”\'\"«»\~\[\]\{\}\n]| )");
    std::regex words_regex(R"([\wĉĝĥĵŝŭĈĜĤĴŜŬ]+|[.,!?;\:\-“„”\'\"«»\~\[\]\{\}\n]| )");
    auto words_begin = std::sregex_iterator(eo_paragraph.begin(), eo_paragraph.end(), words_regex);
    auto words_end = std::sregex_iterator();

    for (std::sregex_iterator it = words_begin; it != words_end; ++it) {
        eo_word_list.push_back(it->str());
    }

    std::string han_text;
    for (int i = 0; i < eo_word_list.size(); ++i) {
        const std::string& word = eo_word_list[i];
        bool is_hyphen_next = (i + 1 < eo_word_list.size()) && (eo_word_list[i + 1] == "-");
        //  判断是不是句首，情况太多了。。。
        bool is_sentence_start = ((i == 0) || (i == 1 && eo_word_list[0] == "\n") ||
            (i - 2 >= 0 && (eo_word_list[i - 1] == " " || eo_word_list[i - 1] == "\n") && eo_word_list[i - 2] == ".") ||
            (i - 3 >= 0 && (eo_word_list[i - 1] == " " || eo_word_list[i - 1] == "\n") && 
                    (eo_word_list[i - 2] == " " || eo_word_list[i - 2] == "\n") && eo_word_list[i - 3] == "."));

        std::string han_word = word_eo_to_han(word, is_hyphen_next, is_sentence_start);
        
        han_text += han_word;
    }

    return han_text;
}

int main() {
    // 循环遍历每个 CSV 文件
    for (const std::string& csv_file : csv_files) {
        std::ifstream file(csv_file);  // 打开CSV文件
        if (!file.is_open()) {
            std::cerr << "Failed to open file: " << csv_file << std::endl;
            return 1;
        }

        std::string line;
        std::getline(file, line);  // 读取第一行（标题），但不使用它
        // 文件可能跨越操作系统，所以必须判断结尾是 CRLF 还是 LF，否则汉字后会带\r，显示完全错误
        bool isCRLF = line.find('\r') != std::string::npos;

        while (std::getline(file, line)) {
            
            if (isCRLF)
                line.erase(std::remove(line.begin(), line.end(), '\r'), line.end());
            std::istringstream iss(line);
            std::string eo_word, han_word;
            if (std::getline(iss, eo_word, ',')) {
                // In case the han field is empty, like "oni," "-o,"
                if (!std::getline(iss, han_word, ',')) han_word = "";
                eo_word = trimHyphens(eo_word);  // 去掉前后的连字符
                dictionary[eo_word] = han_word;  // 将信息存储在unordered_map中
            }
            
        }
    }

    std::cout << "************ĉ、ĝ、ĥ、ĵ、ŝ、ŭ  Ĉ, Ĝ, Ĥ, Ĵ, Ŝ, Ŭ**********" << std::endl;
    std::cout << "Test Dict: o " << dictionary.count("o") << ", oni " << dictionary.count("oni") << ", aŭ " << dictionary.count("aŭ") << std::endl;
    std::cout << "************vorta ekzemplo**********" << std::endl;
    std::cout << word_eo_to_han("internacia") << std::endl;
    std::cout << word_eo_to_han("estas") << std::endl;
    std::cout << word_eo_to_han("vortojn") << std::endl;
    std::cout << word_eo_to_han(".") << std::endl;
    std::cout  << "oni " << word_eo_to_han("oni") << std::endl;
    std::cout  << "partopreni " << word_eo_to_han("partopreni") << std::endl;
    std::cout  << "ĉiopovan " << word_eo_to_han("ĉiopovan") << std::endl;
    std::cout << "************fraza/paragrafa ekzemplo**********" << std::endl;
    std::cout  << "Ĉar aŭ almenaŭ " << paragraph_eo_to_han("Ĉar aŭ almenaŭ ") << std::endl;
    std::cout  << "Ĉharaqueter spezielle " << paragraph_eo_to_han("Ĉharaqueter spezielle ") << std::endl;
    std::cout  << "drako-reĝo " << paragraph_eo_to_han("drako-reĝo") << std::endl;

    // Read the Esperanto text from 'testa-teksto.txt'
    std::ifstream reader("testa-teksto.txt");
    if (!reader.is_open()) {
        std::cerr << "Failed to open input file." << std::endl;
        return 1;
    }

    std::stringstream buffer;
    buffer << reader.rdbuf();
    std::string eo_text = buffer.str();
    reader.close();

    // Convert Esperanto text to Hanzi
    std::string han_text = paragraph_eo_to_han(eo_text);

    // Write the Hanzi text to 'testa-rezulto.cpp.txt'
    std::ofstream writer("testa-rezulto.cpp.txt");
    if (!writer.is_open()) {
        std::cerr << "Failed to open output file." << std::endl;
        return 1;
    }

    writer << han_text;
    writer.close();

    std::cout << "Hanzi test-text saved to 'testa-rezulto.cpp.txt'" << std::endl;

    return 0;
}

// 现在，世界语的帽子符有问题
/* 
************ĉ、ĝ、ĥ、ĵ、ŝ、ŭ  Ĉ, Ĝ, Ĥ, Ĵ, Ŝ, Ŭ**********
Test Dict: o 1, oni 1, aŭ 1
************vorta ekzemplo**********
間族a
是as
詞ojn
.
oni oni
partopreni 部o取i
ĉiopovan ĉio可an
************fraza/paragrafa ekzemplo**********
Ĉar aŭ almenaŭ 因 或 至少
Ĉharaqueter spezielle Ĉharaqueter spezielle
drako-reĝo 龍o-王o
Hanzi test-text saved to 'testa-rezulto.cpp.txt'
*/
