import React from 'react';


const OthelloBoard = () => {
  // Create an 8x8 grid (you can customize this further)
  const rows = 8;
  const cols = 8;

  // Generate the board cells
  const renderCells = () => {
    const cells = [];
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        cells.push(
          <div key={`${row}-${col}`} className="board-cell">
            {/* Customize cell content (e.g., discs) */}
          </div>
        );
      }
    }
    return cells;
  };

  return (
    <div className="othello-board">
      {renderCells()}
    </div>
  );
};

export default OthelloBoard;
