import { React }  from 'react'
import { Link, useNavigate } from "react-router-dom"



const HomePage = () => {

    let navigate = useNavigate();

    let getNewGame = async () => {
        let response = await fetch("https://atomas-backend.herokuapp.com/new_game")
        let data = await response.json()
        navigate(`/games/${data.id}`)
    }

    return (
        <div className = "home">
            <div className = "home-button" onClick = {() => getNewGame()}>
                New Game
            </div>
            <Link to= "/leaderboard">
                <div className = "home-button">
                    Global Leaderboard
                </div>
            </Link>
        </div>
    )
}

export default HomePage