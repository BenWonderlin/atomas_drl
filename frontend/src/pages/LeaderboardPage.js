import React, {useState, useEffect} from 'react'
import { AiFillTrophy } from "react-icons/ai"
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
                <AiFillTrophy/>&nbsp;&nbsp;Global Leaderboard&nbsp;&nbsp;<AiFillTrophy/>
            </div>

            <div className = "leaderboard-label">

            </div>

            <div className = "leaderboard-list">
            
                {
                    leaderboard.map((game, index) => (
                        <LeaderboardItem 
                            key = {index}
                            idx = {index} 
                            game = {game}
                        />
                    ))
                }
            </div>

        </div>
    )
}

export default LeaderboardPage