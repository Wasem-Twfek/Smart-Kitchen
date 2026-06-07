import re

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Standardize units
    text = re.sub(r'kgs?', 'kg', text)
    text = re.sub(r'grams?', 'g', text)
    text = re.sub(r'liters?', 'l', text)
    text = re.sub(r'mls?', 'ml', text)
    # Remove special characters except basic punctuation
    text = re.sub(r'[^a-z0-9,.!?\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == '__main__':
    with open('../data/raw_recipes.txt', 'r', encoding='utf-8') as f:
        raw = f.read()
    cleaned = clean_text(raw)
    with open('../data/cleaned_recipes.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print('Cleaned text written to data/cleaned_recipes.txt') 