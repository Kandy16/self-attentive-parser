import trees

basePath = '../self-attentive-parser/models/de_elmo/'#de_char_1_1/'
gold_treebank = trees.load_trees(basePath+'gold.txt')
predicted_treebank = trees.load_trees(basePath+'predicted.txt')

print("Loaded {:,} examples.".format(len(gold_treebank)))
print("Loaded {:,} examples.".format(len(predicted_treebank)))

for idx in range(len(predicted_treebank)):
    gold_sentences = [node.word for node in gold_treebank[idx].leaves()]
    predict_sentences =  [node.word for node in predicted_treebank[idx].leaves()]
    if(len(gold_sentences) == len(predict_sentences)):
        for idx1 in range(len(gold_sentences)):
            if(gold_sentences[idx1] != predict_sentences[idx1]):
                print('Sentence '+str(idx+1)+' fails! Not same')
                break
    else:
        print('Sentence ' + str(idx + 1) + ' fails! Not even same length')

# If nothing printed then the sentence ordering is perfect
failed_noun_count = 0
failed_verb_count = 0

total_noun_count = 0
total_verb_count = 0

for idx in range(len(predicted_treebank)):
    gold_tree_nodes = [gold_treebank[idx]]
    predicted_tree_nodes = [predicted_treebank[idx]]

    gold_nouns = []
    gold_verbs = []
    while gold_tree_nodes:
        node = gold_tree_nodes.pop()
        if isinstance(node, trees.InternalTreebankNode):
            gold_tree_nodes.extend(reversed(node.children))
            #print(node.label)
            if (node.label == 'NX-ON'):
                gold_nouns.extend([node.word for node in node.leaves()])
            if(node.label == 'LK'):
                gold_verbs.extend([node.word for node in node.leaves()])

    predicted_nouns = []
    predicted_verbs = []
    while predicted_tree_nodes:
        node = predicted_tree_nodes.pop()
        if isinstance(node, trees.InternalTreebankNode):
            predicted_tree_nodes.extend(reversed(node.children))
            if (node.label == 'NX-ON'):
                predicted_nouns.extend([node.word for node in node.leaves()])
            if (node.label == 'LK'):
                predicted_verbs.extend([node.word for node in node.leaves()])

    #print(gold_nouns, predicted_nouns)
    #print(gold_verbs, predicted_verbs)

    if(len(predicted_nouns) == len(gold_nouns)):# & len(predicted_nouns) > 0):
        for idx2 in range(len(predicted_nouns)):
            if(predicted_nouns[idx2] != gold_nouns[idx2]):
                failed_noun_count += 1
                break
    else:
        failed_noun_count += 1

    if (len(predicted_verbs) == len(gold_verbs)):# & len(predicted_verbs) > 0):
        for idx2 in range(len(predicted_verbs)):
            if (predicted_verbs[idx2] != gold_verbs[idx2]):
                failed_verb_count += 1
                break
    else:
        failed_verb_count += 1

    total_noun_count = total_noun_count + len(gold_nouns)
    total_verb_count = total_verb_count + len(gold_verbs)

print('For comparison of Nouns - '+str(total_noun_count - failed_noun_count) + ' success out of '+ str(total_noun_count))
print('For comparison of Verbs - '+str(total_verb_count - failed_verb_count) + ' success out of '+ str(total_verb_count))
