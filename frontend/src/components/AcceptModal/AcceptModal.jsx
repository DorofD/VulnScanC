import React from 'react';
import ReactDOM from 'react-dom';
import "./AcceptModal.css";

export default function AcceptModal({ isOpen, children, onClose }) {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <>
      <div className="overlayAccept" onClick={onClose}></div>
      <div className="modalAccept">
        {children}
      </div>
    </>,
    document.getElementById('modal-root')
  );
};
