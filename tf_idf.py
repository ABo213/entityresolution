from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
def tfidf_extraction(texts, vectorizer=None, max_features=5):
	if (vectorizer == None):
		vectorizer = TFIDF(binary="True", strip_accents="unicode", ngram_range=(1,1), analyzer='word', stop_words='english', max_features=max_features)
		tfidf = vectorizer.fit_transform(texts)
	else:
		tfidf = vectorizer.transform(texts)
	return tfidf, vectorizer
 