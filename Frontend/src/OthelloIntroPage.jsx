// OthelloPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './OthelloIntroPageStyle.css'

const OthelloPage = () => {
  return (
    <div className="othello-page">
      {/* Background */}
      <div className="background-image">
        {/* Set your background image here */}
        {<img style={{borderRadius: '5px'}} src="/images/orthello_pic.png" alt="Beautiful Landscape" />}
      </div>

      {/* Rules of Othello */}
      <div className="rules">
  <h1>Before the Start</h1>
  <p>
    Your best friend Tim told his wife that, he is an Othello Master.
    But actually, he sucks.
  </p>
  <p>
    Today you come to his house and Tim's wife wants to know "how good" he is on Othello.
  </p>
  <p>
    To protect your best friend's glory, you have to play a game with Tim and let him win.
    Let's go!
  </p>
  <p>
    PS: Othello is a 2-player board game on an 8x8 board.
    For detailed rules, you can refer to the{' '}  
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


<Link to="/play">
  <button className="play-button">Play Othello</button>
</Link>


    </div>
  );
};

export default OthelloPage;
