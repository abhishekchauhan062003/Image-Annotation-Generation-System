import React from 'react';
import ShinyText from './ShinyText';
import "../App.css";
import { useNavigate } from 'react-router-dom';
function Hero() {
  const navigate = useNavigate();

    const handleClick = () => {
        navigate('/form');
    };
  return (
    <div className='hero'>
        <div className="container col-xxl-8 px-4 py-5">
    <div className="row flex-lg-row-reverse align-items-center g-5 py-5">
      <div className="col-10 col-sm-8 col-lg-6">
        {/* <img src="bootstrap-themes.png" className="d-block mx-lg-auto img-fluid" alt="Bootstrap Themes" width="700" height="500" loading="lazy"> */}
      </div>
      <div className="col-lg-6">
        <h1 className="display-5 fw-bold lh-1 mb-3">Image Annotation Generation System</h1>
        <p className="lead">Use AI to automatically generate detailed and descriptive captions for any images, enhancing accessibility, improving search engine optimization, and providing a better user experience by describing the visual content with accurate and engaging text.</p>
        <div className="d-grid gap-2 d-md-flex justify-content-md-start">
          <button type="button" className="btn btn-primary btn-lg px-4 me-md-2" onClick={handleClick}>  
    <ShinyText text="Generate" disabled={false} speed={3} className='custom-class' />
    </button>
        </div>
      </div>
    </div>
  </div>
    </div>

  )
};
export default Hero;
