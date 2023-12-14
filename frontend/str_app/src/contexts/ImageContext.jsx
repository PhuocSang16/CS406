import { createContext, useState, useRef, useEffect } from 'react';

export const ImageContext = createContext({});



export const ImageProvider = ({ children, resultFromApi, imageURL }) => {

    const imageRef = useRef(null);

    const [imageWidth, setImageWidth] = useState(null);
    const [imageHeight, setImageHeight] = useState(null);

    const handleImageLoad = () => {
        if (imageRef.current && imageRef.current.complete) {
            setImageWidth(imageRef.current.width);
            setImageHeight(imageRef.current.height);
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
            }}
        >
            {children}
        </ImageContext.Provider>
    )
}