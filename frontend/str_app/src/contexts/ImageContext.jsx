import { createContext, useState, useRef, useEffect } from 'react';

export const ImageContext = createContext({});



export const ImageProvider = ({ children, resultFromApi, imageURL }) => {

    const imageRef = useRef(null);

    const [imageWidth, setImageWidth] = useState(null);
    const [imageHeight, setImageHeight] = useState(null);
    const [scaleX, setScaleX] = useState(1);
    const [scaleY, setScaleY] = useState(1);

    const handleImageLoad = () => {
        if (imageRef.current && imageRef.current.complete) {
            let scale = imageRef.current.height / imageRef.current.width
            setImageWidth(window.innerWidth * 0.5);
            setImageHeight(window.innerWidth * 0.5 * scale);
            setScaleX(window.innerWidth * 0.5 / imageRef.current.width)
            setScaleY((window.innerWidth * 0.5 * scale) / imageRef.current.height)
        }
    };

    return (
        <ImageContext.Provider
            value={{
                resultFromApi,
                imageURL,
                handleImageLoad,
                imageRef,
                imageWidth,
                setImageWidth,
                imageHeight,
                setImageHeight,
                scaleX,
                scaleY,
                setScaleX,
                setScaleY
            }}
        >
            {children}
        </ImageContext.Provider>
    )
}