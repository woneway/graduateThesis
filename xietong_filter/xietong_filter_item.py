#-*- coding: utf-8 -*-
'''
Created on 2018/4/22
@author: woneway
'''
import sys
import random
import math
import os
from operator import itemgetter

from collections import defaultdict

random.seed(0)


class ItemBasedCF(object):
    ''' TopN recommendation - Item Based Collaborative Filtering '''

    def __init__(self):
        self.trainset = {}
        self.testset = {}

        self.n_sim_product = 20
        self.n_rec_product = 10

        self.product_sim_mat = {}
        self.product_popular = {}
        self.product_count = 0

        print('Similar product number = %d' % self.n_sim_product, file=sys.stderr)
        print('Recommended product number = %d' %
              self.n_rec_product, file=sys.stderr)

    @staticmethod
    def loadfile(filename):
        ''' load a file, return a generator. '''
        fp = open(filename, 'r')
        for i, line in enumerate(fp):
            yield line.strip('\r\n')
            if i % 100000 == 0:
                print ('loading %s(%s)' % (filename, i), file=sys.stderr)
        fp.close()
        print ('load %s succ' % filename, file=sys.stderr)

    def generate_dataset(self, filename, pivot=0.7):
        ''' load rating data and split it to training set and test set '''
        trainset_len = 0
        testset_len = 0

        for line in self.loadfile(filename):
            user, product, rating= line.split(',')
            # split the data by pivot
            if random.random() < pivot:
                self.trainset.setdefault(user, {})
                self.trainset[user][product] = int(rating)
                trainset_len += 1
            else:
                self.testset.setdefault(user, {})
                self.testset[user][product] = int(rating)
                testset_len += 1

        print ('split training set and test set succ', file=sys.stderr)
        print ('train set = %s' % trainset_len, file=sys.stderr)
        print ('test set = %s' % testset_len, file=sys.stderr)

    def calc_product_sim(self):
        ''' calculate product similarity matrix '''
        print('counting products number and popularity...', file=sys.stderr)

        for user, products in self.trainset.items():
            for product in products:
                # count item popularity
                if product not in self.product_popular:
                    self.product_popular[product] = 0
                self.product_popular[product] += 1

        print('count products number and popularity succ', file=sys.stderr)

        # save the total number of products
        self.product_count = len(self.product_popular)
        print('total product number = %d' % self.product_count, file=sys.stderr)

        # count co-rated users between items
        itemsim_mat = self.product_sim_mat
        print('building co-rated users matrix...', file=sys.stderr)

        for user, products in self.trainset.items():
            for m1 in products:
                itemsim_mat.setdefault(m1, defaultdict(int))
                for m2 in products:
                    if m1 == m2:
                        continue
                    itemsim_mat[m1][m2] += 1

        print('build co-rated users matrix succ', file=sys.stderr)

        # calculate similarity matrix
        print('calculating product similarity matrix...', file=sys.stderr)
        simfactor_count = 0
        PRINT_STEP = 2000000

        for m1, related_products in itemsim_mat.items():
            for m2, count in related_products.items():
                itemsim_mat[m1][m2] = count / math.sqrt(
                    self.product_popular[m1] * self.product_popular[m2])
                simfactor_count += 1
                if simfactor_count % PRINT_STEP == 0:
                    print('calculating product similarity factor(%d)' %
                          simfactor_count, file=sys.stderr)

        print('calculate product similarity matrix(similarity factor) succ',
              file=sys.stderr)
        print('Total similarity factor number = %d' %
              simfactor_count, file=sys.stderr)

    def recommend(self, user):
        ''' Find K similar products and recommend N products. '''
        K = self.n_sim_product
        N = self.n_rec_product
        rank = {}
        watched_products = self.trainset[user]

        for product, rating in watched_products.items():
            for related_product, similarity_factor in sorted(self.product_sim_mat[product].items(),
                                                           key=itemgetter(1), reverse=True)[:K]:
                if related_product in watched_products:
                    continue
                rank.setdefault(related_product, 0)
                rank[related_product] += similarity_factor * rating
        # return the N best products
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    def evaluate(self):
        ''' print evaluation result: precision, recall, coverage and popularity '''
        print('Evaluation start...', file=sys.stderr)

        N = self.n_rec_product
        #  varables for precision and recall
        hit = 0
        rec_count = 0
        test_count = 0
        # varables for coverage
        all_rec_products = set()
        # varables for popularity
        popular_sum = 0

        for i, user in enumerate(self.trainset):
            if i % 500 == 0:
                print ('recommended for %d users' % i, file=sys.stderr)
            test_products = self.testset.get(user, {})
            rec_products = self.recommend(user)
            for product, _ in rec_products:
                if product in test_products:
                    hit += 1
                all_rec_products.add(product)
                popular_sum += math.log(1 + self.product_popular[product])
            rec_count += N
            test_count += len(test_products)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_products) / (1.0 * self.product_count)
        popularity = popular_sum / (1.0 * rec_count)

        print ('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' %
               (precision, recall, coverage, popularity), file=sys.stderr)


if __name__ == '__main__':
    ratingfile = os.path.join('xietong_filter', 'xietong.csv')
    itemcf = ItemBasedCF()
    itemcf.generate_dataset(ratingfile)
    itemcf.calc_product_sim()
    itemcf.evaluate()