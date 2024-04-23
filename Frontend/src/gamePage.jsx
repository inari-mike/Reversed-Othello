import React, { useState, useEffect } from 'react';
import { Board } from './OthelloBoard';
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
      Waiting for your choice: {sec_display}s
    </div>
  )
}
const OthelloGame = () => {
  const [history, setHistory] = useState([initializeBoard()]);
  const [currentMove, setCurrentMove] = useState(0);
  const [flag, setFlag] = useState(0);
  const [xIsNext, setXIsNext] = useState(true);
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

  // // Timer effect (runs once on component mount)
  // useEffect(() => {
  //   // const interval = setInterval(() => {
  //   //   setTimer((prevTimer) => prevTimer + 1);
  //   // }, 1000);

  //   // return () => clearInterval(interval); // Cleanup on unmount
  // }, []);

  // Reset game
  const handleReset = () => {
    if (confirm("Are you sure you want to reset the game?")) {
      setFlag(0);
      // setTimer(0);
      set_game_reset_times(prev=>prev+1);
      jumpTo(0);
      setXIsNext(true);
    }
  };

  // Handle navigation to home
  const handleGoHome = () => {
    // history.push('/'); // Navigate to OthelloPage // TODO fix issue
    if (confirm("Go back to the home page? The game state will not be saved.")) {
      window.location.href = "../";
    }
  };
//
  return (
    <div className="othello-game">
      <h1>Save Tim (Reversed Othello)</h1>
      <h6>Target: Lose the Game</h6>
      {/* <div className="timer">Timer: {timer} seconds</div> */}
      <div className='button-container'>
        <button className="home-button" onClick={handleGoHome}></button>
        <button className="reset-button" onClick={handleReset}>
          Reset
        </button>
      </div>
      <div className="total-steps">Total Steps: {currentMove}</div>
      {/* Add your 8x8 board component here */}
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} flag={flag}/>
      </div>
      
      {xIsNext?<Timer game_start_time={game_reset_times}></Timer>:null}
    </div>
  );
};

export default OthelloGame;
