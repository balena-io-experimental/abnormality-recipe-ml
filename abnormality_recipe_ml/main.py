"""Anomaly detection example for CPU, RAM, disk usage."""
from random import randint

import gradio as gr
from river import tree

LABELS = {True: 'Abnormal', False: 'Normal'}
# Use decision tree induction algorithm suitable for streaming data
MODEL = tree.HoeffdingTreeClassifier(max_depth=4)


def train_model(iterations: int = 50000) -> None:
    """Train on the assumption that all >50% and at least one >90% is an anomaly."""
    for _ in range(iterations):
        x = {metric: randint(1, 100) for metric in ['cpu', 'ram', 'disk']}
        y = LABELS[min(x.values()) > 50 and max(x.values()) > 90]
        MODEL.learn_one(x, y)


def predict_usage(cpu, ram, disk, is_abnormal):
    """Make the prediction and update with feedback."""
    x = {'cpu': cpu, 'ram': ram, 'disk': disk}
    result = MODEL.predict_proba_one(x), MODEL.debug_one(x)
    MODEL.learn_one(x, LABELS[is_abnormal], sample_weight=100)
    return result


def launch_interface():
    """Launch the Gradio interface."""
    cpu = gr.inputs.Slider(1, 100, 1, 30)
    ram = gr.inputs.Slider(1, 100, 1, 20)
    disk = gr.inputs.Slider(1, 100, 1, 50)

    gr.Interface(
        fn=predict_usage,
        inputs=[
            cpu,
            ram,
            disk,
            gr.inputs.Checkbox(label='Is abnormal?'),
        ],
        outputs=[
            gr.outputs.Label(label='Prediction'),
            gr.outputs.Textbox(label='Heuristics (debug)'),
        ],
    ).launch()


def start():
    """Initialize the model and expose."""
    train_model()
    return launch_interface()


if __name__ == '__main__':
    start()
