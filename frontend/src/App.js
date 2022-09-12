import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";


import './App.css';
import Header from "./components/Header";
import HomePage from  "./pages/HomePage";
import LeaderboardPage from "./pages/LeaderboardPage";
import GamePage from "./pages/GamePage";
import InfoPage from "./pages/InfoPage";

function App() {

  return (
    <Router>
      <div className = "container">
        <div className = "app">
          <Header />
          <Routes>
            <Route path = "/" element = {<HomePage/>} />
            <Route path = "/leaderboard" element = {<LeaderboardPage/>} />
            <Route path = "/games/:id" element = {<GamePage/>} />
            <Route path = "/info" element = {<InfoPage/>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
