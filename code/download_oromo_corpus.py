"""
download_oromo_corpus.py
Download and filter only Afaan Oromo texts from EthioLLM corpus
"""

from datasets import load_dataset
import os
import re

def is_afaan_oromo(text, language_field):
    """
    Check if a text is in Afaan Oromo.
    Uses multiple detection methods.
    """
    
    # Method 1: Check language field
    if language_field:
        lang_lower = str(language_field).lower()
        if 'oromo' in lang_lower or 'afaan' in lang_lower:
            return True
    
    # Method 2: Check for common Oromo words
    # Common Oromo words that are unique to the language
    oromo_keywords = [
        'dabalataan', 'bu\'uuraaleen', 'misoomaa', 'qonnaan', 
        'bultoonni', 'omisha', 'salphaa', 'gabaaf', 'dhiyeessan',
        'carraa', 'uumu', 'himan', 'akkas', 'ta\'e', 'isaanii',
        'kanaaf', 'garuu', 'akkuma', 'hanga', 'achitti'
    ]
    
    text_lower = text.lower()
    for keyword in oromo_keywords:
        if keyword in text_lower:
            return True
    
    # Method 3: Check for other language markers
    # If it contains Amharic/Ge'ez characters (Unicode 1200-137F), skip
    amharic_pattern = re.compile(r'[\u1200-\u137F]')
    if amharic_pattern.search(text):
        return False
    
    # If it contains too many English words, skip
    english_words = len(re.findall(r'\b[a-z]{3,}\b', text))
    total_words = len(text.split())
    if total_words > 0 and english_words / total_words > 0.5:
        return False
    
    # Method 4: Check for Afaan Oromo specific characters
    oromo_chars = ['ch', 'dh', 'ny', 'sh', 'ts', 'ph', 'zh']
    text_lower = text.lower()
    oromo_char_count = sum(text_lower.count(char) for char in oromo_chars)
    if oromo_char_count > 0:
        return True
    
    # Default: uncertain, include but mark
    return 'uncertain'

print("=" * 70)
print("FILTERED CORPUS DOWNLOAD - AFAN OROMO ONLY")
print("=" * 70)

# Load the dataset
print("\n📥 Loading EthioLLM corpus...")
print("   This is ~500MB and may take 5-10 minutes to download.")
print("   Please wait...")

try:
    dataset = load_dataset("EthioNLP/ethiollm-corpus", split="train")
    print(f"\n✅ Dataset loaded successfully!")
    print(f"   Total examples in corpus: {len(dataset):,}")
except Exception as e:
    print(f"\n❌ Error loading dataset: {e}")
    print("\nIf this fails, use the manual collection method (Option B).")
    exit(1)

# Create output folder
os.makedirs('corpus/raw/oromo_only', exist_ok=True)

# Filter and save
print("\n🔍 Filtering for Afaan Oromo texts...")
print("   This may take a few minutes.")

saved = 0
skipped = 0
uncertain = 0

for i, example in enumerate(dataset):
    text = example['text']
    language = example.get('language', example.get('lang', ''))
    
    # Check if text is Afaan Oromo
    result = is_afaan_oromo(text, language)
    
    if result == True:
        # Save Oromo text
        if len(text) > 100:  # Skip very short texts
            with open(f'corpus/raw/oromo_only/oromo_{saved:04d}.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            saved += 1
    elif result == 'uncertain':
        # Save but mark as uncertain
        with open(f'corpus/raw/oromo_only/uncertain_{uncertain:04d}.txt', 'w', encoding='utf-8') as f:
            f.write(f"LANGUAGE: {language}\n\n{text}")
        uncertain += 1
    else:
        skipped += 1
    
    # Show progress
    if (i + 1) % 500 == 0:
        print(f"   Processed: {i+1:,} | Oromo: {saved} | Uncertain: {uncertain} | Skipped: {skipped}")

# Summary
print("\n" + "=" * 70)
print("📊 FILTERING COMPLETE")
print("=" * 70)
print(f"   Afaan Oromo texts saved: {saved}")
print(f"   Uncertain texts saved: {uncertain}")
print(f"   Non-Oromo texts skipped: {skipped}")
print(f"   Total processed: {saved + uncertain + skipped:,}")
print(f"\n📁 Files saved to: corpus/raw/oromo_only/")

# Sample verification
if saved > 0:
    print("\n🔍 Sample of first Oromo text:")
    with open('corpus/raw/oromo_only/oromo_0000.txt', 'r', encoding='utf-8') as f:
        sample = f.read()
    print(f"   {sample[:200]}...")

print("\n🎉 Corpus download complete!")
print("\n⚠️ IMPORTANT: Verify the files are actually in Afaan Oromo.")
print("   Open a few files and check the content.")