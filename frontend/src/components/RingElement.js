import React from 'react'

const RingElement = ({idx, value, size, nameArr, colorArr}) => {
    
    const ringRadius = 150;
    const elementRadius = 16;

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

            <div className = "element-label">
                {nameArr.at(value) || defaultName}
            </div>

            <div className = "element-value"
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