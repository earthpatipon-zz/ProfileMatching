def poisci_pare(text):
    sents = text.split('.')
    print sents
    answer = [sent.split() for sent in sents if sent]
    return answer

print poisci_pare("Hello world. This is great.")