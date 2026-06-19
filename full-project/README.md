## Higher Education Data Analysis — Notes

### Part 1 — Correlation Between Admission Rates and Tuition Fees

- Universities with 100% acceptance rates generally have much lower tuition fees.
- Universities with the lowest acceptance rates tend to have much higher tuition fees.
- Outside these extreme cases, there's only a weak negative correlation: as acceptance rates rise, tuition fees generally fall.

**Conclusion:**
- This pattern may be explained by university prestige. Institutions with highly competitive admissions can charge higher tuition thanks to reputation, demand, and perceived value, while less selective universities may attract students who prioritise accessibility and affordability.
- From a business perspective, universities with lower acceptance rates admit fewer students, so higher tuition fees could help maintain financial viability.
- **Evaluation:** Since the correlation is weak once extreme values are excluded, acceptance rate alone isn't a reliable predictor of tuition fees. A student can't assume a higher acceptance rate will necessarily mean significantly lower tuition costs.

### Part 2 — Graduate Salaries in Relation to Tuition Fees and Admission Rates

**Where do the lowest-paid graduates show up on the graph?**
- Visually, the lowest-paid graduates correspond to the warmest colours on the plot (red/orange).
- The greatest concentration of these points sits toward the left-hand side of the graph, particularly among universities charging less than $10,000 in tuition fees.
- These universities also tend to have relatively high admission rates, indicating they're generally less selective institutions.

**Conclusion:**
- The data suggests graduates from lower-cost, less selective universities tend to earn lower salaries ten years after graduation.
- This is supported by the opposite end of the graph, where universities with higher tuition fees and lower admission rates are more commonly associated with higher graduate earnings.
- One possible explanation is that more selective universities may offer advantages such as stronger academic reputations, employer recognition, alumni networks, career support services, and industry connections, all of which could contribute to improved graduate outcomes.

**Evaluation:**
- While the overall trend suggests a relationship between tuition fees, selectivity, and graduate earnings, the graph shows considerable variation throughout the data.
- The relationship should therefore be read as a correlation rather than a causal effect. Higher tuition fees or lower admission rates don't necessarily *cause* higher salaries; other factors — student ability, degree specialisation, socioeconomic background, geographic location, and labour-market conditions — may also influence graduate earnings.

### Part 3 — Institutions Where the Bottom Income Quintile Receives Money

- The question asks how many institutions have a negative value for the bottom 20% of earners (quintile).
- A negative net price means the student effectively receives more financial support than they pay towards tuition.
- The aim is therefore to count institutions where the `NPT41_PUB` or `NPT41_PRIV` value is below zero.
- Income groups are divided into five categories (1–5), each representing a quintile, with `NPT41` referring to the lowest income group.

### Part 4 — Net Prices Across Income Quintiles at Private Universities

- At private universities, the bottom income quintile pays roughly **71%** of the amount paid by the top income quintile.
- This is a smaller gap between income groups than at public universities, where the bottom quintile pays about **52%** of the top.

### Admission Rate and Completion Rate Correlation

- The correlation between admission rate and completion rate is approximately **−0.34**, a weak negative relationship.
- This suggests less selective institutions tend to have slightly lower completion rates, though admission selectivity alone isn't a strong predictor of completion outcomes.
