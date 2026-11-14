import re
import math
from collections import Counter

VOWELS = set("аеёиоуыэюя")
CONSONANTS = set("бвгджзйклмнпрстфхцчшщ")
SONORANTS = set("лмнрй")
EXPLOSIVES_HISSING = set("бпдтгкжшщчц")

STOPWORDS = {
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то",
    "все", "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за",
    "бы", "по", "только", "ее", "мне", "было", "вот", "от", "меня", "еще", "нет",
    "о", "из", "ему", "теперь", "когда", "даже", "ну", "вдруг", "ли", "если", "уже"
}


def levenshtein(s1: str, s2: str) -> int:
    """Расстояние Левенштейна для поиска паронимической аттракции."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def extract_consonant_skeleton(word: str) -> str:
    """Извлекает согласный скелет слова для оценки консонанса."""
    return "".join(ch for ch in word.lower() if ch in CONSONANTS)


def simple_russian_stem(word: str) -> str:
    """Базовый стеммер без зависимостей для выделения корневой основы."""
    w = word.lower()
    if len(w) <= 4:
        return w
    w = re.sub(
        r"(ющими|ющимися|ащими|ящими|вшими|ыми|ими|ого|его|ому|ему|ами|ями|ах|ях|ой|ей|ом|ем|ую|юю|ая|яя|ое|ее|ые|ие|ть|ти|ся|сь)$",
        "",
        w,
    )
    return w if len(w) >= 3 else word.lower()


def analyze_khakimullin_method(text: str) -> dict:
    """
    Комплексный анализ текста по 13-метрической архитектуре Метода Хакимуллина.
    Zero-dependency Python NLP Analyzer v2.0.
    """
    clean_text = text.strip()
    if not clean_text:
        return {"error": "Empty text provided"}

    lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
    sentences = [s.strip() for s in re.split(r"[\.\!\?]+", clean_text) if s.strip()]
    words = re.findall(r"[а-яё]+", clean_text.lower())

    if not words:
        return {"error": "No Cyrillic words found"}

    # =========================================================================
    # БАЗОВЫЕ КОЛИЧЕСТВЕННЫЕ МЕТРИКИ (v1.0 Core)
    # =========================================================================
    char_counts = Counter(clean_text.lower())
    total_chars = len(clean_text)
    shannon_entropy = round(
        -sum((count / total_chars) * math.log2(count / total_chars) for count in char_counts.values()),
        3,
    )

    unique_words = set(words)
    ttr = round(len(unique_words) / len(words), 3)

    letters_only = [ch for ch in clean_text.lower() if ch in VOWELS or ch in CONSONANTS]
    consonant_count = sum(1 for ch in letters_only if ch in CONSONANTS)
    consonant_ratio = round(consonant_count / max(1, len(letters_only)), 3)

    cluster_pattern = re.compile(r"[бвгджзйклмнпрстфхцчшщ]{3,}")
    words_with_clusters = sum(1 for w in words if cluster_pattern.search(w))
    cluster_density = round(words_with_clusters / len(words), 3)

    # =========================================================================
    # УРОВЕНЬ I: ФОНОЛОГИЧЕСКАЯ МАТРИЦА (Tier I)
    # =========================================================================
    alliterated_lines = 0
    for line in lines:
        line_words = re.findall(r"[а-яё]+", line.lower())
        if len(line_words) >= 2:
            line_cons = []
            for w in line_words:
                line_cons.extend(set(ch for ch in w if ch in CONSONANTS))
            counts = Counter(line_cons)
            if counts and counts.most_common(1)[0][1] >= min(3, len(line_words)):
                alliterated_lines += 1
    horizontal_alliteration = round(alliterated_lines / max(1, len(lines)), 3)

    skeletons = [extract_consonant_skeleton(w) for w in words]
    valid_skeletons = [s for s in skeletons if len(s) >= 2]
    skel_counts = Counter(valid_skeletons)
    consonance_matches = sum(1 for s in valid_skeletons if skel_counts[s] > 1)
    consonance_density = round(consonance_matches / max(1, len(valid_skeletons)), 3)

    long_words = list(dict.fromkeys(w for w in words if len(w) >= 4))
    paronym_pairs = []
    for i in range(len(long_words)):
        for j in range(i + 1, len(long_words)):
            w1, w2 = long_words[i], long_words[j]
            if abs(len(w1) - len(w2)) <= 2:
                dist = levenshtein(w1, w2)
                if 1 <= dist <= 2 and w1[:2] == w2[:2]:
                    paronym_pairs.append(f"{w1}-{w2}")
    paronym_index = round(len(paronym_pairs) / max(1, len(long_words)), 3)

    # =========================================================================
    # УРОВЕНЬ II: РИТМИКО-МЕТРИЧЕСКИЙ ДВИГАТЕЛЬ (Tier II)
    # =========================================================================
    syllables_per_line = [sum(1 for ch in line.lower() if ch in VOWELS) for line in lines]
    mean_syl = sum(syllables_per_line) / max(1, len(syllables_per_line))
    variance_syl = sum((x - mean_syl) ** 2 for x in syllables_per_line) / max(1, len(syllables_per_line))
    cv_rhythm = round(math.sqrt(variance_syl) / max(0.1, mean_syl), 3)

    internal_breaks = sum(
        len(re.findall(r"(?<=\w)[\.\!\?]\s+(?=[А-ЯЁ])|\s+[-—]\s*$|[-—]\s+", line))
        for line in lines
    )
    syncopation_score = round(cv_rhythm + (internal_breaks / max(1, len(lines))), 3)

    # =========================================================================
    # УРОВЕНЬ III: СЕМАНТИЧЕСКАЯ ГЕОМЕТРИЯ И ПРОЗА (Tier III)
    # =========================================================================
    content_words = [w for w in words if w not in STOPWORDS and len(w) >= 3]
    stems = [simple_russian_stem(w) for w in content_words]
    stem_positions = {}
    for idx, st in enumerate(stems):
        stem_positions.setdefault(st, []).append(idx)

    distant_loops = sum(
        1 for positions in stem_positions.values()
        if len(positions) >= 2 and (positions[-1] - positions[0]) >= 5
    )
    distant_repetition_index = round(distant_loops / max(1, len(set(stems))), 3)

    hard_count = sum(1 for ch in letters_only if ch in EXPLOSIVES_HISSING)
    soft_count = sum(1 for ch in letters_only if ch in SONORANTS)
    phonosemantic_tension = round(hard_count / max(1, hard_count + soft_count), 3)

    complex_words = [w for w in content_words if len(w) >= 8]
    defamiliarization_density = round(
        (len(complex_words) / max(1, len(content_words))) * (len(content_words) / max(1, len(words))),
        3,
    )

    sent_lengths = [len(re.findall(r"[а-яё]+", s.lower())) for s in sentences]
    if len(sent_lengths) > 1:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        var_len = sum((x - mean_len) ** 2 for x in sent_lengths) / len(sent_lengths)
        prose_accent_pulse = round(math.sqrt(var_len) / max(0.1, mean_len), 3)
    else:
        prose_accent_pulse = 0.0

    # =========================================================================
    # ИНТЕГРАЛЬНЫЙ ИНДЕКС МЕТОДА ХАКИМУЛЛИНА (K-Index)
    # =========================================================================
    k_index = round(
        (
            (shannon_entropy / 5.0) * 1.5
            + ttr * 1.5
            + cluster_density * 2.0
            + horizontal_alliteration
            + consonance_density
            + paronym_index * 1.5
            + min(1.0, syncopation_score)
            + distant_repetition_index * 1.5
            + phonosemantic_tension
            + defamiliarization_density * 2.0
            + min(1.0, prose_accent_pulse)
        )
        / 10.0,
        3,
    )

    return {
        "core_metrics": {
            "shannon_entropy": shannon_entropy,
            "ttr_lexical_diversity": ttr,
            "consonant_ratio": consonant_ratio,
            "consonant_cluster_density": cluster_density,
        },
        "tier_1_phonology": {
            "horizontal_alliteration": horizontal_alliteration,
            "consonance_density": consonance_density,
            "paronymic_attraction_index": paronym_index,
            "paronym_pairs": paronym_pairs[:5],
        },
        "tier_2_rhythm": {
            "rhythmic_cv": cv_rhythm,
            "syncopation_score": syncopation_score,
        },
        "tier_3_semantics": {
            "distant_semantic_loops": distant_loops,
            "distant_repetition_index": distant_repetition_index,
            "phonosemantic_tension": phonosemantic_tension,
            "defamiliarization_density": defamiliarization_density,
            "prose_accent_pulse": prose_accent_pulse,
        },
        "K_INDEX_TOTAL": k_index,
    }


def print_report(results: dict) -> None:
    """Форматированный вывод отчёта в консоль."""
    if "error" in results:
        print(f"Ошибка: {results['error']}")
        return

    print("=" * 60)
    print("THE KHAKIMULLIN METHOD (МЕТОД ХАКИМУЛЛИНА) — NLP AUDIT v2.0")
    print("=" * 60)

    sections = [
        ("БАЗОВЫЕ МЕТРИКИ (CORE)", results["core_metrics"]),
        ("УРОВЕНЬ I: ФОНОЛОГИЧЕСКАЯ МАТРИЦА", results["tier_1_phonology"]),
        ("УРОВЕНЬ II: РИТМИКО-МЕТРИЧЕСКИЙ ДВИГАТЕЛЬ", results["tier_2_rhythm"]),
        ("УРОВЕНЬ III: СЕМАНТИЧЕСКАЯ ГЕОМЕТРИЯ", results["tier_3_semantics"]),
    ]

    for title, data in sections:
        print(f"\n[{title}]")
        for key, val in data.items():
            print(f"  {key:<30}: {val}")

    print("\n" + "=" * 60)
    print(f"ИТОГОВЫЙ ИНДЕКС ПЛОТНОСТИ (K-INDEX): {results['K_INDEX_TOTAL']}")
    print("=" * 60)


if __name__ == "__main__":
    sample_text = """
В шелесте своей орбиты -
Сахар,
Случайно
Столкнулся с другой галактикой
Сияющим гало.

Градинками
Тростника Кубы
Из ложки стальной зажатой
