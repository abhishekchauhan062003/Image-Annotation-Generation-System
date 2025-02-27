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
return (

<div className="container marketing my-5">

        
        <div className="row">
          <div className="col-lg-4" style={centre}>
            <img className="rounded-circle" src={myPhoto} alt="Generic placeholder image" width="140" height="140"/>
            <h3>Abhishek Chauhan</h3>
            <p>Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Praesent commodo cursus magna.</p>
            
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
        </div>
    </div>
    )
}
export default About;