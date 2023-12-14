import { createContext, useState, useRef, useEffect } from 'react';

export const AppContext = createContext({});

export const AppProvider = ({ children }) => {

    const [resultsFromApi, setResultsFromApi] = useState([]);

    const [imageURLs, setImageURLs] = useState([]);
    const [selectedImageName, setSelectedImageName] = useState("None");
    const [selectedImageWidth, setSelectedImageWidth] = useState(-1);
    const [selectedImageHeight, setSelectedImageHeight] = useState(-1);

    const [selectedBbox, setSelectedBbox] = useState("[],[],[],[]");
    const [selectedBboxLabel, setSelectedBboxLabel] = useState("None");
    const [selectedBboxConfDetSCore, setSelectedBboxConfDetScore] = useState(-1);
    const [selectedBboxConfRecSCore, setSelectedBboxConfRecScore] = useState(-1);

    const [filesDidUpload, setFilesDidUpload] = useState(false);

    return (
        <AppContext.Provider
            value={{
                resultsFromApi,
                setResultsFromApi,
                imageURLs,
                setImageURLs,
                selectedImageName,
                setSelectedImageName,
                selectedImageWidth,
                setSelectedImageWidth,
                selectedImageHeight,
                setSelectedImageHeight,
                selectedBbox,
                setSelectedBbox,
                selectedBboxLabel,
                setSelectedBboxLabel,
                selectedBboxConfDetSCore,
                setSelectedBboxConfDetScore,
                selectedBboxConfRecSCore,
                setSelectedBboxConfRecScore,
                filesDidUpload,
                setFilesDidUpload
            }}
        >
            {children}
        </AppContext.Provider>
    )
}


