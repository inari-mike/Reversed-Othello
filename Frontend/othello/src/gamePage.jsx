import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory

import OthelloBoard from './OthelloBoard'; // Import your 8x8 board component
import './styling_for_game_page.css'
const OthelloGame = () => {
  const history = useHistory(); // Get the history object

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
  };

  // Handle navigation to home
  const handleGoHome = () => {
    history.push('/'); // Navigate to OthelloPage
  };

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
      <OthelloBoard />
    </div>
  );
};

export default OthelloGame;
