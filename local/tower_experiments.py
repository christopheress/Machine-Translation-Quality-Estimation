import torch
from transformers import pipeline

bnb_4bit_compute_dtype=torch.float16

pipe = pipeline("text-generation", model="Unbabel/TowerInstruct-v0.1", torch_dtype=torch.float16, device_map="auto")
# We use the tokenizer’s chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {"role": "user", "content": "You are an annotator for machine translation quality. Your task is to identify errors and assess the quality of the translation.\n"
                                "Source (English): Yes that means when I work out I really don’t care how many calories it burns, and I don’t change my numbers or macros because of how much I burned.\n"
                                "Translation (German): Ja, das bedeutet, dass ich mich beim Training nicht wirklich darum kümmere, wie viele Kalorien es verbrennt, und ich ändere meine Zahlen oder Makros nicht, weil ich so viel verbrannt habe.\n"
                                "Each error may consist of several consecutive words and must be categorized as either 'minor' or 'major'. Minor errors refer to smaller imperfections, and purely subjective opinions about the translation while major errors impact the usability or understandability of the content.\n"
                                "Based on the above source and translation pair, list the errors you find. If you find no errors, simply output 'Translation has no errors.'"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=False)
print("--------------------------------------------")
print(outputs[0]["generated_text"])
print(outputs)

