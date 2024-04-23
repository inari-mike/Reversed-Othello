// App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import OthelloPage from './OthelloIntroPage'; 
import OthelloGame from './gamePage.jsx'


function App() {
  return (
    <div className="App">
      <Router>
        
          <Route exact path="/" component={OthelloPage} /> {/* Render the OthelloPage component */}
          <Route path="/play" component={OthelloGame} /> {/* Othello game page */}
          {/* Other routes */}
        
      </Router>
    </div>
  );
}
export default App;

