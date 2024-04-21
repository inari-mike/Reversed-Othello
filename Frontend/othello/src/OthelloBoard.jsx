import React from 'react';
import { useState } from 'react';
import './OthelloBoardStyle.css'

export function Square({ value, onSquareClick, highlight, xIsNext}) {
  const squareClassName = `square ${highlight ? 'highlighted' : ''}`;

  return (
    <button className={squareClassName} onClick={onSquareClick} disabled={!highlight || !xIsNext}>
      {value}
      {highlight && <span className="highlight-text">·</span>}
    </button>
  );
}

export function Board({ xIsNext, squares, onPlay, flag }) {
  const boardSize = 8;
  let validMoves = calculateValidMoves();
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

    return validMoves;
  }  
  function handleClick(i) {
    const validMoves = calculateValidMoves();
    // if (currentMove === 64 || squares[i]) {
    //   return;
    // }
    const nextSquares = squares.slice();
    const flippedSquares = calculateFlippedSquares(i);


    if (flippedSquares.length >= 0) {
      flippedSquares.forEach((index) => {
        nextSquares[index] = xIsNext ? 'X' : 'O';
      });
    }



    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    };
    onPlay(nextSquares,flag,!xIsNext);
    if (validMoves.length === 0){
      console.log("ha????");
      // flag = 1-flag;
      // console.log(xIsNext);
      // xIsNext = !xIsNext;
      // console.log(xIsNext);
      // validMoves = calculateValidMoves();
    };    
  }


  if (validMoves.length === 0){
    flag = 1-flag;
    console.log(xIsNext);
    xIsNext = !xIsNext;
    console.log(xIsNext);
    validMoves = calculateValidMoves();
  };

  let status;
  if (validMoves.length === 0) {
    const winner = countPieces(squares);
    if (winner != "Draw") {
      // console.log('w')
      status = 'Winner: ' + winner;
    } else {
      status = 'Draw';
      // console.log('D')

    };
    } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
    };
    
    if (xIsNext) {
      status = "Your turn(X)!";
    } else {
      const nextSquares = squares.slice();
      console.log(nextSquares);
    }
  

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
                xIsNext={xIsNext}
              />
            );
          })}
        </div>
      ))}
    </>
  ); 
}

// export function jumpto(){
//   const [currentMove, setCurrentMove] = useState(0);
//   setCurrentMove(0);
// };

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

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
        <button onClick={() => jumpTo(0)}>Go to game start</button>
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