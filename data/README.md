# Data

- `jlpt_n5_n2_grammar.csv`: grammar patterns, meanings, and example sentences are original content
  written for this project, with no external source.
Load it with:

```
python manage.py import_cards data/jlpt_n5_n2_grammar.csv
```

`jlpt_n5_n2_vocab.csv` is the vocabulary used by the app (N5 to N2, about 4,900 words).
Load it with:

```
python manage.py import_cards data/jlpt_n5_n2_vocab.csv
```

## Sources and licences

- **Word lists and JLPT levels:** Jonathan Waller, [tanos.co.uk/jlpt](https://www.tanos.co.uk/jlpt/),
  licensed [CC BY](https://creativecommons.org/licenses/by/4.0/). Plain-text conversions by
  [Bluskyo/JLPT_Vocabulary](https://github.com/Bluskyo/JLPT_Vocabulary).
- **English meanings:** [JMdict](https://www.edrdg.org/jmdict/j_jmdict.html), the property of the
  [Electronic Dictionary Research and Development Group](https://www.edrdg.org/), used in conformance
  with the [EDRDG licence](https://www.edrdg.org/edrdg/licence.html)
  (CC BY-SA 4.0). Meanings were matched automatically (word + reading) and shortened to the first
  usable sense.

The CSV is a derived dataset and is shared under **CC BY-SA 4.0** with the credits above.
The application code is licensed separately (see the repository `LICENSE`).

## Notes

- The JLPT has never published an official vocabulary list. These levels are a community
  reconstruction from past exams, so treat them as a guide.
- A few entries from the source PDFs were cut off mid-word and could not be matched; they were skipped.
- Meanings are the primary dictionary sense and can be incomplete for words with several uses.

