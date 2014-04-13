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

  <section|Pivoted Length Normalization Results>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Apache_(disambiguation)>|<cell|0.157835>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.152856>>|<row|<cell|Mod_proxy>|<cell|0.151663>>|<row|<cell|Western_Apache_language>|<cell|0.145874>>|<row|<cell|Apache_Trail>|<cell|0.143866>>|<row|<cell|Plains_Apache_language>|<cell|0.141442>>|<row|<cell|Mod_ssl>|<cell|0.140792>>|<row|<cell|Fort_Apache_Indian_Reservation>|<cell|0.139391>>|<row|<cell|Apache_TomEE>|<cell|0.136530>>|<row|<cell|Fort_Apache>|<cell|0.135704>>>>>|Query
  results for ``apache''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Aries>|<cell|0.220485>>|<row|<cell|Apache_ServiceMix>|<cell|0.165268>>|<row|<cell|Apache_(disambiguation)>|<cell|0.157835>>|<row|<cell|Aries_Marine>|<cell|0.157389>>|<row|<cell|Aries_(comics)>|<cell|0.153568>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.152856>>|<row|<cell|Mod_proxy>|<cell|0.151663>>|<row|<cell|Apache_Aries>|<cell|0.151362>>|<row|<cell|USS_Aries_(PHM-5)>|<cell|0.148377>>|<row|<cell|OSGi_Specification_Implementations>|<cell|0.147210>>>>>|Query
  results for ``apache aries''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Apache_(disambiguation)>|<cell|0.250162>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.242271>>|<row|<cell|Aries>|<cell|0.241095>>|<row|<cell|Mod_proxy>|<cell|0.240380>>|<row|<cell|Apache_ServiceMix>|<cell|0.237173>>|<row|<cell|Western_Apache_language>|<cell|0.231205>>|<row|<cell|Apache_Trail>|<cell|0.228023>>|<row|<cell|Plains_Apache_language>|<cell|0.224180>>|<row|<cell|Mod_ssl>|<cell|0.223150>>|<row|<cell|Fort_Apache_Indian_Reservation>|<cell|0.220929>>>>>|Query
  results for ``apache apache aries''>

  <section|Requiring All Query Terms>

  <subsection|Without Requiring All Terms>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|James>|<cell|0.185760>>|<row|<cell|Apache_James>|<cell|0.171157>>|<row|<cell|Apache_(disambiguation)>|<cell|0.157835>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.152856>>|<row|<cell|Mod_proxy>|<cell|0.151663>>|<row|<cell|Battle_of_Fort_Apache>|<cell|0.146745>>|<row|<cell|Western_Apache_language>|<cell|0.145874>>|<row|<cell|Apache_Trail>|<cell|0.143866>>|<row|<cell|Plains_Apache_language>|<cell|0.141442>>|<row|<cell|Mod_ssl>|<cell|0.140792>>>>>|Query
  results for ``apache james''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Forrest>|<cell|0.269122>>|<row|<cell|Forrest_(surname)>|<cell|0.226635>>|<row|<cell|Apache_Forrest>|<cell|0.218972>>|<row|<cell|John_Forrest_(disambiguation)>|<cell|0.207705>>|<row|<cell|Forrest_(given_name)>|<cell|0.202369>>|<row|<cell|James_Forrest>|<cell|0.189919>>|<row|<cell|George_Forrest>|<cell|0.184893>>|<row|<cell|Forrest_Gump_–_Original_Motion_Picture_Score>|<cell|0.173833>>|<row|<cell|David_Forrest_(Australian_politician)>|<cell|0.171349>>|<row|<cell|Forrest,_Manitoba>|<cell|0.167464>>>>>|Query
  results for ``apache forrest''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Aries>|<cell|0.220485>>|<row|<cell|Apache_ServiceMix>|<cell|0.165268>>|<row|<cell|Apache_(disambiguation)>|<cell|0.157835>>|<row|<cell|Aries_Marine>|<cell|0.157389>>|<row|<cell|Aries_(comics)>|<cell|0.153568>>|<row|<cell|Apache_Rocks_the_Bottom!>|<cell|0.152856>>|<row|<cell|Mod_proxy>|<cell|0.151663>>|<row|<cell|Apache_Aries>|<cell|0.151362>>|<row|<cell|USS_Aries_(PHM-5)>|<cell|0.148377>>|<row|<cell|OSGi_Specification_Implementations>|<cell|0.147210>>>>>|Query
  results for ``apache aries''>

  <subsection|Requiring All Terms>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|James>|<cell|0.185760>>|<row|<cell|Apache_James>|<cell|0.171157>>|<row|<cell|Battle_of_Fort_Apache>|<cell|0.146745>>|<row|<cell|James_Kirker>|<cell|0.139125>>|<row|<cell|Mari_Apache>|<cell|0.135101>>|<row|<cell|James_H._Turpin>|<cell|0.134121>>|<row|<cell|Apache–Mexico_Wars>|<cell|0.131857>>|<row|<cell|Apache_Wars>|<cell|0.131042>>|<row|<cell|Apache_Kid>|<cell|0.128378>>|<row|<cell|James_B._Gillett>|<cell|0.124260>>>>>|Query
  results for ``apache james''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Forrest>|<cell|0.269122>>|<row|<cell|Apache_Forrest>|<cell|0.218972>>|<row|<cell|Apache_Kid>|<cell|0.141312>>|<row|<cell|Gump>|<cell|0.137806>>|<row|<cell|Apache_XML>|<cell|0.125621>>|<row|<cell|Geronimo>|<cell|0.106817>>|<row|<cell|List_of_Apache_Software_Foundation_projects>|<cell|0.106125>>|<row|<cell|Apache_Ambush>|<cell|0.093786>>|<row|<cell|List_of_places_in_Arizona_(A–G)>|<cell|0.084701>>|<row|<cell|The_Adventures_of_Rin_Tin_Tin>|<cell|0.080854>>>>>|Query
  results for ``apache forrest''>

  <small-table|<block|<tformat|<table|<row|<cell|Document
  ID>|<cell|Score>>|<row|<cell|Aries>|<cell|0.220485>>|<row|<cell|Apache_ServiceMix>|<cell|0.165268>>|<row|<cell|Apache_Aries>|<cell|0.151362>>|<row|<cell|OSGi_Specification_Implementations>|<cell|0.147210>>|<row|<cell|Apache_Felix>|<cell|0.128895>>|<row|<cell|List_of_rockets_launched_from_Esrange>|<cell|0.099404>>|<row|<cell|Write-ahead_logging>|<cell|0.082353>>|<row|<cell|OSGi>|<cell|0.069220>>|<row|<cell|Link_16>|<cell|0.053584>>>>>|Query
  results for ``apache aries''>

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

  Tf-idf weights for forum posts perform poorly, as they can down-weight
  terms like ``apache'', which are common in the forums but not the
  encyclopedia, so we use raw term weights.

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

  \;
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|1>>
    <associate|auto-10|<tuple|4|3>>
    <associate|auto-11|<tuple|4.1|3>>
    <associate|auto-12|<tuple|7|3>>
    <associate|auto-13|<tuple|8|3>>
    <associate|auto-14|<tuple|9|4>>
    <associate|auto-15|<tuple|4.2|4>>
    <associate|auto-16|<tuple|10|4>>
    <associate|auto-17|<tuple|11|4>>
    <associate|auto-18|<tuple|12|4>>
    <associate|auto-19|<tuple|5|5>>
    <associate|auto-2|<tuple|2|1>>
    <associate|auto-20|<tuple|5.1|5>>
    <associate|auto-21|<tuple|5.2|?>>
    <associate|auto-22|<tuple|5.3|?>>
    <associate|auto-3|<tuple|1|1>>
    <associate|auto-4|<tuple|2|1>>
    <associate|auto-5|<tuple|3|2>>
    <associate|auto-6|<tuple|3|2>>
    <associate|auto-7|<tuple|4|2>>
    <associate|auto-8|<tuple|5|2>>
    <associate|auto-9|<tuple|6|3>>
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