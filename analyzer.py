import re
import math
from collections import Counter

VOWELS = set("аеёиоуыэюя")
CONSONANTS = set("бвгджзйклмнпрстфхцчшщ")

def analyze_text_metrics(text: str) -> dict:
    """
    Calculates baseline phonological and information-theoretic metrics
    from The Khakimullin Method (Метод Хакимуллина) for Russian text.
    """
    clean_chars = [ch.lower() for ch in text if ch.isalpha() or ch.isspace()]
    char_stream = "".join(clean_chars)

    # 1. Shannon Character Entropy (bits/char)
    char_counts = Counter(char_stream)
    total_chars = len(char_stream)
    entropy = -sum(
        (count / total_chars) * math.log2(count / total_chars)
        for count in char_counts.values()
    ) if total_chars > 0 else 0.0

    # 2. Lexical Diversity Index (Type-Token Ratio)
    words = re.findall(r"[а-яё]+", text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    ttr = unique_words / total_words if total_words > 0 else 0.0

    # 3. Consonant Ratio & Consonant Clusters (3+ consecutive consonants)
    letters = [ch for ch in text.lower() if ch in VOWELS or ch in CONSONANTS]
    consonant_ratio = sum(1 for ch in letters if ch in CONSONANTS) / len(letters) if letters else 0.0

    clusters = re.findall(r"[бвгджзйклмнпрстфхцчшщ]{3,}", text.lower())
    cluster_density = len(clusters) / total_words if total_words > 0 else 0.0

    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "ttr": round(ttr, 3),
        "shannon_entropy": round(entropy, 3),
        "consonant_ratio": round(consonant_ratio, 3),
        "clusters_found": clusters,
        "cluster_density_per_word": round(cluster_density, 3),
    }

if __name__ == "__main__":
    sample_prose = (
        "Раздался оглушительный скрежет деформируемого металла. "
        "Толстая обшивка скручивалась под моими пальцами, как размокший картон. "
        "Полтора метра в ширину. Два в длину. "
        "Я не собирался умирать в этом гробу. Не сегодня."
    )

    metrics = analyze_text_metrics(sample_prose)
    print("The Khakimullin Method — Text Metrics Report:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
