import gradio as gr
from utils import LOG
from model import OpenAIModel
from translator import PDFTranslator

def translate_pdf(pdf_file ,format,api_key,model_name):
    LOG.debug(f"[翻译任务]\n源文件: {pdf_file}\n源语言: {api_key}\n目标语言: {model_name}")
    openai_model = OpenAIModel(model=model_name, api_key=api_key)

    try:
        # 实例化翻译器并执行翻译
        translator = PDFTranslator(openai_model)
        translator.translate_pdf(pdf_file.name,format)
    except Exception as e:
        return f"翻译出错：{str(e)}"

def create_interface():
    # 使用gr.Interface创建界面
    iface = gr.Interface(
        fn=translate_pdf,
        title="PDF文档翻译器",
        inputs=[
            gr.File(label="上传PDF文件", file_types=[".pdf"]),
            gr.Dropdown(
                label="输出格式",
                choices=["PDF", "Markdown"],
                value="PDF"
            ),
            gr.Textbox(label="OpenAI API Key", placeholder="请输入您的API密钥"),
            gr.Dropdown(
                label="模型选择",
                choices=["gpt-3.5-turbo", "gpt-4"],
                value="gpt-3.5-turbo"
            )
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )
    iface.launch()

if __name__ == "__main__":

    # 启动Gradio应用
    create_interface()
