import React, { useContext, useEffect } from 'react';
import { AppContext } from '../../contexts/AppContext';

import cx from '../ClassUtils/ClassUtils';
import './Info.scss'

function Info() {

    const { selectedImageName, selectedImageWidth, selectedImageHeight, selectedBbox, selectedBboxLabel, selectedBboxConfDetSCore, selectedBboxConfRecSCore } = useContext(AppContext);

    return (
        <React.Fragment>
            <h2>BOUNDING BOX INFORMATION:</h2>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Image name:</span>
                <span className={cx("info-value")}>{selectedImageName}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Image width:</span>
                <span className={cx("info-value")}>{selectedImageWidth}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Image height:</span>
                <span className={cx("info-value")}>{selectedImageHeight}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Coordinate:</span>
                <span className={cx("info-value")}>{selectedBbox}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Label:</span>
                <span className={cx("info-value")}>{selectedBboxLabel}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Detection confidence:</span>
                <span className={cx("info-value")}>{selectedBboxConfDetSCore}</span>
            </div>
            <div className={cx("info-row")}>
                <span className={cx("info-label")}>Recognition confidence:</span>
                <span className={cx("info-value")}>{selectedBboxConfRecSCore}</span>
            </div>
        </React.Fragment>
    )
}

export default Info;