import React, { useState, useContext } from 'react';

import BoundingBoxes from '../BoundingBoxes/BoundingBoxes';
import { ImageContext } from '../../contexts/ImageContext';
import cx from '../ClassUtils/ClassUtils';

function ImageUpload() {

    const { handleImageLoad, imageWidth, imageHeight, imageURL, imageRef } = useContext(ImageContext);
    const [scale, setScale] = useState(1);

    const handleZoom = (event) => {
        const MIN_SCALE = 0.6;
        const MAX_SCALE = 2;
        if (event.deltaY < 0 && scale < MAX_SCALE) {
            // Zoom in
            setScale(scale * 1.05);
        }
        else if (event.deltaY > 0 && scale > MIN_SCALE) {
            // Zoom out
            setScale(scale * 0.95);
        }
    };

    return (
        <React.Fragment>
            <div
                className={cx('bbox-container')}
                onWheel={handleZoom}
                style={{
                    transform: `scale(${scale})`
                }}
            >
                <svg
                    className={cx("svg-container")}
                    width={imageWidth}
                    height={imageHeight}
                >
                    <BoundingBoxes />
                </svg>
                {
                    imageURL === null ?
                        "Your image will be shown here. You can also scroll your mouse to zoom in/out." :
                        <img
                            ref={imageRef}
                            src={imageURL}
                            alt="Uploaded"
                            width={imageWidth}
                            height={imageHeight}
                            onLoad={handleImageLoad}
                        />
                }
            </div>
        </React.Fragment>
    )
}

export default ImageUpload;