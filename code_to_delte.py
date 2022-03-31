# if __name__ == '__main__':
#     processes = []
#     for year in range(2016, 2022):
#         for month in range(1, 13):
#             p = Process(target=tweets_for_one_month, 
#                  args=(year,month,))
#             p.start()
#             processes.append(p)     
        
#     for p in processes:
#         p.join()


# from datetime import timedelta
# from string import ascii_letters, digits
# from os import mkdir, path
DETECT_SPECIAL_CHARS = re.compile("[\U000fe19b\U000fe19c\U000fe1b5\U000fe19d\U000fe19f\U000e0067\U0001f9b1\U000e007f\U000e0062\U000e006e\U000e0065\ue6fd\ue67b\ue67a\ue422\ue41f\ue327\ue224\ue40f\U000feb9d\ue703\U000fe527\ue677\ue222\ue221\uf8ff\ue694\U0001f7e1\U0001f90f\ue438\U000feb18\U0001f9dc\ue050\ue219\ue670\ue110\U0001f92e\U000feb5e\ue41d\ue32c\ue139\ue312\ue63e\ue748\U0001f7e2\ue046\ue033\ue112\U000fec17\ue335\ue035\ue44b\U000feb0d\U000fe32d\U000fe040\U0001f9e3\U000fe043\ue301\U0001fac2\ue009\U000fe354\ue00a\U000fe326\U000fe326\U000fe7f0\ue21d\ue21e\ue21f\ue444\ue66a\ue307\ue331\ue437\U0001f9a0\ue68d\ue405\ue21c\ue326\ue40c\ue03e\ue326\ue03e\U0001f9d6\ue304\U000fe987\ue681\U0001f993\ue305\ue427\ue303\ue118\ue404\ue32a\ue6ee\ue72d\ue6a4\ue22c\ue68d\U000fe1a8\ue20c\U0001fa84\ue04e\U000fe35b\U0001f9ed\U000fe54f\U000feb16\U000feb15\U000fe33d\ue704\ue105\ue01d\ue510\U000feb69\U000feb76\U000feb69\U000feb69\ue03f\ue12f\U000fe324\ue201\ue115\ue316\ue122\ue313\ue129\ue10f\ue03d\ue04a\ue02f\U000fe1b6\U000feb5c\ue058\ue71c\uf707\U000fe046\ue413\ue6e0\ue406\ue03c\ue042\ue411\ue410\U000fe333\U000fe041\ue402\ue6ec\ue72e\ue011\U000fe329\U000fe338\ue701\U000fe1b2\ue419\ue407\U000fe01f\U000feb75\U000feb85\ue022\U0001f9ba\ue347\ue32b\U000fe7d9\U000fe502\U0001f992\ue32e\U000feb5b\ue401\U000fe32a\U000fe1b3\U000fe341\U0001f9ce\ue314\ue725\ue32b\ue204\ue40e\ue00e\ue223\ue420\U0001f9d5\U0001f9e2\U0001fab0\U0001fac0\U0001f9e8\U0001f9d8\ue6ff\ue6fc\ue408\U0001f976\ue416\ue709\ue447\ue119\ue41b\U000fe351\ue418\ue148\U000fe335\ue030\ue31d\U0001fa78\ue747\ue702\ue306\ue106\ue698\ue057\ue529\U0001f91f\ue414\U000fe04d\U0001f9b9\U0001f90c\uf60d\U000fe532\ue67f\U000fe4f5\U0001f9e4\ue027\U000fe34a\ue409\ue22f\ue40a\ue049\ue04b\U000fe347\ue00f\U0001f9d4\ue754\ue311\ue113\U0001f964\ue11c\U000feb99\U000fec00\ue700\U0001f9e6\U000fe526\ue432\ue695\ue108\ue13c\ue319\ue676\U000fe03d\ue012\ue20f\ue220\U0001f972\ue6ac\U0001f966\ue643\u2060\U0001f9cd\U0001f9a7\U0001f962\ue328\ue71b\U000feb0f\U000feb6a\ue107\U000fe344\uf815\ue421\ue684\U0001f92f\U0001f9a6\U000fe358\ue6f6\ue008\U000feb9a\ue01b\U000fe340\ue70a\ue41e\U000feb55\ue056\ue32d\ue328\ue40d\ue337\ue743\ue417\ue023\ue403\ue6ef\ue6f0\ue415\ue056\ue022\ue412\U0001f92b\U000feb14\U0001f9b6\U000fe339\U000fe320\U000fe323\U000feb0e\U000fe342\U0001f92c\U000fe512\U000fe517\U000fe520\U000fe331\U000fe32c\U0001f971\U0001f9d0\U000fe33a\U0001f9ff\U0001f94d\U0001f975\U000fe19e\U000fe541\U000feb13\U0001f929\U000fe32f\U000fe343\U0001f9da\U0001f9af\ue757\U000fe1ab\U000fe1a5\U0001f928\U0001f9a5\U0001f974\U0001f973\U0001f90e\U0001f92a\U000feb9f\U000feb97\U000fe330\U000feb9e\U000fe334\U000feb96\ue537\U000fe327\U000fe334\U000fe33e\u200c\u200d\u202c\u200e\u202b\U0001f90d\u2067\u200f\u200b\U0001f97a\U0001f932\u2066\u2069\U0001f90d\U0001f970\U0001f92d\U0001f9e1\ue032\ue059\u06dd]")

