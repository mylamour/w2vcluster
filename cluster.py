import os
import re
import sys
import click

from simhash import Simhash
from sklearn.cluster import KMeans, Birch
from gensim.models import word2vec

def w2v(filename):
    """
        You need customsize load_file function with special pre-process.
        In this situtaion, we use word2vec to have a pre-process
    """

    if not os.path.isfile(filename):
        print("Please make sure your file was exists.")
        sys.exit(1)

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

    model = word2vec.Word2Vec(sentences, min_count=10)
    word_vectors = model.wv.syn0

    return model, word_vectors

def schash(filename):
    """
        simhash compute
    """
    pass

def wordembeding(sentences):
    pass

def writetofile(ofile,word_centroid_list_sort):
    with open(ofile, 'w') as output:
        output.write("origin\tcluster_type\n")
        for word_centroid in word_centroid_list_sort:
            line = word_centroid[0] + '\t' + str(word_centroid[1]) + '\n'
            output.write(line)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--filename','-f',help="train data")
@click.option('--output','-o',help="output filename")
@click.option('--ktype','-k', default=10, phelp="Cluster number ")
def kmeans(filename,output,ktype):
    """
        use Kmeans have a cluster
    """
    model, word_vectors = w2v(filename)

    n_words = word_vectors.shape[0]
    vec_size = word_vectors.shape[1]

    #  K means training
    kmeans = KMeans(n_clusters= ktype, n_jobs=-1, random_state=0)
    idx = kmeans.fit_predict(word_vectors)

    # Type & Word
    word_centroid_list = list(zip(model.wv.index2word, idx))
    word_centroid_list_sort = sorted(word_centroid_list, key=lambda el: el[1], reverse=False)

    # Write 2 file
    writetofile(output, word_centroid_list_sort)

@cli.command()
@click.option('--filename','-f',help="train data")
@click.option('--output','-o',help="output filename")
@click.option('--ktype','-k', default=10, help="Cluster number ")
def birch(filename,output,ktype):
    """
        use BIRCH cluster training
    """
    pass
    # model, word_vectors = w2v(filename)

    # n_words = word_vectors.shape[0]
    # vec_size = word_vectors.shape[1]

    # #  K means training
    # kmeans = KMeans(n_clusters= ktype, n_jobs=-1, random_state=0)
    # idx = kmeans.fit_predict(word_vectors)

    # # Use Simhash
    # word_centroid_list = list(zip(model.wv.index2word, idx))
    # word_centroid_list_simhash = [(Simhash(get_features(item[0])).value,item[1]) for item in word_centroid_list]

    # Use BIRCH training
    # better: cf is 4, sample in cs is 20
    brc = Birch(branching_factor=50, n_clusters=None, threshold=0.5,compute_labels=True)
    # brc.fit(word_centroid_list_simhash)
    brc.fit_predict(word_centroid_list_simhash)

if __name__ == '__main__':
    cli()