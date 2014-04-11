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

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Apache_Isis>|<cell|0.232290>>|<row|<cell|Southern_Apache_Museum>|<cell|0.216969>>|<row|<cell|Apache_Excalibur>|<cell|0.206819>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.199597>>|<row|<cell|Apache_Incubator>|<cell|0.195659>>|<row|<cell|Fort_Apache>|<cell|0.193399>>|<row|<cell|Apache_Directory>|<cell|0.189683>>|<row|<cell|Apache_Forrest>|<cell|0.188877>>|<row|<cell|Western_Apache_language>|<cell|0.187994>>|<row|<cell|Plains_Apache_language>|<cell|0.186527>>>>>|Query
  results for ``apache''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Aries>|<cell|0.278531>>|<row|<cell|Apache_Aries>|<cell|0.250711>>|<row|<cell|Apache_Isis>|<cell|0.232290>>|<row|<cell|Southern_Apache_Museum>|<cell|0.216969>>|<row|<cell|Apache_Excalibur>|<cell|0.206819>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.199597>>|<row|<cell|Apache_Incubator>|<cell|0.195659>>|<row|<cell|Fort_Apache>|<cell|0.193399>>|<row|<cell|Apache_Directory>|<cell|0.189683>>|<row|<cell|Apache_Forrest>|<cell|0.188877>>>>>|Query
  results for ``apache aries''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Apache_Isis>|<cell|0.368171>>|<row|<cell|Southern_Apache_Museum>|<cell|0.343888>>|<row|<cell|Apache_Excalibur>|<cell|0.327800>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.316355>>|<row|<cell|Apache_Aries>|<cell|0.313229>>|<row|<cell|Apache_Incubator>|<cell|0.310112>>|<row|<cell|Fort_Apache>|<cell|0.306531>>|<row|<cell|Aries>|<cell|0.304566>>|<row|<cell|Apache_Directory>|<cell|0.300640>>|<row|<cell|Apache_Forrest>|<cell|0.299363>>>>>|Query
  results for ``apache apache aries''>

  \;
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|1>>
    <associate|auto-2|<tuple|2|1>>
    <associate|auto-3|<tuple|1|1>>
    <associate|auto-4|<tuple|2|?>>
    <associate|auto-5|<tuple|3|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|table>
      <tuple|normal|Query results for ``apache''|<pageref|auto-3>>

      <tuple|normal|Query results for ``apache aries''|<pageref|auto-4>>

      <tuple|normal|Query results for ``apache apache
      aries''|<pageref|auto-5>>
    </associate>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Database
      Creation and Storage> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>TF-IDF
      Results> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>