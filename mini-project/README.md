### Purpose

- This analysis serves as practice for using the pandas library in Python.
- It carries out a thorough analysis of the 2020 Python Developer Survey, as well as the 2021 Stack Overflow survey.
- The datasets are cleaned, sorted, and analysed using various pandas techniques to outline interesting statistical data, which can be comprehensively reviewed via the print statements.

### Key Comparison — Developer Experience

- An interesting comparison can be made about the experience of Python developers between the two surveys.
- The Python survey concludes that ~9.6% of developers have 11+ years of experience, whereas the Stack Overflow survey indicates a much larger result at ~37%.

### Why the Comparison Isn't Straightforward

- At first, one may conclude that the majority who filled out the Python survey are at the earlier stages of their programming career.
- However, a valid comparison cannot be made between the two surveys in their current state. This is because the Stack Overflow survey asked developers about their **overall** programming experience, and we filtered the dataset to include only answers that mentioned Python.
- There are two reasons why asking for overall experience may skew the results:
  1. Someone who may have used Python for less than 3 months but has 11+ years of experience across other languages **may** have been included, since we filtered by any string that *includes* Python, rather than answers that solely read 'Python'.
  2. The likelihood of someone who has been programming for a while having some Python experience is very high. Thus, at the higher end of experience, many developers are filtered into our analysis.

### Recommendation

- To mitigate this, the Python Developer Survey could include an 'overall programming experience' question in the future, so that data from the two surveys can be directly compared.
