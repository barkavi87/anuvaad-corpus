# Anuvaad Toolkit: Anuvaad English Tokenizer extending nltk tokenizer
#
# Author: Aroop <aroop.ghosh@tarento.com>
# URL: <http://developers.anuvaad.org/>

import re
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktTrainer, PunktLanguageVars
from nltk.tokenize import sent_tokenize

"""
Utility class for first page tokenizer for anuvaad project
"""
class AnuvaadEngTokenizer(object):
    """
    Default abbrevations
    """
    _abbrevations_with_space = ['of ', 'NO. ','Pvt. ', 'NOS. ','Smt. ','Sec. ','Spl. ','Mr. ','ft. ','kgs. ','kg. ','Dr. ','Ms. ','Ltd. ','Pty. ','Assn. ','St. ','Vol. ','pp. ','Co. ','Pty. ','Rs. ','Sh. ','M/S. ','Mrs. ','Vs. ']
    _abbrevations_without_space = ['Crl.']
    _tokenizer = None
    _regex_search_texts = []
    _brackets_abbrevations = []
    _dot_with_char_abbrevations = []
    _dot_with_quote_abbrevations = []
    _dot_with_number_abbrevations = []
    _dot_with_beginning_number_abbrevations = []
    
    def __init__(self, abbrevations=None):
        if abbrevations is not None:
            self._abbrevations_without_space.append(abbrevations)
        punkt_param = PunktParameters()
        with open('utils/tokenizer_data/starter.txt', encoding='utf8') as f:
            text = f.read()
        punkt_param.sent_starters = text.split('\n')
        self._regex_search_texts = []
        self._dot_abbrevations = []
        self._brackets_abbrevations = []
        self._dot_with_char_abbrevations = []
        self._dot_with_number_abbrevations = []
        self._dot_with_beginning_number_abbrevations = []
        self._tokenizer = PunktSentenceTokenizer(train_text=punkt_param,lang_vars=BulletPointLangVars())

    def tokenize(self, text):
        print('--------------Process started-------------')
        text = self.serialize_pattern(text)
        text = self.serialize_with_abbrevations(text)
        text = self.serialize_dots(text)
        text = self.serialize_brackets(text)
        text = self.serialize_dot_with_number(text)
        text = self.serialize_dot_with_number_beginning(text)
        text = self.serialize_quotes_with_number(text)
        sentences = self._tokenizer.tokenize(text)
        output = []
        for se in sentences:
            se = self.deserialize_pattern(se)
            se = self.deserialize_dots(se)
            se = self.deserialize_brackets(se)
            se = self.deserialize_dot_with_number(se)
            se = self.deserialize_dot_with_number_beginning(se)
            se = self.deserialize_quotes_with_number(se)
            output.append(self.deserialize_with_abbrevations(se))
        print('--------------Process finished-------------')
        return output

    def serialize_brackets(self, text):
        patterns = re.findall(r'([(][0-9a-zA-Z.-]{1,}[)])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._brackets_abbrevations.append(pattern)
                text = pattern_obj.sub('WW_'+str(index)+'_WW', text)
                index+=1
        return text

    def deserialize_brackets(self, text):
        index = 0
        if self._brackets_abbrevations is not None and isinstance(self._brackets_abbrevations, list):
            for pattern in self._brackets_abbrevations:
                pattern_obj = re.compile(re.escape('WW_'+str(index)+'_WW'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_quotes_with_number(self, text):
        patterns = re.findall(r'([ ][“][0-9a-zA-Z]{1,}[.])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_quote_abbrevations.append(pattern)
                text = pattern_obj.sub(' ZZ_'+str(index)+'_ZZ', text)
                index+=1
        return text

    def deserialize_quotes_with_number(self, text):
        index = 0
        if self._dot_with_quote_abbrevations is not None and isinstance(self._dot_with_quote_abbrevations, list):
            for pattern in self._dot_with_quote_abbrevations:
                pattern_obj = re.compile(re.escape('ZZ_'+str(index)+'_ZZ'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dot_with_number_beginning(self, text):
        patterns = re.findall(r'(^[0-9]{1,}[.])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_beginning_number_abbrevations.append(pattern)
                text = pattern_obj.sub('YY_'+str(index)+'_YY', text)
                index+=1
        return text

    def deserialize_dot_with_number_beginning(self, text):
        index = 0
        if self._dot_with_beginning_number_abbrevations is not None and isinstance(self._dot_with_beginning_number_abbrevations, list):
            for pattern in self._dot_with_beginning_number_abbrevations:
                pattern_obj = re.compile(re.escape('YY_'+str(index)+'_YY'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dot_with_number(self, text):
        patterns = re.findall(r'(?:[ ][0-9]{1,}[.])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_number_abbrevations.append(pattern)
                text = pattern_obj.sub(' XX_'+str(index)+'_XX', text)
                index+=1
        return text

    def deserialize_dot_with_number(self, text):
        index = 0
        if self._dot_with_number_abbrevations is not None and isinstance(self._dot_with_number_abbrevations, list):
            for pattern in self._dot_with_number_abbrevations:
                pattern_obj = re.compile(re.escape('XX_'+str(index)+'_XX'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dots(self, text):
        pattern = re.compile(r'([.]{3,})')
        text = pattern.sub('XX__XX', text)
        return text

    def deserialize_dots(self, text):
        pattern = re.compile(re.escape('XX__XX'), re.IGNORECASE)
        text = pattern.sub('......', text)
        return text

    def serialize_pattern(self, text):
        patterns = re.findall(r'(?:[a-zA-Z][.]){2,}',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_char_abbrevations.append(pattern)
                text = pattern_obj.sub('$$_'+str(index)+'_$$', text)
                index+=1
        return text

    def deserialize_pattern(self, text):
        index = 0
        if self._dot_with_char_abbrevations is not None and isinstance(self._dot_with_char_abbrevations, list):
            for pattern in self._dot_with_char_abbrevations:
                pattern_obj = re.compile(re.escape('$$_'+str(index)+'_$$'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text
           
    def serialize_with_abbrevations(self, text):
        index = 0
        index_for_without_space = 0
        for abbrev in self._abbrevations_with_space:
            pattern = re.compile(re.escape(abbrev), re.IGNORECASE)
            text = pattern.sub('#'+str(index)+'# ', text)
            index += 1
        for abbrev in self._abbrevations_without_space:
            pattern = re.compile(re.escape(abbrev), re.IGNORECASE)
            text = pattern.sub('#'+str(index_for_without_space)+'##', text)
            index_for_without_space += 1
        return text

    def deserialize_with_abbrevations(self, text):
        index = 0
        index_for_without_space = 0
        for abbrev in self._abbrevations_with_space:
            pattern = re.compile(re.escape('#'+str(index)+'# '), re.IGNORECASE)
            text = pattern.sub(abbrev, text)
            index += 1
        for abbrev in self._abbrevations_without_space:
            pattern = re.compile(re.escape('#'+str(index_for_without_space)+'##'), re.IGNORECASE)
            text = pattern.sub(abbrev, text)
            index_for_without_space += 1
        return text


class BulletPointLangVars(PunktLanguageVars):
    text = []
    with open('utils/tokenizer_data/train.txt', encoding='utf8') as f:
        text = f.read()
    sent_end_chars = text.split('\n')
    
    # # punkt = PunktTrainer()
    # # punkt.train(text,finalize=False, verbose=False)
    # # punkt.finalize_training(verbose=True)
# text = ''
# with open('data5.txt', encoding='utf8') as f:
#     text = f.read()
# tokenizer = AnuvaadEngTokenizer()
# tokenizer.tokenize(text)
    