import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory

import OthelloBoard from './OthelloBoard'; // Import your 8x8 board component
import {Square, Board} from './OthelloBoard';
import { AiOutlineHome } from "react-icons/ai";
import { BiRefresh } from "react-icons/bi";

import './styling_for_game_page.css'
const OthelloGame = () => {
  const [history, setHistory] = useState([initializeBoard()]);
  const [currentMove, setCurrentMove] = useState(0);
  const [flag, setFlag] = useState(0);
  const [xIsNext, setXIsNext] = useState(true);
  console.log(flag);
  console.log(xIsNext);
  console.log(currentMove);
  const currentSquares = history[currentMove];

  function initializeBoard() {
    const initialSquares = Array(64).fill(null); // Assuming a 64-square board
    initialSquares[27] = 'O'; // Black piece
    initialSquares[28] = 'X'; // White piece
    initialSquares[35] = 'X'; // White piece
    initialSquares[36] = 'O'; // Black piece
    return initialSquares;
  }  

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

  const [timer, setTimer] = useState(0);

  // Timer effect (runs once on component mount)
  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  // Reset game
  const handleReset = () => {
    setFlag(0);
    setTimer(0);
    jumpTo(0);
    setXIsNext(true);
  };

  // Handle navigation to home
  const handleGoHome = () => {
    //history.push('/'); // Navigate to OthelloPage
    const confirmed = window.confirm("Are you sure you want to go home? Your game progress will be lost.");
    if (confirmed) {
    console.log("I got it"); // Display message if confirmed
    history.push('/'); // Navigate to OthelloPage
  }
  };
//
return (
  <div className="othello-game">
    <h1>Othello Game</h1>
    <div className="timer">Timer: {timer} seconds</div>
    <div className="button-container">
      <button className="home-button" onClick={handleGoHome}><AiOutlineHome /></button>
      <button className="reset-button" onClick={handleReset}><BiRefresh /></button>
    </div>
    <div className="total-steps">Total Steps: {currentMove}</div>
    <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} flag={flag}/>
    </div>
  </div>
);

};

// console.log("kk")
// printSomeStuff();
export default OthelloGame;
