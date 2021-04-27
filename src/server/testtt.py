import collections
import math

class BLEU(tf.keras.metrics.Metric):
  def __init__(self, name = 'BLEU', **kwargs):
    super(BLEU, self).__init__(name = name, **kwargs)
    self.bleu = self.add_weight(name = 'ctp', initializer = 'zeros')

  def _get_ngrams(self, segment, max_order):
    """Extracts all n-grams upto a given maximum order from an input segment.
    Args:
      segment: text segment from which n-grams will be extracted.
      max_order: maximum length in tokens of the n-grams returned by this
          methods.
    Returns:
      The Counter containing all n-grams upto max_order in segment
      with a count of how many times each n-gram occurred.
    """
    ngram_counts = collections.Counter()
    for order in range(1, max_order + 1):
      for i in range(0, len(segment) - order + 1):
        ngram = tuple(segment[i:i+order])
        ngram_counts[ngram] += 1
    return ngram_counts

  def _compute_bleu_score(self,x, y,
                          max_order=4,smooth=False):
    """Computes BLEU score of translated segments against one or more references.
    Args:
      reference_corpus: list of lists of references for each translation. Each
        reference should be tokenized into a list of tokens.
      translation_corpus: list of translations to score. Each translation
        should be tokenized into a list of tokens.
      max_order: Maximum n-gram order to use when computing BLEU score.
      smooth: Whether or not to apply Lin et al. 2004 smoothing.
    Returns:
      3-Tuple with he BLEU score, n-gram precisions, geometric mean of n-gram
      precisions and brevity penalty.
    """
    # decoding
    y = tf.math.argmax(y, axis = 2)

    def _func(reference_corpus, translation_corpus):
      reference_corpus = reference_corpus.numpy()
      translation_corpus = translation_corpus.numpy()
      #tf.print(reference_corpus.shape, translation_corpus.shape)
      matches_by_order = [0] * max_order
      possible_matches_by_order = [0] * max_order
      reference_length = 0
      translation_length = 0
      for (reference, translation) in zip(reference_corpus,
                                          translation_corpus):
        reference_length += len(reference)
        translation_length += len(translation)
        #tf.print(len(reference), len(translation))
        merged_ref_ngram_counts = collections.Counter()
        
        merged_ref_ngram_counts |= self._get_ngrams(reference, max_order)
        translation_ngram_counts = self._get_ngrams(translation, max_order)
        overlap = translation_ngram_counts & merged_ref_ngram_counts
        for ngram in overlap:
          matches_by_order[len(ngram)-1] += overlap[ngram]
        for order in range(1, max_order+1):
          possible_matches = len(translation) - order + 1
          if possible_matches > 0:
            possible_matches_by_order[order-1] += possible_matches

      precisions = [0] * max_order
      for i in range(0, max_order):
        if smooth:
          precisions[i] = ((matches_by_order[i] + 1.) /
                          (possible_matches_by_order[i] + 1.))
        else:
          if possible_matches_by_order[i] > 0:
            precisions[i] = (float(matches_by_order[i]) /
                            possible_matches_by_order[i])
          else:
            precisions[i] = 0.0
      #tf.print('precision', precisions)
      if min(precisions) > 0:
        p_log_sum = sum((1. / max_order) * math.log(p) for p in precisions)
        geo_mean = math.exp(p_log_sum)
      else:
        geo_mean = 0

      ratio = float(translation_length) / reference_length

      if ratio > 1.0:
        bp = 1.
      else:
        bp = math.exp(1 - 1. / ratio)

      bleu = geo_mean * bp
      #tf.print('bleu', bleu)
      return bleu

    bleu = tf.py_function(func = _func, inp = [x, y], Tout = tf.float32)
    return bleu

  def update_state(self, y_true, y_pred, sample_weight = None):
    bleu = self._compute_bleu_score(y_true, y_pred)
    self.bleu.assign(bleu)

  def result(self):
    return self.bleu

  def reset_states(self):
    self.bleu.assign(0)t
