import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './components/pages/Home';
import Game from './components/pages/Game';
import Leaderboard from './components/pages/Leaderboard';

//font-awesome library
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTshirt, faTimes, faBars } from '@fortawesome/free-solid-svg-icons';

library.add(faTshirt, faTimes, faBars)
// https://github.com/briancodex/react-website-v1/tree/starter
function App() {
  return (
    <>
    <Router>
      <Navbar />
      <Switch>
        <Route path = '/' exact component = {Home}/>
        <Route path = '/game' component = {Game}/>
        <Route path = '/leaderboard' component = {Leaderboard}/>
      </Switch>
    </Router>
    </>
  );
}

export default App;
