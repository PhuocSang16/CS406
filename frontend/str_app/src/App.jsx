import React, { useContext, useEffect } from 'react';
import './scss/App.scss';
import cx from './components/ClassUtils/ClassUtils';

import { ImageProvider } from './contexts/ImageContext';
import { AppContext } from './contexts/AppContext';

import ImageUpload from './components/ImageUpload/ImageUpload'
import FileUpload from './components/FileUpload/FileUpload';
import Info from './components/Info/Info'



function App() {

    const { resultsFromApi, imageURLs } = useContext(AppContext);

    // Stop the wheeling event on .gallery
    useEffect(() => {
        const galleryElement = document.querySelector('.gallery');

        const handleWheel = (e) => {
            e.preventDefault();
        };

        galleryElement.addEventListener('wheel', handleWheel, { passive: false });

        return () => {
            galleryElement.removeEventListener('wheel', handleWheel);
        };
    }, []);

    return (
        <div className={cx("main")}>
            <div className={cx("gallery")}>
                <FileUpload />
                {
                    resultsFromApi.length === 0 ?
                        "Images will be shown in this orange box. Scroll your mouse wheel HERE to zoom in/out them." :
                        resultsFromApi.map((result, index) => (
                            <ImageProvider key={index} resultFromApi={result} imageURL={imageURLs[index]}>
                                <ImageUpload />
                            </ImageProvider>
                        ))}
            </div>
            <div className={cx("info-container")}>
                <Info />
            </div>
        </div>
    );
}

export default App;
