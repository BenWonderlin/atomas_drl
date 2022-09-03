import React, {useState, useEffect} from 'react'
import LeaderboardItem from '../components/LeaderboardItem'

const LeaderboardPage = () => {

    let [leaderboard, setLeaderboard] = useState([])

    useEffect(() => {
        getLeaderboard()
    }, [])

    let getLeaderboard = async () => {
        let response = await fetch('/leaderboard/')
        let data = await response.json()
        console.log("DATA:", data)
        setLeaderboard(data)
    }

    return (
        <div className = "leaderboard">

            <div className = "leaderboard-header">
                <h2 className = "leaderboard-title">{'\u272D'}  Global Leaderboard</h2>
                <p className = "leaderboard-count"> (Top 50)</p>
            </div>

            <div className = "leaderboard-list">
                {
                    leaderboard.map((game, index) => (
                        <LeaderboardItem key = {index} game = {game} />
                    ))
                }
            </div>

        </div>
    )
}

export default LeaderboardPage