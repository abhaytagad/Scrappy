import json
import re
import os

class StoreDataPipeline:
    def open_spider(self, spider):
        # Open the file in append mode to store raw JSON data
        self.file_name = 'hindi_data.json'
        
        # If the file does not exist, create an empty array in JSON format
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump([], f)  # Initialize the file with an empty array
        
        # Open the file in append mode for FastText training data
        self.text_file = open('hindi_data.txt', 'a', encoding='utf-8')

    def close_spider(self, spider):
        # Close the plain text file when spider is done
        self.text_file.close()

    def url_exists(self, url):
        """Check if a given URL exists in the JSON file"""
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    if item.get('url') == url:
                        return True
        except (json.JSONDecodeError, FileNotFoundError):
            return False  # Return False if file is empty or does not exist
        return False

    def process_item(self, item, spider):
        print(f"Processing item: {item}")  # Debugging
        
        # Check if the URL already exists
        if self.url_exists(item.get('url')):
            print(f"Skipping item, URL already exists: {item.get('url')}")
            return item  # Skip processing if URL exists

        # Write raw data to the JSON file if URL does not exist
        try:
            with open(self.file_name, 'r+', encoding='utf-8') as f:
                try:
                    # Load the existing data
                    data = json.load(f)
                except json.JSONDecodeError:
                    # If the file is empty, initialize it as an empty list
                    data = []

                # Append the new item to the list
                data.append(dict(item))

                # Move the file pointer to the beginning and write the updated data
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()  # Ensure no old data remains beyond the new content
        except Exception as e:
            print(f"Error writing to JSON file: {e}")
            return item
        
        # Preprocess the Hindi text and save it to the plain text file
        for sentence in item['hindi_text']:
            preprocessed_text = self.preprocess_hindi_text(sentence)
            if preprocessed_text:  # Only write sentences that meet the criteria (more than 4 words)
                self.text_file.write(preprocessed_text + '\n')
        
        return item

    def preprocess_hindi_text(self, text):
        # Remove unwanted words like 'कॉपी लिंक' and 'शेयर'
        text = re.sub(r'कॉपी लिंक|शेयर', '', text)
        
        # Remove extra spaces or newlines caused by the removal
        text = re.sub(r'\s+', ' ', text).strip()

        # Check if the sentence has more than 4 words
        if len(text.split()) > 4:  # This ensures only sentences with more than 4 words are processed
            return text
        return None  # Return None for sentences that don't meet the criteria
