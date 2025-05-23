import React, { useState, useCallback } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import "../App.css";

const Form = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [caption, setCaption] = useState(null);
  const [useWebcam, setUseWebcam] = useState(false);
  const webcamRef = React.useRef(null);

  const videoConstraints = {
    width: 500,
    height: 300,
    facingMode: "user"
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const captureWebcamImage = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      setPreview(imageSrc);
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], "webcam.jpg", { type: "image/jpeg" });
          setSelectedImage(file);
          
          // Stop the webcam stream
          const stream = webcamRef.current.video.srcObject;
          if (stream) {
            stream.getTracks().forEach(track => track.stop());
          }
          
          // Hide the webcam UI
          setUseWebcam(false);
        });
    }
  }, [webcamRef]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (selectedImage) {
      const formData = new FormData();
      formData.append('file', selectedImage);

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setCaption(response.data.caption);
      } catch (error) {
        console.error('Error uploading the file', error);
      }
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setCaption(null);
    setUseWebcam(false);
  };

  return (
    <div className="form-body">
      <div className="row">
        <div className="form-holder">
          <div className="form-content">
            <div className="form-items">
              <h3>Enter Image below to generate text</h3>
              <div className="form-check mb-3">
                <input
                  type="checkbox"
                  checked={useWebcam}
                  onChange={() => {
                    setUseWebcam(!useWebcam);
                    setPreview(null);
                    setSelectedImage(null);
                  }}
                /> Use Webcam Instead
              </div>
              
              <form onSubmit={handleSubmit}>
                <div className="col-md-12">
                  {!useWebcam ? (
                    <input
                      className="form-control"
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                      required={!preview}
                    />
                  ) : (
                    <>
                      <Webcam
                        audio={false}
                        height={300}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        width={500}
                        videoConstraints={videoConstraints}
                      />
                      <br />
                      <button 
                        type="button" 
                        onClick={captureWebcamImage} 
                        className="btn btn-secondary mt-2"
                      >
                        Capture
                      </button>
                    </>
                  )}
                  
                  {preview && (
                    <div className="mt-3">
                      <img
                        src={preview}
                        alt="Selected"
                        style={{ maxWidth: '100%', height: 'auto', maxHeight: '300px' }}
                      />
                    </div>
                  )}
                </div>

                <div className="form-check">
                  <p>We will not share your data.</p>
                </div>
                
                <div className="form-button mt-3">
                  <button 
                    id="submit" 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={!selectedImage}
                  >
                    Generate
                  </button>
                  
                  {caption && (
                    <div className="mt-3">
                      <h4>Caption</h4>
                      <p>{caption}</p>
                      <button 
                        type="button" 
                        onClick={handleReset} 
                        className="btn btn-primary"
                      >
                        Reset
                      </button>
                    </div>
                  )}
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Form;