<TeXmacs|1.99.1>

<style|generic>

<\body>
  <doc-data|<doc-title|Web Search Project
  1>|<doc-author|<author-data|<author-name|Steven Xu, 350256>>>>

  <section|Database Creation and Storage>

  Data was stored using python's <with|font-shape|italic|pickle>, as the
  <with|font-shape|italic|shelve> module was too slow to be used on windows,
  which was the primary development platform.

  Only the frequency matrix was stored instead of the tf-idf matrix for
  flexibility, as the frequency matrix was needed to be used for later
  sections. The tf-idf matrix was then calculated upon initialization time
  when search queries were run.

  The frequency matrix was stored as a sparse row matrix. A sparse column
  matrix was not used as rows were accessed more often than columns.

  The inverted index was stored as a python dictionary, with each term
  mapping to a list of document id's.

  <section|TF-IDF Results>

  See results.txt.

  <section|Pivoted Length Normalization Results>

  Increasing <math|s> increeases the effect of unit-length normalization,
  which decreases the gain in weight long documents have. When <math|s=1>,
  all term vectors (documents) are normalized to the same length, which
  removes the effect of pivoted length normalization.

  See results.txt.

  <section|Requiring All Query Terms>

  See results.txt

  <section|Disambiguation by Source Context>

  <subsection|Rocchio's>

  We can perform query expansion using the user's current forum post and the
  subforum he's in. Let <math|q<rsub|0>> be the original query,
  <math|d<rsub|u>> be the user's current post and <math|D<rsub|F>> be the set
  of posts in the subforum, then we use the expanded query vector:

  <\equation*>
    q<rsub|e>=\<alpha\>q<rsub|0>+\<beta\>d<rsub|u>+\<gamma\><frac|1|<around*|\||D<rsub|F>|\|>><big|sum><rsub|d\<in\>D<rsub|F>>d
  </equation*>

  For efficiency we then take the top <math|k> terms which are common to the
  wikipedia articles.

  <subsubsection|Forum Weights>

  Tf-idf weights for forum posts perform poorly, as they can down-weight
  terms like ``apache'', which are common in the forums but not the
  encyclopedia.

  Instead, the following weighting scheme was used which tries to extract
  common terms in the forum but not in wikipedia:

  <\equation*>
    w<rsub|t>=log<around*|(|1+<frac|1|<around*|\||T<rsub|A>|\|>><big|sum><rsub|d\<in\>D<rsub|A>>f<rsub|d,t>|)>-log<around*|(|1+<frac|1|<around*|\||T<rsub|W>|\|>><big|sum><rsub|d\<in\>D<rsub|W>>f<rsub|d,t>|)>
  </equation*>

  Where <math|D<rsub|A>> is the set of apache forum posts and
  <math|D<rsub|W>> the set of wikipedia documents, and <math|T<rsub|A>>,
  <math|T<rsub|W>> the set of terms.

  <subsection|Rocchio's with SVD>

  We can use still rocchio's, but first transform the set of wikipedia
  documents and apache forum documents into a semantic space using SVD. We
  include the forum documents to extract more relevant topics.

  We can then use Rocchio's, then instead of using term weights, we are using
  topic weights, which might provide more query expansion. This gives more
  importance to topics contained in the subforum and in the post.

  <subsection|Cluster Distances>

  We can interpret the forum documents as a hierarchical cluster, and give a
  bonus weight to wikipedia documents closer to the clusters of forum
  documents that we are looking for. Let <math|d> be a distance function
  between a document and a set of documents, then we want a document,
  <math|r> which minimizes:

  <\equation*>
    \<alpha\>\<cdot\>d<around*|(|r,<around*|{|q<rsub|0>|}>|)>+\<beta\>\<cdot\>d<around*|(|r,<around*|{|d<rsub|u>|}>|)>+\<gamma\>\<cdot\>d<around*|(|r,D<rsub|f>|)>
  </equation*>

  If we take the average distance, <math|d<around*|(|r,D|)>=<frac|1|<around*|\||D|\|>><big|sum><rsub|d\<in\>D>r\<cdot\>d>,
  then we get rocchio's query expansion. But we can also take the minimum
  distance to the cluster, using <math|d<around*|(|r,D|)>=min<big|sum><rsub|d\<in\>D>r\<cdot\>d>.

  <section|Disambiguation Implementation>

  See results.txt.
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|1>>
    <associate|auto-10|<tuple|6|3>>
    <associate|auto-11|<tuple|5|3>>
    <associate|auto-12|<tuple|6|3>>
    <associate|auto-13|<tuple|5|3>>
    <associate|auto-14|<tuple|5.1|4>>
    <associate|auto-15|<tuple|5.2|4>>
    <associate|auto-16|<tuple|5.3|4>>
    <associate|auto-17|<tuple|5.1|4>>
    <associate|auto-18|<tuple|5.2|4>>
    <associate|auto-19|<tuple|5.3|5>>
    <associate|auto-2|<tuple|2|1>>
    <associate|auto-20|<tuple|5.1|5>>
    <associate|auto-21|<tuple|5.2|?>>
    <associate|auto-22|<tuple|5.3|?>>
    <associate|auto-3|<tuple|3|1>>
    <associate|auto-4|<tuple|4|1>>
    <associate|auto-5|<tuple|5|2>>
    <associate|auto-6|<tuple|5.1|2>>
    <associate|auto-7|<tuple|5.1.1|2>>
    <associate|auto-8|<tuple|5.2|2>>
    <associate|auto-9|<tuple|5.3|3>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Database
      Creation and Storage> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>TF-IDF
      Results> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|3<space|2spc>Pivoted
      Length Normalization Results> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|4<space|2spc>Requiring
      All Query Terms> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|5<space|2spc>Disambiguation
      by Source Context> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5><vspace|0.5fn>

      <with|par-left|<quote|1tab>|5.1<space|2spc>Rocchio's
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-6>>

      <with|par-left|<quote|2tab>|5.1.1<space|2spc>Forum Weights
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-7>>

      <with|par-left|<quote|1tab>|5.2<space|2spc>Rocchio's with SVD
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-8>>

      <with|par-left|<quote|1tab>|5.3<space|2spc>Cluster Distances
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-9>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|6<space|2spc>Disambiguation
      Implementation> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-10><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>