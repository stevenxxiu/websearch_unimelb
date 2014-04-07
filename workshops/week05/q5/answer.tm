<TeXmacs|1.99.1>

<style|generic>

<\body>
  <section|Binary Class Ranking>

  Let <math|v<rsub|p>> and <math|v<rsub|n>> be the mean pseudo document for
  positive and negative classes respectively. The the decision boundary using
  rocchio is the hyperplane separating them, not spheres around them. If the
  distance to <math|v<rsub|n>> is ignored, then documents far away but
  equidistant from the hyperplane to the <math|v<rsub|p>> side will probably
  be positive, while negative to the <math|v<rsub|n>> side.

  For a test document <math|v>, we can instead compute
  <math|d<around*|(|v,v<rsub|p>|)>-d<around*|(|v,v<rsub|n>|)>> as a score of
  how close the document is to the postive class.
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
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Cluster
      Representation> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>