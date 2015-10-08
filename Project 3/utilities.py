# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:14:13 2015

@author: Kya
"""
from __future__ import division
import re
import numpy as np
import pandas as pd


def make_data_set(datafile, label):
    dataset = []
    data = datafile.read()
    entries = data.split('\n\n')
    value = ''

    if label == 'per:spouse':
        value = 'PERSON'
    if label == 'per:employee of':
        value = 'ORGANIZATION'
    if label == 'org:country of headquarters':
        value = 'LOCATION'
    if label == 'org top members/employees':
        value = 'PERSON'

    for e in entries:
        lines = e.split('\n')
        entity = ''
        filler = ''
        goodfeatures = []
        tokens = []
        depend = []

        for l in lines:
            if l.startswith('ENTITY'):
                entity = l
                esplit = entity.split(':', 1)
                entity = esplit[1].lstrip()
            if l.startswith('SLOT'):
                filler = l
                fsplit = filler.split(':', 1)
                filler = fsplit[1].lstrip()
            if l.startswith('TOKEN'):
                t = l
                tsplit = t.split(':', 1)
                tokens.append(tsplit[1].lstrip())
            if l.startswith('DEPEND'):
                d = l
                dsplit = d.split(':', 1)
                depend.append(dsplit[1].lstrip())

        t2 = []  # dependencies index throwaway
        for t in tokens:
            t2.append(t)

        indexes = []
        for t in t2:
            words = t.split()
            words = [{'word': s[0], 'pos': s[1], 'ne': s[2]} for s in [w.split('/', 2) for w in words]]
            indexes = words

        dependencies = []
        for d in depend:
            dmatch = re.findall(r'\d+\s\d+\s[a-z]+', d)
            dsplit = []
            for d in dmatch:
                dsplit.append(d.split())
            dlabels = [{'head': int(d[0]) - 1, 'modifier': int(d[1]) - 1, 'label': d[2]} for d in dsplit]
            dependencies = dlabels

        # chunk together words with same NE, resulting list of words is checked against existence of entity, filler, and candidates
        nil_can = []  # list of nil candidates
        for t in tokens:
            words = t.split()
            words = [{'word': s[0], 'pos': s[1], 'ne': s[2]} for s in
                     [w.split('/', 2) for w in words if not w.startswith('http:')]]
            for w in xrange(len(words) - 1):
                if w < len(words):
                    if words[w]['ne'] != 'O':
                        if w + 1 < len(words):
                            if words[w]['ne'] == words[w + 1]['ne']:
                                nw = words[w]['word'] + ' ' + words[w + 1]['word']
                                words[w]['word'] = nw
                                words[w + 1]['ne'] = '-'  # flag for deletion
                                if w + 2 < len(words):
                                    if words[w]['ne'] == words[w + 2]['ne']:
                                        nw = nw + ' ' + words[w + 2]['word']
                                        words[w]['word'] = nw
                                        words[w + 2]['ne'] = '-'
                                        if w + 3 < len(words):
                                            if words[w]['ne'] == words[w + 3]['ne']:
                                                nw = nw + ' ' + words[w + 3]['word']
                                                words[w]['word'] = nw
                                                words[w + 3]['ne'] = '-'
                words = [w for w in words if w['ne'] != '-']  # delete all the entries flagged for deletion

            for w in words:
                if w['ne'] == value and not re.search(entity, w['word']) and not re.search(filler, w['word']):
                    nil_can.append(w)

        # ===========================================================================================
        # sometimes filler is Single, so...
        filler_exceptions = ['Single', 'Children', 'Married', 'Divorced']
        if filler in filler_exceptions:
            # make lexical feature
            entity_split = entity.lower().split()
            index_entity = []
            entity0_index = ''
            entity_last = ''
            entity_length = len(entity_split)
            e_index_count = 0

            for i in xrange(len(indexes) - entity_length):
                e_index_count += 1
                if indexes[i]['word'].lower() == entity_split[0] and indexes[i + (entity_length - 1)]['word'].lower() == \
                        entity_split[entity_length - 1]:
                    entity0_index = e_index_count - 1

            for i in xrange(entity_length):
                index_entity.append(entity0_index + i)

            entity_last = index_entity[entity_length - 1]
            first0 = index_entity[0]
            firstn = entity_last
            first_indexes = index_entity

            lleft = []
            lright = []

            for i in xrange(len(indexes)):
                if i < first0:
                    lleft.append(indexes[i])
                if i > firstn:
                    lright.append(indexes[i])

            leftwords = []
            rightwords = []

            for i in lleft:
                word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                leftwords.append(word)
            leftwords = ' '.join(leftwords)
            goodfeatures.append(leftwords)

            for i in lright:
                word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                rightwords.append(word)
            rightwords = ' '.join(rightwords)
            goodfeatures.append(rightwords)

            # make syntactic feature
            sleft = []
            sright = []
            for d in dependencies:
                head = d['head']
                mod = d['modifier']
                if head in first_indexes or mod in first_indexes:
                    if head < first0 or mod < first0:
                        sleft.append(d)
                    if head > firstn or mod > firstn:
                        sright.append(d)

            rw_1 = []
            rw_2 = []
            lw_1 = []
            lw_2 = []
            if sleft:
                if sleft[0]:
                    lw_1.append(sleft[0])
                    lw_2.append(sleft[0])
                if len(sleft) == 2:
                    lw_2.append(sleft[1])
            if sright:
                if sright[0]:
                    rw_1.append(sright[0])
                    rw_2.append(sright[0])
                if len(sright) == 2:
                    rw_2.append(sright[1])

            # print lw_2, rw_2
            if rw_1:
                for r in rw_1:
                    if r['head'] != str:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                for r in rw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                rw_1 = x
            if rw_2:
                for r in rw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in rw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                rw_2 = ' '.join(rx)
            if lw_1:
                for r in lw_1:
                    r['head'] = indexes[r['head']]['word']
                    r['modifier'] = indexes[r['modifier']]['word']
                for r in lw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                lw_1 = x
            if lw_2:
                for r in lw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in lw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                lw_2 = ' '.join(rx)

            if not rw_1:
                rw_1 = ''
            if not rw_2:
                rw_2 = ''
            if not lw_1:
                lw_1 = ''
            if not lw_2:
                lw_2 = ''

            # put together the feature
            f01 = rw_1
            f02 = rw_2
            f10 = lw_1
            f11 = lw_1 + ' ' + rw_1
            f12 = lw_1 + ' ' + rw_2
            f20 = lw_2
            f21 = lw_2 + ' ' + rw_1
            f22 = lw_2 + ' ' + rw_2

            # goodfeatures.append(f00)
            goodfeatures.append(f01)
            goodfeatures.append(f02)
            goodfeatures.append(f10)
            goodfeatures.append(f11)
            goodfeatures.append(f12)
            goodfeatures.append(f20)
            goodfeatures.append(f21)
            goodfeatures.append(f22)

        # ===========================================================================================
        else:  # normal fillers
            # get index of entity and filler
            entity_split = entity.lower().split()
            filler_split = filler.lower().split()
            index_entity = []
            index_filler = []
            entity0_index = ''
            filler0_index = ''
            entity_last = ''
            filler_last = ''
            entity_length = len(entity_split)
            filler_length = len(filler_split)
            e_index_count = 0
            f_index_count = 0

            for i in xrange(len(indexes) - entity_length):
                e_index_count += 1
                if indexes[i]['word'].lower() == entity_split[0] and indexes[i + (entity_length - 1)]['word'].lower() == \
                        entity_split[entity_length - 1]:
                    entity0_index = e_index_count - 1

            for i in xrange(len(indexes) - filler_length):
                f_index_count += 1
                if indexes[i]['word'].lower() == filler_split[0] and indexes[i + (filler_length - 1)]['word'].lower() == \
                        filler_split[filler_length - 1]:
                    filler0_index = f_index_count - 1

            for i in xrange(entity_length):
                index_entity.append(entity0_index + i)

            for i in xrange(filler_length):
                index_filler.append(filler0_index + i)

            entity_last = index_entity[entity_length - 1]
            filler_last = index_filler[filler_length - 1]

            first0 = ''
            firstn = ''
            second0 = ''
            secondn = ''
            first_indexes = []
            second_indexes = []

            if index_entity[0] < index_filler[0]:
                first0 = index_entity[0]
                firstn = entity_last
                second0 = index_filler[0]
                secondn = filler_last
                first_indexes = index_entity
                second_indexes = index_filler
            else:
                first0 = index_filler[0]
                firstn = filler_last
                second0 = index_entity[0]
                secondn = entity_last
                first_indexes = index_filler
                second_indexes = index_entity

            # make lexical goodfeatures
            lleft = []
            lbet = []
            lright = []

            for i in xrange(len(indexes)):
                if i < first0:
                    lleft.append(indexes[i])
                elif i > firstn and i < second0:
                    lbet.append(indexes[i])
                elif i > secondn:
                    lright.append(indexes[i])

            leftwords = []
            betwords = []
            rightwords = []

            for i in lleft:
                word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                leftwords.append(word)
            leftwords = ' '.join(leftwords)
            goodfeatures.append(leftwords)

            for i in lbet:
                word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                betwords.append(word)
            betwords = ' '.join(betwords)
            goodfeatures.append(betwords)

            for i in lright:
                word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                rightwords.append(word)
            rightwords = ' '.join(rightwords)
            goodfeatures.append(rightwords)

            # make syntactic good features
            sleft = []
            sright = []
            s_dp_begin = []  # potential beginning of dependency path
            s_dp_end = []  # potential end of dependency path
            sbet = []
            for d in dependencies:
                head = d['head']
                mod = d['modifier']
            if head in first_indexes or mod in first_indexes:
                if head < first0 or mod < first0:
                    sleft.append(d)
                if head > firstn or mod > firstn:
                    s_dp_begin.append(d)
            if head in second_indexes or mod in second_indexes:
                if head > secondn or mod > secondn:
                    sright.append(d)
                if head < second0 or mod < second0:
                    s_dp_end.append(d)
            if head > firstn and head < second0 and mod > firstn and mod < second0:
                sbet.append(d)

            dependency_path = []
            if s_dp_begin and s_dp_end:
                for i in s_dp_begin:
                    path = []
                    path.append(i)
                    a = ''
                    if i['head'] in first_indexes:
                        a = i['modifier']
                    else:
                        a = i['head']
                    if a not in second_indexes:
                        c = 0
                        for s in s_dp_end:
                            b = ''
                            if s['head'] < second0:
                                b = s['head']
                            else:
                                b = s['modifier']
                            if a == b:
                                path.append(s)
                            else:
                                if sbet:
                                    d = 0
                                    for i in sbet:
                                        if a == i['head'] or a == i['modifier']:
                                            path.append(i)
                                        if a == i['head']:
                                            a = i['modifier']
                                        else:
                                            a = i['head']
                                        break
                                    d += 1
                                    if d == len(sbet):
                                        path = []
                                        break
                        c += 1
                        if c == len(s_dp_end):
                            path = []
                            break
                dependency_path = path

            # put together the feature
            # get windows
            rw_1 = []
            rw_2 = []
            lw_1 = []
            lw_2 = []
            if sleft:
                if sleft[0]:
                    lw_1.append(sleft[0])
                    lw_2.append(sleft[0])
                if len(sleft) == 2:
                    lw_2.append(sleft[1])
            if sright:
                if sright[0]:
                    rw_1.append(sright[0])
                    rw_2.append(sright[0])
                if len(sright) == 2:
                    rw_2.append(sright[1])

            if rw_1:
                for r in rw_1:
                    if r['head'] != str:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                for r in rw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                rw_1 = x

            if rw_2:
                for r in rw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in rw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                rw_2 = ' '.join(rx)

            if lw_1:
                for r in lw_1:
                    r['head'] = indexes[r['head']]['word']
                    r['modifier'] = indexes[r['modifier']]['word']
                for r in lw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                lw_1 = x

            if lw_2:
                for r in lw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in lw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                lw_2 = ' '.join(rx)

            if dependency_path:
                for d in dependency_path:
                    if type(d[
                                'head']) == int:  # because for whatever reason it really didn't want to accept that d['head'] is infact an int
                        # convert indexes to words
                        d['head'] = indexes[d['head']]['word']
                        d['modifier'] = indexes[d['modifier']]['word']
                        # convert dependencies from dict to string, join dependencies together into single string
                dp = []
                for d in dependency_path:
                    x = str(d['head']) + '/' + str(d['modifier']) + '/' + str(d['label'])
                    dp.append(x)
                dependency_path = ' '.join(dp)

            # turn everything into a str to get around concatenation issues
            if not dependency_path:
                dependency_path = ''
            if not rw_1:
                rw_1 = ''
            if not rw_2:
                rw_2 = ''
            if not lw_1:
                lw_1 = ''
            if not lw_2:
                lw_2 = ''

            # put together the feature
            f00 = dependency_path
            f01 = dependency_path + ' ' + rw_1
            f02 = dependency_path + ' ' + rw_2
            f10 = lw_1 + ' ' + dependency_path
            f11 = lw_1 + ' ' + dependency_path + ' ' + rw_1
            f12 = lw_1 + ' ' + dependency_path + ' ' + rw_2
            f20 = lw_2 + ' ' + dependency_path
            f21 = lw_2 + ' ' + dependency_path + rw_1
            f22 = lw_2 + ' ' + dependency_path + rw_2

            goodfeatures.append(f00)
            goodfeatures.append(f01)
            goodfeatures.append(f02)
            goodfeatures.append(f10)
            goodfeatures.append(f11)
            goodfeatures.append(f12)
            goodfeatures.append(f20)
            goodfeatures.append(f21)
            goodfeatures.append(f22)


        # ===========================================================================================
        # make the 'real' entity_pair entry
        goodfeatures = [g for g in goodfeatures if g != '' and g != ' ' and g != '  ']  # filter out empty features
        entity_pair = {'entity': entity, 'filler': filler, 'label': label, 'features': goodfeatures}
        dataset.append(entity_pair)

        # ===========================================================================================
        # make nil candidate pairs + features
        # if len(nil_can) >= 2:
        for n in nil_can[:1]:  # Question 2!
            nilfeatures = []
            nil = 'nil'

            can_split = n['word'].split()
            index_can = []
            can0_index = ''
            can_last = ''
            can_length = len(can_split)
            c_index_count = 0

            for i in xrange(len(indexes) - can_length):
                c_index_count += 1
                if indexes[i]['word'] == can_split[0] and indexes[i + (can_length - 1)]['word'] == can_split[
                            can_length - 1]:
                    can0_index = c_index_count - 1
                    for i in xrange(can_length):
                        index_can.append(can0_index + i)

                    can_last = index_can[can_length - 1]
                    first0 = ''
                    firstn = ''
                    second0 = ''
                    secondn = ''

                    if index_entity[0] < index_can[0]:
                        first0 = index_entity[0]
                        firstn = entity_last
                        second0 = index_can[0]
                        secondn = can_last
                    else:
                        first0 = index_can[0]
                        firstn = can_last
                        second0 = index_entity[0]
                        secondn = entity_last

                    lleft = []
                    lbet = []
                    lright = []

                    for i in xrange(len(indexes)):
                        if i < first0:
                            lleft.append(indexes[i])
                        elif i > firstn and i < second0:
                            lbet.append(indexes[i])
                        elif i > secondn:
                            lright.append(indexes[i])

                    leftwords = []
                    betwords = []
                    rightwords = []

                    for i in lleft:
                        word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                        leftwords.append(word)
                    leftwords = ' '.join(leftwords)
                    nilfeatures.append(leftwords)

                    for i in lbet:
                        word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                        betwords.append(word)
                    betwords = ' '.join(betwords)
                    nilfeatures.append(betwords)

                    for i in lright:
                        word = i['word'] + '/' + i['pos'] + '/' + i['ne']
                        rightwords.append(word)
                    rightwords = ' '.join(rightwords)
                    nilfeatures.append(rightwords)

            # make nil syntactic feature
            sleft = []
            sright = []
            s_dp_begin = []  # potential beginning of dependency path
            s_dp_end = []  # potential end of dependency path
            sbet = []
            for d in dependencies:
                head = d['head']
                mod = d['modifier']
                if head in first_indexes or mod in first_indexes:
                    if head < first0 or mod < first0:
                        sleft.append(d)
                    if head > firstn or mod > firstn:
                        s_dp_begin.append(d)
                if head in second_indexes or mod in second_indexes:
                    if head > secondn or mod > secondn:
                        sright.append(d)
                    if head < second0 or mod < second0:
                        s_dp_end.append(d)
                if head > firstn and head < second0 and mod > firstn and mod < second0:
                    sbet.append(d)

            dependency_path = []
            if s_dp_begin and s_dp_end:
                for i in s_dp_begin:
                    path = []
                    path.append(i)
                    a = ''
                    if i['head'] in first_indexes:
                        a = i['modifier']
                    else:
                        a = i['head']
                    if a not in second_indexes:
                        c = 0
                        for s in s_dp_end:
                            b = ''
                            if s['head'] < second0:
                                b = s['head']
                            else:
                                b = s['modifier']
                            if a == b:
                                path.append(s)
                            else:
                                if sbet:
                                    d = 0
                                    for i in sbet:
                                        if a == i['head'] or a == i['modifier']:
                                            path.append(i)
                                            if a == i['head']:
                                                a = i['modifier']
                                            else:
                                                a = i['head']
                                            break
                                        d += 1
                                        if d == len(sbet):
                                            path = []
                                            break
                        c += 1
                        if c == len(s_dp_end):
                            path = []
                            break
                dependency_path = path

            # put together the feature
            # get windows
            rw_1 = []
            rw_2 = []
            lw_1 = []
            lw_2 = []
            if sleft:
                if sleft[0]:
                    lw_1.append(sleft[0])
                    lw_2.append(sleft[0])
                if len(sleft) == 2:
                    lw_2.append(sleft[1])
            if sright:
                if sright[0]:
                    rw_1.append(sright[0])
                    rw_2.append(sright[0])
                if len(sright) == 2:
                    rw_2.append(sright[1])

            if rw_1:
                for r in rw_1:
                    if r['head'] != str:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                for r in rw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                rw_1 = x

            if rw_2:
                for r in rw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in rw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                rw_2 = ' '.join(rx)

            if lw_1:
                for r in lw_1:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                for r in lw_1:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                lw_1 = x

            if lw_2:
                for r in lw_2:
                    if r['head'] == int:
                        r['head'] = indexes[r['head']]['word']
                        r['modifier'] = indexes[r['modifier']]['word']
                rx = []
                for r in lw_2:
                    x = str(r['head']) + '/' + str(r['modifier']) + '/' + str(r['label'])
                    rx.append(x)
                lw_2 = ' '.join(rx)

            if dependency_path:
                for d in dependency_path:
                    if type(d[
                                'head']) == int:  # because for whatever reason it really didn't want to accept that d['head'] is infact an int
                        # convert indexes to words
                        d['head'] = indexes[d['head']]['word']
                        d['modifier'] = indexes[d['modifier']]['word']
                        # convert dependencies from dict to string, join dependencies together into single string
                dp = []
                for d in dependency_path:
                    x = str(d['head']) + '/' + str(d['modifier']) + '/' + str(d['label'])
                    dp.append(x)
                dependency_path = ' '.join(dp)

            # turn everything into a str to get around concatenation issues
            if not dependency_path:
                dependency_path = ''
            if not rw_1:
                rw_1 = ''
            if not rw_2:
                rw_2 = ''
            if not lw_1:
                lw_1 = ''
            if not lw_2:
                lw_2 = ''

            # put together the feature
            f00 = dependency_path
            f01 = dependency_path + ' ' + rw_1
            f02 = dependency_path + ' ' + rw_2
            f10 = lw_1 + ' ' + dependency_path
            f11 = lw_1 + ' ' + dependency_path + ' ' + rw_1
            f12 = lw_1 + ' ' + dependency_path + ' ' + rw_2
            f20 = lw_2 + ' ' + dependency_path
            f21 = lw_2 + ' ' + dependency_path + rw_1
            f22 = lw_2 + ' ' + dependency_path + rw_2

            nilfeatures.append(f00)
            nilfeatures.append(f01)
            nilfeatures.append(f02)
            nilfeatures.append(f10)
            nilfeatures.append(f11)
            nilfeatures.append(f12)
            nilfeatures.append(f20)
            nilfeatures.append(f21)
            nilfeatures.append(f22)

            # ===========================================================================================
            # make nil_entity_pair
            nilfeatures = [g for g in nilfeatures if
                           g != '' and g != ' ' and g != '  ']  # filer out empty features
            nil_entity_pair = {'entity': entity, 'filler': n['word'], 'label': nil, 'features': nilfeatures}
            dataset.append(nil_entity_pair)

    return dataset


def make_feature_vector(data, features):
    # borrowed from project 2a best submission

    fv = np.matrix(np.zeros((len(data), features.shape[0] + 1)))

    # Bias
    fv[:, 0] = 1

    for i, e in enumerate(data):
        # Regular Vector
        e = pd.Series(e)
        counts = e.value_counts()

        # Feature Vector
        for j, f in enumerate(features):
            if f in counts.index:
                fv[i, j + 1] = counts.ix[f]

    return fv


def compute_stats(gold, predicted, _class=''):
    tp = tn = fp = fn = 0

    for g, p in zip(gold, predicted):

        if g == p:
            if g == _class:
                tp += 1
            else:
                tn += 1

        else:
            if g == _class:
                fn += 1
            else:
                fp += 1

    return tp, tn, fp, fn


def compute_metrics(tp, tn, fp, fn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    f1 = 2 * (precision * recall / (precision + recall))

    return accuracy, precision, recall, f1


def print_metrics(accuracy, precision, recall, f1):
    print 'Accuracy:\t%.3f' % accuracy
    print 'Precision:\t%.3f' % precision
    print 'Recall:\t\t%.3f' % recall
    print 'F1:\t\t%.3f' % f1
