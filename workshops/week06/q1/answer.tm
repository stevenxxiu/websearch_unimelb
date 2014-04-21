<TeXmacs|1.99.1>

<style|generic>

<\body>
  <section|BIM with full knowledge>

  The weight for each term in the probabilistic model is: <math|w<rsub|t>=log
  <frac|p<rsub|t>|1-p<rsub|t>>+log <frac|1-u<rsub|t>|u<rsub|t>>>. Let
  <math|N> be the # of documents, <math|R> be the # of relevant documents,
  <math|f<rsub|t>> the # of documents that term <math|t> appears in, and
  <math|r<rsub|t>> the # of relevant documents that term <math|t> appears in.

  Then using MLE, <math|<wide|p|^><rsub|t>=<frac|r<rsub|t>|R>,<wide|u|^><rsub|t>=<frac|f<rsub|t>-r<rsub|t>|N-R>>.
  Putting this into <math|w<rsub|t>>, we get:

  <\equation*>
    <tabular|<tformat|<table|<row|<cell|w<rsub|t>>|<cell|=log
    <frac|r<rsub|t>|R-r<rsub|t>>+log <frac|<around*|(|N-R|)>-<around*|(|f<rsub|t>-r<rsub|t>|)>|f<rsub|t>-r<rsub|t>>>>|<row|<cell|>|<cell|=log
    \ <frac|r<rsub|t>\<cdot\><around*|(|<around*|(|N-R|)>-<around*|(|f<rsub|t>-r<rsub|t>|)>|)>|<around*|(|R-r<rsub|t>|)>\<cdot\><around*|(|f<rsub|t>-r<rsub|t>|)>>>>>>>
  </equation*>

  If <math|t> appears in every relevant document, then
  <math|f<rsub|t>=r<rsub|t>>, we have:

  <\equation*>
    w<rsub|t>=log <frac|p<rsub|t>|1-p<rsub|t>>=log
    <frac|r<rsub|t>|R-r<rsub|t>>=log <frac|f<rsub|t>|R-f<rsub|t>>
  </equation*>

  \;

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
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Speeding
      Up Clustering> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>