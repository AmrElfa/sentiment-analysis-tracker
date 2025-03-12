from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    words = text.split()
    if len(words) > 700:
        text = " ".join(words[:700])
    summary = summarizer_pipeline(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']