# def clean_name(dirname):
#     valid = set(ascii_letters + digits)
#     return ''.join(a for a in dirname if a in valid)


# def twint_search(searchterm, since, until, json_name):
#     '''
#     Twint search for a specific date range.
#     Stores results to json.
#     '''
#     c = twint.Config()
#     c.Search = searchterm
#     c.Since = since
#     c.Until = until
#     c.Hide_output = True
#     c.Store_json = True
#     c.Output = json_name
#     c.Debug = True

#     try:
#         twint.run.Search(c)    
#     except (KeyboardInterrupt, SystemExit):
#         raise
#     except:
#         print("Problem with %s." % since)




# def twint_loop(searchterm, since, until):

#     dirname = clean_name(searchterm)
#     try:
#     # Create target Directory
#         mkdir(dirname)
#         print("Directory" , dirname ,  "Created ")
#     except FileExistsError:
#         print("Directory" , dirname ,  "already exists")

#     daterange = pd.date_range(since, until)

#     for start_date in daterange:

#         since= start_date.strftime("%Y-%m-%d")
#         until = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")

#         json_name = '%s.json' % since
#         json_name = path.join(dirname, json_name)

#         print('Getting %s ' % since )
#         twint_search(searchterm, since, until, json_name)




# twint_loop('#womensmarch', '01-01-2018', '01-08-2018')



# from glob import glob

# glob(path.join('womensmarch','*.json'))


# file_names = glob(path.join('womensmarch','*.json'))
# dfs = [pd.read_json(fn, lines = True) for fn in file_names]
# wm2018_df = pd.concat(dfs)

# wm2018_df.info()


# import twint
# from datetime import datetime
# from datetime import timedelta

# days = [1,2,3]

# for n in days:
#     c = twint.Config()
#     c. Search = 'Potro'
#     c. Count = True
#     c. Format = 'Username: {username} | Date: {date}'
#     c. Output = str(n)+'.csv'

#     st = datetime. strptime('2019-04-03','%Y-%m-%d')
#     end = datetime. strptime('2019-04-04', '%Y-%m-%d')

#     stdt = st + timedelta(days=n)
#     enddt = end + timedelta(days=n)
#     ststr = stdt.strftime ('%Y-%m-%d')
#     endstr = enddt.strftime ('%Y-%m-%d')

#     c. Since = ststr
#     c. Until = endstr
#     twint.run.Search(c)




# import numpy as np
# #Important Parameters
# VOCAB_SIZE = len(vocabs)
# EMBEDDING_DIM = model.wv["لا"].shape[0]
# w2v = np.zeros((VOCAB_SIZE, EMBEDDING_DIM))
# import os
# if not os.path.exists("projections"):
#     os.mkdir("projections")
# # tsv_file_path = FOLDER_PATH+"metadata.tsv"
# with open("projections/metadata.tsv",'w+') as file_metadata:
#     for i,word in enumerate(model.wv.index_to_key[:VOCAB_SIZE]):
#         w2v[i] = model.wv[word]
#         file_metadata.write(word + '\n')

# # import tensorflow as tf
# # from tensorboard.plugins import projector
# # # TENSORBOARD_FILES_PATH = FOLDER_PATH
# # tf.compat.v1.disable_eager_execution()
# # sess = tf.compat.v1.InteractiveSession()
# # with tf.device('/cpu:0'):
# #     embedding = tf.Variable(w2v, trainable=False ,name="embedding")
# # sess.run(tf.compat.v1.global_variables_initializer())
# # server = tf.compat.v1.train.Saver()
# # writer = tf.compat.v1.summary.FileWriter("projections", sess.graph)
# # config = projector.ProjectorConfig()
# # embed = config.embeddings.add()
# # embed.tensor_name = "embedding"
# # embed.metadata_path = "metadata.tsv"
# # projector.visualize_embeddings(writer, config)
# # server.save(sess, "projections/model.ckpt", global_step=VOCAB_SIZE)