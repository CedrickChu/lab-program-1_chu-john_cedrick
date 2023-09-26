# still Work in Progress
import re
import csv
import pandas as pd


class PorterStemmer:

    # A consonant will be denoted as c
    @staticmethod
    def _c():
        return '[^aeiou]'
    #A Vowel will be donoted as v
    @staticmethod
    def _v():
        return '[aeiouy]'

    #consecutive c will be denoted as C
    @staticmethod
    def _C():
        return f'{PorterStemmer._c()}[^aeiouy]*'

    #consecutive v will be denoted as V
    @staticmethod
    def _V():
        return f'{PorterStemmer._v()}[aeiou]*'


    @staticmethod
    def _VC():
        return f'{PorterStemmer._v()}{PorterStemmer._c()}'


    @staticmethod
    def _mgr0():
        return f'^({PorterStemmer._C()})*({PorterStemmer._VC()})*{PorterStemmer._V()}'

    @staticmethod
    def _meq1():
        return f'^({PorterStemmer._C()})*({PorterStemmer._VC()})*({PorterStemmer._VC()})*{PorterStemmer._V()}?'

    @staticmethod
    def _mgr1():
        return f'^({PorterStemmer._C()})*({PorterStemmer._VC()})*{PorterStemmer._V()}({PorterStemmer._VC()})*{PorterStemmer._V()}'

    @staticmethod
    def _hv(word):
        if re.search(PorterStemmer._V(), word):
            return "1"
        return "0"
    
    @staticmethod
    def _normalize(w):
        first = w[0]
        if first == 'y':
            w = first.upper() + w[1:]
        return w.lower().replace('[^a-zA-Z]+', '')

    @staticmethod
    def _doStep1a(w):
        # Define regular expressions for the Step 1a rules
        re1 = re.compile('^(.+?)(ss|i)es$')
        re2 = re.compile('^(.+?)([^s])s$')

        if re1.match(w):
            w = re1.sub(r'\1\2', w)
        elif re2.match(w):
            w = re2.sub(r'\1\2', w)

        return w




    @staticmethod
    def _doStep1b(w):
        re1 = re.compile('^(.+?)eed$')
        re2 = re.compile('^(.+?)(ed|ing)$')
        if re1.match(w):
            fp = re1.match(w)
            re1 = re.compile(PorterStemmer._mgr0())
            if re1.match(fp[1]):
                re1 = re.compile('.$')
                w = re1.sub('', w)
        elif re2.match(w):
            fp = re2.match(w)
            stem = fp[1]
            re2 = re.compile(PorterStemmer._hv(stem))
            if re2.match(stem):
                w = stem
                re2 = re.compile('(at|bl|iz)$')
                re3 = re.compile('([^aeiouylsz])\\1$')
                re4 = re.compile(f'^{PorterStemmer._C()}{PorterStemmer._v()}[^aeiouwxy]$')
                if re2.match(w):
                    w += 'e'
                elif re3.match(w):
                    re3 = re.compile('.$')
                    w = re3.sub('', w)
                elif re4.match(w):
                    w += 'e'
        return w

    @staticmethod
    def _doStep1c(w):
        re1 = re.compile(f'^(.*{PorterStemmer._v()}.*)y$')
        if re1.match(w):
            fp = re1.match(w)
            stem = fp[1]
            w = stem + 'i'
        return w

    @staticmethod
    def _step2():
        return {
            'ational': 'ate',
            'tional': 'tion',
            'enci': 'ence',
            'anci': 'ance',
            'izer': 'ize',
            'bli': 'ble',
            'alli': 'al',
            'entli': 'ent',
            'eli': 'e',
            'ousli': 'ous',
            'ization': 'ize',
            'ation': 'ate',
            'ator': 'ate',
            'alism': 'al',
            'iveness': 'ive',
            'fulness': 'ful',
            'ousness': 'ous',
            'aliti': 'al',
            'iviti': 'ive',
            'biliti': 'ble',
            'logi': 'log'
        }

    @staticmethod
    def _step3():
        return {
            'icate': 'ic',
            'ative': '',
            'alize': 'al',
            'iciti': 'ic',
            'ical': 'ic',
            'ful': '',
            'ness': ''
        }
  

    @staticmethod
    def _doStep2(w):
        re1 = re.compile('^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$')
        if re1.match(w):
            fp = re1.match(w)
            stem = fp[1]
            suffix = fp[2]
            re1 = re.compile(PorterStemmer._mgr0())
            if re1.match(stem):
                w = stem + PorterStemmer._step2()[suffix]
        return w

    @staticmethod
    def _doStep3(w):
        re1 = re.compile('^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$')
        if re1.match(w):
            fp = re1.match(w)
            stem = fp[1]
            suffix = fp[2]
            re1 = re.compile(PorterStemmer._mgr0())
            if re1.match(stem):
                w = stem + PorterStemmer._step3()[suffix]
        return w

    @staticmethod
    def _doStep4(w):
        re1 = re.compile('^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$')
        re2 = re.compile('^(.+?)(s|t)(ion)$')
        if re1.match(w):
            fp = re1.match(w)
            stem = fp[1]
            re1 = re.compile(PorterStemmer._mgr1())
            if re1.match(stem):
                w = stem
        elif re2.match(w):
            fp = re2.match(w)
            stem = fp[1] + fp[2]
            re2 = re.compile(PorterStemmer._mgr1())
            if re2.match(stem):
                w = stem
        return w

    @staticmethod
    def _doStep5(w):
        re1 = re.compile('^(.+?)e$')
        if re1.match(w):
            fp = re1.match(w)
            stem = fp[1]
            re1 = re.compile(PorterStemmer._mgr1())
            re2 = re.compile(PorterStemmer._meq1())
            re3 = re.compile(f'^{PorterStemmer._C()}{PorterStemmer._v()}[^aeiouwxy]$')
            if re1.match(stem) or (re2.match(stem) and not re3.match(stem)):
                w = stem
        re1 = re.compile('ll$')
        re2 = re.compile(PorterStemmer._mgr1())
        if re1.match(w) and re2.match(w):
            re1 = re.compile('.$')
            w = re1.sub('', w)
        return w

    @staticmethod
    def stem(w):
        if len(w) < 3:
            return w

        steps = [
            PorterStemmer._normalize,
            PorterStemmer._doStep1a,
            PorterStemmer._doStep1b,
            PorterStemmer._doStep1c,
            PorterStemmer._doStep2,
            PorterStemmer._doStep3,
            PorterStemmer._doStep4,
            PorterStemmer._doStep5
        ]

        for step in steps:
            w = step(w)

        return w

