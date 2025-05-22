import React from 'react';
import "../App.css";
import { useState } from "react";
// import DragAndDrop from './DragAndDrop';
// function Form() {import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [caption, setCaption] = useState(null);

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
        setCaption(response.data.caption); // Backend returns caption in JSON response
      } catch (error) {
        console.error('Error uploading the file', error);
      }
    }
  };
  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setCaption(null);
  };
  return (
    <>
    <div className="form-body ">
    <div className="row">
        <div className="form-holder">
            <div className="form-content">
                <div className="form-items">
                    <h3>Enter Image below to generate text</h3>
                    <form className="" onSubmit={handleSubmit}>
                        <div className="col-md-12">
                        {/* <DragAndDrop/> */}
                            <input className="form-control" type="file" accept="image/*" onChange={handleImageChange} name="name" placeholder="Key Words" required/>
                            {preview && <img src={preview} alt="Selected" style={{ width: '500px', height: '300px', paddingTop:'1rem' }} />}
                        </div>
                    <div className="form-check">
                      <p className="">We will not share your data.</p>
                    </div>
                        <div className="form-button mt-3">
                            <button id="submit" type="submit" className="btn btn-primary">Generate</button>
                            <div className='my-2'>

                                {caption && (
                                                <div>
                                                <h4>Caption</h4>
                                                <p>{caption}</p>
                                                <button id="submit" type="button" onClick={handleReset} className="btn btn-primary">Reset</button>
                                                </div>
                                            )}
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</>
  )
}

export default Form;
