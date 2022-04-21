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
    if request.method == 'POST':
        text = request.POST['text']
        num_of_sentss = len(nltk.sent_tokenize(text))
        method = int(request.POST['method'])
        size = int(request.POST['size'])
    else:
        text = request.GET.get('text')
        num_of_sentss = len(nltk.sent_tokenize(text))
        method = int(request.GET.get('method'))
        size = int(request.GET.get('size'))


    ########### functions for method 1 ###########################################################################


    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.append("'s")

    def preprocess(sentence):
            punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~[...][\n][..]'
            formatting_sentence = sentence.lower()
            tokens = []
            for token in nltk.word_tokenize(formatting_sentence):
                tokens.append(token)
            tokens = [word for word in tokens if word not in stopwords and word not in punctuation]
            formatted_sent = ' '.join(token for token in tokens)
            return formatted_sent


    def summy(text, number_of_sentences):
        original_text = text
        formatted_text = preprocess(original_text)
        
        word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_text))
        highest_frequency = max(word_frequency.values())
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word] / highest_frequency)
        sentence_list = nltk.sent_tokenize(original_text)
        
        score_sentences = {}
        for sentence in sentence_list:
            for word in nltk.word_tokenize(sentence):
                if word in word_frequency.keys():
                    if sentence not in score_sentences.keys():
                        score_sentences[sentence] = word_frequency[word]
                    else:
                        score_sentences[sentence] += word_frequency[word]
                        
        import heapq
        best_sentences = heapq.nlargest(number_of_sentences, score_sentences, key=score_sentences.get)
        
        return sentence_list, best_sentences, word_frequency, score_sentences


    
    ########### functions for method 2 ###########################################################################

    # f-n for calculating the score for each one of the sentences and distance between important words in sentence
    def calculate_sent_score(sentences, important_words, distance):
        scores = [] #stroing the scores of each one of the sentences
        sentence_index = 0 #index for each one of the sentences
        
        for sent in [nltk.word_tokenize(sent) for sent in sentences]:
            
            word_index = [] #indexes of the important words in the original sentences
            for word in important_words:
                try:
                    word_index.append(sent.index(word))
                except ValueError:
                    pass
            
            word_index.sort() #sorted list of indexes of important words in every sentence

            if len(word_index) == 0:
                continue
            
            #[0, 1, 2]
            groups_list = []
            group = [word_index[0]]
            i = 1 #for while loop 
            while i < len(word_index):
                if word_index[i] - word_index[i-1] < distance:
                    group.append(word_index[i])
                else:
                    groups_list.append(group[:]) #accessing all the elements of the list
                    group = [word_index[i]]
                    
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

        



    
    if len(text) == 0:
        summary = 'Nice joke..'

    elif method == 1 and size == 1:

        all_sentences = nltk.sent_tokenize(text)
        lenght = len(all_sentences)
        for sent in all_sentences:
            sent = preprocess(sent)

        formatted_text = ' '.join(all_sentences)

        sentence_list, best_sentences, word_frequency, score_sentences = summy(formatted_text, int(lenght/4))

        summary = ' '.join(best_sentences)

    elif method == 1 and size == 2:

        all_sentences = nltk.sent_tokenize(text)
        lenght = len(all_sentences)
        for sent in all_sentences:
            sent = preprocess(sent)

        formatted_text = ' '.join(all_sentences)

        sentence_list, best_sentences, word_frequency, score_sentences = summy(formatted_text, int(lenght/2))

        summary = ' '.join(best_sentences)

    elif method == 1 and size == 3:

        all_sentences = nltk.sent_tokenize(text)
        lenght = len(all_sentences)
        for sent in all_sentences:
            sent = preprocess(sent)

        formatted_text = ' '.join(all_sentences)

        sentence_list, best_sentences, word_frequency, score_sentences = summy(formatted_text, int(lenght*0.75))

        summary = ' '.join(best_sentences)



    elif method == 2 and size == 1:

        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss/4))

        summary = ' '.join(best_sentences)

    elif method == 2 and size == 2:


        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss/2))

        summary = ' '.join(best_sentences)

    elif method == 2 and size == 3:


        original_text, best_sentences, sentences_score = summarize(text, 5, 2, int(num_of_sentss*0.75))

        summary = ' '.join(best_sentences)

    else:
        summary = 'Nice joke..'


    return render(request, 'summarization/summary.htm', {'summary':summary})