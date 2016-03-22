'''
Maps Penn Treebank POS tags to morphosyntactic attributes. Excerpted from 
wsj.py,
Utilities for working with Penn Treebank Wall Street Journal data.
@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2011-05-01
'''
from __future__ import print_function, division
from future_builtins import map, filter, zip

from collections import defaultdict

def posinfo():
    '''
    >>> dict(posinfo()['VBP'])
    {'finite': True, 'tag': 'VBP', 'description': 'Verb, non-3rd person singular present', 'verbal': True}
    '''
    # http://www.computing.dcu.ie/~acahill/tagset.html
    # tag groups: j = adjective, n = nominal, d = determiner, v = verbal, f = finite, r = adverbial, x = function/closed-class
    #   Aside from f and x, these are mutually exclusive and can be interpreted as coarse tags.
    TABLE = '''
    CC    x Coordinating conjunction    >> and, but, or...
    CD      Cardinal Number
    DT   dx Determiner
    EX    x Existential there
    FW      Foreign Word
    IN    x Preposision or subordinating conjunction
    JJ   j  Adjective
    JJR  j  Adjective, comparative
    JJS  j  Adjective, superlative
    LS      List Item Marker
    MD   vx Modal    >> can, could, might, may...
    NN   n  Noun, singular or mass
    NNP  n  Proper Noun, singular
    NNPS n  Proper Noun, plural
    NNS  n  Noun, plural
    PDT  dx Predeterminer    >> all, both ... when they precede an article
    POS   x Possessive Ending    >> 's
    PRP  nx Personal Pronoun    >> I, me, you, he...
    PRP$ nx Possessive Pronoun    >> my, your, mine, yours...
    RB   r  Adverb    >> Most words that end in -ly as well as degree words like quite, too and very
    RBR  r  Adverb, comparative    >> Adverbs with the comparative ending -er, with a strictly comparative meaning
    RBS  r  Adverb, superlative
    RP    x Particle
    SYM     Symbol    >> Should be used for mathematical, scientific or technical symbols
    TO    x to
    UH      Interjection    >> e.g. uh, well, yes, my...
    VB   v  Verb, base form    >> subsumes imperatives, infinitives and subjunctives
    VBD fv  Verb, past tense    >> includes the conditional form of the verb to be
    VBG  v  Verb, gerund or persent participle
    VBN  v  Verb, past participle
    VBP fv  Verb, non-3rd person singular present
    VBZ fv  Verb, 3rd person singular present
    WDT  dx Wh-determiner    >> e.g. which, and that when it is used as a relative pronoun
    WP   nx Wh-pronoun    >> e.g. what, who, whom...
    WP$  nx Possessive wh-pronoun
    WRB  rx Wh-adverb    >> how, where why
    #
    $
    ''
    (
    )
    -LRB-    (
    -RRB-    )
    -LSB-    [
    -RSB-    ]
    -LCB-    {
    -RCB-    }
    ,
    .
    :
    ``
    '''
    info = {}
    for ln in TABLE.strip().splitlines():
        ln = ln.strip()
        entry = defaultdict(lambda: False)
        if ln[0] in '()[]{}-' or ' ' not in ln:
            if ln[0] in '()[]{}-':
                entry['bracket'] = True
            entry['tag'] = ln.split()[0]
            entry['punct'] = True
            entry['symbol'] = True
            if ln in ("''", "``"): entry['quote'] = True
        else:
        # TODO: traces?
            if '>>' in ln:
                entry['extra'] = ln[ln.index('>> ')+3:]
                ln = ln[:ln.index('>> ')].strip()
            parts = ln.split()
            entry['tag'] = parts[0]
            atts = '' 
            if parts[1][0].islower():
                atts = parts[1]
                del parts[1]
            entry['description'] = ' '.join(parts[1:])
            if 'Possessive' in entry['description']:
                entry['possessive'] = True
            if atts:
                if 'x' in atts: entry['functional'] = True
                if 'n' in atts: entry['nominal'] = True
                if 'nx' in atts: entry['pronominal'] = True
                if 'j' in atts: entry['adjectival'] = True
                if 'v' in atts: entry['verbal'] = True
                if 'r' in atts: entry['adverbial'] = True
                if 'd' in atts: entry['determiner'] = True
                if 'f' in atts: entry['finite'] = True
                coarse = ['n' in atts, 'v' in atts, 'd' in atts, 'r' in atts, 'j' in atts]
                if sum(coarse)==1:
                    entry['coarse'] = 'nvdrj'[coarse.index(True)]
                else:
                    assert sum(coarse)==0
                    entry['coarse'] = entry['tag'] 
            else:
                entry['coarse'] = entry['tag']
                
            if entry['tag'].startswith('W'): entry['wh'] = True
        info[entry['tag']] = entry
        
    info['LS']['symbol'] = True
    info['SYM']['symbol'] = True
    info['NNP']['proper'] = True
    info['NNPS']['proper'] = True
    info['FW']['foreign'] = True
    return info

def poses(**criteria):
    '''
    Retrieves a list of all tags meeting the specified criteria, where criteria are boolean attribute
    names in the entries of the object returned by posinfo().
    
    >>> poses(finite=True)
    set(['VBZ', 'VBP', 'VBD'])
    >>> poses(nominal=True, pronominal=False)
    set(['NNPS', 'NNS', 'NN', 'NNP'])
    >>> poses(functional=True, nominal=False, verbal=False, adverbial=False, determiner=False, possessive=False)
    set(['CC', 'TO', 'RP', 'EX', 'IN'])
    '''
    return {entry['tag'] for entry in posinfo().values() if sum(entry[attn]==v for attn,v in criteria.items())==len(criteria)}

def posAttributes(tag):
    return posinfo()[tag]