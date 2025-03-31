import React from "react";
import caption from "../photos/captions.png";
import "../App.css";
import { useState } from "react";

function Navbar() {
  const [text, setText] = useState("Login");
  const imgstyle = {
    height: "50px",
    width: "200px",
  };
  const navstyle = {
    backgroundColor: "rgba(30, 30, 30)",
  };
  function hideLogin(){
    document.getElementById('Login').classList.add('hidden');
    document.getElementById('SignUp').classList.remove('hidden');
    setText('SignUp');
  }
  function hideSignup(){
    document.getElementById('SignUp').classList.add('hidden');
    document.getElementById('Login').classList.remove('hidden');
    setText('LogIn');
  }
  return (
    <nav className="navbar navbar-expand-lg navbar-dark " style={navstyle}>
      <div className="container-fluid">
        <a href="/">
          <img src={caption} alt="caption" style={imgstyle} />
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <div>
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="/">
                  Home
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/about">
                  About
                </a>
              </li>
            </ul>
          </div>
          <div className="ms-auto">
            <button
              type="button"
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            >
              Login
            </button>

            <div
              class="modal fade"
              id="exampleModal"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                      Login
                    </h1>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>
                  <div class="modal-body">
                    <div id="Login">
                      <div class="mb-3 row">
                        <label
                          for="staticEmail"
                          class="col-sm-2 col-form-label"
                        >
                          Email
                        </label>
                        <div>
                          <input type="text" class="form-control" />
                        </div>
                      </div>
                      <div>
                        <label
                          for="inputPassword"
                          class="col-form-label"
                        >
                          Password
                        </label>
                        <div>
                          <input
                            type="password"
                            class="form-control"
                            id="inputPassword"
                          />
                        </div>
                        <label htmlFor=""><p>Don't Have an Account? <a href="#" onClick={hideLogin}>Sign Up</a></p></label>
                      </div>
                    </div>
                    <div class="hidden" id="SignUp">
                    <div class="mb-3 row">
                      <label for="staticEmail" class="col-form-label">
                        Email
                      </label>
                      <div>
                        <input type="text" class="form-control" />
                      </div>
                    </div>
                    <div>
                      <label
                        for="inputPassword"
                        class="col-form-label"
                      >
                        Password
                      </label>
                      <div >
                        <input
                          type="password"
                          class="form-control"
                          id="inputPassword"
                        />
                      </div>
                      <label
                        for="inputPassword"
                        class="col-form-label"
                      >
                        Re-enter Password
                      </label>
                      <div>
                        <input
                          type="password"
                          class="form-control"
                          id="inputPassword"
                        />
                      </div>
                      <label htmlFor=""><p>Have an Account? <a href="#" onClick={hideSignup}>Login</a></p></label>
                    </div>
                  </div>
                    <div class="modal-footer">
                      <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                      >
                        Close
                      </button>
                      <button type="button" class="btn btn-primary">
                        <span>{text}</span>
                      </button>
                    </div>
                  </div>
                  
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
