import asyncio
import sys
import json
import uvicorn
from fastapi import Depends, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import aiofiles
from pydantic import BaseModel
import os
from io import BytesIO
import numpy as np
import cv2
import zipfile
from SceneTextPipeline import SceneTextPipeline
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR ,'frontend')

pipeline = SceneTextPipeline('C:\\Demo_XLA\\vietnamese-scene-text-recognition\\mmocr\\configs\\textdet\\dbnetpp\\dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py',
                                    'C:\\Demo_XLA\\vietnamese-scene-text-recognition\\pretrained\\dbnetpp\\vintext_best_dbnetpp.pth',
                                    'C:\\Demo_XLA\\vietnamese-scene-text-recognition\\pretrained\\parseq\\vintext_best_parseq.ckpt')

app = FastAPI(
    title="ASR_app",
    description="Demo website for Digital Image Processing project",
)

app.mount("/frontend", StaticFiles(directory=FRONTEND_FOLDER), name="Frontend")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-zip/")
async def upload_zip(files: UploadFile = File(...)):
    try:
        batch_images = []
        img_names = []
        results = []

        with zipfile.ZipFile(io.BytesIO(await files.read()), 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                    file_data = zip_ref.read(filename)
                    
                    file_stream = BytesIO(file_data)
                    nparr = np.frombuffer(file_stream.getvalue(), np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    batch_images.append(image)
                    img_names.append(filename)

            
            batch_results = pipeline(batch_images)

            for result, img_name in zip(batch_results, img_names):
                result['img_name'] = img_name
                print(result['width'])
                # Bug fix logic for recog_scores
                result['recog_scores'] = [
                    score.item() if np.isscalar(score) else score
                    for score in result['recog_scores']
                ]

                results.append(result)
        #print(results)
        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
