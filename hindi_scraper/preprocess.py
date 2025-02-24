import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_hindi_text(hindi_text):
    """
    Advanced Preprocessing of the scraped Hindi text:
    - Remove unwanted characters (punctuation, numbers, emojis, URLs, etc.).
    - Remove English words and non-Hindi text.
    - Tokenize the text into words.
    - Remove stopwords.
    - Return cleaned, tokenized text.
    """
    # Step 1: Remove slugs, URLs, and file-like patterns (e.g., anything that looks like a URL or slug)
    hindi_text = re.sub(r'(http\S+|www\S+|slug\S+|[_-]\S+)', '', hindi_text)

    # Step 2: Remove all non-Hindi characters, keeping only Devanagari characters and spaces
    hindi_text_cleaned = re.sub(r'[^\u0900-\u097F\s]', '', hindi_text)

    # Step 3: Remove any English words or alphabets
    hindi_text_cleaned = re.sub(r'[a-zA-Z]', '', hindi_text_cleaned)

    # Step 4: Remove digits or numbers
    hindi_text_cleaned = re.sub(r'\d+', '', hindi_text_cleaned)

    # Step 5: Remove extra spaces (multiple spaces to single space)
    hindi_text_cleaned = re.sub(r'\s+', ' ', hindi_text_cleaned).strip()

    # Step 6: Tokenize the cleaned text into words
    tokens = word_tokenize(hindi_text_cleaned)

    # Step 7: Load Hindi stopwords from NLTK and remove them from the tokenized text
    stop_words = set(stopwords.words('hindi'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Return tokenized and cleaned text as a single string
    return ' '.join(filtered_tokens)

def save_preprocessed_text(hindi_text_list, output_file):
    """
    Save preprocessed text into a plain text file for FastText training or other NLP tasks.
    """
    with open(output_file, 'a', encoding='utf-8') as f:
        for sentence in hindi_text_list:
            preprocessed_text = preprocess_hindi_text(sentence)
            if preprocessed_text.strip():
                f.write(preprocessed_text + '\n')

# Example usage
if __name__ == "__main__":
    hindi_text_list = [
        'यह एक उदाहरण वाक्य है।',
        'This is an English sentence that should be removed.',
        'यह दूसरा उदाहरण है! Thanks for scraping 🧡.',
        'स्क्रैपिंग के लिए धन्यवाद। slug-ak123-filing-details/_summary',
        'अक्सर-कमजोरी-th-with-some-non-hindi-text'
    ]
    
    save_preprocessed_text(hindi_text_list, 'preprocessed_hindi.txt')
    print("Preprocessed text saved to 'preprocessed_hindi.txt'")
