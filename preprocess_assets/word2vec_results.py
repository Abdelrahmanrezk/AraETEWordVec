
from sklearn.decomposition import PCA
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import arabic_reshaper
import pandas as pd


EMOJIS = ['🤣', '😂', '😁', '😜', '😝', '😄', '😆', '😎', '😭', '😩', '😫', '😔', '💔', '😢', '😰', '😞',
         '🌻', '🌸', '🌷', '🍃', '🌹', '💐', '🌿', "⏰", "⏱", "⌚", "🕖", "⏱️", "📲", "📱", "📞", "☎️",
         "💸", "💰", "كاش", "🤑", "💲", "🇪🇸", "🇮🇹", "🇫🇷", "🇦🇷", "🇩🇪", "🇰🇼", "🇦🇪", "🇧🇭", "🇴🇲", "🇸🇦", "🇶🇦"]

SENTIMENT_WORDS = ["متكامل", "مرتزق", "عميل", "خائن", "متطور", "ممتاز", "خرافي", "جاسوس", "سافل", "خسيس", "قذر", "رائع", "رهيب", "مذهل", "قواد", "مخنث", "مطبل", "موهوب", "مهاري"]

NER_WORDS = ["نت", "انستجرام", "فيسبوك", "IT", "HR", "AI", "راوتر", "مودم", "رسيفر", "marketing", "الدبابات", "المدرعات", "الطائرات", 
             "شاومي", "سوني", "لينوفو", "سامسونج", "هواوي", "ايفون", "الصواريخ", "الرادار", "الباصات", "القطار", "السياره", "الدراجه",
             "سوني", "تويتر", "سنابشات", "الواتساب", "design", "اكتوبر", "يونيو", "اغسطس", "نوفمبر", "مايو", "تموز", "شباط", "ايلول",
             "محمد", "ابراهيم", "عيسي", "اسماعيل", "هند", "ساره", "مرام", "ريما", "خلود",
            "ايران", "تركيا", "البحرين", "الكويت", "قطر", "السودان", "الجزائر", "تونس", "مصر",
            "مختبر", "مركز", "بلديه", "نقابه", "جمعيه", "شركه", "مؤسسه", "معهد", "اكاديميه"]






def init_graph_style(figsize=(10, 8), graph_style=['fivethirtyeight']):
	plt.style.use(graph_style)
	plt.figure(figsize=figsize)
	plt.axis('off')
	return True

def tsne_graph(model, symbols,n_iter, learning_rate):
	'''
	The function used to make dimension reduction for our trained word2vec into 2-d instead of high-dimension.
	Argument
	symbols       : list, list that contain either words or emojis(symbols of language in general)
	n_iter        : int, The number of iteration required to train the model.
	learning_rate : float, the step that the model take at each step of learning.
	
	Return
		tsne_df_scale: dataframe, 2-dimension dataframe that contain the reduced representation into just 2 latent factors.
	'''
	# Design the configuration of the model
	tsne = TSNE(n_components=2, verbose=1, perplexity=10, n_iter=n_iter, learning_rate=learning_rate)

	# retrieve the representation of each symbol in the list
	symbols_representation = model.wv[symbols]

	# fit and transform these high-dimension representation into 2-dimension representation
	tsne_scale_results = tsne.fit_transform(symbols_representation)

	# Build data frame from these 2-dimension representation
	tsne_df_scale = pd.DataFrame(tsne_scale_results, columns=['tsne1', 'tsne2'])

	print("The shape of our word_features is:", tsne_df_scale.shape)

	return tsne_df_scale



def word_display(tsne_df_scale, words, image_name_to_save):

	plt.scatter(tsne_df_scale.iloc[:, 0], tsne_df_scale.iloc[:, 1], marker='P',s=13, c="red") 

	for i, word in enumerate(words):
	    # handle Arabic words to display from right to left and as complete word not just separate chars
	    word = arabic_reshaper.reshape(word) # handle arabic words on ploting
	    word = get_display(word)
	    # plot each word beside its point
	    plt.annotate(word, xy=(tsne_df_scale.iloc[i, 0], tsne_df_scale.iloc[i, 1]),fontsize=15, color='black')
	plt.savefig('images/' + image_name_to_save)

	return True