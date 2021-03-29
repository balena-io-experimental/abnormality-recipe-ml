FROM balenablocks/librosa-aarch64:raspberrypi4-64

COPY . /app
WORKDIR /app

RUN pip install git+https://github.com/online-ml/river --upgrade
RUN pip install gradio

EXPOSE 7860
CMD ["python", "abnormality_recipe_ml/main.py"]
