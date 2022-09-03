import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

const GamePage = () => {

    const { id } = useParams();
    const [game, setGame] = useState(null);

    const getGame = async () => {
        const response = await fetch(`/games/${id}/`);
        const data = await response.json();
        setGame(data);
    }

    useEffect(() =>{
        getGame()
    }, [id]);

    return (
        <div className = "game">

            <div className = "game-header">
                {"\u269B"}
            </div>

            <h1>
                {game?.score}
            </h1>
        </div>
  )
}

export default GamePage