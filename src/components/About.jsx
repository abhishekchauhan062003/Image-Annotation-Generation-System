  import React from "react"
  import myPhoto from "../photos/myPhoto.png"
  import Ashutosh from "../photos/Ashutosh.png"
  import Lokesh from "../photos/Lokesh.jpg"
  import "../App.css";
 
  function About(){
    const teamMembers = [
    {
      name: "Abhishek Chauhan",
      photo: myPhoto,
      role: "AI Model Developer",
      contributions: [
        "Built LSTM-based RNN for image captioning",
        "Integrated VGG-16 + LSTM for predictions",
        "Deployed Flask API for real-time processing"
      ]
    },
    {
      name: "Ashutosh Upreti",
      photo: Ashutosh,
      role: "Frontend Developer",
      contributions: [
        "Designed responsive UI for image captions",
        "Connected API for real-time generation",
        "Optimized React state & performance"
      ]
    },
    {
      name: "Lokesh Joshi",
      photo: Lokesh,
      role: "Backend Developer",
      contributions: [
        "Developed CNN for feature extraction",
        "Applied VGG-16 for visual analysis",
        "Built Flask API for image processing"
      ]
    }
  ];
      const technologies = [
    { name: "Frontend", tech: "React.js, Bootstrap" },
    { name: "Backend", tech: "Flask (Python)" },
    { name: "AI Models", tech: "VGG16 (CNN), LSTM, BLIP" },
    { name: "Other Tools", tech: "OpenCV, NLTK" }
  ];
      
  return (
  <div>
    <div className="card-all">
     <div className="container py-3 text-dark">
      
      <div className="project-details shadow-sm border-0">
        <h1 className="mb-4 text-center fw-bold">About <span className="text-primary">Captions.io</span></h1>
        <p>
        <strong>Captions.io</strong> is an AI-powered image annotation generation system developed to enhance accessibility,
        improve content discoverability, and support better user interaction with visual media.
      </p>
      <p>
        This project automatically generates meaningful, descriptive captions for images using deep learning techniques,
        combining computer vision and natural language processing.
      </p>
      <p>
        It was created as part of an academic project at <strong>Graphic Era Hill University, Bhimtal</strong>,
        with the goal of addressing real-world challenges like image accessibility for visually impaired users,
        better SEO for media content, and automated metadata generation.
      </p>

      </div>
      

      <section className="technologies-section project-details my-3 py-5">
        <div className="container">
          <h2 className="text-center mb-5"><strong>Technologies We Used</strong> </h2>
          <div className="row">
            {technologies.map((tech, index) => (
              <div className="col-md-3 mb-4" key={index}>
                <div className="tech-card card h-100 shadow-sm border-0">
                  <div className="card-body text-center">
                    <h5 className="card-title text-primary">{tech.name}</h5>
                    <p className="card-text">{tech.tech}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      <section className="team-section project-details my-3 py-5">
        <div className="container">
          <h2 className="text-center mb-5"><strong>Our Team</strong></h2>
          <div className="row">
            {teamMembers.map((member, index) => (
              <div className="col-md-4 mb-4" key={index}>
                <div className="team-card card h-100 shadow-sm border-0">
                  <div className="card-body text-center p-4">
                    <img 
                      src={member.photo} 
                      alt={member.name} 
                      className="rounded-circle mb-3" 
                      width="140" 
                      height="140"
                    />
                    <h4 className="mb-2">{member.name}</h4>
                    <h6 className="text-muted mb-3">{member.role}</h6>
                    <ul className="text-start ps-3">
                      {member.contributions.map((item, i) => (
                        <li key={i} className="mb-2">{item}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      
    </div>
  


      </div>
      </div>
      )
  }
  export default About;