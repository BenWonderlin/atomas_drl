import React from 'react'

const LeaderboardItem = ({game}) => {
  return (
      <div className = "leaderboard-list-item">
        <h3>
          {game.score}
        </h3>
      </div>
    )
  }

export default LeaderboardItem