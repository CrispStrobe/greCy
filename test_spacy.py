#!/usr/bin/env python

"""
Runs a comprehensive 10-point capabilities test on an
installed greCy spaCy model.

Version 3: Fixes Test 10 for modern spacy-transformers.
"""

import spacy
import sys

def run_tests():
    MODEL_TO_TEST = "grc_proiel_trf"

    # --- 1. Load Model ---
    print(f"--- 1. Loading Model: {MODEL_TO_TEST} ---")
    try:
        nlp = spacy.load(MODEL_TO_TEST)
        print(f"Model loaded successfully.")
        print(f"Pipeline: {nlp.pipe_names}\n")
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"\nMake sure you have successfully installed the model.", file=sys.stderr)
        print(f"Try running: python ./test_dl.py {MODEL_TO_TEST}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during model loading: {e}", file=sys.stderr)
        print("This may be due to a package conflict. Are you in a clean virtual environment?", file=sys.stderr)
        sys.exit(1)


    # --- 2. Basic Tokenization, Lemma & POS ---
    print("--- 2. Token, Lemma, and POS Tagging ---")
    text = "καὶ πρὶν μὲn ἐν κακοῖσι κειμένην ὅμως ἐλπίς μʼ ἀεὶ προσῆγε σωθέντος τέκνου ἀλκήν τινʼ εὑρεῖν κἀπικούρησιν δόμον"
    doc = nlp(text)
    
    print(f"{'Text':<12} | {'Lemma':<12} | {'POS':<7} | {'Fine-Grained Tag':<15}")
    print("-" * 50)
    for token in doc:
        print(f'{token.text:<12} | {token.lemma_:<12} | {token.pos_:<7} | {token.tag_}')
    
    # --- 3. Morphological Features ---
    print("\n--- 3. Morphological Features (for non-punctuation) ---")
    print(f"{'Text':<12} | {'Morphology':<50}")
    print("-" * 65)
    for token in doc:
        if token.pos_ not in ['PUNCT', 'SPACE']:
            print(f'{token.text:<12} | {token.morph}')

    # --- 4. Syntactic Dependency Parsing ---
    print("\n--- 4. Syntactic Dependency Parsing ---")
    print(f"{'Text':<12} | {'Dependency':<10} | {'Head':<12} | {'Children'}")
    print("-" * 70)
    for token in doc:
        children = [c.text for c in token.children]
        print(f'{token.text:<12} | {token.dep_:<10} | {token.head.text:<12} | {children}')

    # --- 5. Noun Chunks (Phrase Structure) ---
    print("\n--- 5. Noun Chunks (Phrases) ---")
    
    try:
        print(f"{'Chunk Text':<25} | {'Root Word':<10} | {'Root Dependency'}")
        print("-" * 60)
        
        chunks = list(doc.noun_chunks)
        if not chunks:
            print("No noun chunks found in this text.")
        else:
            for chunk in chunks:
                print(f'{chunk.text:<25} | {chunk.root.text:<10} | {chunk.root.dep_}')
    
    except NotImplementedError as e:
        print(f"Skipping test: This model does not support noun chunking.")
        print(f"Error details: {e}")

    # --- 6. Sentence Splitting (SBD) ---
    print("\n--- 6. Sentence Splitting ---")
    text_long = "Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε. ὡς μήτε τὰ γενόμενα ἐξ ἀνθρώπων τῷ χρόνῳ ἐξίτηλα γένηται, μήτε ἔργα μεγάλα τε καὶ θωμαστά, ἀκλεᾶ γένηται."
    doc_long = nlp(text_long)
    for i, sent in enumerate(doc_long.sents):
        print(f'Sentence {i+1}: {sent.text}')

    # --- 7. Token Attributes (Booleans) ---
    print("\n--- 7. Token Attributes (Booleans) ---")
    print(f"{'Text':<12} | {'Is Punct':<8} | {'Is Quote':<8} | {'Is Stop':<8}")
    print("-" * 40)
    for token in doc:
        print(f'{token.text:<12} | {str(token.is_punct):<8} | {str(token.is_quote):<8} | {str(token.is_stop):<8}')

    # --- 8. Named Entity Recognition (NER) ---
    print("\n--- 8. Named Entity Recognition (NER) ---")
    if 'ner' not in nlp.pipe_names:
        print("Skipping test: 'ner' component not found in model pipeline.")
        print(f"Pipeline: {nlp.pipe_names}")
    else:
        ner_doc = nlp("τοῦ δὲ Ἡροδότου ἐν Θουρίοις.")
        if not ner_doc.ents:
            print("No entities found in the text.")
        else:
            print(f"{'Entity Text':<15} | {'Label'}")
            print("-" * 30)
            for ent in ner_doc.ents:
                print(f'{ent.text:<15} | {ent.label_}')

    # --- 9. Word Similarity (Contextual) ---
    print("\n--- 9. Word Similarity (Contextual) ---")
    print("Note: Similarity warnings (W007, W008) are expected.")
    print("This model uses context-tensors, not static vectors,")
    print("so token.similarity() will default to 0.0.")
    token1 = doc[6]  # κειμένην (lying)
    token2 = doc[12] # σωθέντος (saved)
    token3 = doc[13] # τέκνου (child)
    
    try:
        sim1_2 = token1.similarity(token2)
        sim2_3 = token2.similarity(token3)
        print(f"Similarity between '{token1.text}' and '{token2.text}': {sim1_2:.4f}")
        print(f"Similarity between '{token2.text}' and '{token3.text}': {sim2_3:.4f}")
    except ImportError:
        print("Could not run similarity test: 'numpy' package not found.")
    except Exception as e:
        print(f"Could not run similarity test: {e}")

    # --- 10. Accessing Transformer Data ---
    print("\n--- 10. Accessing Transformer Data (trf-model specific) ---")
    if doc.has_extension("trf_data"):
        trf_data = doc._.trf_data
        print(f"Transformer data is present.")
        
        # --- FIX ---
        # The 'TransformerData' object holds outputs in a list.
        # The last hidden state is the first element of that list.
        try:
            hidden_state = trf_data.outputs[0]
            print(f"Shape of last hidden state: {hidden_state.shape}")
            # The pooler output is often the second element
            if len(trf_data.outputs) > 1:
                 pooler_output = trf_data.outputs[1]
                 print(f"Shape of pooler output: {pooler_output.shape}")
        except Exception as e:
            print(f"Could not access transformer output tensors: {e}")
            print(f"Available attributes: {dir(trf_data)}")
        # --- END FIX ---
            
    else:
        print("Skipping test: Transformer data extension ('_.trf_data') not found.")

    print("\n--- All 10 tests complete. ---")

if __name__ == "__main__":
    run_tests()