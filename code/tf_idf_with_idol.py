from morphological_analysis import analysis
from tf_idf import tf_idf

BLOG = 'mana_blog.csv'
LEMMAS = '/home/output/mana_lemmas.csv'

analysis(BLOG, LEMMAS)
tf_idf(LEMMAS)
