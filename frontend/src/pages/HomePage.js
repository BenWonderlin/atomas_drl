import { React }  from 'react'
import { Link, useNavigate } from "react-router-dom"



const HomePage = () => {

    let navigate = useNavigate();

    let getNewGame = async () => {
        let response = await fetch("/new_game")
        let data = await response.json()
        navigate(`/games/${data.id}`)
    }

    return (
        <div className = "home">
            <div className = "home-button" onClick = {() => getNewGame()}>
                <h4>
                    New Game
                </h4>
            </div>
            <Link to= "/leaderboard">
                <div className = "home-button">
                    <h4>
                        Global Leaderboard
                    </h4>
                </div>
            </Link>
        </div>
    )
}

export default HomePage