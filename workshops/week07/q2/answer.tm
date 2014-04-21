<TeXmacs|1.99.1>

<style|generic_user>

<\body>
  <section|Rank Equivalence>

  <with|font-series|bold|Lemma: >For a binary query <math|q> vector and a
  document <math|d>, <math|-D<rsub|KL><around*|(|M<rsub|q><around*|\<\|\|\>||\<nobracket\>>M<rsub|d>|)>\<sim\><big|sum><rsub|i=1><rsup|<around*|\||q|\|>>P<around*|(|q<rsub|i><around*|\|||\<nobracket\>>M<rsub|d>|)>>
  given the MLE model, where <math|q<rsub|i>> are random variables, and the
  equivalence is defined over the rankings of a set of documents <math|D>.

  <\proof>
    \;

    <\equation*>
      <tabular|<tformat|<table|<row|<cell|-D<rsub|KL><around*|(|M<rsub|q><around*|\<\|\|\>|M<rsub|d>|\<nobracket\>>|)>>|<cell|=-<big|sum><rsub|i=1><rsup|<around*|\||q|\|>><frac|1|<around*|\||q|\|>>\<cdot\><around*|(|log<around*|(|<frac|1|<around*|\||q|\|>>|)>-log<around*|(|P<around*|(|q<rsub|i>\<mid\>M<rsub|d>|)>|)>|)>>>|<row|<cell|>|<cell|\<sim\>-<big|sum><rsub|i=1><rsup|<around*|\||q|\|>><around*|(|log<around*|(|<frac|1|<around*|\||q|\|>>|)>-log<around*|(|P<around*|(|q<rsub|i>\<mid\>M<rsub|d>|)>|)>|)>>>|<row|<cell|>|<cell|\<sim\><big|sum><rsub|i=1><rsup|<around*|\||q|\|>>P<around*|(|q<rsub|i>\<mid\>M<rsub|d>|)>>>>>>
    </equation*>

    \;
  </proof>

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
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Rank
      Equivalence> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>