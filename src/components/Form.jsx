import React, { useState, useCallback, useEffect, useRef } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import "../App.css";

const Form = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [caption, setCaption] = useState(null);
  const [useWebcam, setUseWebcam] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const webcamRef = useRef(null);

  const videoConstraints = {
    width: 500,
    height: 300,
    facingMode: "user"
  };

  const stopWebcam = () => {
    if (webcamRef.current) {
      const stream = webcamRef.current.video?.srcObject;
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    }
    setIsWebcamActive(false);
  };

  const toggleWebcam = () => {
    const newState = !useWebcam;
    setUseWebcam(newState);
    setPreview(null);
    setSelectedImage(null);
    
    if (!newState) {
      stopWebcam();
    } else {
      setIsWebcamActive(true);
    }
  };

  useEffect(() => {
    return () => {
      stopWebcam();
    };
  }, []);

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
    if (!webcamRef.current) return;
    
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      setPreview(imageSrc);
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], "webcam.jpg", { type: "image/jpeg" });
          setSelectedImage(file);
          stopWebcam();
          setUseWebcam(false);
        });
    }
  }, [webcamRef]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (selectedImage) {
      setIsLoading(true);
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
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setCaption(null);
    stopWebcam();
    setUseWebcam(false);
  };

  return (
    <div className="form-body">
      <div className="row">
        <div className="form-holder">
          <div className="form-content">
            <div className="form-items" style={{top: "2.5rem"}}>
              <h3>Enter Image below to <strong className='text-primary'>generate</strong> text</h3>
              <div className="form-check mb-3 mt-2">
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={useWebcam}
                    onChange={toggleWebcam}
                  />
                  <span className="slider round"></span>
                  <span className="toggle-label">Use Webcam Instead</span>
                </label>
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
                      {isWebcamActive ? (
                        <Webcam
                          audio={false}
                          height={300}
                          ref={webcamRef}
                          screenshotFormat="image/jpeg"
                          width={500}
                          videoConstraints={videoConstraints}
                        />
                      ) : (
                        <div className="webcam-placeholder">
                          <p>Webcam is starting...</p>
                        </div>
                      )}
                      <br />
                      <button 
                        type="button" 
                        onClick={captureWebcamImage} 
                        className="btn btn-secondary mt-2"
                        disabled={!isWebcamActive}
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
                
                <div className="form-button rounded-2 mt-3">
                  <button 
                    id="submit" 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={!selectedImage || isLoading}
                  >
                    {isLoading ? 'Generating...' : 'Generate'}
                  </button>
                  <br />
                  {isLoading && (
                    <div className="loader-6 mt-3" style={{
                      width: '48px',
                      height: '48px',
                      display: 'inline-block',
                      position: 'relative',
                      transform: 'rotate(45deg)',
                      scale: '0.7',
                      marginLeft: '20px'
                    }}>
                      <div style={{
                        content: '""',
                        boxSizing: 'border-box',
                        width: '24px',
                        height: '24px',
                        position: 'absolute',
                        left: '0',
                        top: '-24px',
                        animation: 'animloader 4s ease infinite'
                      }}></div>
                      <div style={{
                        content: '""',
                        boxSizing: 'border-box',
                        position: 'absolute',
                        left: '0',
                        top: '0',
                        width: '24px',
                        height: '24px',
                        background: '#00A9FE',
                        boxShadow: '0 0 10px rgba(0, 0, 0, 0.15)',
                        animation: 'animloader2 2s ease infinite'
                      }}></div>
                    </div>
                  )}
                  
                  {caption && !isLoading && (
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

      <style>
        {`
          .toggle-switch {
            display: flex;
            align-items: center;
            cursor: pointer;
          }
          
          .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
          }
          
          .slider {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
            background-color: #ccc;
            transition: .4s;
            border-radius: 24px;
            margin-right: 10px;
          }
          
          .slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
          }
          
          input:checked + .slider {
            background-color: #2196F3;
          }
          
          input:checked + .slider:before {
            transform: translateX(26px);
          }
          
          .toggle-label {
            font-weight: 500;
          }
          
          .webcam-placeholder {
            width: 500px;
            height: 300px;
            background-color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
          }

          @keyframes animloader {
            0% {
              box-shadow: 0 24px rgba(255, 255, 255, 0), 24px 24px rgba(255, 255, 255, 0),
                24px 48px rgba(255, 255, 255, 0), 0px 48px rgba(255, 255, 255, 0);
            }
            12% {
              box-shadow: 0 24px #5d5d5d, 24px 24px rgba(255, 255, 255, 0),
                24px 48px rgba(255, 255, 255, 0), 0px 48px rgba(255, 255, 255, 0);
            }
            25% {
              box-shadow: 0 24px #5d5d5d, 24px 24px #5d5d5d,
                24px 48px rgba(255, 255, 255, 0), 0px 48px rgba(255, 255, 255, 0);
            }
            37% {
              box-shadow: 0 24px #5d5d5d, 24px 24px #5d5d5d, 24px 48px #5d5d5d,
                0px 48px rgba(255, 255, 255, 0);
            }
            50% {
              box-shadow: 0 24px #5d5d5d, 24px 24px #5d5d5d, 24px 48px #5d5d5d,
                0px 48px #5d5d5d;
            }
            62% {
              box-shadow: 0 24px rgba(255, 255, 255, 0), 24px 24px #5d5d5d,
                24px 48px #5d5d5d, 0px 48px #5d5d5d;
            }
            75% {
              box-shadow: 0 24px rgba(255, 255, 255, 0), 24px 24px rgba(255, 255, 255, 0),
                24px 48px #5d5d5d, 0px 48px #5d5d5d;
            }
            87% {
              box-shadow: 0 24px rgba(255, 255, 255, 0), 24px 24px rgba(255, 255, 255, 0),
                24px 48px rgba(255, 255, 255, 0), 0px 48px #5d5d5d;
            }
            100% {
              box-shadow: 0 24px rgba(255, 255, 255, 0), 24px 24px rgba(255, 255, 255, 0),
                24px 48px rgba(255, 255, 255, 0), 0px 48px rgba(255, 255, 255, 0);
            }
          }

          @keyframes animloader2 {
            0% {
              transform: translate(0, 0) rotateX(0) rotateY(0);
            }
            25% {
              transform: translate(100%, 0) rotateX(0) rotateY(180deg);
            }
            50% {
              transform: translate(100%, 100%) rotateX(-180deg) rotateY(180deg);
            }
            75% {
              transform: translate(0, 100%) rotateX(-180deg) rotateY(360deg);
            }
            100% {
              transform: translate(0, 0) rotateX(0) rotateY(360deg);
            }
          }
        `}
      </style>
    </div>
  );
};

export default Form;