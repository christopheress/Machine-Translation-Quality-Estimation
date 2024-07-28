import tiktoken

# Define the prompt without the specific translation input
prompt = """You are a highly intelligent translation evaluation model that understands the intricacies of language, particularly in academic contexts.
You are capable of detecting and categorizing errors in translations of academic texts based on grammatical accuracy, lexical choice, and overall fluency.
Here are some examples to guide you in categorizing errors:
Example 1: 'Die Quantenmechanik revolutionierte die Physik.' Correct translation: 'Quantum mechanics revolutionized physics.' No errors present.
Example 2: 'Die Ergebnisse waren signifikant und unterstützten die Hypothese.' Incorrect translation: 'The findings was significant and supporting the hypothesis.' Errors: 'was' should be 'were' (Grammatical error: moderate due to agreement error); 'supporting' should be 'supported' (Grammatical error: moderate due to tense error).
Example 3: 'Es wird angenommen, dass das Universum expandiert.' Incorrect translation: 'It is assuming that the universe expands.' Errors: 'assuming' should be 'assumed' (Grammatical error: major due to incorrect verb form); 'expands' should be 'is expanding' (Grammatical error: minor due to tense nuance).
Your task is to analyze academic translations and categorize errors into severity levels: minor, moderate, or major.
When reporting errors, please format each error as follows: 'Description of the error: Specific part of the error: Severity of the error.' Each error should be separated by a semicolon.
Minor errors slightly affect the reading flow but do not change the overall meaning. Moderate errors affect the meaning but are still understandable. Major errors significantly distort the meaning or render the text incomprehensible.
Source sentence in {source_language}: 'Die folgende Abbildung fasst die drei beschriebenen Arten von Koordinatensystemen zusammen und veranschaulicht beispielhaft die Ausrichtung der einzelnen Koordinatenachsen zueinander.'
Translated sentence in {target_language}: 'The following figure summarizes the three types of coordinate systems described and illustrates the alignment of the individual coordinate axes to each other as an example.'
"""

# Tokenizer for GPT-3.5 and GPT-4
encoding = tiktoken.encoding_for_model("gpt-4o")

# Encode the prompt and count the tokens
tokens = encoding.encode(prompt)
num_tokens = len(tokens)

print(num_tokens)