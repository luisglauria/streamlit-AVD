# Justificativa das métricas — Dashboard 2

> Desempenho Alto = aluno com `final_exam_score` igual ou acima da mediana da turma (variável `situacao`). Por construção, a proporção geral fica próxima de 50%; por isso ela só é usada segmentada (métrica 4).

## Métrica 1: Média da nota final

- **Variável:** `final_exam_score`
- **O que mede:** A média das notas obtidas pelos alunos na avaliação final.
- **Por que foi escolhida:** Permite visualizar rapidamente o desempenho acadêmico geral da turma.
- **Público-alvo:** Coordenação pedagógica e professores.
- **Qual decisão pode ser apoiada por essa métrica?** Identificar se a turma precisa de reforço, revisão de conteúdos ou acompanhamento adicional. «Inclua aqui a referência que você usaria para dizer que a média está baixa, por exemplo uma meta da escola.»
- **O que comunica ao público-alvo:** O nível geral da turma na avaliação final, em uma escala de 0 a 100.

## Métrica 2: Média de horas de estudo

- **Variável:** `study_time_hours`
- **O que mede:** A quantidade média de horas por dia que os alunos dedicam aos estudos.
- **Por que foi escolhida:** Na EDA, a variável apresentou correlação positiva com a nota final («confirme o valor: Spearman = 0,56, moderada»), e representa um hábito que pode ser acompanhado pela escola. Isso indica associação, não causa.
- **Público-alvo:** Professores, coordenação pedagógica e alunos.
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar a necessidade de orientar os alunos sobre organização da rotina e hábitos de estudo.
- **O que comunica ao público-alvo:** Quantas horas por dia, em média, os alunos dedicam aos estudos.

## Métrica 3: Variação média da nota

- **Variável:** Diferença entre `final_exam_score` e `previous_grade`.
- **O que mede:** A variação média dos alunos entre a nota anterior e a nota final.
- **Por que foi escolhida:** Mostra se o desempenho dos alunos melhorou ou piorou entre as duas notas. «Confirme antes de manter esta frase: as duas variáveis estão na mesma escala, de 0 a 100.»
- **Público-alvo:** Coordenação pedagógica e professores.
- **Qual decisão pode ser apoiada por essa métrica?** Identificar se há melhora ou queda média no desempenho e onde vale investigar com mais atenção. A métrica não mostra o motivo da variação.
- **O que comunica ao público-alvo:** Um valor positivo indica melhora média; um valor negativo indica redução média no desempenho.

## Métrica 4: Desempenho Alto por faixa de frequência

- **Variável:** `attendance_percent`, agrupada nas faixas Baixa (até 75%), Média (acima de 75% até 90%) e Alta (acima de 90%), em comparação com `situacao`.
- **O que mede:** A proporção de alunos classificados como Desempenho Alto em cada faixa de frequência.
- **Por que foi escolhida:** Os dados mostram uma diferença entre as faixas: 33,8% na faixa Baixa, 48,1% na Média e 60,8% na Alta. Os cortes de 75% e 90% são faixas operacionais para facilitar a interpretação, e não limites estatisticamente ótimos.
- **Público-alvo:** Coordenação pedagógica e professores.
- **Qual decisão pode ser apoiada por essa métrica?** Priorizar o acompanhamento dos alunos com baixa frequência e investigar possíveis dificuldades de participação.
- **O que comunica ao público-alvo:** Mostra uma associação entre frequência e desempenho, mas não permite afirmar que a frequência causa diretamente o resultado. O gráfico exibe o número de alunos (`n`) de cada faixa junto com a proporção.