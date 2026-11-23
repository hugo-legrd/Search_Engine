# Search_Engine

Search Engine in Python - Find TED Talks relevant to the keywords entered.

Results are ranked with a TF-IDF score computed on the talk transcripts, and displayed in a small Tkinter interface. Click a result to open the talk in your browser.

## Requirements

- Python 3 (Tkinter included)
- `TED_transcripts.csv` and `ted_main.csv` from the [TED Talks dataset on Kaggle](https://www.kaggle.com/datasets/rounakbanik/ted-talks), placed next to the script

## Usage

```bash
python FinalGUI.py
```

Type your keywords, then press Enter or click **Search**.
