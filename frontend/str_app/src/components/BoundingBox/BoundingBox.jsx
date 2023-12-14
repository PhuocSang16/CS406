// { points, id, className, onClick, imageWidth, imageHeight, imageRef }
import { useContext } from 'react';
import { ImageContext } from '../../contexts/ImageContext';
import { AppContext } from '../../contexts/AppContext';

import cx from '../ClassUtils/ClassUtils';


function BoundingBox({ index, polygon }) {
    const { imageWidth, imageHeight, imageRef, resultFromApi } = useContext(ImageContext);
    const { setSelectedBbox, setSelectedImageName, setSelectedImageWidth, setSelectedImageHeight, setSelectedBboxConfDetScore, setSelectedBboxConfRecScore, setSelectedBboxLabel } = useContext(AppContext);

    const scaleX = imageWidth ? imageWidth / imageRef.current.width : 1;
    const scaleY = imageHeight ? imageHeight / imageRef.current.height : 1;

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