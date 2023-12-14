import React, { useRef, useContext } from 'react';
import { AppContext } from '../../contexts/AppContext';

import cx from '../ClassUtils/ClassUtils';


function FileUpload() {

    const JSZip = require("jszip");
    const { resultsFromApi, setResultsFromApi, setImageURLs, setFilesDidUpload, filesDidUpload } = useContext(AppContext);

    const inputFileRef = useRef(null);

    const handleButtonClick = () => {
        inputFileRef.current.click();
    };

    const handleFileChange = async (event) => {
        const uploadedFile = event.target.files[0];

        if (uploadedFile.name !== 'images.zip') {
            alert('Please upload a file named images.zip');
            return;
        }

        const reader = new FileReader();

        reader.onload = async (event) => {
            const zipData = event.target.result;
            const blob = new Blob([zipData], { type: 'application/zip' });

            const formData = new FormData();
            formData.append('files', blob, 'images.zip');

            // Try updating imageURLs
            try {
                const zip = await JSZip.loadAsync(zipData);
                const imageUrlsPromises = [];

                zip.forEach((relativePath, zipEntry) => {
                    // Skip directories
                    if (zipEntry.dir) return;

                    // Assuming images are in the root directory of the zip file
                    const imagePromise = zipEntry.async('blob').then(fileData => {
                        const imageUrl = URL.createObjectURL(fileData);
                        return imageUrl;
                    });

                    imageUrlsPromises.push(imagePromise);
                });

                const imageUrls = await Promise.all(imageUrlsPromises);
                setImageURLs(imageUrls);
                setFilesDidUpload(true);
                // Now you have an array of image URLs (imageUrls)
                // Store this array in your context or state as needed
                // For example, setResultsFromApi(imageUrls);

            } catch (error) {
                console.error('There was a problem with unzipping the file:', error);
                setFilesDidUpload(false);
            }

            // Fetch API
            try {
                const response = await fetch('http://localhost:8000/upload-zip', {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }

                const data = await response.json();
                setResultsFromApi(data);

            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }



        };

        reader.readAsArrayBuffer(uploadedFile);
    };

    const handleDownloadJson = () => {
        const jsonString = JSON.stringify(resultsFromApi);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'results.json'; // File name after downloaded
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };


    return (
        <div className={cx("button-container")}>
            <input
                type="file"
                id="image-input"
                style={{ display: 'none' }}
                ref={inputFileRef}
                onChange={handleFileChange}
            />
            <button className={cx("upload-button")} onClick={handleButtonClick}>
                Upload image
            </button>
            {filesDidUpload && (
                <button className={cx("download-json-button")} onClick={handleDownloadJson}>Download JSON</button>
            )}
        </div>
    )
}

export default FileUpload;