porter = PorterStemmer()

# Create a set of stopwords
stopwords = set()

# Open the stopwords file with UTF-8 encoding
with open("stopwords.txt", "r", encoding="utf-8") as stopword_file:
    stopwords.update(line.strip() for line in stopword_file)

# Create an empty list to store the filtered tokens
filtered_tokens = []

# Open the CSV file with UTF-8 encoding
with open('4-cols_15k-rows.csv - 4-cols_15k-rows.csv.csv', 'r', encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        for cell in row:
            # Tokenize the text by splitting on spaces and removing punctuation
            cell_tokens = re.findall(r'\b\w+\b', cell.lower())
            
            # Filter out stopwords
            filtered_cell_tokens = [token for token in cell_tokens if token not in stopwords]
            
            filtered_tokens.extend(filtered_cell_tokens)

# Perform stemming on filtered tokens
stemmed_tokens = [porter.stem(token) for token in filtered_tokens]

# Convert the stemmed tokens back to a string
stemmed_text = ' '.join(stemmed_tokens)

# Create a DataFrame to store the stemmed data
processed_df = pd.DataFrame({'': [stemmed_text]})

# Specify the path for the output CSV file
output_file_path = 'stemmed-dataset_15k-rows_chu-john_cedrick.csv'

try:
    # Write the stemmed data to the output CSV file with UTF-8 encoding
    processed_df.to_csv(output_file_path, index=False, encoding='utf-8')
    print(f"Stemmed data has been written to {output_file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
