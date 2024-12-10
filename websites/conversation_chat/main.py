from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


# Sample text data
texts = ["hello world" , "machine learning"]

# Create a CountVectorizer with character-level analysis
vectorizer = TfidfVectorizer(analyzer='char') # try it with ngram and without ngram 

# Fit and transform the text data
char_features = vectorizer.fit_transform(texts)

# Convert to array to see the features
char_features_array = char_features.toarray()

print(char_features_array)