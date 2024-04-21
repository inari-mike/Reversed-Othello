import React from 'react';
import { useState, useEffect  } from 'react';
import GameModal from './GameModal';

import './OthelloBoardStyle.css'

function Square({ value, onSquareClick, highlight }) {
  const squareClassName = `square ${highlight ? 'highlighted' : ''}`;

  return (
    <button className={squareClassName} onClick={onSquareClick} disabled={!highlight}>
      {value}
      {highlight && <span className="highlight-text">·</span>}
    </button>
  );
}

function Board({ xIsNext, squares, onPlay }) {
  const boardSize = 8;
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Function to open the modal
  const openModal = () => {
    setIsModalOpen(true);
  };

  // Function to close the modal
  const closeModal = () => {
    setIsModalOpen(false);
  };

  function calculateFlippedSquares(i) {
    const flippedSquares = [];
    // Define the directions to check for valid flips
    const directions = [
      [-1, -1], // NW
      [-1, 0],  // N
      [-1, 1],  // NE
      [0, -1],  // W
      [0, 1],   // E
      [1, -1],  // SW
      [1, 0],   // S
      [1, 1],   // SE
    ];

    // Check each direction for valid flips
    directions.forEach(([dx, dy]) => {
      let x = i % boardSize;
      let y = Math.floor(i / boardSize);
      let validFlip = false;
      let flipIndices = [];

      while (true) {
        x += dx;
        y += dy;
        const index = y * boardSize + x;

        if (x < 0 || x >= boardSize || y < 0 || y >= boardSize) {
          break; // Out of bounds
        }

        if (squares[index] === null) {
          break; // Empty square
        }

        if (squares[index] === (xIsNext ? 'X' : 'O')) {
          validFlip = true;
          break;
        }

        flipIndices.push(index);
      }

      if (validFlip) {
        flippedSquares.push(...flipIndices);
      }
    });

    return flippedSquares;
  }

  function calculateValidMoves() {
    const validMoves = [];
    for (let i = 0; i < boardSize * boardSize; i++) {
      if (!squares[i]) {
        const flippedSquares = calculateFlippedSquares(i);
        if (flippedSquares.length > 0) {
          validMoves.push(i);
        }
      }
    }
    // console.log(xIsNext)
    // console.log(validMoves)
    //seems as though there is a loop constantly runnning here

    return validMoves;
  }  
  function handleClick(i) {
    const validMoves = calculateValidMoves();
    // if (currentMove === 64 || squares[i]) {
    //   return;
    // }
    const nextSquares = squares.slice();
    const flippedSquares = calculateFlippedSquares(i);
    // const validMoves = calculateValidMoves();


    if (flippedSquares.length >= 0) {
      flippedSquares.forEach((index) => {
        nextSquares[index] = xIsNext ? 'X' : 'O';
      });
    }

    // if (validMoves.length >= 0) {
    //   validMoves.forEach((index) => {
    //     nextSquares[index] = 'G';
    //   });
    // }


    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    onPlay(nextSquares);
    const winner = countPieces(nextSquares);
    if (winner !== "Draw" || validMoves.length === 0) {
      openModal(); // Open modal when there's a winner or draw
    }
  }
  function handleReset() {
    // Reset the game state here
    closeModal(); // Close the modal after resetting
  }

  function handleBackToGame() {
    // Handle navigation back to the game page
    closeModal(); // Close the modal after navigating back
  }

  //useEffect(() => {
  const validMoves = calculateValidMoves();
  let status;
  if (validMoves.length === 0) {
    const winner = countPieces(squares);
    if (winner != "Draw") {
      //console.log('w')
      alert('Winner: ' + winner); // Popup for winner

      status = 'Winner: ' + winner;
    } else {
      status = 'Draw';
      alert('Draw'); // Popup for draw

      // console.log('D')
      
    };
    //setIsModalOpen(true); // Show the modal
    } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
    // console.log('n')

  }
//}, [squares,xIsNext]);
  // const winner = calculateWinner(squares);
  // let status;
  // if (winner) {
  //   status = 'Winner: ' + winner;
  // } else {
  //   status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  // }


  return (
    <>
      <div className="status">{status}</div>
      {Array.from({ length: boardSize }).map((_, row) => (
        <div className="board-row" key={row}>
          {Array.from({ length: boardSize }).map((_, col) => {
            const index = row * boardSize + col;
            const isMoveValid = validMoves.includes(index);
            let value = squares[index]; // Initialize value
            
            return (
              <Square
                key={index}
                value={squares[index]}
                onSquareClick={() => handleClick(index)}
                highlight={isMoveValid} // Add this prop to Square component
              />
            );
          })}
        </div>
      ))}
      {/* Board rendering logic... */}
      {isModalOpen && (
        <GameModal isOpen={isModalOpen} onClose={closeModal} status={status} />
      )}
    </>
  ); 
}

export default function Game() {
  const [history, setHistory] = useState([initializeBoard()]);
  const [currentMove, setCurrentMove] = useState(0);
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];

  function initializeBoard() {
    const initialSquares = Array(64).fill(null); // Assuming a 64-square board
    initialSquares[27] = 'O'; // Black piece
    initialSquares[28] = 'X'; // White piece
    initialSquares[35] = 'X'; // White piece
    initialSquares[36] = 'O'; // Black piece
    return initialSquares;
  }  

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }
  const moves = history.map((squares, move) => (
    <li key={move}>
      {move === 0 && (
        <button onClick={() => jumpTo(move)}>Go to game start</button>
      )}
    </li>
  ));
    

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
    </div>
  );
}


function countPieces(squares) {
  let count_X = 0;
  let count_O = 0;
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const index = row * 8 + col;
      const cell = squares[index];
      if (cell === 'X') {
        count_X++;
      } else if (cell === 'O') {
        count_O++;
      }
    }
  }
  if (count_O > count_X) {
    return "O";
  } else if (count_X > count_O){
    return "X";
  } else{
    return "Draw";
  }
}

// export function printSomeStuff(){
//   console.log("hello");
// }