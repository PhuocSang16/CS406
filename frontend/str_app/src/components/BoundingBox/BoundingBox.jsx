// { points, id, className, onClick, imageWidth, imageHeight, imageRef }
import { useContext } from 'react';
import { ImageContext } from '../../contexts/ImageContext';
import { AppContext } from '../../contexts/AppContext';

import cx from '../ClassUtils/ClassUtils';


function BoundingBox({ index, polygon }) {
    const { imageWidth, imageHeight, imageRef, resultFromApi , scaleX, scaleY} = useContext(ImageContext);
    const { setSelectedBbox, setSelectedImageName, setSelectedImageWidth, setSelectedImageHeight, setSelectedBboxConfDetScore, setSelectedBboxConfRecScore, setSelectedBboxLabel } = useContext(AppContext);
    console.log(scaleX, scaleY)
    // let scaleX = 1
    // let scaleY = 1
    
    // if (imageWidth)
    //     if (imageHeight === 271.5)
    //     {
    //         scaleX = imageWidth ? 362 / 800 :1//imageWidth / imageRef.current.width : 1;
    //         scaleY = imageHeight ? 271.5 / 600: 1 //imageHeight / imageRef.current.height: 1;
    //         console.log(scaleX, scaleY)
    //     }
    //     else
    //     {
    //         scaleX = imageWidth / imageRef.current.width
    //         scaleY = imageHeight / imageRef.current.height
    //     }
    // if (imageWidth) 
    //     console.log(imageWidth, imageRef.current.width, imageHeight, imageRef.current.height)

    const scaledPoints = polygon.map(([x, y]) => [x * scaleX, y * scaleY]);
    const pointsString = scaledPoints.map(([x, y]) => `${x},${y}`).join(' ');

    const handleBoundingBoxClick = (index, polygon) => {
        console.log(`Box ID: ${index}   Points: ${JSON.stringify(polygon)}`);
        setSelectedImageName(resultFromApi.img_name);
        setSelectedImageWidth(imageWidth);
        setSelectedImageHeight(imageHeight);

        setSelectedBbox(polygon.map(([x, y]) => `[${x} ${y}]`).join(","));
        setSelectedBboxLabel(resultFromApi.texts[index]);
        setSelectedBboxConfDetScore(resultFromApi.det_scores[index]);
        setSelectedBboxConfRecScore(resultFromApi.recog_scores[index]);
    }


    return (
        <polygon
            className={cx("bounding-box")}
            points={pointsString}
            onClick={() => { handleBoundingBoxClick(index, polygon) }}
        />
    );
}

export default BoundingBox;