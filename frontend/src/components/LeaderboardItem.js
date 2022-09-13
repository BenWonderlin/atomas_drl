import React from 'react'
import {Link} from 'react-router-dom'

const LeaderboardItem = ({game, idx}) => {
  return (
      <Link to = {`/games/${game.id}`}>

        <div className = "leaderboard-item">

          <div className = "leaderboard-item-rank">
            #{idx+1}
          </div> 

          <div className = "leaderboard-item-stat-bold">
            {game.player_name}
          </div>

          <div className = "leaderboard-item-stat-bold">
           {game.score}
          </div>

          <div className = "leaderboard-item-stat">
            {game.turns_taken}
          </div>

          <div className = "leaderboard-item-stat">
            {game.ai_assisted ? "Assisted" : "Human"}
          </div>


        </div>
      </Link>
    )
  }

export default LeaderboardItem