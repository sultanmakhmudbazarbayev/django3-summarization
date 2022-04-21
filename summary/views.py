from django.shortcuts import render
from django.http import HttpResponse
import re
import nltk
import string 
nltk.download('punkt')
nltk.download('stopwords')
import heapq


# Create your views here.


def home(request):
    return render(request, 'summarization/home.htm')

def summary(request):
    
    text = request.GET.get('text')
    num_of_sentss = len(nltk.sent_tokenize(text))
    method = int(request.GET.get('method'))
    size = int(request.GET.get('size'))
    
    print(method)
    print(size)
    
    if len(text) == 0:
        summary = 'Nice joke..'

    elif method == 1 and size == 1:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(sentence):
            formatting_sentence = sentence.lower()
            tokens = []
            for token in nltk.word_tokenize(formatting_sentence):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_sent = ' '.join(token for token in tokens)
            return formatted_sent


        formatted_sent = preprocess(text)
        formatted_sent
        
        word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_sent))
        word_frequency

        highest_freq = max(word_frequency.values())

        for word in word_frequency.keys():
        #     print(word)
            word_frequency[word] = word_frequency[word] / highest_freq

        sentence_list = nltk.sent_tokenize(text)
        sentence_list

        score_sentences = {}
        for sent in sentence_list:
        #     print(sent)
            for word in nltk.word_tokenize(sent.lower()):
        #         print(word)
                if sent not in score_sentences.keys():
                    score_sentences[sent] = word_frequency[word]
                else:
                    score_sentences[sent] += word_frequency[word]

        print("Len Score_sen " + str(len(score_sentences)))
        best_sentences = heapq.nlargest(int((len(score_sentences))/4), score_sentences, key = score_sentences.get)

        summary = ' '.join(best_sentences)

    elif method == 1 and size == 2:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(sentence):
            formatting_sentence = sentence.lower()
            tokens = []
            for token in nltk.word_tokenize(formatting_sentence):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_sent = ' '.join(token for token in tokens)
            return formatted_sent


        formatted_sent = preprocess(text)
        formatted_sent
        
        word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_sent))
        word_frequency

        highest_freq = max(word_frequency.values())

        for word in word_frequency.keys():
        #     print(word)
            word_frequency[word] = word_frequency[word] / highest_freq

        sentence_list = nltk.sent_tokenize(text)
        sentence_list

        score_sentences = {}
        for sent in sentence_list:
        #     print(sent)
            for word in nltk.word_tokenize(sent.lower()):
        #         print(word)
                if sent not in score_sentences.keys():
                    score_sentences[sent] = word_frequency[word]
                else:
                    score_sentences[sent] += word_frequency[word]

        print("Len Score_sen " + str(len(score_sentences)))
        best_sentences = heapq.nlargest(int((len(score_sentences))/2), score_sentences, key = score_sentences.get)

        summary = ' '.join(best_sentences)

    elif method == 1 and size == 3:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(sentence):
            formatting_sentence = sentence.lower()
            tokens = []
            for token in nltk.word_tokenize(formatting_sentence):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_sent = ' '.join(token for token in tokens)
            return formatted_sent


        formatted_sent = preprocess(text)
        formatted_sent
        
        word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_sent))
        word_frequency

        highest_freq = max(word_frequency.values())

        for word in word_frequency.keys():
        #     print(word)
            word_frequency[word] = word_frequency[word] / highest_freq

        sentence_list = nltk.sent_tokenize(text)
        sentence_list

        score_sentences = {}
        for sent in sentence_list:
        #     print(sent)
            for word in nltk.word_tokenize(sent.lower()):
        #         print(word)
                if sent not in score_sentences.keys():
                    score_sentences[sent] = word_frequency[word]
                else:
                    score_sentences[sent] += word_frequency[word]

        print("Len Score_sen " + str(len(score_sentences)))
        best_sentences = heapq.nlargest(int((len(score_sentences))*0.75), score_sentences, key = score_sentences.get)

        summary = ' '.join(best_sentences)



    elif method == 2 and size == 1:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(text):
            formatted_text = text.lower()
            tokens = []
            for token in nltk.word_tokenize(formatted_text):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_text = ' '.join(word for word in tokens)
            
            return formatted_text

        # global formatted_text
        # formatted_text = preprocess(text)

        # f-n for calculating the score for each one of the sentences and distance between important words in sentence
        def calculate_sent_score(sentences, important_words, distance):
            scores = [] #stroing the scores of each one of the sentences
            sentence_index = 0 #index for each one of the sentences
            
            for sent in [nltk.word_tokenize(sent) for sent in sentences]:
        #         print('---------------')
        #         print(sent)
                
                word_index = [] #indexes of the important words in the original sentences
                for word in important_words:
                    try:
                        word_index.append(sent.index(word))
                    except ValueError:
                        pass
                
                word_index.sort() #sorted list of indexes of important words in every sentence
        #         print(word_index)

                if len(word_index) == 0:
                    continue
                
                #[0, 1, 2]
                groups_list = []
                group = [word_index[0]]
                i = 1 #for while loop 
                while i < len(word_index):
                    if word_index[i] - word_index[i-1] < distance:
                        group.append(word_index[i])
        #                 print('group', group)
                    else:
                        groups_list.append(group[:]) #accessing all the elements of the list
                        group = [word_index[i]]
        #                 print('group', group)
                        
                    i += 1
                groups_list.append(group) #The more groups in the same group the more important the sentence is
                
                max_group_score = 0
                for g in groups_list:
                    important_words_in_group = len(g)
                    total_words_in_group = g[-1] - g[0] + 1 #total words in group
                    score = 1.0 * important_words_in_group**2 / total_words_in_group
                    
                    if score > max_group_score:
                        max_group_score = score
                        
                scores.append((max_group_score, sentence_index))
                sentence_index += 1
                
        #     print('final scores', scores)
            return scores

        # text and number of important words(appear most in the text) we want to select
        def summarize(text, top_n_words, distance, number_of_sentences):
            original_sentences = [sent for sent in nltk.sent_tokenize(text)]
        #     print(original_sentences) 
            
            formatted_text = [preprocess(original_sentence) for original_sentence in original_sentences]
        #     print(formatted_text)
            
            words = [word for sentence in formatted_text for word in nltk.word_tokenize(sentence)] #every word in a text
        #     print(words)
            
            frequency = nltk.FreqDist(words)
        #     return frequency #frequency of each one of the word

            top_n_words = [word[0] for word in frequency.most_common(top_n_words)] #finding the the most frequent words using the f-n most_common(number_of_words)
        #     print(top_n_words)

            sentences_score = calculate_sent_score(formatted_text, top_n_words, distance)
        #     print(sentences_score)

            best_sentences = heapq.nlargest(number_of_sentences, sentences_score)
        #     print(best_sentences)
            
            best_sentences = [original_sentences[i] for(score, i) in best_sentences]
        #     print(best_sentences)

            return original_sentences, best_sentences, sentences_score

        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss/4))

        print(num_of_sentss)

        summary = ' '.join(best_sentences)

    elif method == 2 and size == 2:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(text):
            formatted_text = text.lower()
            tokens = []
            for token in nltk.word_tokenize(formatted_text):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_text = ' '.join(word for word in tokens)
            
            return formatted_text

        # global formatted_text
        # formatted_text = preprocess(text)

        # f-n for calculating the score for each one of the sentences and distance between important words in sentence
        def calculate_sent_score(sentences, important_words, distance):
            scores = [] #stroing the scores of each one of the sentences
            sentence_index = 0 #index for each one of the sentences
            
            for sent in [nltk.word_tokenize(sent) for sent in sentences]:
        #         print('---------------')
        #         print(sent)
                
                word_index = [] #indexes of the important words in the original sentences
                for word in important_words:
                    try:
                        word_index.append(sent.index(word))
                    except ValueError:
                        pass
                
                word_index.sort() #sorted list of indexes of important words in every sentence
        #         print(word_index)

                if len(word_index) == 0:
                    continue
                
                #[0, 1, 2]
                groups_list = []
                group = [word_index[0]]
                i = 1 #for while loop 
                while i < len(word_index):
                    if word_index[i] - word_index[i-1] < distance:
                        group.append(word_index[i])
        #                 print('group', group)
                    else:
                        groups_list.append(group[:]) #accessing all the elements of the list
                        group = [word_index[i]]
        #                 print('group', group)
                        
                    i += 1
                groups_list.append(group) #The more groups in the same group the more important the sentence is
                
                max_group_score = 0
                for g in groups_list:
                    important_words_in_group = len(g)
                    total_words_in_group = g[-1] - g[0] + 1 #total words in group
                    score = 1.0 * important_words_in_group**2 / total_words_in_group
                    
                    if score > max_group_score:
                        max_group_score = score
                        
                scores.append((max_group_score, sentence_index))
                sentence_index += 1
                
        #     print('final scores', scores)
            return scores

        # text and number of important words(appear most in the text) we want to select
        def summarize(text, top_n_words, distance, number_of_sentences):
            original_sentences = [sent for sent in nltk.sent_tokenize(text)]
        #     print(original_sentences) 
            
            formatted_text = [preprocess(original_sentence) for original_sentence in original_sentences]
        #     print(formatted_text)
            
            words = [word for sentence in formatted_text for word in nltk.word_tokenize(sentence)] #every word in a text
        #     print(words)
            
            frequency = nltk.FreqDist(words)
        #     return frequency #frequency of each one of the word

            top_n_words = [word[0] for word in frequency.most_common(top_n_words)] #finding the the most frequent words using the f-n most_common(number_of_words)
        #     print(top_n_words)

            sentences_score = calculate_sent_score(formatted_text, top_n_words, distance)
        #     print(sentences_score)

            best_sentences = heapq.nlargest(number_of_sentences, sentences_score)
        #     print(best_sentences)
            
            best_sentences = [original_sentences[i] for(score, i) in best_sentences]
        #     print(best_sentences)

            return original_sentences, best_sentences, sentences_score

        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss/2))

        print(num_of_sentss)

        summary = ' '.join(best_sentences)

    elif method == 2 and size == 3:

        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.append("'s")

        def preprocess(text):
            formatted_text = text.lower()
            tokens = []
            for token in nltk.word_tokenize(formatted_text):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
            formatted_text = ' '.join(word for word in tokens)
            
            return formatted_text

        # global formatted_text
        # formatted_text = preprocess(text)

        # f-n for calculating the score for each one of the sentences and distance between important words in sentence
        def calculate_sent_score(sentences, important_words, distance):
            scores = [] #stroing the scores of each one of the sentences
            sentence_index = 0 #index for each one of the sentences
            
            for sent in [nltk.word_tokenize(sent) for sent in sentences]:
        #         print('---------------')
        #         print(sent)
                
                word_index = [] #indexes of the important words in the original sentences
                for word in important_words:
                    try:
                        word_index.append(sent.index(word))
                    except ValueError:
                        pass
                
                word_index.sort() #sorted list of indexes of important words in every sentence
        #         print(word_index)

                if len(word_index) == 0:
                    continue
                
                #[0, 1, 2]
                groups_list = []
                group = [word_index[0]]
                i = 1 #for while loop 
                while i < len(word_index):
                    if word_index[i] - word_index[i-1] < distance:
                        group.append(word_index[i])
        #                 print('group', group)
                    else:
                        groups_list.append(group[:]) #accessing all the elements of the list
                        group = [word_index[i]]
        #                 print('group', group)
                        
                    i += 1
                groups_list.append(group) #The more groups in the same group the more important the sentence is
                
                max_group_score = 0
                for g in groups_list:
                    important_words_in_group = len(g)
                    total_words_in_group = g[-1] - g[0] + 1 #total words in group
                    score = 1.0 * important_words_in_group**2 / total_words_in_group
                    
                    if score > max_group_score:
                        max_group_score = score
                        
                scores.append((max_group_score, sentence_index))
                sentence_index += 1
                
        #     print('final scores', scores)
            return scores

        # text and number of important words(appear most in the text) we want to select
        def summarize(text, top_n_words, distance, number_of_sentences):
            original_sentences = [sent for sent in nltk.sent_tokenize(text)]
        #     print(original_sentences) 
            
            formatted_text = [preprocess(original_sentence) for original_sentence in original_sentences]
        #     print(formatted_text)
            
            words = [word for sentence in formatted_text for word in nltk.word_tokenize(sentence)] #every word in a text
        #     print(words)
            
            frequency = nltk.FreqDist(words)
        #     return frequency #frequency of each one of the word

            top_n_words = [word[0] for word in frequency.most_common(top_n_words)] #finding the the most frequent words using the f-n most_common(number_of_words)
        #     print(top_n_words)

            sentences_score = calculate_sent_score(formatted_text, top_n_words, distance)
        #     print(sentences_score)

            best_sentences = heapq.nlargest(number_of_sentences, sentences_score)
        #     print(best_sentences)
            
            best_sentences = [original_sentences[i] for(score, i) in best_sentences]
        #     print(best_sentences)

            return original_sentences, best_sentences, sentences_score

        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss*0.75))

        print(num_of_sentss)

        summary = ' '.join(best_sentences)

    else:
        summary = 'Nice joke..'


    return render(request, 'summarization/summary.htm', {'summary':summary})