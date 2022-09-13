import React from 'react'

const InfoPage = () => {
  return (
    <div className = "info">

          <h1>
            Welcome to Deep Atomas!
          </h1>

          <h2>
            An AI-assisted implementation of the mobile game Atomas
          </h2>

          <div className = "info-entry">
            <h3>
              How do I play?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Build symmetric patterns of atoms by placing the center atoms on the outer ring. 
            Place Plus Atoms on lines of symmetry to accumulate score and reduce your atom count.
            Leverage Minus Atoms to rearrange your atoms before you run out of space!
          </div>

          <div className = "info-entry">
            <h3>
              What's so deep about Deep Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deep Atomas is equipped with an AI agent that uses Deep Q-Learning to study millions of games of Atomas.
            Tapping the brain icon will let Deep Atomas take a turn for you, but beware— 
            Deep Atomas is currently quite shallow. It averages about 75 points per game.
          </div>

          <div className = "info-entry">
            <h3>
              Where can I play the original Atomas?
            </h3>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max Gittel's Atomas is available Google Play Store and the Apple App Store. It includes some features not implemented here. Check it out!
          </div>

        </div>
  )
}

export default InfoPage