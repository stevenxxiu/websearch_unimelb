<TeXmacs|1.99.1>

<style|generic>

<\body>
  <section|KL Divergence>

  Assume that:

  <\equation*>
    D<rsub|KL><around*|(|P<around*|\<\|\|\>||\<nobracket\>>Q|)>=<big|sum><rsub|i>P<around*|(|i|)>\<cdot\>log<around*|(|<frac|P<around*|(|i|)>|Q<around*|(|i|)>>|)>
  </equation*>

  <\equation*>
    M<rsub|Q><rprime|'>=<around*|(|1-\<lambda\>|)>M<rsub|Q>+\<lambda\>M<rsub|B>
  </equation*>

  Smoothing is not required for <math|P>, as it does not cause any
  divide-by-zero problems.

  The ranking for Shakespeare's plays agrees with the ranking except for the
  rankings of gNs and KJV texts being swapped (which have similar scores).
  The rankings for the lectures are produced when <math|\<lambda\>=0.9>, i.e.
  when more weight is given to the background model (IDF), this possibly
  means that SP and gNS share more distinguishing terms than SP and KJV.

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
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>BIM
      with full knowledge> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>