from doctest import OutputChecker
import re
import csv
import pandas as pd
from multiprocessing import Pool
import sys



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
    
    #*o - the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    @staticmethod
    def _apply_cvc_rule(w):
        if len(w) >= 3:
            cvc = re.search(f'.*{PorterStemmer._C()}{PorterStemmer._V()}{PorterStemmer._C()}$', w)
            if cvc:
                if w[-1] != 'w' or w[-1] != 'x' or w[-1] != 'y':
                    return True
                else:
                    return False
        else:
            return False
  
    #*d - the stem ends with a double consonant (e.g. -TT, -SS).
    @staticmethod
    def _apply_d_rule(w):
        if len(w) >= 2:
            return w[-2:] == w[-1:]
        else:
            return False

    def has_vowel(w):
        if re.search(r'[aeiouy]', w[:-3]):
            return True
        return False
        
    #m is the number of consecutive _VC in the word
    @staticmethod
    def _calculate_m(w):
        pattern = re.compile(f'{PorterStemmer._V()}{PorterStemmer._C()}')
        vc_pairs = pattern.findall(w)
        return len(vc_pairs)
    
    # getting rid of -sses -ies or -ss. -s.
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


    
    # getting rid of -eed. -ed. -ing. etc.
    # getting rid of -eed. -ed. -ing. etc.
    @staticmethod
    def _doStep1b(w):
        m = PorterStemmer._calculate_m(w)
        step1b2ed = False
        step1b2ing = False
        if re.match('.*eed$', w) and m > 0:
            return re.sub('eed$', 'ee', w)
        elif PorterStemmer.has_vowel(w) and re.match('.*ed$', w):
            w = re.sub('ed$', '', w)
            step1b2ed = True
            
        elif PorterStemmer.has_vowel(w) and re.match('.*ing$', w):
            w = re.sub('ing$', '', w)
            step1b2ing = True
            
        if step1b2ed and step1b2ing:
            if re.match('.*at$', w):
                return re.sub('at', 'ate', w)
            elif re.match('.*bl$', w):
                return re.sub('bl', 'ble', w)
            elif re.match('.*iz$', w):
                return re.sub('iz', 'ize', w)
            elif re.match('.*s$', w):
                return re.sub('s', '', w)
            #(*d and not (*L or *S or *Z)) -> single letter (Example : hopp(ing) -> hop ; tann(ed) -> tan ; fall(ing) -> fall ; hiss(ing) -> hiss ; fizz(ed) -> fizz)
            elif PorterStemmer._apply_d_rule(w) and w[-1] not in ('L', 'S', 'Z'): 
                return w[:-1]
            elif m == 1 and PorterStemmer._apply_cvc_rule(w):
                return w
            else:
                return w
        return w

    
    #getting rid of -y. and change it to i
    @staticmethod
    def _doStep1c(w):
        if PorterStemmer.has_vowel(w) and re.match('.*y$', w):
            return re.sub('y$', 'i', w)
        else:
            return w
        
    #getting rid of other suffixes
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
        elif m > 0 and re.match('.*alli$', w):
            return re.sub('alli$', 'al', w)
        elif m > 0 and re.match('.*entli$', w):
            return re.sub('entli$', 'ent', w)
        elif m > 0 and re.match('.*eli$', w):
            return re.sub('eli$', 'e', w)
        elif m > 0 and re.match('.*ousli$', w):
            return re.sub('ousli$', 'ous', w)
        elif m > 0 and re.match('.*ization$', w):
            return re.sub('ization$', 'ize', w)
        elif m > 0 and re.match('.*ation$', w):
            return re.sub('ation$', 'ate', w)
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
        
    #getting rid of more suffixes
    @staticmethod
    def _doStep3(w):
        m = PorterStemmer._calculate_m(w)
        if m > 0 and re.match('.*icate$', w):
            return re.sub('icate$', 'ic', w)
        elif m > 0 and re.match('.*ative$', w):
           return re.sub('ative$', '', w)
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
    
    #getting rid of more suffixes
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
        #(m>1 and (*S or *T)) ION -> (Example : adoption -> adopt; repulsion -> repuls)
        elif m > 1 and re.match('.*sion$', w):
            return re.sub('sion$', 's', w)
        elif m > 1 and re.match('.*tion$', w):
            return re.sub('tion$', 't', w)
  
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
    
    #(m>1) E -> (Example : trade -> trad; name -> name)
    #(m=1 and not *o) E -> (Example : cease -> ceas) where *o is word that ends with cvc
    @staticmethod
    def _doStep5a(w):
        m = PorterStemmer._calculate_m(w)
        if m > 1 and re.match('.*e$', w):
            return re.sub('e$', '', w)
        elif m == 1 and re.match('.*e$', w) and not PorterStemmer._apply_cvc_rule(w):
            return w
        else:
            pass
        return w


    #removing final suffixes
    @staticmethod
    def _doStep5b(w):
        m = PorterStemmer._calculate_m(w)
        if m > 1 and re.match('.*dd$', w):
            return re.sub('dd$', 'd', w)
        elif m > 1 and re.match('.*ll$', w):
            return re.sub('ll$', 'l', w)
        return w

    #steps to stem
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
#stopwords = set()

# Open the stopwords file with UTF-8 encoding
#ith open("stopwords.txt", "r", encoding="utf-8") as stopword_file:
    #stopwords.update(line.strip() for line in stopword_file)

def stem_cell(cell):
    cell_tokens = re.findall(r'\b\w+\b|[\'.,?"<>-]', cell.lower())
    stemmed_tokens = [porter.stem(token) for token in cell_tokens]
    return ' '.join(stemmed_tokens)

def process_row(row):
    stemmed_row = [stem_cell(cell) for cell in row]
    return stemmed_row

def main():
    try:
        with open('4-cols_15k-rows.csv - 4-cols_15k-rows.csv.csv', 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
   

            # Create an empty list to store the stemmed paragraphs
            stemmed_paragraphs = []


            # Create a Pool of worker processes for parallel processing
            with Pool() as pool:
                for stemmed_row in pool.imap(process_row, csv_reader):
                    stemmed_paragraphs.append(stemmed_row)


            # Create a DataFrame with the stemmed paragraphs
            processed_df = pd.DataFrame(stemmed_paragraphs, columns=['instruction', 'context', 'response', 'category'])

            # Specify the path for the output CSV file
            output_file_path = 'stemmed-dataset_15k-rows_chu-john_cedrick.csv'

            processed_df.to_csv(output_file_path, index=False, encoding='utf-8')
            print(f"Stemmed data has been written to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()