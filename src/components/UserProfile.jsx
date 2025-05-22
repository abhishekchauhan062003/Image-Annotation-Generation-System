import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const UserProfile = () => {
  const [username] = useState("johndoe_99");
  const [firstName, setFirstName] = useState('John');
  const [lastName, setLastName] = useState('Doe');
  const [isEditing, setIsEditing] = useState(false);
  const [points, setPoints] = useState(150);

  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMessage, setPasswordMessage] = useState('');

  const handleSave = () => setIsEditing(false);
  const handlePasswordChange = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setPasswordMessage("Passwords do not match.");
      return;
    }
    setPasswordMessage("Password changed successfully!");
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setShowPasswordForm(false);
    setShowPassword(false);
  };

  const handleBuyPoints = () => {
    setPoints(points + 50); // Mock buy
  };

  return (
    <div className="container-fluid min-vh-100 d-flex justify-content-center align-items-center bg-light text-black">
      <div className="row w-100 p-4" style={{ maxWidth: '1000px' }}>
        
        {/* Left Profile Section */}
        <div className="col-md-4 d-flex flex-column align-items-center">
          <div
            className="rounded-circle border border-dark d-flex justify-content-center align-items-center mb-3"
            style={{
              width: '130px',
              height: '130px',
              fontSize: '14px',
              backgroundColor: '#f0f0f0',
              border: '3px solid #007bff',
            }}
          >
            <img
              src="https://www.gravatar.com/avatar?d=mp&s=200" // Sample image URL for Gravatar
              alt="Profile"
              className="rounded-circle"
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </div>
          <div className="border px-4 py-2 rounded text-center w-75">
            {username}
          </div>
        </div>

        {/* Right Info Section */}
        <div className="col-md-8 border border-dark p-4 rounded shadow-lg">
          <div className="row mb-3">
            <div className="col-md-6 mb-3">
              {isEditing ? (
                <input
                  type="text"
                  className="form-control"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              ) : (
                <div className="border p-3 rounded text-center">{firstName}</div>
              )}
            </div>
            <div className="col-md-6 mb-3">
              {isEditing ? (
                <input
                  type="text"
                  className="form-control"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
              ) : (
                <div className="border p-3 rounded text-center">{lastName}</div>
              )}
            </div>
          </div>

          {/* Edit Button */}
          <div className="mb-3">
            <button
              className="btn btn-outline-primary w-100"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? 'Cancel Editing' : 'Edit Username'}
            </button>
          </div>

          {isEditing && (
            <div className="mb-3">
              <button className="btn btn-success w-100" onClick={handleSave}>
                Save Changes
              </button>
            </div>
          )}

          {/* Points */}
          <div className="row mb-3">
            <div className="col-md-6 mb-2">
              <div className="border p-3 rounded text-center">
                Your Current Points: <strong>{points}</strong>
              </div>
            </div>
            <div className="col-md-6 mb-2">
              <button className="btn btn-outline-warning w-100" onClick={handleBuyPoints}>
                Buy More Points
              </button>
            </div>
          </div>

          {/* Password Change Button */}
          <div className="mb-3">
            <button
              className="btn btn-outline-secondary w-100"
              onClick={() => setShowPasswordForm(!showPasswordForm)}
            >
              {showPasswordForm ? 'Cancel Password Change' : 'Change Password'}
            </button>
          </div>

          {showPasswordForm && (
            <form onSubmit={handlePasswordChange}>
              <input
                type={showPassword ? 'text' : 'password'}
                className="form-control mb-2"
                placeholder="Current Password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />
              <input
                type={showPassword ? 'text' : 'password'}
                className="form-control mb-2"
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <input
                type={showPassword ? 'text' : 'password'}
                className="form-control mb-2"
                placeholder="Confirm New Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
              <div className="form-check mb-2">
                <input
                  className="form-check-input"
                  type="checkbox"
                  id="showPasswordCheck"
                  checked={showPassword}
                  onChange={() => setShowPassword(!showPassword)}
                />
                <label className="form-check-label" htmlFor="showPasswordCheck">
                  Show Password
                </label>
              </div>
              <button type="submit" className="btn btn-success w-100">
                Submit Password Change
              </button>
            </form>
          )}

          {passwordMessage && (
            <div className="mt-3 alert alert-info py-2 px-3" role="alert">
              {passwordMessage}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
