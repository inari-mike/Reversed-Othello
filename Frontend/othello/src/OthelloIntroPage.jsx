// OthelloPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';


const OthelloPage = () => {
  return (
    <div className="othello-page">
      {/* Background */}
      <div className="background-image">
        {/* Set your background image here */}
        {<img src="/public/images/orthello_pic.png" alt="Beautiful Landscape" />}
      </div>

      {/* Rules of Othello */}
      <div className="rules">
  <h1>Othello Rules</h1>
  <p>
    Othello (also known as Reversi) is a two-player board game played on an 8x8 grid.
    The goal is to have the majority of your color (black or white) discs on the board
    at the end of the game. For detailed rules, you can refer to the{' '}
    <a
      href="https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english"
      target="_blank"
      rel="noopener noreferrer"
    >
      official Othello rules
    </a>
    .
  </p>
</div>


<Link to="/othello-game">
  <button className="play-button">Play Othello</button>
</Link>


    </div>
  );
};

export default OthelloPage;
