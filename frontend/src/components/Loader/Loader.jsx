import React from 'react';
import './Loader.css';

export default function Loader({ withOverlay = true }) {
  return (
    <>
      {/* {withOverlay && <div className="overlayLoader"></div>} */}
      {withOverlay && <div className="overlayLoader"></div>}
      <div className='loaderContainer'>

        <div className="loader-wrapper">
          <span className="loader"></span>
        </div>
        {/* <div class="loaderTitle">Ожидайте<span class="dots"></span></div> */}
      </div>
    </>
  );
}