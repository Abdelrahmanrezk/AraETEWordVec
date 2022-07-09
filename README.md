# AraETEWordVec


We provide our paper with code used for that research from first stage of collecting more than 350 million tweet, to provide free word embedding in Arabic language and run on different dataset to see the model ability compared to other available models.


We will start by some examples to show our work, then we will start to let you know how you can go from collecting data to the end of research.




## How to use to get Similar words & others

```

import gensim
from sklearn.decomposition import PCA
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import arabic_reshaper
import pandas as pd
from word2vec_results import *


# Once you download the model from drive link you can pass the direction of
# any model you need

# Example
rezk_model = gensim.models.Word2Vec.load("model_dir/continuous_bow_fullgram_vec_size_300-d_min_count_100")

similar_tokens = rezk_model.wv.most_similar('🤣')
print(similar_tokens)

'''
[('😆', 0.8333120942115784),
 ('😁', 0.8321138024330139),
 ('😜', 0.8205730319023132),
 ('😏', 0.819418728351593),
 ('😅', 0.8010570406913757),
 ('😒', 0.7967824339866638),
 ('هه', 0.7967004776000977),
 ('😂', 0.7781848907470703),
 ('😬', 0.7624844312667847),
 ('😀', 0.7618412375450134)]
'''

similar_tokens = rezk_model.wv.most_similar('🇰🇼')
print(similar_tokens)

'''
[('🇴🇲', 0.6610525846481323),
 ('العيد_الوطني_الكويتي', 0.6014205813407898),
 ('اليوم_الوطني_الكويتي', 0.5943148732185364),
 ('🇦🇪', 0.5859056711196899),
 ('الكويت', 0.5772003531455994),
 ('🇸🇦', 0.5617915987968445),
 ('🇶🇦', 0.5346092581748962),
 ('عمان', 0.5341886281967163),
 ('🇯🇴', 0.5333636999130249),
 ('الحبيبه', 0.5255107283592224)]
'''

similar_tokens = rezk_model.wv.most_similar('كوفيد')
print(similar_tokens)

'''
[('كوفيد-', 0.8830006122589111),
 ('كوفيد_', 0.8637586832046509),
 ('Covid', 0.7545498609542847),
 ('بكوفيد', 0.7023125886917114),
 ('الكوفيد', 0.6937721967697144),
 ('كورونا', 0.6714788675308228),
 ('كوڤيد', 0.6528131365776062),
 ('COVID', 0.6056150794029236),
 ('بـكوفيد-', 0.600813090801239),
 ('فيروس', 0.5611270666122437)]
'''

similar_tokens = rezk_model.wv.most_similar('منصه_مدرستي')
print(similar_tokens)

'''
[('تعليم_جده', 0.6406617164611816),
 ('لعوده_حضوريه_امنه', 0.6082739233970642),
 ('تعليم_المخواه', 0.6013671159744263),
 ('تعليم_الطائف', 0.5990505814552307),
 ('الملف_الاعلامي_بوزاره_التعليم', 0.5927740931510925),
 ('تعليم_عسير', 0.5926639437675476),
 ('تعليم_مكه', 0.5854555368423462),
 ('تعليم_الرياض', 0.581294059753418),
 ('تعليم_الرس', 0.5742909908294678),
 ('تعليم_القصيم', 0.5729984641075134)]

'''

NER_WORDS = ["نت", "انستجرام", "فيسبوك", "IT", "HR", "AI", "راوتر", "مودم", "رسيفر", "marketing", "الدبابات", "المدرعات", "الطائرات", 
             "شاومي", "سوني", "لينوفو", "سامسونج", "هواوي", "ايفون", "الصواريخ", "الرادار", "الباصات", "القطار", "السياره", "الدراجه",
             "سوني", "تويتر", "سنابشات", "الواتساب", "design", "اكتوبر", "يونيو", "اغسطس", "نوفمبر", "مايو", "تموز", "شباط", "ايلول",
             "محمد", "ابراهيم", "عيسي", "اسماعيل", "هند", "ساره", "مرام", "ريما", "خلود",
            "ايران", "تركيا", "البحرين", "الكويت", "قطر", "السودان", "الجزائر", "تونس", "مصر",
            "مختبر", "مركز", "بلديه", "نقابه", "جمعيه", "شركه", "مؤسسه", "معهد", "اكاديميه"]


# Using functions in side word2vec_results.py to display graphs in image below

# Reduce the dimension of NER_WORDS
tsne_df_scale = tsne_graph(rezk_model, NER_WORDS, 1400, .03)

_ = init_graph_style(figsize=(16, 10))

_ = word_display(tsne_df_scale, NER_WORDS, "NER_WORDS.png")

```

### 
<img src="images/NER_WORDS_2.png">


## How to use to train your ML or DL Model



### Collecting Tweets

To collect this large dataset we have used twint project that help you collect very large number of tweets instead of waiting months to collect your dataset using twitter API, and as to be legal with twittter developer we have not provide this dataset except for resarch work.

```python

pip3 install -r requirements.txt

# or you have to clone the project in case of error(I have doing that)
# https://github.com/twintproject/twint
```

This work of collecting this large number of tweets is splited into two files:
- create directories from 2008 to 2021
- inside each of these directories create Month_01 to Month_12 case senstive
- twitter_configs.py inside preprocess_assets direction, which contain documented code and the main file.
- Twitter Crawling 2018 to 2021.ipynb inside notebooks direction, notebook to run the code that depends on twitter_configs file.


### Collecting Tweets