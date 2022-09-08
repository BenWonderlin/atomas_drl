import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import RingElement from '../components/RingElement'
import CenterElement from '../components/CenterElement'
import RingButton from '../components/RingButton'

const GamePage = () => {


    const valueToNameArr = [
        "",
        "H","He","Li","Be","B","C","N","O","F","Ne",
        "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
        "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
        "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
        "Nb","Mo","Tc","Ru","Rh","Pb","Ag","Cd","-","+",
    ] 

    const valueToColorArr = [
        "#000000",
        "#63b9d5","#d1c991","#4c6168","#c8c8c8","#7d5353",
        "#3b3b3b","#2cc6b2","#6fec98","#ecc46f","#be0086",
        "#e69d7a","#9e80ea","#797979","#4a4070","#d7463f",
        "#375e7c","#6d1d7b","#9a3da5","#4d8946","#f0f0f0",
        "#5fbb77","#5a5a5a","#5f9ebb","#a488b5","#dc4a4a",
        "#ab967d","#4371e6","#bac395","#b95739","#b4b4b4",
        "#39b975","#979273","#738498","#424242","#d4753c",
        "#3ca0d4","#d22c1f","#ff9d29","#b129ff","#d6e43a",
        "#75dceb","#8ba38c","#eea1e2","#563e32","#88d17a",
        "#9eabbe","#dcdcdc","#5560c8", "blue", "#dc4a4a"
    ]


    const { id } = useParams();
    const [game, setGame] = useState(null);

    const getGame = async () => {
        const response = await fetch(`/games/${id}`);
        const data = await response.json();
        setGame(data);
    }

    const putGameAction = async (action) => {
        const putRequestOption = {
            method: 'PUT',
        };
        const response = await fetch(`/games/${id}?action=${action}`,  putRequestOption);
        const data = await response.json()
        setGame(data);
    }

    useEffect(() =>{
        getGame()
    }, [id]);


    return (
        <div className = "game">

            <div className = "game-header">
                Score: {game?.score} | Turns Taken: {game?.turns_taken}
            </div>

            <div className = "game-ring-elements">

                <div className = "game-ring-border"/>

                {
                    game?.ring_elements.split(',').filter(element => element).map((value, index) => (
                        <RingElement 
                            key = {index}
                            idx = {index} 
                            value = {value} 
                            size = {game?.ring_elements.split(',').filter(element => element).length}
                            nameArr= {valueToNameArr}
                            colorArr = {valueToColorArr}
                        />
                    ))
                }

                {   !game?.terminal &&
                    game?.ring_elements.split(',').filter(element => element).map((value, index) => (
                        <RingButton
                            key = {index}
                            idx = {index}
                            size = {game?.ring_elements.split(',').filter(element => element).length}
                            callback = {putGameAction}
                        />
                    ))
                }

                <CenterElement
                    key = {0}
                    value = {game?.center_element}
                    nameArr = {valueToNameArr}
                    colorArr = {valueToColorArr}
                />

            </div>
        </div>
  )
}

export default GamePage