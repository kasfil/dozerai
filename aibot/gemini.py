import re
from pathlib import Path
from venv import logger

import google.generativeai as genai
from PIL import Image
from PIL.Image import Image as ImageType

from config import GEMINI_TOKEN

genai.configure(api_key=GEMINI_TOKEN)
MODEL_ID = "gemini-1.5-flash-8b"


async def ask_gemini(question: str, images_path: list[Path] | None = None):
    """
    Ask Gemini a question and get a response.

    Args:
        question (str): The question to ask Gemini.
        images_path (list[Path] | None, optional): The list of paths to images. Defaults to None.

    Returns:
        AsyncGenerateContentResponse: The response from Gemini.
    """
    system_instruction = """You are a safety, health, and environment expert auditor.
you will always comment any unsafe actions or behaviors, and you are responsible
on any accident that happens. so that you must prevent any accident before it
happens. when you reply to a question you should reply with your answer in markdown format.
"""

    model = genai.GenerativeModel(MODEL_ID, system_instruction=system_instruction)

    if images_path is None:
        images_path = []
    messages: list[str | ImageType] = [question]

    if images_path:
        for img in images_path:
            try:
                image = Image.open(img)
                messages.append(image)
            except Exception as e:
                logger.error(e)

    return await model.generate_content_async(messages)


async def rate_gemini(prompt: str, img: Path) -> tuple[float, str]:
    system_instruction = """role: Experienced EHS auditor
task: Evaluate images related to workplace safety, health, and environment
rating scale: 0 - 10 (10 being the highest rating)
output format: markdown
[rate]
comment:"""

    model = genai.GenerativeModel(MODEL_ID, system_instruction=system_instruction)

    if not prompt:
        prompt = "Please rate the image"

    image = Image.open(img)
    messages = [prompt, image]

    response = await model.generate_content_async(messages)
    pattern = r"\[(\d+)\]\s+[Cc]omment[s]?:[\s]?(.*)"
    matches = re.findall(pattern, response.text)
    return float(matches[0][0]), matches[0][1]
