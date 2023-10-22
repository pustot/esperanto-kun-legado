#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <unordered_map>
#include <vector>
#include <string>

// TODO: this c++ implementation is not finished

// TODO: （當前通過禁用-op-跳過，但沒解決比如別的詞根或真正用-op-者。比如可以限制-op- -on- 只用於數字前）
// ĉiopovan 每op蛋an

// 创建一个空字典来存储字典信息
std::map<std::string, std::string> dictionary = {
    // TODO: 如何正确处理不在一词之末的语法后缀，如 loĝantaro
        {"ant", ""}, {"int", ""}, {"ont", ""},
        {"at", ""}, {"it", ""}, {"ot", ""}
};

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

// 循环遍历每个 CSV 文件
for (const std::string& csv_file : csv_files) {
    std::ifstream file(csv_file);  // 打开CSV文件
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << csv_file << std::endl;
        return 1;
    }

    std::string line;
    std::getline(file, line);  // 读取第一行（标题），但不使用它

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string eo_word, han_word;
        if (std::getline(iss, eo_word, ',') && std::getline(iss, han_word, ',')) {
            eo_word = trimHyphens(eo_word);  // 去掉前后的连字符
            dictionary[eo_word] = han_word;  // 将信息存储在unordered_map中
        }
    }
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

    if (!std::isalpha(word.back())) {
        if (word.size() == 1) {
            return std::make_pair(word, "");
        }
        suffix = std::string(1, word.back());
        word = word.substr(0, word.size() - 1);
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
            word = word.pop_back();
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