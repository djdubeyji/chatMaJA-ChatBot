import gradio as gr
from qa_pipeline import answer_query_streaming

gradio_app = gr.ChatInterface(
    answer_query_streaming,
    title="Chat Maja - Your PubMed expert",
    description='''Retrieval-Augmented Question Answering chatbot, based on quite a few abstracts from PubMed. <br>
            Explore the code on <a href="https://github.com/mstaczek/QAsystem-INLPT-WS2023" target="_blank" style="color: #fff;">GitHub</a> - Authors: Agata Kaczmarek, Pranjal Sharma, Jan Smoleń, Mateusz Stączek.''',
)

if __name__ == "__main__":
    gradio_app.launch()