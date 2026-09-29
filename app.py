import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
from uscs_soil_classifier import classify_soil

def classify_and_plot(gravel, sand, fines, ll, pl, cu, cc, organic):
    # Input validation: percentages should sum to 100 (allow small tolerance)
    total = gravel + sand + fines
    if abs(total - 100.0) > 0.5:
        return "Error: gravel + sand + fines must sum to 100%.", None
    # Compute plasticity index
    pi = ll - pl
    if pi < 0:
        # In USCS, LL < PL not possible; treat as error
        result = classify_soil(gravel, sand, fines, ll, pl, cu, cc, organic)
    else:
        result = classify_soil(gravel, sand, fines, ll, pl, cu, cc, organic)
    # Prepare bar chart of grain sizes
    fig, ax = plt.subplots(figsize=(4, 2))
    categories = ['Gravel (>4.75 mm)', 'Sand (0.075–4.75 mm)', 'Fines (<0.075 mm)']
    values = [gravel, sand, fines]
    bars = ax.bar(categories, values, color=['#ff9999', '#66b3ff', '#99ff99'])
    ax.set_ylabel('Percent (%)')
    ax.set_title('Grain Size Distribution')
    ax.set_ylim(0, 100)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}',
                ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    return result, fig

with gr.Blocks(title="USCS Soil Classifier", theme="soft") as demo:
    gr.Markdown("## USCS Soil Classifier (ASTM D2487)")
    with gr.Row():
        with gr.Column():
            gravel = gr.Number(label="Gravel (%) >4.75 mm", value=20.0, minimum=0, maximum=100, step=0.1)
            sand = gr.Number(label="Sand (%) 0.075–4.75 mm", value=30.0, minimum=0, maximum=100, step=0.1)
            fines = gr.Number(label="Fines (%) <0.075 mm", value=50.0, minimum=0, maximum=100, step=0.1)
            ll = gr.Number(label="Liquid Limit LL (%)", value=30.0, minimum=0, maximum=100, step=0.1)
            pl = gr.Number(label="Plastic Limit PL (%)", value=15.0, minimum=0, maximum=100, step=0.1)
            cu = gr.Number(label="Coefficient of Uniformity Cu", value=4.0, minimum=0, step=0.1)
            cc = gr.Number(label="Coefficient of Curvature Cc", value=1.0, minimum=0, step=0.01)
            organic = gr.Checkbox(label="Organic?", value=False)
            classify_btn = gr.Button("Classify")
        with gr.Column():
            output = gr.Textbox(label="Classification Result", lines=6)
            plot = gr.Plot(label="Grain Size Distribution", show_label=True)

    classify_btn.click(fn=classify_and_plot,
                       inputs=[gravel, sand, fines, ll, pl, cu, cc, organic],
                       outputs=[output, plot])

demo.launch(server_name="0.0.0.0", server_port=7860)
