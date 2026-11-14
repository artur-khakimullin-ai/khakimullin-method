import math
import re
from collections import Counter

VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouyAEIOUY")
CONSONANTS = set("бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩbcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ")

# Базовый словарь распространенных поэтических штампов и канцеляризмов
CLICHE_PATTERNS = [
    r"любов[ьи]\s*[-—]?\s*кров[ьи]",
    r"душ[аеу]\s*[-—]?\s*тишин[аеу]",
    r"осенн(ий|яя|ее|ие)\s+(ветер|дождь|грусть|печаль)",
    r"холодн(ый|ая|ое|ые)\s+(ветер|дождь|взгляд|сердце)",
    r"разбит(ое|ым|ом)\s+сердц(е|ем|а)",
    r"слез[аы]\s+на\s+глазах",
    r"в\s+рамках\s+данного",
    r"на\s+сегодняшний\s+день",
    r"играет\s+важную\s+роль"
]

def tokenize(text: str):
    return re.findall(r"[а-яА-ЯёЁa-zA-Z]+(?:-[а-яА-ЯёЁa-zA-Z]+)*", text.lower())

def shannon_entropy(text: str) -> float:
    cleaned = re.sub(r"\s+", "", text.lower())
    if not cleaned:
        return 0.0
    counts = Counter(cleaned)
    length = len(cleaned)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())

def analyze_phonology(words):
    total_letters = 0
    consonant_count = 0
    cluster_words = []

    for word in words:
        letters = [ch for ch in word if ch in VOWELS or ch in CONSONANTS]
        total_letters += len(letters)
        consonant_count += sum(1 for ch in letters if ch in CONSONANTS)

        # Поиск кластеров из 3 и более согласных подряд
        streak = 0
        has_cluster = False
        for ch in letters:
            if ch in CONSONANTS:
                streak += 1
                if streak >= 3:
                    has_cluster = True
            else:
                streak = 0
        if has_cluster:
            cluster_words.append(word)

    consonant_ratio = (consonant_count / total_letters) if total_letters else 0.0
    cluster_density = (len(cluster_words) / len(words)) if words else 0.0
    return consonant_ratio, cluster_density, cluster_words

def check_authenticity(text: str, ttr: float, entropy: float, cluster_density: float):
    lower_text = text.lower()
    found_cliches = []
    for pattern in CLICHE_PATTERNS:
        matches = re.findall(pattern, lower_text)
        if matches:
            found_cliches.append(pattern)

    # Расчет индекса аутентичности (0-100)
    score = 50.0
    score += min(ttr * 30.0, 30.0)             # Вклад лексического разнообразия
    score += min(max(entropy - 3.5, 0) * 10, 12.0)  # Вклад информационной энтропии
    score += min(cluster_density * 100, 8.0)   # Вклад фонетического сопротивления
    score -= len(found_cliches) * 15.0         # Штраф за обнаруженные клише
    score = max(0.0, min(100.0, score))

    return round(score, 1), found_cliches

def generate_report(text: str, title: str = "Без названия", mode: str = "Universal (Syllabo-Tonic / Tonic / Prose)"):
    words = tokenize(text)
    total_words = len(words)
    unique_words = len(set(words))
    ttr = (unique_words / total_words) if total_words else 0.0
    entropy = shannon_entropy(text)
    cons_ratio, cluster_density, cluster_words = analyze_phonology(words)
    auth_score, cliches = check_authenticity(text, ttr, entropy, cluster_density)

    print("=" * 64)
    print("АНАЛИТИЧЕСКИЙ ОТЧЁТ (МЕТОД ХАКИМУЛЛИНА v1.2)")
    print("=" * 64)
    print(f"Объект анализа : {title}")
    print(f"Режим анализа  : {mode}")
    print("-" * 64)
    print("1. КОЛИЧЕСТВЕННЫЕ И ФОНОЛОГИЧЕСКИЕ ПОКАЗАТЕЛИ")
    print(f"   • Всего слов (Total Words)           : {total_words}")
    print(f"   • Уникальных слов (Unique Words)     : {unique_words}")
    print(f"   • Лексическое разнообразие (TTR)     : {ttr:.4f} ({ttr*100:.1f}%)")
    print(f"   • Энтропия Шеннона (Shannon Entropy) : {entropy:.4f} bits/char")
    print(f"   • Доля согласных (Consonant Ratio)   : {cons_ratio:.4f} ({cons_ratio*100:.1f}%)")
    print(f"   • Плотность кластеров (3+ согласных) : {cluster_density:.4f} ({cluster_density*100:.2f}%)")
    if cluster_words:
        print(f"   • Слова с кластерами                 : {', '.join(cluster_words)}")
    print("-" * 64)
    print("2. ДИАГНОСТИКА АУТЕНТИЧНОСТИ И КЛИШЕ")
    print(f"   • Обнаружено клише и штампов         : {len(cliches)}")
    print(f"   • Итоговый индекс аутентичности      : {auth_score} / 100")
    print("=" * 64)

if __name__ == "__main__":
    sample_text = """
    Мысли торжественней ночью,
    Есть у них дар спасения.
    Только проблема вот в чём:
    Отключено отопление.
    """
    generate_report(sample_text, title="Тестовый фрагмент (Силлабо-тоника)")
