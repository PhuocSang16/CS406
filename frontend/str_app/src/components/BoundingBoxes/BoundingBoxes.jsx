import { useContext } from 'react';
import BoundingBox from '../BoundingBox/BoundingBox';
import { ImageContext } from '../../contexts/ImageContext';

const BoundingBoxes = () => {

    const { resultFromApi } = useContext(ImageContext);

    return (
        <>
            {resultFromApi['det_polygons'] &&
                resultFromApi['det_polygons'].map((polygon, index) => (
                    <BoundingBox 
                        key={index} index={index} 
                        polygon={polygon} 
                        rawWidth={resultFromApi['width']} 
                        rawHeight={resultFromApi['height']}
                    />
                ))}
        </>
    );
};

export default BoundingBoxes;
