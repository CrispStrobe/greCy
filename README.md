# greCy: Ancient Greek models for spaCy (forked)

This is a fork of [Jacobo/greCy](https://github.com/Jacobo/greCy), which provides Ancient Greek models for spaCy.

The installer in the original `grecy` package is broken. This fork provides fixed models, a robust installation script, and a [live Gradio demo](https://www.google.com/search?q=%23-live-demo).

-----

## 🚀 Live Demo

You can test the `grc_proiel_trf` and other models live on our Hugging Face Space:

**[https://huggingface.co/spaces/cstr/spacy\_de](https://huggingface.co/spaces/cstr/spacy_de)**

### 🎯 API Client Demo (Dart)

This repository also includes `test_spacy_api.dart`, a Dart script for testing the live demo's public API. It serves as a complete, commented example for consuming a streaming Gradio API from a non-Python environment.

**The script demonstrates how to:**

  * Call a Gradio streaming API (the 2-step `POST` for an `event_id` and `GET` for the stream).
  * Parse the Server-Sent Events (SSE) as they arrive.
  * Interpret the final JSON and HTML results.
  * Parse the HTML to extract NER entities and check the status of visualizations.
  * Display all analysis in a clean, user-friendly table directly in your console.

#### Prerequisites

1.  **Install the Dart SDK** on your system.

2.  Add the `http` package to your `pubspec.yaml` (you may need to create this file if you're not in a full Dart project):

    ```yaml
    name: grecy_api_test

    environment:
      sdk: '>=3.0.0 <4.0.0'

    dependencies:
      http: ^1.2.1 # Or any recent version
    ```

3.  Run `dart pub get` to install the dependency.

#### Usage

**1. Run the Test:**
This command will run all 6 tests and print a clean, formatted summary to your console.

```bash
dart ./test_spacy_api.dart
```

**Example Console Output:**

```text
🚀 STARTING TEST (test_1_en): Model=en, Text="Apple is looking..."
----------------------------------------------------------------------
✅ STEP 1 (POST) successful. Event ID: ...
Waiting for stream...
✅ STEP 2 (Stream "complete") successful.

--- 📊 MORPHOLOGICAL & SYNTACTIC ANALYSIS ---
+---------+---------+-------+-----+----------------------------------+------------+
| Word    | Lemma   | POS   | Tag | Morphology                       | Dependency |
+=========+=========+=======+=====+==================================+============+
| Apple   | Apple   | PROPN | NNP | Number=Sing                      | nsubj      |
| is      | be      | AUX   | VBZ | Mood=Ind|Number=Sing|Person=3...| aux        |
...
+---------+---------+-------+-----+----------------------------------+------------+

--- 🌳 DEPENDENCY PARSE VISUALIZATION ---
  ✅ Dependency Parse SVG generated. (Pass --save-visuals to save file)

--- 🏷️ NAMED ENTITY RECOGNITION (NER) ---
  ✨ Entities Found:
    • Apple                (ORG)
    • U.K.                 (GPE)
    • $1 billion           (MONEY)
======================================================================
```

**2. Save Visualizations (Optional):**
To save the visual dependency parses (as `.svg`) and NER charts (as `.html`), use the `--save-visuals` flag.

```bash
dart ./test_spacy_api.dart --save-visuals
```

This will create an `api_results` directory and save the files there for you to open in a browser.

-----

## Installation (Recommended Method)

This fork provides pre-packaged wheel (`.whl`) files for all models in a [GitHub Release](https://github.com/CrispStrobe/greCy/releases/tag/v1.0-models). This method allows you to install directly from a URL and **prevents dependency conflicts** caused by outdated packages.

### Step 1: Install Modern Libraries

First, install your main, modern libraries. All transformer (`_trf`) models require `spacy-transformers`.

```bash
pip install spacy>=3.7
pip install spacy-transformers>=1.1.0
````

### Step 2: Install greCy Models

Add the models you need to your `requirements.txt` file or `pip install` them from the command line.

**You can add the `--no-deps` flag.** This tells `pip` to install *only* the model files and to **not** install its old, broken dependencies (like `transformers 4.25.1`), which else might break your environment.

**Example `requirements.txt`:**

```txt
# 1. Install modern libraries
spacy>=3.7
spacy-transformers>=1.1.0

# 2. Install greCy models, ignoring their dependencies
#    Note: The filenames use underscores (e.g., grc_perseus_trf) to be valid.
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_trf-3.7.5-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_trf-3.7.5-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_trf-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_trf-0.0.0-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_ner_trf-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_ner_trf-0.0.0-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_lg-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_lg-0.0.0-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_lg-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_lg-0.0.0-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_sm-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_sm-0.0.0-py3-none-any.whl) --no-deps
[https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_sm-0.0.0-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_perseus_sm-0.0.0-py3-none-any.whl) --no-deps
```

**Or, to install a single model from the command line:**

```bash
pip install [https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_trf-3.7.5-py3-none-any.whl](https://github.com/CrispStrobe/greCy/releases/download/v1.0-models/grc_proiel_trf-3.7.5-py3-none-any.whl) --no-deps
```

-----

## Usage

Once installed, you can use the models in any Python script.

```python
import spacy

# Load the model you installed (using an underscore)
nlp = spacy.load("grc_proiel_trf")

text = "καὶ πρὶν μὲν ἐν κακοῖσι κειμένην ὅμως ἐλπίς μʼ ἀεὶ προσῆγε σωθέντος τέκνου ἀλκήν τινʼ εὑρεῖN κἀπικούρησιν δόμον"

doc = nlp(text)

print(f"{'Text':<12} | {'Lemma':<12} | {'POS':<7}")
print("-" * 35)
for token in doc:
    print(f'{token.text:<12} | {token.lemma_:<12} | {token.pos_:<7}')
```

-----

## Developer: Manual Installation (from this repo)

This is an alternative method if you want to build the wheels from scratch.

### 1\. Create a Clean Virtual Environment

```bash
# We use conda-forge for current packages
conda create -n grecy_env -c conda-forge python=3.11
conda activate grecy_env
```

### 2\. Install Base Packages

```bash
pip install spacy grecy spacy-transformers
```

### 3\. Download and Install the Model

Use the `install_model.py` script provided in this repository.

```bash
# This script will download the model, cache it, and install it
python install_model.py grc_proiel_trf
```

**Available models to install:**

  * `grc_proiel_trf` (Recommended)
  * `grc_perseus_trf`
  * `grc_ner_trf`
  * `grc_proiel_lg`
  * `grc_perseus_lg`
  * `grc_proiel_sm`
  * `grc_perseus_sm`

### 4\. Validate Your Installation

Use the `test_spacy_modular.py` script (also in this repo) to run a capability test.

```bash
python test_spacy_modular.py grc_proiel_trf
```

-----


## Original repo readme info

greCy is a set of spaCy ancient Greek models and its installer. The models were trained using the [Perseus](https://universaldependencies.org/treebanks/grc_perseus/index.html) and  [Proiel UD](https://universaldependencies.org/treebanks/grc_proiel/index.html) corpora. Prior to installation, the models can be tested on my [Ancient Greek Syntax Analyzer](https://huggingface.co/spaces/Jacobo/syntax) on the [Hugging Face Hub](https://huggingface.co/), where you can also check the various performance metrics of each model.

In general, models trained with the Proiel corpus perform better in POS Tagging and Dependency Parsing, while Perseus models are better at sentence segmentation using punctuation, and Morphological Analysis. Lemmatization is similar across models because they share the same neural lemmatizer in two variants: the most accurate lemmatizer was trained with word vectors, and the other was not. The best models for lemmatization are the large models . 

### Installation

First install the python package as usual:

``` bash
pip install -U grecy
```

Once the package is successfully installed, you can proceed to dowload and install any of the followings models:

* grc_perseus_sm
* grc_proiel_sm
* grc_perseus_lg
* grc_proiel_lg
* grc_perseus_trf
* grc_proiel_trf


The models can be installed from the terminal (...) 
where you replace MODEL by any of the model names listed above.  The suffixes after the corpus name, _sm, _lg, and _trf, indicate the size of the model which directly depends on the word embedding used for training. The smallest models end in _sm (small) and are the less accurate ones: they are good for testing and building lightweight apps. The _lg and _trf are the large and transformers models which are more accurate. The _lg were trained using fasttext word vectors in the spaCy floret version, and the _trf models were trained using a special version of BERT, pertained by ourselves with the largest available Ancient Greek corpus, namely, the TLG.  The vectors for large models were also trained with the TLG corpus.


### Loading

As usual, you can load any of the four models with the following Python lines:

```
import spacy
nlp = spacy.load("grc_proiel_XX")
```
Remember to replace  _XX  with the size of the model you would like to use, this means, _sm for small, _lg for large, and _trf for transformer. The _trf model is the most accurate but also the slowest.

### Use

spaCy is a powerful NLP library with many application. The most basic of its function is the morpho-syntantic annotation of texts for further processing. A common routine is to load a model, create a doc object, and process a text:

```
import spacy
nlp = spacy.load("grc_proiel_sm")

text = "καὶ πρὶν μὲν ἐν κακοῖσι κειμένην ὅμως ἐλπίς μʼ ἀεὶ προσῆγε σωθέντος τέκνου ἀλκήν τινʼ εὑρεῖν κἀπικούρησιν δόμον"

doc = nlp(text)

for token in doc:
    print(f'{token.text}, lemma: {token.lemma_} pos:{token.pos_}')
    
```

#### The apostrophe issue

Unfortunaly, there is no consensus among the different internet projects that offer ancient Greek texts about how to represent the Ancient Greek apostrophe. Modern Greek simply uses the regular apostrophe, but ancient texts available in Perseus and Perseus under Philologic use various unicode characters for the apostrophe. Instead of the apostrophe, we find the Greek koronis, modifier letter apostrophe, and right single quotation mark. Provisionally, I have opted to use modifier letter apostrophe in the corpus  with which I trained the models. This means, that if you want the greCy models to properly handle the apostrophe you have to make sure that the Ancient Greek texts that you are processing use the modifier letter apostrophe **ʼ** (U+02BC ). Otherwise the models will fail to lemmatize and tag some words in your texts that ends with an 'apostrophe'.

### Building

I offer here the project file, I use to train the models in case you want to customize your models for your specific needs. The six standard spaCy models (small, large, and transformer) are built and packaged using the following commands:


1. python -m spacy project assets
2. python -m spacy project run all

### Performance

For a general comparison, I share here the metrics of the Proiel transformer grc_proiel_trf and grc_perseys_trf.  These models use for fine-tuning a transformer that was specifically trained to be used with spaCy and, consequently, makes the model much smaller than the alternatives offered by Python nlp libraries such as Stanza and Trankit (for more information on the transformer model and how it was trained see [aristoBERTo](https://huggingface.co/Jacobo/aristoBERTo)).  The greCy's _trf models outperform Stanza and Trankit in most metrics and have the advantage that their size is only ~430 MB vs.  the 1.2 GB of the Trankit model trained with XLM Roberta.  See table  below:

#### Proiel

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 71.74 | 98.45 | 98.53 | 94.18 | 96.59 | 85.79 | 82.30 |
| Trankit | 99.91 	| 67.60     |97.86 	| 97.93 |93.03 	  | 97.50 |85.63 	|82.31  |
| Stanza  | 100	    | 51.65	    | 97.38	| 97.75	| 92.09	  | 97.42	| 80.34 |76.33  |

#### Perseus

| Library | Tokens	| Sentences	| UPOS	| XPOS	| UFeats	|Lemmas	|UAS	  |LAS	  |
|  ---    | ---     | ---       | ---   | ---   | ---     | ---   | ---   | ---   |
| spaCy   | 100     | 99.38     | 96.75 | 96.82 | 95.16 | 97.33 | 81.92 | 77.26 |
| Trankit | 99.71 | 98.70 |93.97 	| 87.25 |91.66 	  | 88.52  |83.48 	|78.56  |
| Stanza  | 99.8	 | 98.85	| 92.54	| 85.22	| 91.06	| 88.26	| 78.75 |73.35  |
| OdyCy | -	| 84.09	| 97.32	| 94.18	| 94.09	| 93.89	| 81.40 |76.42 |

### Caveat 

Metrics, however, can be misleading. This becomes particularly obvious when you work with texts that are not part of the training and evaluation dataset. In addition, greCy's lemmatizers (in all sizes) exhibit lower benchmarks in comparison to the above mentioned nlp libraries, but they have a substantially larger vocabulary than the Stanza and Trankit models because they were trained with a complemental lemma corpus derived from Giussepe G.A. Celano [lemmatized corpus](https://github.com/gcelano/LemmatizedAncientGreekXML). This means that the greCy's lemmatizers perform better than Trankit and Stanza when processing texts not included in the Perseus and Proiel datasets. 

### Future Developments

This project was initiated as part of the [Diogenet Project](https://diogenet.ucsd.edu/), a research initiative that focuses on the automatic extraction of social relations from Ancient Greek texts. As part of this project, greCy will add first, in a non distant future,  a NER pipeline for the identification of entities; later I hope also to offer pipeline for the extraction of social relation from Greek texts. This pipeline should contribute to the study of social networks in the ancient world. 

