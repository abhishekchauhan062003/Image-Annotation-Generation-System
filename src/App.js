import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import Form from './components/Form';


import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import About from './components/About';
function App() {
  return (
        <>
            <Navbar />
            
            <Router>
            <Routes>
                <Route path="/" element={<Hero />} />
                <Route path="/form" element={<Form/>} />
                <Route path="/about" element={<About/>} />
                {/* <Route path="/Login" element={} /> */}
            </Routes>
        </Router>
            <div className='footer'>
                <Footer />
            </div> 
            
            {/* <Login/> */}
            
        </>
  );
}

export default App;
