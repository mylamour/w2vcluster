import os,sys
import click
from sklearn.cluster import KMeans
from gensim.models import word2vec

def load_file(filename):
    """
        You need customsize load_file function with special pre-process
    """
    sentences = []

    with open(filename,'r') as scmd:
        next(scmd)
        for line in scmd.readlines():
            # sentences.append(line.strip('\n').split(",")[0])
            try:
                scmd_line = line.rstrip('\n').rsplit(",")
                sentences.append(scmd_line[:-1]*int(scmd_line[-1]))
            except Exception as e:
                pass
    return sentences

@click.group()
def cli():
    pass

@cli.command()
@click.option('--data',help="train data")
@click.option('--o',help="output filename")
@click.option('--k',default=10, help="Cluster number ")
def w2vecluster(data,o,k):
    """
        word2vec & have a cluster
    """

    if not os.path.isfile(data):
        print("Please make sure your file was exists.")
        sys.exit(1)

    sentences = load_file(data)

    model = word2vec.Word2Vec(sentences, min_count=10)
    word_vectors = model.wv.syn0
    n_words = word_vectors.shape[0]
    vec_size = word_vectors.shape[1]

    #  K means training
    kmeans = KMeans(n_clusters= k, n_jobs=-1, random_state=0)
    idx = kmeans.fit_predict(word_vectors)

    # Type & Word
    word_centroid_list = list(zip(model.wv.index2word, idx))
    word_centroid_list_sort = sorted(word_centroid_list, key=lambda el: el[1], reverse=False)

    with open(o, 'w') as output:
        output.write("srv_cmd\srv_cmd_cluster\n")
        for word_centroid in word_centroid_list_sort:
            line = word_centroid[0] + '\t' + str(word_centroid[1]) + '\n'
            output.write(line)

if __name__ == '__main__':
    cli()