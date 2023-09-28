    @staticmethod
    def _doStep5a(w):
        m = PorterStemmer._calculate_m(w)
        cvc = PorterStemmer._apply_cvc_rule(w)  # Pass 'w' as an argument
        if m > 1 and re.match('.*e$', w):
            return re.sub('e$', '', w)
        elif m == 1 and re.match('.*e$', w) and not cvc:
            return w
        else:
            pass
        return w