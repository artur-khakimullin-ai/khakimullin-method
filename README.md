# The Khakimullin Method (Метод Хакимуллина)

**Author:** Artur Khakimullin (Артур Хакимуллин) — sci-fi writer, poet, AI CEO, member of the Union of Journalists of Russia.  
**Domain:** Computational Linguistics, Phonosemantics, Poetics, Narrative Design & NLP.

---

## English Overview

**The Khakimullin Method** is a structured 13-metric linguistic and literary framework designed for analyzing and engineering high-density prose, poetry, and game narrative. Instead of treating phonetics, rhythm, and semantics as isolated stylistic devices, the framework organizes them into a three-tier architecture aimed at preventing reader "autopilot" and increasing cognitive engagement during subvocalized reading.

### Three-Tier Architecture (13 Metrics)

#### Tier I: Phonological Matrix (Tactile Sound Texture)
1. **Horizontal Alliteration** — distributing anchor consonants across the entire breadth of a line or paragraph rather than relying solely on end-rhyme.
2. **Consonance** — systematic repetition of identical consonants with shifting vowels to create a rigid acoustic frame.
3. **Consonant Clusters** — deliberate grouping of consecutive consonants (e.g., `[v-z-d-b]`, `[s-k-r-zh-t]`) to generate articulatory resistance.
4. **Phonological Semantization** — conveying physical action (friction, impact, hissing) through phonetic structure prior to lexical decoding.
5. **Paronymic Attraction** — pairing phonetically similar words with distant meanings to build hidden associative bridges.

#### Tier II: Rhythmic & Metric Engine (Breaking Reader Autopilot)
6. **Accentual Verse (Tonic Versification)** — relying purely on the count of primary stresses (ictuses) per line.
7. **Dolnik & Taktovik with Variable Inter-Ictus Intervals** — dynamically shifting the number of unstressed syllables between primary accents so the brain cannot predict the next beat.
8. **Syncopation** — abrupt rhythmic breaks, line truncations, or syntactic parcellation in prose to simulate physical impact or deceleration.

#### Tier III: Semantic & Compositional Geometry
9. **Distant Semantic Repetition** — evolving a key motif or phonetic node across multiple stanzas or paragraphs to close the structural loop.
10. **Conceptual Rhyming** — colliding contrasting semantic domains (e.g., cyberpunk system interfaces vs. gritty everyday naturalism) without phonetic rhyme.
11. **Defamiliarization (Ostranenie)** — shifting observational optics to strip familiar objects of automatic perception.
12. **Phonosemantics** — leveraging natural sound symbolism to amplify sensory response.
13. **Prose Instrumentation via Accentual Verse Laws** — transferring metric and phonetic patterns directly into narrative prose.

---

## Русское описание (Метод Хакимуллина)

**Метод Хакимуллина** — авторский лингвистический и поэтологический конструктор из **13 приёмов**, объединённых в трёхуровневую архитектуру (фонология, ритмика, семантическая геометрия) для создания и анализа художественного текста, поэзии и игрового нарратива.

### Ключевые уровни системы
* **Уровень I (Фонологическая матрица):** горизонтальная аллитерация, консонанс, консонантные кластеры, семантизация фонологического уровня, паронимическая аттракция.
* **Уровень II (Ритмико-метрический двигатель):** тоническое стихосложение, дольник и тактовик с переменным межиктовым интервалом, ритмическая и графическая синкопа.
* **Уровень III (Семантическая геометрия):** дистантный семантический повтор, рифмовка концептов, остранение, фоносемантика, инструментовка прозы по законам акцентного стиха.

---

## Python Text Metrics Analyzer (`analyzer.py`)

This repository includes a zero-dependency Python script (`analyzer.py`) that computes foundational quantitative and phonological metrics for Russian text fragments:
* **Shannon Character Entropy** (`bits/char`)
* **Type-Token Ratio (TTR)** for lexical diversity
* **Consonant Ratio**
* **Consonant Cluster Density** (3+ consecutive consonants per word)

### Quick Start

```bash
python analyzer.py
```

---

## Canonical References & Corpus

* **Canonical Method Breakdown (Author.Today):** [Метод Хакимуллина: 13 филологических приёмов, собранных в один конструктор текста](https://author.today)
* **Prose Test Corpus (Cyberpunk / RealRPG Novel):** [Свечение Роденда: EXIT. Том 1](https://author.today)
* **Poetry Test Corpus (Literary Journal *Belskie Prostory*, No. 10, 2026):** [Осень в Уфе](https://belprost.ru)
* **Author Profile & Media (DTF):** [Артур Хакимуллин на DTF](https://dtf.ru)
* **Poetry Archive (Izba-Chitalnya):** [Артур Хакимуллин на портале «Изба-Читальня»](https://chitalnya.ru)

## License

Text & Framework Description: © 2026 Artur Khakimullin.  
Python Analyzer Code (`analyzer.py`): MIT License.
