<TeXmacs|1.99.1>

<style|generic>

<\body>
  <section|Speeding Up Clustering>

  To speed up generating <math|P> given an inverted index, for each document
  we can compute only the similarities for the documents which share it's
  terms.

  Let there be <math|n> documents, <math|t> terms in a document on average,
  and <math|d> documents a term appears in on average.

  To calculate the upper-trianglar distance matrix, we can assume without
  loss of generality that we calculate the full matrix, as there is only a
  constant factor of 2 difference. Each document needs to have it's
  similarity computed for <math|t\<cdot\>d> documents on average, hence take
  <math|O<around*|(|n\<cdot\>t\<cdot\>d|)>> total time. Getting the nearest
  neighbors has the same time complexity. This is faster if
  <math|t\<cdot\>d\<ll\>n>.

  The assumptions are not very good, as due to the Zipf distribution, some
  documents will contain many terms and some terms will appear in most
  documents.

  We can ignore terms with low weight for all documents to speed up the
  similarity computation.

  \;
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|?>>
    <associate|auto-2|<tuple|1|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Clustering>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>