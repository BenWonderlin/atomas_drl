import React from 'react'

const CenterElement = ({value, nameArr, colorArr}) => {

    const elementRadius = 16;

    const defaultColor = "#fff";
    const defaultName = "";

    return (

        <div className = "center-element-container"
            style = {{

                width: 2 * elementRadius,
                height: 2 * elementRadius,
                borderRadius: elementRadius,

                backgroundColor: colorArr.at(value) || defaultColor,

            }}>

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

export default CenterElement