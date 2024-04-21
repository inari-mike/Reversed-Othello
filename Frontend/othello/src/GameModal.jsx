// GameModal.jsx
const GameModal = ({ isOpen, onClose, status }) => {
    if (!isOpen) return null;
  
    return (
      <div className="modal">
        <div className="modal-content">
          <h2>{status}</h2>
          <button onClick={onClose}>Back to Game</button>
          <button onClick={() => window.location.reload()}>Reset Game</button>
        </div>
      </div>
    );
  };
  
  export default GameModal;
  