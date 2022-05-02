# AraETEWordVec


We provide our paper with code used for that research from first stage of collecting more than 350 million tweet, to provide free word embedding in Arabic language and run on different dataset to see the model ability compared to other available models.


We will start by some examples to show our work, then we will start to let you know how you can go from collecting data to the end of research.




## How to use

### Collecting Tweets

To collect this large dataset we have used twint project that help you collect very large number of tweets instead of waiting months to collect your dataset using twitter API, and as to be legal with twittter developer we have not provide this dataset except for resarch work.

```python

pip3 install twint

# or you have to clone the project in case of error(I have doing that)
# https://github.com/twintproject/twint
```

This work of collecting this large number of tweets is splited into two files:
- create directories from 2008 to 2021
- inside each of these directories create Month_01 to Month_12 case senstive
- twitter_configs.py inside preprocess_assets direction, which contain documented code and the main file.
- Twitter Crawling 2018 to 2021.ipynb inside notebooks direction, notebook to run the code that depends on twitter_configs file.


### Collecting Tweets