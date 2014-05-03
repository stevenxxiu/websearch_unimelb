<TeXmacs|1.99.1>

<style|generic>

<\body>
  <section|<math|>Intercept Interpretation>

  <math|\<beta\><rsub|0>> is the weight given to a document without it
  containing any terms. In terms of probability, this is the logit function
  of the prior belief that a document belongs to this class.

  If <math|\<beta\><rsub|0>=0> and the document <math|d> has no terms, then
  <math|logit<around*|(|P<around*|(|c\<mid\>d|)>|)>=0>, hence
  <math|P<around*|(|c\<mid\>d|)>=1/2>.

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
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Logistic
      Functions> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>