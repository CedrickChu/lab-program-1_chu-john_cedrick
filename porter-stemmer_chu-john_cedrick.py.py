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
        return f'{PorterStemmer._c()}+'

    #consecutive v will be denoted as V
    @staticmethod
    def _V():
        return f'{PorterStemmer._v()}+'

    #m is the number of consecutive _VC in the word
    @staticmethod
    def _calculate_m(w):
        pattern = re.compile(f'{PorterStemmer._V()}{PorterStemmer._C()}')
        vc_pairs = pattern.findall(w)
        return len(vc_pairs)
    
    #Step1 - checking if word has match ending then change it.
    @staticmethod
    def _doStep1a(w):
        if re.match('.*sses$', w):
            return re.sub('sses$', 'ss', w)
        elif re.match('.*ies$', w):
            return re.sub('ies$', 'i', w)
        elif re.match('.*ss$', w):
            return re.sub('ss$', 'ss', w)
        elif re.match('.*s$', w):
            return re.sub('s$', '', w)
        else:
            pass
        return w

    @staticmethod
    def _doStep1b(w):
        m = PorterStemmer._calculate_m(w)
        if re.match('.*eed$', w) and m > 0:
            return re.sub('eed$', 'ee', w)
        elif re.match(f'.*{PorterStemmer._v()}*ed$', w) and m > 0:
            return re.sub('ed$', '', w)
        elif re.match(f'.*{PorterStemmer._v()}*ing$', w) and m > 0:
            return re.sub('ing$', '', w)
        elif re.match(f'.*{PorterStemmer._v()}*s$', w) and m > 0:
            return re.sub('s$', '', w)
        else:
            pass
        return w

    @staticmethod
    def _doStep1c(w):
        if re.match(f'.*{PorterStemmer._v()}y$', w):
            return re.sub('y$', 'i', w)
        return w
        
    @staticmethod
    def _doStep2(w):
        m = PorterStemmer._calculate_m(w)
        if m > 0 and re.match('.*ational$', w):
            return re.sub('ational$', 'ate', w)
        elif m > 0 and re.match('.*tional$', w):
            return re.sub('tional$', 'tion', w)
        elif m > 0 and re.match('.*enci$', w):
            return re.sub('enci$', 'ence', w)
        elif m > 0 and re.match('.*anci$', w):
            return re.sub('anci$', 'ance', w)
        elif m > 0 and re.match('.*izer$', w):
            return re.sub('izer$', 'ize', w)
        elif m > 0 and re.match('.*abli$', w):
            return re.sub('abli$', 'able', w)
        elif m > 0 and re.match('.*ali$', w):
            return re.sub('ali$', 'al', w)
        elif m > 0 and re.match('.*entli$', w):
            return re.sub('entli$', 'ent', w)
        elif m > 0 and re.match('.*eli$', w):
            return re.sub('eli$', 'e', w)
        elif m > 0 and re.match('.*ousli$', w):
            return re.sub('ousli$', 'ous', w)
        elif m > 0 and re.match('.*ization$', w):
            return re.sub('ization$', 'ize', w)
        elif m > 0 and re.match('.*ations$', w):
            return re.sub('ations$', 'ate', w)
        elif m > 0 and re.match('.*ator$', w):
            return re.sub('ator$', 'ate', w)
        elif m > 0 and re.match('.*alism$', w):
            return re.sub('alism$', 'al', w)
        elif m > 0 and re.match('.*iveness$', w):
            return re.sub('iveness$', 'ive', w)
        elif m > 0 and re.match('.*fulness$', w):
            return re.sub('fulness$', 'ful', w)
        elif m > 0 and re.match('.*ousness$', w):
            return re.sub('ousness$', 'ous', w)
        elif m > 0 and re.match('.*aliti$', w):
            return re.sub('aliti$', 'al', w)
        elif m > 0 and re.match('.*iviti$', w):
            return re.sub('iviti$', 'ive', w)
        elif m > 0 and re.match('.*biliti$', w):
            return re.sub('biliti$', 'ble', w)
        return w
        
    @staticmethod
    def _doStep3(w):
        m = PorterStemmer._calculate_m(w)
        if m > 0 and re.match('.*icate$', w):
            return re.sub('icate$', 'ic', w)
        elif m > 0 and re.match('.*ative$', w):
           return re.sub('itive$', '', w)
        elif m > 0 and re.match('.*alize$', w):
            return re.sub('alize$', 'al', w)
        elif m > 0 and re.match('.*iciti$', w):
            return re.sub('iciti$', 'ic', w)
        elif m > 0 and re.match('.*ical$', w):
            return re.sub('ical$', 'ic', w)
        elif m > 0 and re.match('.*ful$', w):
            return re.sub('ful$', '', w)
        elif m > 0 and re.match('.*ness$', w):
            return re.sub('ness$', '', w)
        return w
    
    @staticmethod
    def _doStep4(w):
        m = PorterStemmer._calculate_m(w)
        if m > 1 and re.match('.*al$', w):
            return re.sub('al$', '', w)
        elif m > 1 and re.match('.*ance$', w):
            return re.sub('ance$', '', w)
        elif m > 1 and re.match('.*ence$', w):
            return re.sub('ence$', '', w)
        elif m > 1 and re.match('.*er$', w):
            return re.sub('er$', '', w)
        elif m > 1 and re.match('.*ic$', w):
            return re.sub('ic$', '', w)
        elif m > 1 and re.match('.*able$', w):
            return re.sub('able$', '', w)
        elif m > 1 and re.match('.*ible$', w):
            return re.sub('ible$', '', w)
        elif m > 1 and re.match('.*ant$', w):
            return re.sub('ant$', '', w)
        elif m > 1 and re.match('.*ement$', w):
            return re.sub('ement$', '', w)
        elif m > 1 and re.match('.*ment$', w):
            return re.sub('ment$', '', w)
        elif m > 1 and re.match('.*(sion|tion)$', w):
            return re.sub('(sion|tion)$', '', w)
        elif m > 1 and re.match('.*ou$', w):
            return re.sub('ou$', '', w)
        elif m > 1 and re.match('.*ism$', w):
            return re.sub('ism$', '', w)
        elif m > 1 and re.match('.*ate$', w):
            return re.sub('ate$', '', w)
        elif m > 1 and re.match('.*iti$', w):
            return re.sub('iti$', '', w)
        elif m > 1 and re.match('.*ous$', w):
            return re.sub('ous$', '', w)
        elif m > 1 and re.match('.*ive$', w):
            return re.sub('ive$', '', w)
        elif m > 1 and re.match('.*ize$', w):
            return re.sub('ize$', '', w)
        return w

    @staticmethod
    def _doStep5a(w):
        m = PorterStemmer._calculate_m(w)
        if m > 1 and re.match('.*e$', w) and not re.match('.*o$', w[:-1]):
            return re.sub('e$', '', w)
        else:
            return w
    
    @staticmethod
    def _doStep5b(w):
        m = PorterStemmer._calculate_m(w)
        if m > 1 and re.match('.*dd$', w):
            return re.sub('dd$', 'd', w)
        elif m > 1 and re.match('.*ll$', w):
            return re.sub('ll$', 'l', w)
        return w

    @staticmethod
    def stem(w):
        if len(w) < 3:
            return w

        steps = [
            PorterStemmer._doStep1a,
            PorterStemmer._doStep1b,
            PorterStemmer._doStep1c,
            PorterStemmer._doStep2,
            PorterStemmer._doStep3,
            PorterStemmer._doStep4,
            PorterStemmer._doStep5a,
            PorterStemmer._doStep5b,
        ]
        for step in steps:
            w = step(w)
        return w
    

porter = PorterStemmer()

# Create a set of stopwords
# removing my stopwords.txt to make my output the same as the expected output
stopwords = set()

# Open the stopwords file with UTF-8 encoding
with open("stopwords.txt", "r", encoding="utf-8") as stopword_file:
    stopwords.update(line.strip() for line in stopword_file)

# Create an empty list to store the filtered tokens
filtered_tokens = []

# Open the CSV file with UTF-8 encoding
with open('4-cols_15k-rows.csv - 4-cols_15k-rows.csv.csv', 'r', encoding="utf-8") as file:  # Corrected the filename
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


stemmed_text = ' '.join(stemmed_tokens)

# I removed the first 4 words in the csv file and add it in the DataFrame instead.
processed_df = pd.DataFrame({'instruction,context,response,category': [stemmed_text]})

# Specify the path for the output CSV file
output_file_path = 'stemmed-dataset_15k-rows_chu-john_cedrick.csv'

try:
    processed_df.to_csv(output_file_path, index=False, encoding='utf-8')
    print(f"Stemmed data has been written to {output_file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
