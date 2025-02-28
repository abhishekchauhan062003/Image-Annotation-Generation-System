import React from "react"
import myPhoto from "../photos/myPhoto.png"
import Ashutosh from "../photos/Ashutosh.png"
import Lokesh from "../photos/Lokesh.jpg"
function About(){
    const Styl = {
        width: '500px',
        height: '500px'
    };
    const centre = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        padding: "2rem",
    }
    const ul = {
      listStyleType: "none",
      color: "#5b5b5b",
      fontSize: "1.1rem"
    }
    const img = {
      display: 'flex'
    } 
return (<>
<div className="card">
  
  <div className="card-body">
    <blockquote className="blockquote mb-0">
    <div class="row">
    <div class="col col-md-auto">
    <img className="rounded-circle" src={myPhoto} alt="Generic placeholder image" width="140" height="140" style={img}/>
    </div>
    <div class="col">
    <p style={{paddingLeft:"2rem"}}>Abhishek Chauhan</p>
      
      <ul style = {ul}>
              <li>Developed LSTM-based RNN for image caption generation.</li>
              <li>Integrated VGG-16 for feature extraction and LSTM for sequence prediction.</li>
              <li>Implemented Flask API for real-time caption generation.</li>
            </ul>
      
    </div>
  </div>
    
      
    </blockquote>
  </div>
  <div className="card-body">
    <blockquote className="blockquote mb-0">
    <div class="row">
    <div class="col col-md-auto">
    <img className="rounded-circle" src={Ashutosh} alt="Generic placeholder image" width="140" height="140" style={img}/>
    </div>
    <div class="col">
    <p style={{paddingLeft:"2rem"}}>Ashutosh Upreti</p>
      
      <ul style = {ul}>
              <li>Designed a responsive UI for image annotation and caption display.</li>
              <li>Integrated API endpoints for real-time image caption generation.</li>
              <li>Optimized performance using React hooks and state management.</li>
            </ul>
      
    </div>
  </div>
    
      
    </blockquote>
  </div>
  <div className="card-body">
    <blockquote className="blockquote mb-0">
    <div class="row">
    <div class="col col-md-auto">
    <img className="rounded-circle" src={Lokesh} alt="Generic placeholder image" width="140" height="140" style={img}/>
    </div>
    <div class="col">
    <p style={{paddingLeft:"2rem"}}>Lokesh Joshi</p>
      <ul style = {ul}>
              <li>Developed CNN-based model for image feature extraction.</li>
              <li>Used VGG-16 to extract deep visual features.</li>
              <li>Implemented Flask API for real-time image processing.</li>
            </ul>
      
    </div>
  </div>
    
      
    </blockquote>
  </div>  
</div>
<div className="container marketing my-5">

        
        {/* <div className="row">
          <div className="col-lg-4" style={centre}>
            <img className="rounded-circle" src={myPhoto} alt="Generic placeholder image" width="140" height="140"/>
            <h3>Abhishek Chauhan</h3>
            <ul style = {ul}>
              <li>Developed LSTM-based RNN for image caption generation.</li>
              <li>Integrated VGG-16 for feature extraction and LSTM for sequence prediction.</li>
              <li>Implemented Flask API for real-time caption generation.</li>
            </ul>
           
            
          </div>
          <div className="col-lg-4" style={centre}>
            <img className="rounded-circle" src={Lokesh} alt="Generic placeholder image" width="140" height="140"/>
            <h3>Lokesh Joshi</h3>
            <p>Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Cras mattis consectetur purus sit amet fermentum. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh.</p>
            
          </div>
          <div className="col-lg-4" style={centre}>
            <img className="rounded-circle" src={Ashutosh} alt="Generic placeholder image" width="140" height="140"/>
            <h3>Ashutosh Upreti</h3>
            <p>Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
            
          </div>
        </div> */}
    </div>
    </>
    )
}
export default About;