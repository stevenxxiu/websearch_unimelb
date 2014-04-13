<TeXmacs|1.99.1>

<style|generic>

<\body>
  <doc-data|<doc-title|Web Search Project
  1>|<doc-author|<author-data|<author-name|Steven Xu, 350256>>>>

  <section|Database Creation and Storage>

  The inverted index was stored using mongodb, as the
  <with|font-shape|italic|shelve> module was too slow to be used on windows,
  which was the primary development platform. Two collections were created,
  one being the tf-idf database, the other being the inverted index.

  The tf-idf collection was stored using <math|<around*|(|docid,weights|)>>
  pairs, where <with|font-shape|italic|docid> is the article name of the
  wikipedia document, and weights being a tuple of
  <math|<around*|(|term,weight|)>> pairs. The collection was then indexed by
  <with|font-shape|italic|docid>.

  The inverted index was stored using <math|<around*|(|term,docids|)>> pairs,
  where <with|font-shape|italic|docids> consists of the list of docids of
  documents containing <with|font-shape|italic|term>.

  <section|TF-IDF Results>

  See results.txt.

  <section|Pivoted Length Normalization Results>

  See results.txt.

  <section|Requiring All Query Terms>

  See results.txt

  <section|Disambiguation by Source Context>

  <subsection|Rocchio's>

  We can perform query expansion using the user's current forum post and the
  subforum he's in. Let <math|q<rsub|0>> be the original query,
  <math|p<rsub|u>> be the user's current post and <math|P<rsub|f>> be the set
  of posts in the subforum, then we use the expanded query vector:

  <\equation*>
    q<rsub|e>=\<alpha\>q<rsub|0>+\<beta\>p<rsub|u>+\<gamma\><frac|1|<around*|\||P<rsub|f>|\|>><big|sum><rsub|p<rsub|f>\<in\>P<rsub|f>>p<rsub|f>
  </equation*>

  For efficiency we can then take the top <math|k> terms.

  <subsubsection|Forum Weights>

  Tf-idf weights for forum posts perform poorly, as they can down-weight
  terms like ``apache'', which are common in the forums but not the
  encyclopedia.

  Instead, the following weighting scheme was used which tries to extract
  common terms in the forum but not in wikipedia:

  <\equation*>
    w<rsub|t>=
  </equation*>

  <subsection|Rocchio's with SVD>

  We can use still rocchio's, but first transform the set of wikipedia
  documents and apache forum documents into a semantic space using SVD. We
  include the forum documents to extract more relevant topics.

  We can then use Rocchio's, then instead of using term weights, we are using
  topic weights, which might provide more query expansion. This gives more
  importance to topics contained in the subforum and in the post.

  <subsection|Cluster Distances>

  We can interpret the search document as clusters, and give a bonus weight
  to documents closer to the cluster of forum documents that we are looking
  for. Let <math|d> be a distance function between a document and a set of
  documents, then we want a document, <math|r> which minimizes:

  <\equation*>
    \<alpha\>\<cdot\>d<around*|(|r,<around*|{|q<rsub|0>|}>|)>+\<beta\>\<cdot\>d<around*|(|r,<around*|{|p<rsub|u>|}>|)>+\<gamma\>\<cdot\>d<around*|(|r,P<rsub|f>|)>
  </equation*>

  If we take the average distance, <math|d<around*|(|r,P|)>=<frac|1|<around*|\||P|\|>><big|sum><rsub|p\<in\>P>r\<cdot\>p>,
  then we get rocchio's. But we can also take the minimum distance to the
  cluster, using <math|d<around*|(|r,P|)>=min<big|sum><rsub|p\<in\>P>r\<cdot\>p>.

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
    <\associate|table>
      <tuple|normal|Query results for ``apache''|<pageref|auto-3>>

      <tuple|normal|Query results for ``apache aries''|<pageref|auto-4>>

      <tuple|normal|Query results for ``apache apache
      aries''|<pageref|auto-5>>

      <tuple|normal|Query results for ``apache''|<pageref|auto-7>>

      <tuple|normal|Query results for ``apache aries''|<pageref|auto-8>>

      <tuple|normal|Query results for ``apache apache
      aries''|<pageref|auto-9>>

      <tuple|normal|Query results for ``apache james''|<pageref|auto-12>>

      <tuple|normal|Query results for ``apache forrest''|<pageref|auto-13>>

      <tuple|normal|Query results for ``apache aries''|<pageref|auto-14>>

      <tuple|normal|Query results for ``apache james''|<pageref|auto-16>>

      <tuple|normal|Query results for ``apache forrest''|<pageref|auto-17>>

      <tuple|normal|Query results for ``apache aries''|<pageref|auto-18>>
    </associate>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Database
      Creation and Storage> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>TF-IDF
      Results> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|3<space|2spc>Pivoted
      Length Normalization Results> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-6><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|4<space|2spc>Requiring
      All Query Terms> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-10><vspace|0.5fn>

      <with|par-left|<quote|1tab>|4.1<space|2spc>Without Requiring All Terms
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-11>>

      <with|par-left|<quote|1tab>|4.2<space|2spc>Requiring All Terms
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-15>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|5<space|2spc>Disambiguation
      by Source Context> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-19><vspace|0.5fn>

      <with|par-left|<quote|1tab>|5.1<space|2spc>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-20>>
    </associate>
  </collection>
</auxiliary>