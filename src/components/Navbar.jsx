import React from 'react'
import caption from "../photos/captions.png"
import "../App.css"
function Navbar() {
  const imgstyle = {
    height:'50px',
    width:'200px',
  }
  const navstyle = {
    backgroundColor:"#1E1E1E",
  }
  return (
    <nav className="navbar navbar-expand-lg navbar-dark" style={navstyle}>
  <div className="container-fluid">
    <a href='/'><img src={caption} alt="caption" style={imgstyle}/></a>
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarNav">
      <div>
      <ul className="navbar-nav">
        <li className="nav-item">
          <a className="nav-link active" aria-current="page" href="/">Home</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/about">About</a>
        </li>
      </ul>
      </div>
      <div className='ms-auto'>
      	<button className='btn btn-danger '>Login/SignUp</button>
    </div>
    </div>
  </div>
</nav>
  )
}

export default Navbar;
