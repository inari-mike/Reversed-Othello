import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory

import OthelloBoard from './OthelloBoard'; // Import your 8x8 board component
import {Square, Board} from './OthelloBoard';
import './styling_for_game_page.css'
const OthelloGame = () => {
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

  // const history = useHistory(); // Get the history object

  const [playerTurn, setPlayerTurn] = useState('Black'); // Initialize with Black's turn
  const [totalSteps, setTotalSteps] = useState(0);
  const [timer, setTimer] = useState(0);

  // Timer effect (runs once on component mount)
  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  // Handle turn change
  const handleTurnChange = () => {
    setPlayerTurn((prevTurn) => (prevTurn === 'Black' ? 'White' : 'Black'));
    setTotalSteps((prevSteps) => prevSteps + 1);
  };

  // Reset game
  const handleReset = () => {
    setPlayerTurn('Black');
    setTotalSteps(0);
    setTimer(0);
    jumpTo(0);
  };

  // Handle navigation to home
  const handleGoHome = () => {
    history.push('/'); // Navigate to OthelloPage
  };
//
  return (
    <div className="othello-game">
      <h1>Othello Game</h1>
      <div className="timer">Timer: {timer} seconds</div>
      <div className="turn-block">Player's Turn: {playerTurn}</div>
      <button className="home-button" onClick={handleGoHome}></button>
      <button className="reset-button" onClick={handleReset}>
        Reset
      </button>
      <div className="total-steps">Total Steps: {totalSteps}</div>
      {/* Add your 8x8 board component here */}
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
        <button onClick={() => jumpTo(0)}>Go to game start</button>
      </div>
    </div>  
  );
};

export default OthelloGame;
