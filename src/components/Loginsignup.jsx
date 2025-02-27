import React from 'react'
import "./Loginsignup.css"
function Loginsignup() {
  const styleDiv = {
    margin:0,
    padding:0,
    boxSizing:"border-box",
    backgroundColor: "linear-gradient(to right,#3a7bd5,#3a6073)",
  }
  return (
    <div style={styleDiv}>
    <div className='center'>
      <button className='btn btn-primary'>Login</button>
    </div>
    <div className='popup'>
      <div className='close-btn'>&times;</div>
      <form>
  <div className="mb-3">
    <label for="exampleInputEmail1" className="form-label">Email address</label>
    <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"/>
  </div>
  <div className="mb-3">
    <label for="exampleInputPassword1" className="form-label">Password</label>
    <input type="password" className="form-control" id="exampleInputPassword1"/>
  </div>
  <div className="mb-3 form-check">
    <input type="checkbox" className="form-check-input" id="exampleCheck1"/>
    <label className="form-check-label" for="exampleCheck1">Check me out</label>
  </div>
  <button type="submit" className="btn btn-primary">Submit</button>
</form>
    </div>
    </div>
  )
}

export default Loginsignup;