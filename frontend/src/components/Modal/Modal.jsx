import React from 'react';
import ReactDOM from 'react-dom';
// import
import "./Modal.css";

export default function Modal({ isOpen, children, onClose }) {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <>
      <div className="overlay" onClick={onClose}></div>
      <div className="modal">
        {children}
      </div>
    </>,
    document.getElementById('modal-root')
  );
};
