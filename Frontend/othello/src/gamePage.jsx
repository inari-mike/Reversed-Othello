import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory

import OthelloBoard from './OthelloBoard'; // Import your 8x8 board component
import {Square, Board} from './OthelloBoard';
import './styling_for_game_page.css'

function initializeBoard() {
  const initialSquares = Array(64).fill(null); // Assuming a 64-square board
  initialSquares[27] = 'O'; // Black piece
  initialSquares[28] = 'X'; // White piece
  initialSquares[35] = 'X'; // White piece
  initialSquares[36] = 'O'; // Black piece
  return initialSquares;
} 

const Timer = (game_start_time) => { // when flag change, clear Timer

  const [sec_display, set_sec_display] = useState(0)

  useEffect(() => {
    set_sec_display(0)
    const interval = setInterval(() => {
      set_sec_display((prevTimer) => prevTimer + 1);
    }, 1000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, [game_start_time]);


  return (
    <div className="timer">
      Timer: {sec_display} seconds
    </div>
  )
}
const OthelloGame = () => {
  const [history, setHistory] = useState([initializeBoard()]);
  const [currentMove, setCurrentMove] = useState(0);
  const [flag, setFlag] = useState(0);
  const [xIsNext, setXIsNext] = useState(true);
  console.log(flag);
  console.log(xIsNext);
  console.log(currentMove);
  const currentSquares = history[currentMove];
 
  
  function handlePlay(nextSquares, flag, xIsNext) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setFlag(flag);
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
    setXIsNext(xIsNext);
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const [game_reset_times, set_game_reset_times] = useState(0);

  // Timer effect (runs once on component mount)
  useEffect(() => {
    // const interval = setInterval(() => {
    //   setTimer((prevTimer) => prevTimer + 1);
    // }, 1000);

    // return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  // Reset game
  const handleReset = () => {
    setFlag(0);
    // setTimer(0);
    set_game_reset_times(prev=>prev+1);
    jumpTo(0);
    setXIsNext(true);
  };

  // Handle navigation to home
  const handleGoHome = () => {
    history.push('/'); // Navigate to OthelloPage
  };
//
  return (
    <div className="othello-game">
      <h1>Othello Game</h1>
      {/* <div className="timer">Timer: {timer} seconds</div> */}
      <Timer game_start_time={game_reset_times}></Timer>
      <button className="home-button" onClick={handleGoHome}></button>
      <button className="reset-button" onClick={handleReset}>
        Reset
      </button>
      <div className="total-steps">Total Steps: {currentMove}</div>
      {/* Add your 8x8 board component here */}
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} flag={flag}/>
      </div>
    </div>  
  );
};

export default OthelloGame;
