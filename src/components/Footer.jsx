import React from 'react'
import image from '../photos/images.jpg';
function Footer() {
  return (
    <footer class="bg-dark text-light py-4 mt-auto">
  <div class="container">
    <div class="row align-items-center text-center text-md-start">
      
      
      <div class="col-md-4 mb-3 mb-md-0 d-flex align-items-center justify-content-center justify-content-md-start">
        <img src={image} alt="College Logo" height="60" class="me-2"/>
        <div>
          <p class="mb-0">&copy; 2024 Graphic Era Hill University, Bhimtal</p>
          <small>All rights reserved.</small>
        </div>
      </div>
      
      
      <div class="col-md-8 text-center text-md-end">
        <a href="/" class="text-light text-decoration-none me-3">Home</a>
        <a href="/about" class="text-light text-decoration-none me-3">About</a>
        <a href="/generate" class="text-light text-decoration-none me-3">Generate</a>
      </div>

    </div>
  </div>
</footer>


  )
}

export default Footer;
