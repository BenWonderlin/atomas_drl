import React from 'react'

const RingElement = ({idx, value, size, nameArr, colorArr}) => {

    // Helpers for rendering
    const ringRadius = 160;
    const elementRadius = 20;

    const defaultColor = "#fff";
    const defaultName = "";

    return (

        <div className = "ring-element-container"
            style = {{

                top: - (ringRadius * Math.sin(2 * Math.PI * (idx / size))) + elementRadius,
                left: (ringRadius * Math.cos(2 * Math.PI * (idx / size))) - elementRadius,

                width: 2 * elementRadius,
                height: 2 * elementRadius,
                borderRadius: elementRadius,

                backgroundColor: colorArr.at(value) || defaultColor

            }}
        >

            <div className = "ring-element-label">
                {nameArr.at(value) || defaultName}
            </div>

            <div className = "ring-element-value"
                style = {{
                    
                    top: elementRadius, 
                    left: elementRadius,

                }}
            >
                {value >= 0? value : ""}
            </div>

        </div>

    )
}

export default RingElement