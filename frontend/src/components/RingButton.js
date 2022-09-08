import React from 'react'

const RingButton = ({idx, size, callback}) => {

    const ringRadius = 200;
    const buttonRadius = 10;

    return (
        <div className = "ring-button"
            style = {{

            top: - (ringRadius * Math.sin(2 * Math.PI * ((idx - 0.5) / size))) + buttonRadius + 20,
            left: (ringRadius * Math.cos(2 * Math.PI * ((idx - 0.5) / size))) - buttonRadius,

            width: 2 * buttonRadius,
            height: 2 * buttonRadius,
            borderRadius: buttonRadius,

            }}
            onClick = {() => callback(idx)}
        >
        </div>
    )


}

export default RingButton