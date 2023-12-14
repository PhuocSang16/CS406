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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR ,'frontend')

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

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        nparr = np.frombuffer(content, np.uint8) # 1D array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # Decode the array into an image
        pipeline = SceneTextPipeline('./mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py',
                                    './mmocr/pretrained/epoch_600.pth',
                                    './parseq/outputs/parseq/2023-12-11_19-37-51/checkpoints/epoch=16-step=2193-val_accuracy=86.0536-val_NED=93.7526.ckpt')
        results = pipeline([img])
        
        for image_result in results:
            # Convert recog_scores to Python floats
            image_result['recog_scores'] = [score.item() if np.isscalar(score) else score for score in image_result['recog_scores']]

        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


import io

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

            pipeline = SceneTextPipeline('/mmlabworkspace/Students/visedit/AIC2021/mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py',
                                    '/mmlabworkspace/Students/visedit/AIC2021/mmocr/pretrained/dbnetpp/epoch_600.pth',
                                    '/mmlabworkspace/Students/visedit/AIC2021/parseq/outputs/parseq/2023-12-11_19-37-51/checkpoints/epoch=16-step=2193-val_accuracy=86.0536-val_NED=93.7526.ckpt')
            batch_results = pipeline(batch_images)

            for result, img_name in zip(batch_results, img_names):
                result['img_name'] = img_name

                # Bug fix logic for recog_scores
                result['recog_scores'] = [
                    score.item() if np.isscalar(score) else score
                    for score in result['recog_scores']
                ]

                results.append(result)
        print(results)
        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})




           


       


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)