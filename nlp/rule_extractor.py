import re
import json
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False
from quantulum3 import parser as quant_parser
from pint import UnitRegistry
ureg = UnitRegistry()

def normalize_unit(quantity, unit):
    try:
        q = ureg(f"{quantity} {unit}")
        if q.check('[volume]'):
            return float(q.to('milliliter').magnitude), 'ml'
        elif q.check('[mass]'):
            return float(q.to('gram').magnitude), 'g'
        else:
            return float(quantity), unit
    except Exception:
        return float(quantity), unit

def extract_quantities(text):
    quantities = quant_parser.parse(text)
    norm_quantities = []
    for q in quantities:
        value, unit = normalize_unit(q.value, q.unit.name)
        norm_quantities.append({'value': value, 'unit': unit, 'surface': q.surface})
    return norm_quantities

def extract_if_then_rules_spacy(text):
    # Use spaCy to extract IF-THEN rules (conditional sentences)
    doc = nlp(text)
    rules = []
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if sent_text.lower().startswith('if '):
            # Try to split into condition and action
            if ',' in sent_text:
                parts = sent_text[3:].split(',', 1)
                condition = parts[0].strip()
                action = parts[1].strip()
                rules.append({'if': condition, 'then': action})
    return rules

def extract_entities_spacy(text):
    doc = nlp(text)
    ingredients = set()
    actions = set()
    for token in doc:
        if token.pos_ == 'NOUN' and not token.is_stop:
            ingredients.add(token.lemma_)
        if token.pos_ == 'VERB' and not token.is_stop:
            actions.add(token.lemma_)
    norm_quantities = extract_quantities(text)
    return list(ingredients), list(actions), norm_quantities

def extract_if_then_rules_regex(text):
    rules = []
    pattern = re.compile(r'If ([^.,!?]+)[,\-] (.+?)(?:[.!?]|$)', re.IGNORECASE)
    for match in pattern.finditer(text):
        condition = match.group(1).strip()
        action = match.group(2).strip()
        rules.append({"if": condition, "then": action})
    return rules

def extract_steps(text):
    """
    Extracts main steps (non-IF-THEN) from a block of text.
    Returns a list of steps.
    """
    steps = []
    for line in text.split('.'):
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith('if '):
            continue
        steps.append(line)
    return steps

def process_recipes(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    recipes = [r.strip() for r in content.split('\n\n') if r.strip()]
    structured = []
    for recipe in recipes:
        lines = recipe.split('\n')
        title = lines[0].strip()
        body = ' '.join(lines[1:]).strip()
        if SPACY_AVAILABLE:
            rules = extract_if_then_rules_spacy(body)
            ingredients, actions, norm_quantities = extract_entities_spacy(body)
        else:
            rules = extract_if_then_rules_regex(body)
            ingredients, actions = [], []
            norm_quantities = extract_quantities(body)
        steps = extract_steps(body)
        structured.append({
            "title": title,
            "steps": steps,
            "if_then_rules": rules,
            "ingredients": ingredients,
            "actions": actions,
            "quantities": norm_quantities
        })
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(structured, f, indent=2)
    print(f"Structured recipes written to {output_path}")

if __name__ == "__main__":
    import os
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    CLEANED_PATH = os.path.join(DATA_DIR, 'cleaned_recipes.txt')
    STRUCTURED_PATH = os.path.join(DATA_DIR, 'structured_recipes.json')
    process_recipes(CLEANED_PATH, STRUCTURED_PATH) 